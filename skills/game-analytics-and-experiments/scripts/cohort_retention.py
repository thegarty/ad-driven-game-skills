#!/usr/bin/env python3
"""Calculate exact calendar-day retention from a complete install roster and activity CSV."""

import argparse
import csv
import datetime as dt
import json
from pathlib import Path


def parse_date(value, name):
    if not isinstance(value, str):
        raise ValueError("%s must be YYYY-MM-DD" % name)
    try:
        result = dt.date.fromisoformat(value)
    except ValueError:
        raise ValueError("%s must be YYYY-MM-DD" % name)
    if result.isoformat() != value:
        raise ValueError("%s must be YYYY-MM-DD" % name)
    return result


def rows(path, required):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("%s requires CSV columns %s" % (path, sorted(required)))
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("%s has duplicate column headers" % path)
        return list(reader)


def calculate(installs, activity, as_of, days, population, timezone):
    cutoff = parse_date(as_of, "as_of")
    if not isinstance(population, str) or not population.strip():
        raise ValueError("population must describe the exported install population")
    if not isinstance(timezone, str) or not timezone.strip():
        raise ValueError("timezone must describe the calendar used in both CSVs")
    if not days or any(isinstance(n, bool) or not isinstance(n, int) or n < 1 or n > 3650 for n in days):
        raise ValueError("days must contain integers between 1 and 3650")
    days = sorted(set(days))
    roster = {}
    duplicate_installs = 0
    for row in installs:
        uid = row.get("user_id")
        if not isinstance(uid, str) or not uid.strip():
            raise ValueError("install user_id must be nonempty")
        installed = parse_date(row.get("install_date"), "install_date")
        if uid in roster:
            if roster[uid] != installed:
                raise ValueError("conflicting install dates for a user_id; resolve reinstall identity first")
            duplicate_installs += 1
        roster[uid] = installed
    active = set()
    future_activity = 0
    duplicate_activity = 0
    for row in activity:
        uid = row.get("user_id")
        if not isinstance(uid, str) or uid not in roster:
            raise ValueError("activity user_id is absent from the install roster; align populations")
        date = parse_date(row.get("activity_date"), "activity_date")
        if date < roster[uid]:
            raise ValueError("activity cannot precede installation")
        if date > cutoff:
            future_activity += 1
            continue
        item = (uid, date)
        if item in active:
            duplicate_activity += 1
        active.add(item)
    cohorts = {}
    future_installs = 0
    for uid, installed in roster.items():
        if installed > cutoff:
            future_installs += 1
        else:
            cohorts.setdefault(installed, []).append(uid)
    output = []
    totals = {day: {"day": day, "eligible_installs": 0, "retained_installs": 0} for day in days}
    for installed, users in sorted(cohorts.items()):
        results = []
        age = (cutoff - installed).days
        for day in days:
            mature = age >= day
            eligible = len(users) if mature else 0
            retained = sum((uid, installed + dt.timedelta(days=day)) in active for uid in users) if mature else 0
            results.append({"day": day, "eligible_installs": eligible,
                            "retained_installs": retained,
                            "retention": retained / eligible if eligible else None,
                            "status": "complete" if mature else "immature"})
            totals[day]["eligible_installs"] += eligible
            totals[day]["retained_installs"] += retained
        output.append({"install_date": installed.isoformat(), "installs": len(users), "days": results})
    aggregate = []
    for day in days:
        item = totals[day]
        eligible = item["eligible_installs"]
        item["retention"] = item["retained_installs"] / eligible if eligible else None
        item["status"] = "complete" if eligible else "no_eligible_installs"
        aggregate.append(item)
    return {"evidence_type": "calculated_from_supplied_records", "population": population,
            "calendar_timezone": timezone, "last_complete_date": cutoff.isoformat(),
            "definition": "exact calendar-day retention; install date is day zero",
            "install_count_through_cutoff": sum(len(users) for users in cohorts.values()),
            "cohorts": output, "aggregate": aggregate,
            "diagnostics": {"duplicate_install_rows": duplicate_installs,
                            "duplicate_activity_rows": duplicate_activity,
                            "future_install_rows_excluded": future_installs,
                            "future_activity_rows_excluded": future_activity},
            "limitations": ["Population and date completeness are caller assertions, not verified by this script.",
                            "Preaggregated dates are not converted between timezones.",
                            "No confidence interval, causal effect or unobserved retention tail is estimated."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installs", type=Path, required=True)
    parser.add_argument("--activity", type=Path, required=True)
    parser.add_argument("--as-of", required=True, help="last fully observed date, YYYY-MM-DD")
    parser.add_argument("--days", type=int, nargs="+", default=[1, 7])
    parser.add_argument("--population", required=True, help="explicit exported population label")
    parser.add_argument("--timezone", required=True, help="calendar basis already used in both date columns")
    args = parser.parse_args()
    try:
        result = calculate(rows(args.installs, {"user_id", "install_date"}),
                           rows(args.activity, {"user_id", "activity_date"}),
                           args.as_of, args.days, args.population, args.timezone)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(2, "error: %s\n" % exc)


if __name__ == "__main__":
    main()
