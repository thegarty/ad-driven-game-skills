import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/game-ui-and-navigation/scripts/contrast_check.py"
SPEC = importlib.util.spec_from_file_location("contrast_check", SCRIPT)
contrast = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contrast)


class ContrastTests(unittest.TestCase):
    def test_known_ratios(self):
        self.assertEqual(contrast.check("#FFFFFF", "#000000")["ratio"], 21)
        self.assertEqual(contrast.check("#123456", "#123456")["ratio"], 1)

    def test_symmetric_and_case_insensitive(self):
        self.assertEqual(contrast.check("#abcdef", "#123456")["ratio"],
                         contrast.check("#123456", "#ABCDEF")["ratio"])

    def test_no_rounding_into_pass(self):
        self.assertTrue(contrast.check("#767676", "#FFFFFF")["meets_selected_minimum"])
        self.assertFalse(contrast.check("#777777", "#FFFFFF")["meets_selected_minimum"])
        ratio = contrast.check("#777777", "#FFFFFF")["ratio"]
        self.assertAlmostEqual(ratio, 4.478089453577214, places=12)

    def test_reject_invalid_colours(self):
        for value in ("white", "#FFF", "#FFFFFF00", "FFFFFF", "#GGGGGG", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                contrast.check(value, "#000000")

    def test_reject_invalid_thresholds(self):
        for value in (0, 22, 10**400, float("nan"), float("inf"), True, "4.5"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                contrast.check("#FFFFFF", "#000000", value)

    def test_cli(self):
        for colour, expected in (("#FFFFFF", 0), ("#777777", 1), ("#gggggg", 2)):
            result = subprocess.run([sys.executable, str(SCRIPT), "--foreground", colour,
                                     "--background", "#FFFFFF" if colour != "#FFFFFF" else "#000000"],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stderr)
            if expected != 2:
                self.assertIn("limitations", json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
