#!/usr/bin/env python3
"""Evaluate an explicit, deterministic economy scenario. No game/SDK access."""

import argparse
from decimal import Decimal, localcontext
import json
import math
import sys
from pathlib import Path


def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("%s must be a number" % name)
    try:
        valid = math.isfinite(value) and (value > 0 if positive else value >= 0)
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError("%s must be finite and %s" % (name, "positive" if positive else "nonnegative"))
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
    if not value.is_finite() or value < 0 or not math.isfinite(float(value)):
        raise ValueError("%s must be finite and nonnegative" % name)
    return value


def json_numbers(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, dict):
        return {key: json_numbers(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_numbers(item) for item in value]
    return value


def integer(value, name, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError("%s must be an integer >= %s" % (name, minimum))
    if maximum is not None and value > maximum:
        raise ValueError("%s must be <= %s" % (name, maximum))
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
    if not isinstance(data, dict):
        raise ValueError("scenario must be a JSON object")
    required = {"currency", "steps", "active_minutes_per_step", "normal_income_per_active_minute",
                "initial_balance", "optional_earned_rewards_per_step", "optional_reward_value",
                "optional_reward_cap_total", "spends", "milestones", "assumptions"}
    if set(data) != required:
        raise ValueError("scenario keys differ: missing=%s unknown=%s" %
                         (sorted(required - set(data)), sorted(set(data) - required)))
    currency = text(data["currency"], "currency")
    steps = integer(data["steps"], "steps", 1, 10000)
    minutes = number(data["active_minutes_per_step"], "active_minutes_per_step", True)
    rate = number(data["normal_income_per_active_minute"], "normal_income_per_active_minute")
    balance = number(data["initial_balance"], "initial_balance")
    earned_per_step = integer(data["optional_earned_rewards_per_step"], "optional_earned_rewards_per_step")
    reward_value = number(data["optional_reward_value"], "optional_reward_value")
    cap = integer(data["optional_reward_cap_total"], "optional_reward_cap_total")
    assumptions = data["assumptions"]
    if not isinstance(assumptions, list) or not assumptions:
        raise ValueError("assumptions must be a nonempty list of strings")
    for item in assumptions:
        text(item, "assumption")
    if not isinstance(data["spends"], list) or not isinstance(data["milestones"], list):
        raise ValueError("spends and milestones must be lists")
    spends = {}
    for item in data["spends"]:
        if not isinstance(item, dict) or set(item) != {"step", "label", "cost"}:
            raise ValueError("each spend requires exactly step, label and cost")
        step = integer(item["step"], "spend step", 1, steps)
        label = text(item["label"], "spend label")
        cost = number(item["cost"], "spend cost")
        spends.setdefault(step, []).append({"step": step, "label": label, "cost": cost})
    milestones = []
    labels = set()
    for item in data["milestones"]:
        if not isinstance(item, dict) or set(item) != {"label", "cost"}:
            raise ValueError("each milestone requires exactly label and cost")
        label = text(item["label"], "milestone label")
        if label in labels:
            raise ValueError("milestone labels must be unique")
        labels.add(label)
        cost = number(item["cost"], "milestone cost")
        milestones.append({"label": label, "cost": cost,
                           "first_affordable_step": 0 if balance >= cost else None})
    normal_per_step = calculated(minutes * rate, "calculated normal income")
    timeline = []
    earned_total = 0
    normal_total = 0
    rewards_total = 0
    spent_total = 0
    for step in range(1, steps + 1):
        earned = min(earned_per_step, cap - earned_total)
        reward_income = calculated(earned * reward_value, "calculated reward income")
        normal_total = calculated(normal_total + normal_per_step, "calculated total normal income")
        rewards_total = calculated(rewards_total + reward_income, "calculated total reward income")
        balance = calculated(balance + normal_per_step + reward_income, "calculated balance")
        earned_total += earned
        for item in milestones:
            if item["first_affordable_step"] is None and balance >= item["cost"]:
                item["first_affordable_step"] = step
        spending = []
        for item in spends.get(step, []):
            paid = balance >= item["cost"]
            if paid:
                balance -= item["cost"]
                spent_total = calculated(spent_total + item["cost"], "calculated total spending")
            spending.append({"label": item["label"], "cost": item["cost"],
                             "outcome": "paid" if paid else "insufficient_balance"})
        timeline.append({"step": step, "normal_income": normal_per_step,
                         "assumed_earned_rewards": earned, "reward_income": reward_income,
                         "spends": spending, "closing_balance": balance})
    return {"evidence_type": "simulated", "currency": currency,
            "assumptions": assumptions, "active_minutes": calculated(steps * minutes, "calculated active minutes"),
            "normal_income_total": normal_total, "reward_income_total": rewards_total,
            "assumed_earned_rewards_total": earned_total, "spending_total": spent_total,
            "closing_balance": balance, "milestones": milestones, "timeline": timeline,
            "limitations": ["No human behaviour, retention, ad availability or revenue is predicted.",
                            "Fixed income rate; purchases do not change production.",
                            "Milestones record affordability before scheduled spends; they do not unlock or grant anything.",
                            "One active-time step model; offline income, daily resets and cooldowns are not simulated."]}


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
