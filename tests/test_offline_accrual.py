"""Synthetic arithmetic and replay contract checks; no game/backend/device claim."""

import copy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/game-offline-and-time/scripts/offline_accrual.py"
FIXTURE = ROOT / "skills/game-offline-and-time/assets/offline-example.json"
SPEC = importlib.util.spec_from_file_location("offline_accrual", SCRIPT)
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)


class OfflineAccrualTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_worked_fixture(self):
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["earned_units"], "175")
        self.assertEqual(result["eligible_seconds"], 600)
        self.assertEqual(result["discarded_by_cap_seconds"], 400)
        self.assertEqual(result["proposed_checkpoint_unix_s"], 2000)
        self.assertEqual(result["evidence_type"], "deterministic_model")

    def test_no_boost(self):
        self.data["boosters"] = []
        self.assertEqual(MODEL.evaluate(self.data)["earned_units"], "150")

    def test_committed_interval_cannot_be_reclaimed_from_old_checkpoint(self):
        first = MODEL.evaluate(self.data)
        settlement = first["settlement"]
        self.data["settled_intervals"] = [{key: settlement[key] for key in ("start_unix_s", "end_unix_s")}]
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["earned_units"], "0")
        self.assertEqual(result["already_settled_seconds"], 600)
        self.assertEqual(result["status"], "no_unsettled_eligible_time")
        self.assertEqual(result["settlement"]["claim_id"], settlement["claim_id"])

    def test_proposal_is_deterministic_and_does_not_mutate_input(self):
        original = copy.deepcopy(self.data)
        self.assertEqual(MODEL.evaluate(self.data), MODEL.evaluate(self.data))
        self.assertEqual(original, self.data)

    def test_overlapping_settled_intervals_are_a_union(self):
        self.data["boosters"] = []
        self.data["settled_intervals"] = [
            {"start_unix_s": 1000, "end_unix_s": 1200},
            {"start_unix_s": 1100, "end_unix_s": 1300},
            {"start_unix_s": 1100, "end_unix_s": 1300},
        ]
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["already_settled_seconds"], 300)
        self.assertEqual(result["eligible_seconds"], 300)
        self.assertEqual(result["earned_units"], "75")

    def test_intervals_clip_to_window(self):
        self.data["boosters"] = []
        self.data["settled_intervals"] = [
            {"start_unix_s": 0, "end_unix_s": 1050},
            {"start_unix_s": 1550, "end_unix_s": 2200},
            {"start_unix_s": 2500, "end_unix_s": 2600},
        ]
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["already_settled_seconds"], 100)
        self.assertEqual(result["earned_units"], "125")

    def test_adjacent_boosters_and_expiry_boundary(self):
        self.data["boosters"] = [
            {"start_unix_s": 900, "end_unix_s": 1100, "multiplier": "2"},
            {"start_unix_s": 1100, "end_unix_s": 1200, "multiplier": "3"},
        ]
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["earned_units"], "225")
        self.assertEqual([s["multiplier"] for s in result["segments"]], ["2", "3", "1"])

    def test_overlapping_boosters_require_explicit_stacking_policy(self):
        self.data["boosters"].append({"start_unix_s": 1050, "end_unix_s": 1200, "multiplier": "3"})
        with self.assertRaisesRegex(ValueError, "stacking"):
            MODEL.evaluate(self.data)

    def test_rollback_does_not_move_checkpoint_or_grant(self):
        self.data["resume_unix_s"] = 999
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["status"], "clock_rollback")
        self.assertEqual(result["earned_units"], "0")
        self.assertEqual(result["proposed_checkpoint_unix_s"], 1000)
        self.assertIsNone(result["settlement"])

    def test_no_elapsed_time(self):
        self.data["resume_unix_s"] = 1000
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["status"], "no_elapsed_time")
        self.assertIsNone(result["settlement"])

    def test_zero_cap_settles_whole_absence_without_reward(self):
        self.data["cap_seconds"] = 0
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["earned_units"], "0")
        self.assertEqual(result["discarded_by_cap_seconds"], 1000)
        self.assertEqual(result["proposed_checkpoint_unix_s"], 2000)
        self.assertEqual(result["settlement"]["end_unix_s"], 2000)

    def test_cap_larger_than_absence(self):
        self.data["cap_seconds"] = 2000
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["earned_units"], "275")
        self.assertEqual(result["discarded_by_cap_seconds"], 0)

    def test_zero_rate_is_valid(self):
        self.data["base_rate_per_second"] = "0"
        result = MODEL.evaluate(self.data)
        self.assertEqual(result["earned_units"], "0")
        self.assertEqual(result["eligible_seconds"], 600)

    def test_decimal_amount_is_exact(self):
        self.data.update(resume_unix_s=1003, base_rate_per_second="0.1", boosters=[])
        self.assertEqual(MODEL.evaluate(self.data)["earned_units"], "0.3")

    def test_extreme_mixed_magnitude_total_matches_exact_rational(self):
        rate = "9" * 64
        large = "9" * 64
        fractional = "1." + "0" * 61 + "1"
        end = 10**12
        self.data.update(checkpoint_unix_s=0, resume_unix_s=end, cap_seconds=end,
                         base_rate_per_second=rate, settled_intervals=[], boosters=[
                             {"start_unix_s": 0, "end_unix_s": end - 1, "multiplier": large},
                             {"start_unix_s": end - 1, "end_unix_s": end, "multiplier": fractional},
                         ])
        result = MODEL.evaluate(self.data)
        expected = Fraction(rate) * Fraction(large) * (end - 1) + Fraction(rate) * Fraction(fractional)
        self.assertEqual(Fraction(result["earned_units"]), expected)
        self.assertEqual(sum(Fraction(s["earned_units"]) for s in result["segments"]), expected)

    def test_claim_identity_uses_timeline_currency_and_interval(self):
        first = MODEL.evaluate(self.data)["settlement"]["claim_id"]
        self.data["rule_version"] = "another-rule"
        self.assertEqual(MODEL.evaluate(self.data)["settlement"]["claim_id"], first)
        other_currency = copy.deepcopy(self.data)
        other_currency["currency"] = "another-currency"
        self.assertNotEqual(MODEL.evaluate(other_currency)["settlement"]["claim_id"], first)
        self.data["timeline_id"] = "another-timeline"
        self.assertNotEqual(MODEL.evaluate(self.data)["settlement"]["claim_id"], first)

    def test_missing_and_unknown_fields(self):
        for mutation in ("missing", "unknown"):
            data = copy.deepcopy(self.data)
            if mutation == "missing":
                del data["cap_seconds"]
            else:
                data["extra"] = True
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                MODEL.evaluate(data)

    def test_invalid_scalar_inputs(self):
        invalid = [("schema_version", True), ("checkpoint_unix_s", True),
                   ("resume_unix_s", 1.5), ("cap_seconds", -1),
                   ("resume_unix_s", 10 ** 12 + 1),
                   ("base_rate_per_second", 0.1), ("base_rate_per_second", "NaN"),
                   ("base_rate_per_second", "1e3"), ("base_rate_per_second", "-1"),
                   ("timeline_id", ""), ("assumptions", []), ("assumptions", [1])]
        for key, value in invalid:
            data = copy.deepcopy(self.data)
            data[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                MODEL.evaluate(data)

    def test_invalid_intervals(self):
        invalid = [None, [{"start_unix_s": 2, "end_unix_s": 2}],
                   [{"start_unix_s": 5, "end_unix_s": 4}],
                   [{"start_unix_s": 1, "end_unix_s": 2, "extra": 1}]]
        for value in invalid:
            self.data["settled_intervals"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                MODEL.evaluate(self.data)

    def test_cli_outputs_json(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["earned_units"], "175")

    def test_cli_rejects_invalid_and_missing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.json"
            invalid.write_text("{}", encoding="utf-8")
            for path in (invalid, Path(directory) / "missing.json"):
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
