import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.dest = self.root / "client" / "skills"
        self.repo.mkdir()
        (self.repo / "VERSION").write_text("0.1.0\n")
        for name in ("alpha", "beta"):
            skill = self.repo / "skills" / name
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: %s\ndescription: Test\n---\n" % name)
            (skill / "references/guide.md").write_text("original")

    def tearDown(self):
        self.tmp.cleanup()

    def run_install(self, names=None, **kwargs):
        return installer.install(self.repo, self.dest, names, **kwargs)

    def test_selected_install_is_complete_and_idempotent(self):
        self.assertEqual(self.run_install(["alpha"])[0]["action"], "install")
        self.assertFalse((self.dest / "beta").exists())
        self.assertEqual((self.dest / "alpha/references/guide.md").read_text(), "original")
        before = (self.dest / installer.MANIFEST).read_bytes()
        self.assertEqual(self.run_install(["alpha"])[0]["action"], "unchanged")
        self.assertEqual((self.dest / installer.MANIFEST).read_bytes(), before)

    def test_dry_run_never_creates_destination(self):
        self.run_install(dry_run=True)
        self.assertFalse(self.dest.exists())

    def test_clean_update_requires_flag(self):
        self.run_install()
        (self.repo / "skills/alpha/references/guide.md").write_text("new")
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertEqual((self.dest / "alpha/references/guide.md").read_text(), "original")
        self.run_install(update=True)
        self.assertEqual((self.dest / "alpha/references/guide.md").read_text(), "new")

    def test_local_edit_blocks_entire_batch(self):
        self.run_install(["alpha"])
        (self.dest / "alpha/SKILL.md").write_text("my work")
        with self.assertRaisesRegex(installer.InstallError, "Local changes"):
            self.run_install(["beta", "alpha"], update=True)
        self.assertFalse((self.dest / "beta").exists())
        self.assertEqual((self.dest / "alpha/SKILL.md").read_text(), "my work")

    def test_local_deletion_is_preserved(self):
        self.run_install()
        (self.dest / "alpha/references/guide.md").unlink()
        with self.assertRaises(installer.InstallError):
            self.run_install(update=True)
        self.assertFalse((self.dest / "alpha/references/guide.md").exists())

    def test_extra_local_file_is_preserved(self):
        self.run_install()
        (self.dest / "alpha/notes.txt").write_text("personal")
        with self.assertRaises(installer.InstallError):
            self.run_install(update=True)
        self.assertEqual((self.dest / "alpha/notes.txt").read_text(), "personal")

    def test_unmanaged_skill_is_never_overwritten(self):
        (self.dest / "alpha").mkdir(parents=True)
        (self.dest / "alpha/SKILL.md").write_text("different skill")
        with self.assertRaisesRegex(installer.InstallError, "Unmanaged"):
            self.run_install(update=True)

    def test_bad_selection_and_path_traversal(self):
        for name in ("unknown", "../alpha", "/tmp/alpha", "Alpha"):
            with self.assertRaises(installer.InstallError):
                self.run_install([name])
        self.assertFalse(self.dest.exists())

    def test_profile_selection_union_and_complete_resources(self):
        (self.repo / "profiles.json").write_text(json.dumps({"one": ["alpha"], "both": ["alpha", "beta"]}))
        plans = self.run_install(["beta"], profiles=["one", "both"], dry_run=True)
        self.assertEqual([p["skill"] for p in plans], ["beta", "alpha"])
        self.assertFalse(self.dest.exists())
        self.run_install(profiles=["one"])
        self.assertTrue((self.dest / "alpha/references/guide.md").is_file())
        self.assertFalse((self.dest / "beta").exists())

    def test_bad_profiles_fail_without_destination(self):
        for data in ({"one": ["missing"]}, {"one": ["alpha", "alpha"]}, {"one": []}, [], {"../bad": ["alpha"]}):
            (self.repo / "profiles.json").write_text(json.dumps(data))
            with self.subTest(data=data), self.assertRaises(installer.InstallError):
                self.run_install(profiles=["one"])
            self.assertFalse(self.dest.exists())
        (self.repo / "profiles.json").write_text(json.dumps({"one": ["alpha"]}))
        with self.assertRaisesRegex(installer.InstallError, "Unknown profile"):
            self.run_install(profiles=["missing"])
        self.assertFalse(self.dest.exists())

    def test_profile_update_preserves_local_changes(self):
        (self.repo / "profiles.json").write_text(json.dumps({"one": ["alpha"]}))
        self.run_install(profiles=["one"])
        (self.dest / "alpha/references/guide.md").write_text("my edit")
        with self.assertRaisesRegex(installer.InstallError, "Local changes"):
            self.run_install(profiles=["one"], update=True)
        self.assertEqual((self.dest / "alpha/references/guide.md").read_text(), "my edit")

    def test_duplicate_profile_keys_fail_without_destination(self):
        (self.repo / "profiles.json").write_text('{"starter":["alpha"],"starter":["beta"]}')
        with self.assertRaisesRegex(installer.InstallError, "duplicate JSON key"):
            self.run_install(profiles=["starter"])
        self.assertFalse(self.dest.exists())

    def test_symlinks_are_rejected(self):
        (self.repo / "skills/alpha/link").symlink_to(self.repo / "VERSION")
        with self.assertRaisesRegex(installer.InstallError, "symlink"):
            self.run_install()

    def test_manifest_corruption_does_not_overwrite(self):
        self.run_install()
        (self.dest / installer.MANIFEST).write_text("[]")
        with self.assertRaisesRegex(installer.InstallError, "manifest"):
            self.run_install(update=True)

    def test_failed_manifest_write_restores_all_old_files(self):
        self.run_install()
        original_manifest = (self.dest / installer.MANIFEST).read_bytes()
        (self.repo / "skills/alpha/SKILL.md").write_text("new version")
        with patch.object(installer.os, "replace", side_effect=OSError("simulated disk failure")):
            with self.assertRaises(OSError):
                self.run_install(update=True)
        self.assertIn("name: alpha", (self.dest / "alpha/SKILL.md").read_text())
        self.assertEqual((self.dest / installer.MANIFEST).read_bytes(), original_manifest)
        self.assertFalse(list(self.dest.glob(".ad-game-install-*")))

    def test_failed_restore_keeps_backup_and_restores_remaining_skills(self):
        self.run_install()
        originals = {name: (self.dest / name / "SKILL.md").read_bytes() for name in ("alpha", "beta")}
        original_manifest = (self.dest / installer.MANIFEST).read_bytes()
        for name in originals:
            (self.repo / "skills" / name / "SKILL.md").write_text("new version")
        real_rename = Path.rename

        def fail_beta_restore(path, target):
            if path.name == "beta-old":
                raise OSError("simulated restore failure")
            return real_rename(path, target)

        with patch.object(installer.os, "replace", side_effect=OSError("simulated manifest failure")), \
                patch.object(Path, "rename", fail_beta_restore):
            with self.assertRaisesRegex(installer.InstallError, "rollback incomplete") as raised:
                self.run_install(update=True)
        recovery = list(self.dest.glob(".ad-game-install-*"))
        self.assertEqual(len(recovery), 1)
        self.assertIn(str(recovery[0]), str(raised.exception))
        self.assertEqual((recovery[0] / "beta-old/SKILL.md").read_bytes(), originals["beta"])
        self.assertEqual((self.dest / "alpha/SKILL.md").read_bytes(), originals["alpha"])
        self.assertEqual((self.dest / installer.MANIFEST).read_bytes(), original_manifest)
        self.assertFalse((self.dest / installer.LOCK).exists())

    def test_edit_after_preflight_is_restored_without_overwrite(self):
        self.run_install(["alpha"])
        original_manifest = (self.dest / installer.MANIFEST).read_bytes()
        (self.repo / "skills/alpha/SKILL.md").write_text("new version")
        real_mkdtemp = installer.tempfile.mkdtemp

        def edit_during_staging(*args, **kwargs):
            result = real_mkdtemp(*args, **kwargs)
            (self.dest / "alpha/SKILL.md").write_text("concurrent user edit")
            return result

        with patch.object(installer.tempfile, "mkdtemp", edit_during_staging):
            with self.assertRaisesRegex(installer.InstallError, "Local changes during install"):
                self.run_install(["alpha"], update=True)
        self.assertEqual((self.dest / "alpha/SKILL.md").read_text(), "concurrent user edit")
        self.assertEqual((self.dest / installer.MANIFEST).read_bytes(), original_manifest)
        self.assertFalse(list(self.dest.glob(".ad-game-install-*")))

    def test_second_installer_is_rejected_while_first_holds_lock(self):
        self.run_install(["alpha"])
        (self.repo / "skills/alpha/SKILL.md").write_text("new version")
        real_mkdtemp = installer.tempfile.mkdtemp
        competing_attempts = []

        def competing_install(*args, **kwargs):
            with self.assertRaisesRegex(installer.InstallError, "locked"):
                self.run_install(["alpha"], update=True)
            competing_attempts.append(True)
            return real_mkdtemp(*args, **kwargs)

        with patch.object(installer.tempfile, "mkdtemp", competing_install):
            self.run_install(["alpha"], update=True)
        self.assertEqual(competing_attempts, [True])
        self.assertEqual((self.dest / "alpha/SKILL.md").read_text(), "new version")
        self.assertFalse((self.dest / installer.LOCK).exists())

    def test_edit_to_replacement_preserves_both_user_edit_and_old_backup(self):
        self.run_install(["alpha"])
        original = (self.dest / "alpha/SKILL.md").read_bytes()
        (self.repo / "skills/alpha/SKILL.md").write_text("new version")
        real_rename = Path.rename

        def edit_replacement(path, target):
            result = real_rename(path, target)
            if path.name == "alpha-new":
                (Path(target) / "SKILL.md").write_text("concurrent user edit")
            return result

        with patch.object(Path, "rename", edit_replacement):
            with self.assertRaisesRegex(installer.InstallError, "rollback incomplete"):
                self.run_install(["alpha"], update=True)
        self.assertEqual((self.dest / "alpha/SKILL.md").read_text(), "concurrent user edit")
        recovery = list(self.dest.glob(".ad-game-install-*"))
        self.assertEqual(len(recovery), 1)
        self.assertEqual((recovery[0] / "alpha-old/SKILL.md").read_bytes(), original)

    def test_source_file_removal_updates_clean_install(self):
        self.run_install()
        (self.repo / "skills/alpha/references/guide.md").unlink()
        self.run_install(update=True)
        self.assertFalse((self.dest / "alpha/references/guide.md").exists())

    def test_generated_python_cache_does_not_block_update(self):
        self.run_install()
        (self.dest / "alpha/__pycache__").mkdir()
        (self.dest / "alpha/__pycache__/cache.pyc").write_bytes(b"cache")
        self.assertEqual(self.run_install(["alpha"])[0]["action"], "unchanged")

    def test_destination_cannot_be_source(self):
        with self.assertRaises(installer.InstallError):
            installer.install(self.repo, self.repo / "skills")


if __name__ == "__main__":
    unittest.main()
