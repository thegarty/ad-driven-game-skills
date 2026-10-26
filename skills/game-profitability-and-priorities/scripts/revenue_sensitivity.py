#!/usr/bin/env python3
"""Calculate explicit cohort revenue/CPI scenarios, without predicting retention or ad yield."""

import argparse
from decimal import Decimal, localcontext
import json
import math
from pathlib import Path


def number(value, name, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("%s must be numeric" % name)
    try:
        valid = math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    if not valid or (maximum is not None and value > maximum):
        raise ValueError("%s must be finite, nonnegative%s" % (name, " and <= %s" % maximum if maximum is not None else ""))
    return Decimal(value) if isinstance(value, int) else Decimal(str(value))


def precision_for(data):
    """Allow exact finite-decimal products/sums across the supplied scale range."""
    values = []
    def visit(value):
        if isinstance(value, dict):
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, int) and not isinstance(value, bool):
            values.append(Decimal(value))
        elif isinstance(value, float) and math.isfinite(value):
            values.append(Decimal(str(value)))
    visit(data)
    if not values:
        return 28
    highest = max(value.adjusted() for value in values)
    lowest = min(value.as_tuple().exponent for value in values)
    return max(28, 3 * (highest - lowest + 1) + 20)


def calculated(value, name):
    if not value.is_finite() or not math.isfinite(float(value)):
        raise ValueError("calculated %s is not finite" % name)
    return value


def json_numbers(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, dict):
        return {key: json_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_numbers(item) for item in value]
    return value


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("%s must be a nonempty string" % name)
    return value


def evaluate(data):
    with localcontext() as context:
        context.prec = precision_for(data)
        return json_numbers(evaluate_decimal(data))


def evaluate_decimal(data):
    keys = {"currency", "horizon_days", "population", "assumptions", "scenarios"}
    if not isinstance(data, dict) or set(data) != keys:
        raise ValueError("input requires exactly currency, horizon_days, population, assumptions and scenarios")
    currency = text(data["currency"], "currency")
    population = text(data["population"], "population")
    horizon = data["horizon_days"]
    if isinstance(horizon, bool) or not isinstance(horizon, int) or not 1 <= horizon <= 3650:
        raise ValueError("horizon_days must be an integer between 1 and 3650")
    assumptions = data["assumptions"]
    if not isinstance(assumptions, list) or not assumptions:
        raise ValueError("assumptions must be a nonempty list of strings")
    for assumption in assumptions:
        text(assumption, "assumption")
    if not isinstance(data["scenarios"], list) or not data["scenarios"]:
        raise ValueError("scenarios must be a nonempty list")
    results = []
    names = set()
    scenario_keys = {"label", "input_basis", "retained_active_days_per_install", "impressions_per_active_day",
                     "realized_ecpm", "net_iap_revenue_per_install", "variable_cost_per_install", "cpi"}
    for item in data["scenarios"]:
        if not isinstance(item, dict) or set(item) != scenario_keys:
            raise ValueError("each scenario requires exactly %s" % ", ".join(sorted(scenario_keys)))
        label = text(item["label"], "scenario label")
        if label in names:
            raise ValueError("scenario labels must be unique")
        names.add(label)
        basis = item["input_basis"]
        if basis not in ("synthetic", "observed", "mixed"):
            raise ValueError("input_basis must be synthetic, observed or mixed")
        active_days = number(item["retained_active_days_per_install"], "retained_active_days_per_install", horizon)
        impressions_daily = number(item["impressions_per_active_day"], "impressions_per_active_day")
        ecpm = number(item["realized_ecpm"], "realized_ecpm")
        iap = number(item["net_iap_revenue_per_install"], "net_iap_revenue_per_install")
        variable_cost = number(item["variable_cost_per_install"], "variable_cost_per_install")
        cpi = number(item["cpi"], "cpi")
        impressions = calculated(active_days * impressions_daily, "impressions")
        ad_revenue = calculated(impressions * (ecpm / 1000), "ad revenue")
        revenue = calculated(ad_revenue + iap, "revenue")
        before_acquisition = revenue - variable_cost
        after_acquisition = before_acquisition - cpi
        roas = revenue / cpi if cpi else None
        for name, value in (("contribution before acquisition", before_acquisition),
                            ("contribution after acquisition", after_acquisition), ("ROAS", roas)):
            if value is not None:
                calculated(value, name)
        results.append({"label": label, "input_basis": basis,
                        "impressions_per_install": impressions, "ad_revenue_per_install": ad_revenue,
                        "net_iap_revenue_per_install": iap, "revenue_per_install": revenue,
                        "variable_cost_per_install": variable_cost, "cpi": cpi,
                        "contribution_before_acquisition": before_acquisition,
                        "contribution_after_acquisition": after_acquisition,
                        "break_even_cpi_before_fixed_costs": before_acquisition if before_acquisition >= 0 else None,
                        "revenue_roas": roas,
                        "covers_variable_costs_at_zero_cpi": before_acquisition >= 0})
    return {"evidence_type": "scenario_arithmetic", "currency": currency,
            "population": population, "horizon_days": horizon, "assumptions": assumptions,
            "scenarios": results,
            "limitations": ["The inputs are asserted by the caller; input_basis is not independently verified.",
                            "No retention tail, causal uplift, confidence interval or spend recommendation is inferred.",
                            "Fixed operating/content costs, taxes outside supplied net proceeds, and financing are not modelled.",
                            "Products of averages can hide correlations; use direct cohort revenue where available."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="scenario JSON file")
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, OverflowError) as exc:
        parser.exit(2, "error: %s\n" % exc)


if __name__ == "__main__":
    main()
