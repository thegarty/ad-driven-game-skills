"""Participant population, missingness and reproducibility contracts."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/game-analytics-and-experiments"
SCRIPT = SKILL / "scripts/experiment_readout.py"
spec = importlib.util.spec_from_file_location("experiment_readout", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((SKILL / "assets/experiment-example.json").read_text())

    def evaluate(self):
        return helper.evaluate(self.data, resamples=400)

    def test_known_means_include_unexposed_and_zero_players(self):
        result = self.evaluate()
        self.assertEqual(result["arms"]["control"]["assigned"], 10)
        self.assertEqual(result["arms"]["control"]["exposed"], 9)
        self.assertAlmostEqual(result["arms"]["control"]["mean"], 0.6)
        self.assertAlmostEqual(result["arms"]["treatment"]["mean"], 0.7)
        self.assertAlmostEqual(result["treatment_minus_control"], 0.1)
        self.assertEqual(result["evidence_type"], "synthetic_calculation")
        self.assertNotIn("winner", result)
        self.assertNotIn("significant", result)

    def test_reproducible_without_mutating_input_or_global_rng(self):
        import random
        before = copy.deepcopy(self.data)
        state = random.getstate()
        self.assertEqual(self.evaluate(), self.evaluate())
        self.assertEqual(self.data, before)
        self.assertEqual(random.getstate(), state)
        interval = self.evaluate()["bootstrap_interval"]
        self.assertLess(interval["low"], 0)
        self.assertGreater(interval["high"], 0)

    def test_constant_difference_is_known_but_degenerate_is_flagged(self):
        for row in self.data["participants"]:
            row["outcome"] = 3 if row["arm"] == "treatment" else 1
        result = self.evaluate()
        self.assertEqual(result["treatment_minus_control"], 2)
        self.assertEqual(result["bootstrap_interval"]["low"], 2)
        self.assertEqual(result["bootstrap_interval"]["high"], 2)
        self.assertTrue(any("Degenerate" in item for item in result["warnings"]))

    def test_missing_outcome_is_not_zero_or_excluded(self):
        self.data["participants"][0]["outcome"] = None
        result = self.evaluate()
        self.assertEqual(result["status"], "withheld_incomplete_data")
        self.assertEqual(result["arms"]["control"]["assigned"], 10)
        self.assertEqual(result["arms"]["control"]["missing_outcome"], 1)
        self.assertIsNone(result["arms"]["control"]["mean"])
        self.assertIsNone(result["treatment_minus_control"])
        self.assertIsNone(result["bootstrap_interval"])

    def test_incomplete_observation_with_number_withholds(self):
        self.data["participants"][0]["observation_complete"] = False
        self.assertEqual(self.evaluate()["status"], "withheld_incomplete_data")

    def test_immature_cohort_withholds(self):
        self.data["as_of_date"] = "2026-01-07"
        for row in self.data["participants"]:
            row["observation_complete"] = False
        result = self.evaluate()
        self.assertEqual(result["arms"]["control"]["immature"], 10)
        self.assertIsNone(result["bootstrap_interval"])

    def test_false_completeness_assertion_rejected(self):
        self.data["as_of_date"] = "2026-01-07"
        with self.assertRaisesRegex(ValueError, "before horizon"):
            self.evaluate()

    def test_exact_maturity_boundary(self):
        self.data["as_of_date"] = "2026-01-08"
        self.assertEqual(self.evaluate()["status"], "descriptive_readout")

    def test_duplicate_and_conflicting_assignment_rejected(self):
        for arm in ("control", "treatment"):
            with self.subTest(arm=arm):
                data = copy.deepcopy(self.data)
                duplicate = dict(data["participants"][0], arm=arm)
                data["participants"].append(duplicate)
                with self.assertRaisesRegex(ValueError, "duplicate participant|conflicting assignment"):
                    helper.evaluate(data)

    def test_empty_or_one_arm_has_no_zero_denominator(self):
        for rows in ([], self.data["participants"][:10]):
            with self.subTest(rows=len(rows)):
                self.data["participants"] = rows
                result = self.evaluate()
                self.assertIsNone(result["treatment_minus_control"])
                if not rows:
                    self.assertIsNone(result["assignment_ratio_screen"]["approximate_p_value"])
                else:
                    self.assertLess(result["assignment_ratio_screen"]["approximate_p_value"], 0.01)

    def test_one_per_arm_withholds_interval(self):
        self.data["participants"] = [self.data["participants"][0], self.data["participants"][10]]
        result = self.evaluate()
        self.assertEqual(result["treatment_minus_control"], 0)
        self.assertIsNone(result["bootstrap_interval"])
        self.assertEqual(result["assignment_ratio_screen"]["status"], "unavailable")

    def test_missing_roster_assertion_withholds(self):
        self.data["assignment_roster_complete"] = False
        result = self.evaluate()
        self.assertEqual(result["status"], "withheld_incomplete_data")
        self.assertEqual(result["assignment_ratio_screen"]["status"], "unavailable")

    def test_assignment_screen_known_balance_and_imbalance(self):
        result = self.evaluate()["assignment_ratio_screen"]
        self.assertEqual(result["chi_square"], 0)
        self.assertEqual(result["approximate_p_value"], 1)
        for index, row in enumerate(self.data["participants"]):
            row["arm"] = "control" if index < 19 else "treatment"
        result = self.evaluate()["assignment_ratio_screen"]
        self.assertAlmostEqual(result["chi_square"], 16.2)
        self.assertLess(result["approximate_p_value"], 0.001)

    def test_observational_data_gets_no_assignment_test_or_causal_claim(self):
        self.data["design"] = "observational"
        self.data["evidence_type"] = "observed"
        result = self.evaluate()
        self.assertEqual(result["evidence_type"], "calculation_from_supplied_observations")
        self.assertEqual(result["assignment_ratio_screen"]["status"], "unavailable")
        self.assertTrue(any("associations" in item for item in result["warnings"]))

    def test_negative_net_outcomes_allowed(self):
        self.data["participants"][0]["outcome"] = -1
        self.assertAlmostEqual(self.evaluate()["arms"]["control"]["mean"], 0.5)

    def test_strict_schema_missing_and_unknown_fields(self):
        data = copy.deepcopy(self.data)
        del data["assumptions"]
        with self.assertRaises(ValueError):
            helper.evaluate(data)
        self.data["typo"] = 1
        with self.assertRaises(ValueError):
            self.evaluate()

    def test_invalid_outcomes_and_exposure(self):
        for value in (True, "1", float("nan"), float("inf"), 1e13):
            with self.subTest(value=value):
                self.data["participants"][0]["outcome"] = value
                with self.assertRaises(ValueError):
                    self.evaluate()

    def test_invalid_controls(self):
        for settings in ({"seed": True}, {"seed": -1}, {"resamples": 20},
                         {"resamples": 2.5}, {"confidence": 1}, {"confidence": 0},
                         {"confidence": float("nan")}):
            with self.subTest(settings=settings), self.assertRaises(ValueError):
                helper.evaluate(self.data, **settings)

    def test_quantiles_use_linear_interpolation(self):
        self.assertEqual(helper.quantile([0, 2, 4], 0.25), 1)

    def test_cli_fixture_and_clean_error(self):
        command = [sys.executable, str(SCRIPT)]
        success = subprocess.run(command + [str(SKILL / "assets/experiment-example.json"), "--resamples", "200"], capture_output=True, text=True)
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual(json.loads(success.stdout)["status"], "descriptive_readout")
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.json"
            for content in ('{"schema_version":1,"schema_version":2}', "{", "[]"):
                path.write_text(content)
                failure = subprocess.run(command + [str(path)], capture_output=True, text=True)
                self.assertEqual(failure.returncode, 2)
                self.assertEqual(failure.stdout, "")
                self.assertNotIn("Traceback", failure.stderr)


if __name__ == "__main__":
    unittest.main()
