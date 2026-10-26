# Exact-day cohort retention helper

Python 3.9+, standard library only. From this skill directory:

```bash
python3 scripts/cohort_retention.py \
  --installs assets/installs-example.csv \
  --activity assets/activity-example.csv \
  --as-of 2026-01-08 --days 1 7 \
  --population 'Synthetic example install roster' --timezone UTC
```

The [install fixture](../assets/installs-example.csv) and [activity fixture](../assets/activity-example.csv) are entirely synthetic. JSON output goes to stdout; invalid input produces stderr and exit code 2.

## Contract

- Installs CSV requires `user_id,install_date`, including every install in the chosen population even if it never returned. Use privacy-appropriate identifiers. Exports based only on active users will bias the denominator.
- Activity CSV requires `user_id,activity_date`; an activity must belong to a roster ID and cannot predate installation. Filter the two files to the same population first.
- Dates use strict `YYYY-MM-DD` in one declared calendar timezone. The tool does not convert dates; prepare them consistently upstream. Day zero is the installation calendar date, not a rolling 24-hour window.
- `--as-of` is the last fully observed calendar date, after data-processing lag, not automatically today's date.
- `--days` accepts integers 1–3,650. Each cohort is eligible for day n only when install date + n is on or before the cutoff.
- Exact duplicate installs/activities are deduplicated and counted. Conflicting install dates for the same ID are rejected so reinstall treatment cannot silently change.
- Future installs and activities are excluded and reported. Additional CSV columns are ignored. Empty files with valid headers are supported.

## Interpretation

Per-date and weighted aggregate results include eligible installs, retained installs and retention as a fraction. Immature cohorts and empty denominators return `null`, not zero. Mature cohorts with no activity return zero. Aggregates divide summed retained installs by summed eligible installs; they do not average cohort percentages.

The example produces D1 = 2/3 and D7 = 1/2. The later install is not in the D7 denominator, and the duplicate D7 activity does not count twice. Source population completeness, consent coverage and ingestion reliability remain caller assertions. No statistical confidence, causal uplift or lifetime projection is inferred.
