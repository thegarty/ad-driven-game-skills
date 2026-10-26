"""Numeric and failure-path contracts for the independently installable helpers."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
ECONOMY = ROOT / "skills/game-progression-and-economy"
ANALYTICS = ROOT / "skills/game-analytics-and-experiments"
REVENUE = ROOT / "skills/game-profitability-and-priorities"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


economy = load("economy_scenario", ECONOMY / "scripts/economy_scenario.py")
cohorts = load("cohort_retention", ANALYTICS / "scripts/cohort_retention.py")
revenue = load("revenue_sensitivity", REVENUE / "scripts/revenue_sensitivity.py")


def fixture(path):
    return json.loads(path.read_text(encoding="utf-8"))


class EconomyTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture(ECONOMY / "assets/economy-example.json")

    def test_known_scenario_and_cap(self):
        result = economy.evaluate(self.data)
        self.assertEqual(result["normal_income_total"], 40)
        self.assertEqual(result["reward_income_total"], 10)
        self.assertEqual(result["assumed_earned_rewards_total"], 2)
        self.assertEqual(result["spending_total"], 20)
        self.assertEqual(result["closing_balance"], 30)
        self.assertEqual(result["milestones"][0]["first_affordable_step"], 2)
        self.assertIsNone(result["milestones"][1]["first_affordable_step"])

    def test_free_route(self):
        self.data["optional_earned_rewards_per_step"] = 0
        self.data["optional_reward_cap_total"] = 0
        result = economy.evaluate(self.data)
        self.assertEqual(result["reward_income_total"], 0)
        self.assertEqual(result["closing_balance"], 20)

    def test_initial_milestone_is_step_zero(self):
        self.data["initial_balance"] = 20
        self.assertEqual(economy.evaluate(self.data)["milestones"][0]["first_affordable_step"], 0)

    def test_unaffordable_purchase_is_skipped_not_retried(self):
        self.data["spends"] = [{"step": 1, "label": "expensive", "cost": 20}]
        result = economy.evaluate(self.data)
        self.assertEqual(result["timeline"][0]["spends"][0]["outcome"], "insufficient_balance")
        self.assertEqual(result["spending_total"], 0)
        self.assertEqual(result["closing_balance"], 50)

    def test_spends_execute_in_list_order(self):
        self.data["spends"] = [{"step": 1, "label": "first", "cost": 10},
                               {"step": 1, "label": "second", "cost": 10}]
        result = economy.evaluate(self.data)
        self.assertEqual([x["outcome"] for x in result["timeline"][0]["spends"]],
                         ["paid", "insufficient_balance"])

    def test_fractional_spends_use_decimal_affordability(self):
        self.data.update(steps=1, initial_balance=0.3, normal_income_per_active_minute=0,
                         optional_earned_rewards_per_step=0, optional_reward_cap_total=0,
                         spends=[{"step": 1, "label": "first", "cost": 0.1},
                                 {"step": 1, "label": "second", "cost": 0.2}])
        result = economy.evaluate(self.data)
        self.assertEqual([item["outcome"] for item in result["timeline"][0]["spends"]], ["paid", "paid"])
        self.assertEqual(result["closing_balance"], 0)
        self.assertEqual(result["spending_total"], 0.3)
        json.dumps(result, allow_nan=False)

    def test_decimal_comparison_does_not_hide_a_real_shortfall(self):
        self.data.update(steps=1, initial_balance=0.3, normal_income_per_active_minute=0,
                         optional_earned_rewards_per_step=0, optional_reward_cap_total=0,
                         spends=[{"step": 1, "label": "shortfall", "cost": 0.30000000000000004}])
        self.assertEqual(economy.evaluate(self.data)["timeline"][0]["spends"][0]["outcome"],
                         "insufficient_balance")

    def test_missing_and_unknown_fields(self):
        del self.data["assumptions"]
        with self.assertRaises(ValueError):
            economy.evaluate(self.data)
        self.data["assumptions"] = ["synthetic"]
        self.data["typo"] = 1
        with self.assertRaises(ValueError):
            economy.evaluate(self.data)

    def test_invalid_numeric_inputs(self):
        for value in (-1, float("nan"), float("inf"), True, "2"):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["normal_income_per_active_minute"] = value
                with self.assertRaises(ValueError):
                    economy.evaluate(data)

    def test_invalid_integer_and_duration_inputs(self):
        for field, value in (("steps", 0), ("steps", 10001), ("steps", 1.5),
                             ("optional_reward_cap_total", True), ("active_minutes_per_step", 0)):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data[field] = value
                with self.assertRaises(ValueError):
                    economy.evaluate(data)

    def test_calculation_overflow(self):
        self.data["active_minutes_per_step"] = 1e308
        self.data["normal_income_per_active_minute"] = 10
        with self.assertRaises(ValueError):
            economy.evaluate(self.data)

    def test_duplicate_milestone_is_rejected(self):
        self.data["milestones"].append(copy.deepcopy(self.data["milestones"][0]))
        with self.assertRaises(ValueError):
            economy.evaluate(self.data)


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.installs = cohorts.rows(ANALYTICS / "assets/installs-example.csv", {"user_id", "install_date"})
        self.activity = cohorts.rows(ANALYTICS / "assets/activity-example.csv", {"user_id", "activity_date"})

    def calculate(self, **kwargs):
        args = {"installs": self.installs, "activity": self.activity, "as_of": "2026-01-08",
                "days": [1, 7], "population": "synthetic", "timezone": "UTC"}
        args.update(kwargs)
        return cohorts.calculate(**args)

    def test_exact_day_counts_deduplication_and_maturity(self):
        result = self.calculate()
        d1, d7 = result["aggregate"]
        self.assertEqual((d1["retained_installs"], d1["eligible_installs"]), (2, 3))
        self.assertEqual((d7["retained_installs"], d7["eligible_installs"]), (1, 2))
        self.assertEqual(d7["retention"], 0.5)
        self.assertEqual(result["diagnostics"]["duplicate_activity_rows"], 1)
        self.assertEqual(result["cohorts"][1]["days"][1]["status"], "immature")
        self.assertIsNone(result["cohorts"][1]["days"][1]["retention"])

    def test_no_eligible_installs_is_null_not_zero(self):
        result = self.calculate(as_of="2026-01-01")
        self.assertIsNone(result["aggregate"][0]["retention"])
        self.assertEqual(result["aggregate"][0]["status"], "no_eligible_installs")

    def test_mature_without_activity_is_zero(self):
        result = self.calculate(activity=[])
        self.assertEqual(result["aggregate"][1]["retention"], 0)

    def test_empty_roster(self):
        result = self.calculate(installs=[], activity=[])
        self.assertEqual(result["install_count_through_cutoff"], 0)
        self.assertIsNone(result["aggregate"][0]["retention"])

    def test_future_rows_are_reported(self):
        result = self.calculate(as_of="2026-01-02")
        self.assertEqual(result["diagnostics"]["future_install_rows_excluded"], 1)
        self.assertEqual(result["diagnostics"]["future_activity_rows_excluded"], 3)

    def test_day_after_target_does_not_count_as_exact_day(self):
        result = self.calculate(activity=[{"user_id": "example-b", "activity_date": "2026-01-03"}])
        self.assertEqual(result["aggregate"][0]["retained_installs"], 0)

    def test_duplicate_install_has_no_extra_denominator(self):
        self.installs.append(copy.deepcopy(self.installs[0]))
        result = self.calculate()
        self.assertEqual(result["aggregate"][0]["eligible_installs"], 3)
        self.assertEqual(result["diagnostics"]["duplicate_install_rows"], 1)

    def test_conflicting_reinstall_and_unknown_activity(self):
        with self.assertRaises(ValueError):
            self.calculate(installs=self.installs + [{"user_id": "example-a", "install_date": "2026-01-02"}])
        with self.assertRaises(ValueError):
            self.calculate(activity=[{"user_id": "not-in-roster", "activity_date": "2026-01-02"}])

    def test_activity_before_install(self):
        with self.assertRaises(ValueError):
            self.calculate(activity=[{"user_id": "example-c", "activity_date": "2026-01-01"}])

    def test_invalid_dates_days_and_context(self):
        for kwargs in ({"as_of": "2026-02-30"}, {"as_of": "20260108"}, {"days": [0]},
                       {"days": [True]}, {"days": [1.5]}, {"days": []},
                       {"population": ""}, {"timezone": ""}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    self.calculate(**kwargs)

    def test_missing_csv_header(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.csv"
            path.write_text("user_id\nexample-a\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                cohorts.rows(path, {"user_id", "install_date"})

    def test_weighted_aggregate_not_mean_of_rates(self):
        installs = [{"user_id": "a", "install_date": "2026-01-01"},
                    {"user_id": "b", "install_date": "2026-01-02"},
                    {"user_id": "c", "install_date": "2026-01-02"},
                    {"user_id": "d", "install_date": "2026-01-02"}]
        activity = [{"user_id": "a", "activity_date": "2026-01-02"}]
        self.assertEqual(self.calculate(installs=installs, activity=activity)["aggregate"][0]["retention"], 0.25)


class RevenueTests(unittest.TestCase):
    def setUp(self):
        self.data = fixture(REVENUE / "assets/revenue-example.json")

    def test_known_results_and_retention_tradeoff(self):
        result = revenue.evaluate(self.data)
        first, second = result["scenarios"]
        self.assertEqual(first["impressions_per_install"], 15)
        self.assertAlmostEqual(first["ad_revenue_per_install"], 0.15)
        self.assertAlmostEqual(first["revenue_per_install"], 0.25)
        self.assertAlmostEqual(first["contribution_before_acquisition"], 0.23)
        self.assertAlmostEqual(first["contribution_after_acquisition"], 0.03)
        self.assertAlmostEqual(first["revenue_roas"], 1.25)
        self.assertLess(second["revenue_per_install"], first["revenue_per_install"])
        self.assertEqual(result["evidence_type"], "scenario_arithmetic")

    def test_zero_cpi_has_no_roas(self):
        self.data["scenarios"][0]["cpi"] = 0
        self.assertIsNone(revenue.evaluate(self.data)["scenarios"][0]["revenue_roas"])

    def test_zero_impressions_has_zero_ad_proceeds(self):
        self.data["scenarios"][0]["impressions_per_active_day"] = 0
        self.assertEqual(revenue.evaluate(self.data)["scenarios"][0]["ad_revenue_per_install"], 0)

    def test_negative_contribution_cannot_break_even_at_free_acquisition(self):
        self.data["scenarios"][0]["variable_cost_per_install"] = 1
        result = revenue.evaluate(self.data)["scenarios"][0]
        self.assertLess(result["contribution_before_acquisition"], 0)
        self.assertIsNone(result["break_even_cpi_before_fixed_costs"])
        self.assertFalse(result["covers_variable_costs_at_zero_cpi"])

    def test_fractional_exact_break_even_is_zero(self):
        self.data["scenarios"] = [dict(self.data["scenarios"][0],
                                      retained_active_days_per_install=1, impressions_per_active_day=1,
                                      realized_ecpm=100, net_iap_revenue_per_install=0.7,
                                      variable_cost_per_install=0.8, cpi=0)]
        result = revenue.evaluate(self.data)["scenarios"][0]
        self.assertEqual(result["revenue_per_install"], 0.8)
        self.assertEqual(result["contribution_before_acquisition"], 0)
        self.assertEqual(result["contribution_after_acquisition"], 0)
        self.assertEqual(result["break_even_cpi_before_fixed_costs"], 0)
        self.assertTrue(result["covers_variable_costs_at_zero_cpi"])
        json.dumps(result, allow_nan=False)

    def test_fractional_acquisition_cost_does_not_create_false_loss(self):
        self.data["scenarios"] = [dict(self.data["scenarios"][0], impressions_per_active_day=0,
                                      net_iap_revenue_per_install=0.3, variable_cost_per_install=0.1, cpi=0.2)]
        result = revenue.evaluate(self.data)["scenarios"][0]
        self.assertEqual(result["contribution_before_acquisition"], 0.2)
        self.assertEqual(result["contribution_after_acquisition"], 0)

    def test_missing_and_unknown_fields(self):
        del self.data["scenarios"][0]["cpi"]
        with self.assertRaises(ValueError):
            revenue.evaluate(self.data)
        self.data["scenarios"][0]["cpi"] = 0.2
        self.data["not_a_field"] = 1
        with self.assertRaises(ValueError):
            revenue.evaluate(self.data)

    def test_invalid_numeric_inputs(self):
        for value in (-1, float("nan"), float("inf"), True, "10"):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["scenarios"][0]["realized_ecpm"] = value
                with self.assertRaises(ValueError):
                    revenue.evaluate(data)

    def test_active_days_cannot_exceed_horizon(self):
        self.data["scenarios"][0]["retained_active_days_per_install"] = 31
        with self.assertRaises(ValueError):
            revenue.evaluate(self.data)

    def test_unknown_evidence_and_empty_assumptions(self):
        self.data["scenarios"][0]["input_basis"] = "proven forecast"
        with self.assertRaises(ValueError):
            revenue.evaluate(self.data)
        self.data["scenarios"][0]["input_basis"] = "synthetic"
        self.data["assumptions"] = []
        with self.assertRaises(ValueError):
            revenue.evaluate(self.data)

    def test_overflow_is_rejected(self):
        self.data["scenarios"][0]["impressions_per_active_day"] = 1e308
        with self.assertRaises(ValueError):
            revenue.evaluate(self.data)


class CommandLineTests(unittest.TestCase):
    def run_cli(self, script, *args):
        return subprocess.run([sys.executable, str(script)] + list(map(str, args)),
                              capture_output=True, text=True, timeout=10)

    def test_all_synthetic_examples_produce_json(self):
        commands = [
            (ECONOMY / "scripts/economy_scenario.py", ECONOMY / "assets/economy-example.json"),
            (REVENUE / "scripts/revenue_sensitivity.py", REVENUE / "assets/revenue-example.json"),
            (ANALYTICS / "scripts/cohort_retention.py", "--installs", ANALYTICS / "assets/installs-example.csv",
             "--activity", ANALYTICS / "assets/activity-example.csv", "--as-of", "2026-01-08",
             "--days", "1", "7", "--population", "Synthetic example", "--timezone", "UTC"),
        ]
        for command in commands:
            with self.subTest(script=command[0]):
                result = self.run_cli(*command)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("evidence_type", json.loads(result.stdout))

    def test_invalid_json_and_missing_file_fail_cleanly(self):
        for script in (ECONOMY / "scripts/economy_scenario.py", REVENUE / "scripts/revenue_sensitivity.py"):
            with self.subTest(script=script), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "bad.json"
                path.write_text("{", encoding="utf-8")
                result = self.run_cli(script, path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)
                result = self.run_cli(script, Path(temp) / "absent.json")
                self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
