#!/usr/bin/env python3
"""Model a capped offline settlement; no actual save, wallet or clock access."""

import argparse
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import re


MAX_TIME = 10 ** 12
DECIMAL = re.compile(r"^[0-9]+(?:\.[0-9]+)?$")


def integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_TIME:
        raise ValueError("%s must be an integer from 0 to %d" % (name, MAX_TIME))
    return value


def text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 500:
        raise ValueError("%s must be a nonempty string of at most 500 characters" % name)
    return value


def decimal(value, name):
    if not isinstance(value, str) or len(value) > 64 or not DECIMAL.fullmatch(value):
        raise ValueError("%s must be a nonnegative plain decimal string, at most 64 characters" % name)
    return Decimal(value)


def plain(value):
    result = format(value, "f")
    return result.rstrip("0").rstrip(".") if "." in result else result


def intervals(values, boosters=False):
    if not isinstance(values, list) or len(values) > 1000:
        raise ValueError("interval lists must contain at most 1000 entries")
    required = {"start_unix_s", "end_unix_s"} | ({"multiplier"} if boosters else set())
    result = []
    for value in values:
        if not isinstance(value, dict) or set(value) != required:
            raise ValueError("interval fields must be %s" % sorted(required))
        start = integer(value["start_unix_s"], "interval start")
        end = integer(value["end_unix_s"], "interval end")
        if end <= start:
            raise ValueError("interval end must be after start")
        factor = decimal(value["multiplier"], "multiplier") if boosters else Decimal(1)
        if boosters and factor < 1:
            raise ValueError("booster multiplier must be at least 1")
        result.append((start, end, factor))
    result.sort()
    if boosters and any(left[1] > right[0] for left, right in zip(result, result[1:])):
        raise ValueError("overlapping boosters require a product-specific stacking policy")
    return result


def evaluate(data):
    required = {"schema_version", "timeline_id", "currency", "rule_version",
                "checkpoint_unix_s", "resume_unix_s", "cap_seconds",
                "base_rate_per_second", "boosters", "settled_intervals", "assumptions"}
    if not isinstance(data, dict) or set(data) != required:
        raise ValueError("input fields must be exactly %s" % sorted(required))
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    timeline = text(data["timeline_id"], "timeline_id")
    currency = text(data["currency"], "currency")
    rule = text(data["rule_version"], "rule_version")
    start = integer(data["checkpoint_unix_s"], "checkpoint_unix_s")
    end = integer(data["resume_unix_s"], "resume_unix_s")
    cap = integer(data["cap_seconds"], "cap_seconds")
    rate = decimal(data["base_rate_per_second"], "base_rate_per_second")
    boosts = intervals(data["boosters"], True)
    settled = intervals(data["settled_intervals"])
    assumptions = data["assumptions"]
    if not isinstance(assumptions, list) or not assumptions:
        raise ValueError("assumptions must be a nonempty list")
    for item in assumptions:
        text(item, "assumption")
    result = {"schema_version": 1, "evidence_type": "deterministic_model",
              "timeline_id": timeline, "currency": currency, "rule_version": rule,
              "assumptions": assumptions, "status": "candidate", "earned_units": "0",
              "eligible_seconds": 0, "already_settled_seconds": 0,
              "discarded_by_cap_seconds": max(0, end - start - cap),
              "proposed_checkpoint_unix_s": max(start, end), "settlement": None,
              "segments": [],
              "limitations": ["This is a candidate, not a committed reward or verified clock.",
                              "Caller must commit wallet delta, interval marker and checkpoint atomically.",
                              "First capped seconds are retained; excess seconds are discarded permanently by this model.",
                              "Trusted interval records and one immutable rule snapshot are caller assertions.",
                              "No cloud conflict resolution, calendar reset, fraud protection or currency rounding is implemented."]}
    if end <= start:
        result["status"] = "clock_rollback" if end < start else "no_elapsed_time"
        return result
    eligible_end = min(end, start + cap)
    points = {start, eligible_end}
    for low, high, _ in boosts + settled:
        if low < eligible_end and high > start:
            points.add(max(low, start))
            points.add(min(high, eligible_end))
    ordered = sorted(points)
    earned = Decimal(0)
    # Each accepted decimal has at most 62 fractional places and is < 10**64.
    # Products have at most 124 fractional places; nonnegative segment seconds
    # sum to <= 10**12, so the total is < 10**140. Thus <= 264 decimal positions
    # suffice even when tiny fractional terms join huge terms. Revisit this
    # bound if input lengths, time bounds or interval semantics change.
    with localcontext() as context:
        context.prec = 320
        for low, high in zip(ordered, ordered[1:]):
            seconds = high - low
            if any(a <= low and b >= high for a, b, _ in settled):
                result["already_settled_seconds"] += seconds
                continue
            factor = next((factor for a, b, factor in boosts if a <= low and b >= high), Decimal(1))
            amount = rate * factor * seconds
            earned += amount
            result["eligible_seconds"] += seconds
            result["segments"].append({"start_unix_s": low, "end_unix_s": high,
                                        "seconds": seconds, "multiplier": plain(factor),
                                        "earned_units": plain(amount)})
    claim_bytes = json.dumps([timeline, currency, start, end], separators=(",", ":")).encode("utf-8")
    result["earned_units"] = plain(earned)
    result["settlement"] = {"claim_id": hashlib.sha256(claim_bytes).hexdigest(),
                            "start_unix_s": start, "end_unix_s": end,
                            "earned_units": plain(earned), "rule_version": rule}
    if result["eligible_seconds"] == 0:
        result["status"] = "no_unsettled_eligible_time"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="explicit model JSON")
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError) as exc:
        parser.exit(2, "error: %s\n" % exc)


if __name__ == "__main__":
    main()
