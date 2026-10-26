#!/usr/bin/env python3
"""Two-arm participant-level descriptive readout; no dependency or ship decision.

See references/experiment-helper.md for input and inferential limitations.
"""

import argparse
from datetime import date
import json
import math
from pathlib import Path
import random
import statistics
import sys


FIELDS = {
    "schema_version", "evidence_type", "experiment_id", "population", "metric",
    "unit", "timezone", "outcome_definition", "horizon_days", "as_of_date",
    "design", "assignment_unit", "assignment_roster_complete",
    "expected_treatment_fraction", "assumptions", "participants",
}
ROW_FIELDS = {"participant_id", "arm", "assigned_date", "exposed",
              "observation_complete", "outcome"}


def require_keys(value, keys, label):
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("{} must contain exactly: {}".format(label, ", ".join(sorted(keys))))


def text_value(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonempty string")


def integer(value, label, low, high):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError("{} must be an integer from {} to {}".format(label, low, high))


def number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(label + " must be a finite number")
    try:
        result = float(value)
    except (OverflowError, ValueError):
        raise ValueError(label + " must be a finite number") from None
    if not math.isfinite(result) or abs(result) > 1e12:
        raise ValueError(label + " must be finite with absolute value at most 1e12")
    return result


def calendar_date(value, label):
    text_value(value, label)
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ValueError(label + " must be YYYY-MM-DD") from None
    if parsed.isoformat() != value:
        raise ValueError(label + " must be YYYY-MM-DD")
    return parsed


def quantile(sorted_values, probability):
    position = (len(sorted_values) - 1) * probability
    low = int(position)
    high = min(low + 1, len(sorted_values) - 1)
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * (position - low)


def evaluate(data, seed=42, resamples=2000, confidence=0.95):
    require_keys(data, FIELDS, "input")
    integer(data["schema_version"], "schema_version", 1, 1)
    integer(seed, "seed", 0, 2**32 - 1)
    integer(resamples, "resamples", 200, 20000)
    confidence = number(confidence, "confidence")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    for key in ("experiment_id", "population", "metric", "unit", "timezone", "outcome_definition"):
        text_value(data[key], key)
    if data["evidence_type"] not in ("synthetic", "observed"):
        raise ValueError("evidence_type must be synthetic or observed")
    if data["design"] not in ("randomized", "observational"):
        raise ValueError("design must be randomized or observational")
    if data["assignment_unit"] != "player":
        raise ValueError("this helper supports player assignment only; clusters need another analysis")
    if not isinstance(data["assignment_roster_complete"], bool):
        raise ValueError("assignment_roster_complete must be boolean")
    integer(data["horizon_days"], "horizon_days", 1, 3660)
    as_of = calendar_date(data["as_of_date"], "as_of_date")
    fraction = number(data["expected_treatment_fraction"], "expected_treatment_fraction")
    if not 0 < fraction < 1:
        raise ValueError("expected_treatment_fraction must be between zero and one")
    if not isinstance(data["assumptions"], list) or not data["assumptions"]:
        raise ValueError("assumptions must be a nonempty list")
    for item in data["assumptions"]:
        text_value(item, "assumption")
    if not isinstance(data["participants"], list) or len(data["participants"]) > 10000:
        raise ValueError("participants must be a list of at most 10000 assigned players")
    if len(data["participants"]) * resamples > 50000000:
        raise ValueError("requested bootstrap exceeds 50000000 participant draws; reduce resamples or use another tool")

    values = {"control": [], "treatment": []}
    counts = {arm: dict(assigned=0, exposed=0, mature=0, complete=0, missing_outcome=0,
                       incomplete_observation=0, immature=0) for arm in values}
    seen = {}
    for index, row in enumerate(data["participants"]):
        label = "participants[{}]".format(index)
        require_keys(row, ROW_FIELDS, label)
        text_value(row["participant_id"], label + ".participant_id")
        arm = row["arm"]
        text_value(arm, label + ".arm")
        if arm not in values:
            raise ValueError(label + ".arm must be control or treatment")
        if row["participant_id"] in seen:
            reason = "conflicting assignment" if seen[row["participant_id"]] != arm else "duplicate participant"
            raise ValueError(reason + ": each assigned player must appear exactly once")
        seen[row["participant_id"]] = arm
        assigned = calendar_date(row["assigned_date"], label + ".assigned_date")
        if assigned > as_of:
            raise ValueError(label + ": assignment cannot follow as_of_date")
        for key in ("exposed", "observation_complete"):
            if not isinstance(row[key], bool):
                raise ValueError(label + "." + key + " must be boolean")
        mature = (as_of - assigned).days >= data["horizon_days"]
        if row["observation_complete"] and not mature:
            raise ValueError(label + ": complete observation asserted before horizon has matured")
        outcome = None if row["outcome"] is None else number(row["outcome"], label + ".outcome")
        complete = mature and row["observation_complete"] and outcome is not None
        counter = counts[arm]
        counter["assigned"] += 1
        counter["exposed"] += int(row["exposed"])
        counter["mature"] += int(mature)
        counter["complete"] += int(complete)
        counter["missing_outcome"] += int(outcome is None)
        counter["incomplete_observation"] += int(not row["observation_complete"])
        counter["immature"] += int(not mature)
        if complete:
            values[arm].append(outcome)

    warnings = [
        "Completeness, random assignment and independent player identity are caller assertions, not verified by this calculation.",
        "The percentile bootstrap does not correct peeking, multiple testing, missingness, nonrandom assignment or unobserved rare outcomes.",
    ]
    if data["design"] == "observational":
        warnings.append("Observational arm differences are associations; no causal interpretation is supported.")
    total = sum(item["assigned"] for item in counts.values())
    expected = {"control": total * (1 - fraction), "treatment": total * fraction}
    srm = {"expected_counts": expected, "status": "unavailable", "chi_square": None,
           "approximate_p_value": None,
           "limitation": "Assignment diagnostic only; assumes independent Bernoulli assignment at the declared fraction. Fixed blocks, adaptive allocation and clustered assignment require design-specific checks."}
    if data["design"] == "randomized" and data["assignment_roster_complete"] and min(expected.values()) >= 5:
        stat = math.fsum((counts[arm]["assigned"] - expected[arm])**2 / expected[arm] for arm in counts)
        srm.update(status="screen_only", chi_square=stat, approximate_p_value=math.erfc(math.sqrt(stat / 2)))
    else:
        srm["reason"] = "Requires randomized design, complete assignment roster, and at least five expected players per arm."

    ready = data["assignment_roster_complete"] and all(
        counter["assigned"] > 0 and counter["complete"] == counter["assigned"] for counter in counts.values())
    summary = {}
    for arm, counter in counts.items():
        observed = values[arm]
        summary[arm] = dict(counter, mean=None, standard_deviation=None, minimum=None, maximum=None,
                            nonzero_outcomes=None)
        if ready:
            summary[arm].update(mean=statistics.fmean(observed),
                                standard_deviation=statistics.stdev(observed) if len(observed) > 1 else None,
                                minimum=min(observed), maximum=max(observed),
                                nonzero_outcomes=sum(item != 0 for item in observed))
    result = {
        "evidence_type": "synthetic_calculation" if data["evidence_type"] == "synthetic" else "calculation_from_supplied_observations",
        "experiment_id": data["experiment_id"], "population": data["population"],
        "design_asserted": data["design"], "assignment_unit": data["assignment_unit"],
        "metric": data["metric"], "unit": data["unit"], "outcome_definition": data["outcome_definition"],
        "horizon_days": data["horizon_days"], "as_of_date": data["as_of_date"], "timezone": data["timezone"],
        "assumptions": list(data["assumptions"]), "assignment_roster_complete": data["assignment_roster_complete"],
        "analysis_population": "All supplied assigned players, regardless of exposure; no zero imputation or complete-case comparison.",
        "status": "descriptive_readout" if ready else "withheld_incomplete_data",
        "arms": summary, "assignment_ratio_screen": srm,
        "treatment_minus_control": None, "bootstrap_interval": None,
        "bootstrap_settings": {"seed": seed, "resamples": resamples, "confidence": confidence},
        "warnings": warnings,
    }
    if not ready:
        warnings.append("Comparison withheld: supply a complete assignment roster and fully observed outcomes for both arms; null and incomplete outcomes are not zeros.")
        return result
    result["treatment_minus_control"] = summary["treatment"]["mean"] - summary["control"]["mean"]
    if min(len(items) for items in values.values()) < 30:
        warnings.append("At least one arm has fewer than 30 players. This is a practical small-sample flag, not a validity threshold; percentile intervals can severely under-cover.")
    warnings.append("Inspect rare high-value outcomes, influence and population coverage; resampling cannot reveal a revenue tail absent from this sample.")
    if min(len(items) for items in values.values()) < 2:
        warnings.append("Bootstrap interval withheld: at least two observed players per arm are required even for this descriptive calculation.")
        return result
    rng = random.Random(seed)
    control, treatment = values["control"], values["treatment"]
    differences = []
    for _ in range(resamples):
        c_mean = math.fsum(rng.choice(control) for _ in control) / len(control)
        t_mean = math.fsum(rng.choice(treatment) for _ in treatment) / len(treatment)
        differences.append(t_mean - c_mean)
    differences.sort()
    alpha = (1 - confidence) / 2
    low, high = quantile(differences, alpha), quantile(differences, 1 - alpha)
    result["bootstrap_interval"] = {"method": "within-arm player percentile bootstrap, linear quantiles",
                                    "low": low, "high": high, "confidence": confidence,
                                    "unit": data["unit"]}
    if low == high:
        warnings.append("Degenerate interval: observed samples contain insufficient variation; this does not establish certainty about the population.")
    return result


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key: " + key)
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--resamples", type=int, default=2000)
    parser.add_argument("--confidence", type=float, default=0.95)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
        output = evaluate(data, args.seed, args.resamples, args.confidence)
        print(json.dumps(output, indent=2, allow_nan=False))
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
