# Participant-level experiment helper

Python 3.9+, standard library only. Copying this skill alone preserves the script, fixture and instructions. Run from the skill directory:

```sh
python3 scripts/experiment_readout.py assets/experiment-example.json --seed 42 --resamples 2000 --confidence 0.95
```

It prints JSON and does not modify files. Invalid inputs produce an error on stderr and exit 2; a valid but incomplete dataset returns JSON with `status: withheld_incomplete_data` and exit 0. This is a diagnostic result, not a failed parse or permission to treat missing outcomes as zero.

## Exact input contract

Use [the synthetic fixture](../assets/experiment-example.json). Unknown or missing fields and duplicate JSON object keys are rejected. Participant IDs are opaque local join keys; never publish actual player exports in this library.

| Field | Meaning |
|---|---|
| `schema_version` | Integer `1` |
| `evidence_type` | `synthetic` or `observed`; supplied observations remain unverified by the helper |
| `experiment_id`, `population` | Nonempty experiment reference and precise eligible assigned population |
| `metric`, `unit`, `outcome_definition` | Nonempty metric name, units, and source/window/netting definition; use the same definition for both arms |
| `timezone` | Nonempty timezone used by the upstream calendar aggregation; the helper does not convert timestamps |
| `horizon_days` | Integer 1–3660; DH must be completely observed after assignment date D0 |
| `as_of_date` | Last fully observed calendar date, `YYYY-MM-DD`; not simply today's date |
| `design` | `randomized` or `observational`; an assertion, not validation of causal assignment |
| `assignment_unit` | `player`; other units/cluster designs need a different analysis |
| `assignment_roster_complete` | Boolean assertion that all assigned players in the declared population are included |
| `expected_treatment_fraction` | Planned fraction strictly between 0 and 1; not the observed fraction fitted after data arrives |
| `assumptions` | Nonempty array of explicit nonempty statements, including coverage, identity and design |
| `participants` | At most 10,000 rows, exactly one per assigned player; empty input returns unavailable comparisons |

Each participant row must contain exactly: `participant_id` (nonempty string), `arm` (`control` or `treatment`), `assigned_date` (`YYYY-MM-DD`), `exposed` (boolean), `observation_complete` (boolean), and `outcome` (finite number or `null`). Numeric booleans, infinity, NaN and absolute outcomes over 1e12 are rejected. Signed net outcomes are allowed. Same-arm duplicate IDs and cross-arm conflicting IDs are both errors; fix upstream identity/aggregation instead of dropping duplicates.

`observation_complete` means the entire metric window and all required sources for this player are reconciled. It is not “we saw one event.” The script requires `as_of_date - assigned_date >= horizon_days` before a complete assertion is accepted. For the fixture, outcomes include D0 through D7 inclusive, requiring the end of D7. D0 duration varies with assignment time; the definition is calendar-based, not seven exact 24-hour intervals. A D7 retention indicator could use only D7 if explicitly defined as such. Aggregate dates/windows upstream consistently.

## Output and safeguards

Counts distinguish assigned, exposed, mature, complete, missing outcome and incomplete observation. The latter categories can overlap and must not be added as disjoint buckets. All assigned players stay in the primary population regardless of exposure. The script withholds both-arm means, difference and interval unless the roster is asserted complete and every player in both arms has a mature complete numeric outcome. It never silently supplies zero or conducts a complete-case comparison.

With complete data, report means, standard deviation, range, nonzero outcomes and treatment minus control. At least two players per arm are required for a bootstrap interval; that computational minimum is not statistical adequacy. Each resample draws the original number of players with replacement within each arm. The interval uses linear interpolation between sorted difference quantiles. Seed defaults to 42, resamples to 2,000 and confidence to 0.95. Resamples must be 200–20,000; the script bounds total participant draws to 50 million. The bounds are resource controls, not recommendations for a study.

The assignment ratio screen uses Pearson's two-category chi-square statistic and its asymptotic one-degree-of-freedom tail probability only for a complete randomized roster with at least five expected players per arm. It assumes independent assignment at the declared fraction. It is an integrity screen, **not** a treatment-effect p-value; fixed allocation, blocks, adaptive allocation and cluster designs need appropriate alternatives. Investigate suspicious imbalance using a predeclared diagnostic rule; a large p-value does not verify randomization. See the [worked analysis and primary sources](experiment-analysis.md).

Percentile intervals can under-cover, especially in small or skewed samples. The script warns for small samples and degenerate intervals; it cannot observe a rare payer absent from the data. No automatic winner, significance, ship, payback or causal claim is emitted. Observation status and experimental validity remain responsibilities of the analyst. This helper does not replace randomization checks, missing-data analysis, guardrails, sequential methods, multiplicity correction or a properly powered experiment.
