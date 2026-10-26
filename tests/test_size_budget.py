import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "skills/game-size-and-performance/scripts/artifact_size.py"
SPEC = importlib.util.spec_from_file_location("artifact_size", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class SizeBudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def archive(self, name="game.aab"):
        path = self.root / name
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as target:
            target.writestr("assets/", b"")
            target.writestr("assets/music.ogg", b"a" * 1000)
            target.writestr("assets/icon.png", b"b" * 40)
        return path

    def test_archive_distinguishes_container_and_payload(self):
        path = self.archive()
        result = module.inspect(path)
        self.assertEqual(result["measured_bytes"], path.stat().st_size)
        self.assertEqual(result["entry_uncompressed_bytes"], 1040)
        self.assertEqual(result["entry_count"], 2)
        self.assertLess(result["entry_compressed_bytes"], result["measured_bytes"])
        self.assertEqual(result["largest_entries"][0]["path"], "assets/music.ogg")
        self.assertEqual(result["budget_status"], "not_configured")

    def test_absolute_budget_at_boundary_and_over(self):
        path = self.archive()
        size = path.stat().st_size
        self.assertEqual(module.inspect(path, max_bytes=size)["budget_status"], "passed")
        self.assertEqual(module.inspect(path, max_bytes=size - 1)["budget_status"], "exceeded")

    def test_directory_totals_and_extensions(self):
        directory = self.root / "payload"
        directory.mkdir()
        (directory / "one.txt").write_bytes(b"a" * 12)
        (directory / "two.txt").write_bytes(b"b" * 7)
        (directory / "binary").write_bytes(b"c" * 5)
        result = module.inspect(directory, top=1)
        self.assertEqual(result["measurement"], "directory_file_bytes")
        self.assertEqual(result["measured_bytes"], 24)
        self.assertEqual(result["uncompressed_bytes_by_extension"][".txt"], 19)
        self.assertEqual(len(result["largest_entries"]), 1)

    def test_empty_directory_zero_budget(self):
        self.assertEqual(module.inspect(self.root, max_bytes=0)["budget_status"], "passed")

    def test_growth_and_reduction(self):
        path = self.root / "game.pck"
        path.write_bytes(b"a" * 10)
        baseline = module.inspect(path)
        path.write_bytes(b"b" * 25)
        self.assertEqual(module.inspect(path, baseline=baseline, max_growth_bytes=14)["budget_status"], "exceeded")
        self.assertEqual(module.inspect(path, baseline=baseline, max_growth_bytes=15)["growth_bytes"], 15)
        path.write_bytes(b"c" * 3)
        result = module.inspect(path, baseline=baseline, max_growth_bytes=0)
        self.assertEqual(result["growth_bytes"], -7)
        self.assertEqual(result["budget_status"], "passed")

    def test_mismatched_and_invalid_baseline_rejected(self):
        path = self.archive()
        for baseline in ([], {}, {"schema_version": 1, "measurement": "directory_file_bytes", "artifact_kind": "directory", "measured_bytes": 10}):
            with self.assertRaises(ValueError):
                module.inspect(path, baseline=baseline)
        baseline = module.inspect(path)
        baseline["measured_bytes"] = True
        with self.assertRaises(ValueError):
            module.inspect(path, baseline=baseline)

    def test_invalid_limits_and_missing_baseline(self):
        path = self.archive()
        for value in (-1, True, 1.5, float("nan")):
            with self.assertRaises(ValueError):
                module.inspect(path, max_bytes=value)
        with self.assertRaises(ValueError):
            module.inspect(path, max_growth_bytes=1)
        for value in (0, 1001, True):
            with self.assertRaises(ValueError):
                module.inspect(path, top=value)

    def test_invalid_archive_and_missing_file(self):
        path = self.root / "broken.apk"
        path.write_bytes(b"not a zip")
        with self.assertRaises(ValueError):
            module.inspect(path)
        with self.assertRaises(ValueError):
            module.inspect(self.root / "missing")

    def test_symlink_target_and_nested_symlink_rejected(self):
        path = self.archive()
        alias = self.root / "alias"
        alias.symlink_to(path)
        with self.assertRaises(ValueError):
            module.inspect(alias)
        with self.assertRaises(ValueError):
            module.inspect(self.root)

    def test_duplicate_and_traversal_names_are_only_reported_never_extracted(self):
        path = self.root / "odd.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w") as target:
                target.writestr("same", b"a")
                target.writestr("same", b"bb")
                target.writestr("../escaped", b"ccc")
        result = module.inspect(path)
        self.assertEqual(result["entry_uncompressed_bytes"], 6)
        self.assertEqual(result["duplicate_archive_entry_names"], ["same"])
        self.assertFalse((self.root.parent / "escaped").exists())

    def test_opaque_file_cannot_claim_payload_size(self):
        path = self.root / "data.pck"
        path.write_bytes(b"pck")
        result = module.inspect(path)
        self.assertEqual(result["artifact_kind"], "opaque_file")
        self.assertIsNone(result["entry_uncompressed_bytes"])

    def test_cli_json_and_budget_exit_codes(self):
        path = self.archive()
        result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["budget_status"], "not_configured")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-bytes", "1"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["budget_status"], "exceeded")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--max-growth-bytes", "1"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("baseline", result.stderr)


if __name__ == "__main__":
    unittest.main()
