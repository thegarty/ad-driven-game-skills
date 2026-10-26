# A defensible experiment readout

The following workflow is original guidance. Primary methods sources were checked **2026-10-26**. Distinguish a proposed test, synthetic calculation, observational association and randomized experiment throughout the output.

## Define the effect before collecting it

Write the intervention, eligible population, assignment unit, primary metric, time horizon, practical effect worth acting on and guardrails. State whether randomization is independent per player, blocked/stratified, clustered or adaptive. Document assignment persistence, identity merges, concurrent experiments and whether returning players can cross arms. The analysis must match the design.

For an ad change, cumulative publisher ad revenue plus net purchase proceeds per **assigned player** through a declared age can be a primary metric. Retention, failure-to-grant, crashes and abandoned sessions can be guardrails. Exposed-user revenue or eCPM can diagnose mechanism; neither automatically estimates the effect of offering the feature to the assigned population.

## Assignment and exposure are different denominators

Build the readout by left-joining outcomes to a complete assignment roster. Keep eligible assigned players who never use the feature. Exposure is useful for verifying delivery and explaining dilution, but conditioning on a behavior affected by treatment can break comparability. An exposed-only comparison is generally descriptive unless a valid analysis for that estimand was designed.

Never turn an absent revenue event into zero without an explicit coverage rule. Zero is justified only when source completeness and identity reconciliation make it an observed zero. A disabled SDK, delayed paid event, denied analytics collection or failed account join can all create absence. Report missingness by arm and source, resolve data failures, and predefine any sensitivity analysis. The supplied helper conservatively withholds the comparison if any assigned outcome is incomplete.

## Integrity checks before effects

Check duplicate/conflicting assignments, sample ratio against the planned allocation, exposure rate, first exposure time, metric coverage, date maturity, variant/config revision and mutually exclusive eligibility. A sample ratio mismatch is a diagnostic symptom; inspect assignment, filtering and event loss rather than simply rebalance or discard inconvenient records. [Fabijan and colleagues, primary SRM research](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/).

An approximately balanced assignment count does not prove randomization. Verify the assignment implementation and delivery logs. For fixed blocks, geographic clusters or adaptive allocation, use a design-aware diagnostic instead of the helper's simple binomial-allocation screen.

## Uncertainty and stopping

Compute at the randomization unit. Many ad impressions from one player do not create many independent randomized observations. Inspect zero outcomes, high-value tails and player influence. Do not remove large purchases after seeing which arm they favor; any trimming/winsorization changes the estimand and must be declared and reported alongside the original metric.

The helper resamples complete players within each arm and returns a percentile interval for the difference in means. This illustrates uncertainty but can be unreliable with small samples or rare heavy tails. Hesterberg's methodological paper specifically discusses poor small-sample coverage of common percentile intervals; a narrow or degenerate interval is not a certificate of certainty. [Hesterberg, 2015, primary statistical paper](https://arxiv.org/abs/1411.5279).

For real decisions choose an analysis suited to the design and metric, review its assumptions, and plan sample size from project variability and the smallest useful effect. The helper does not perform power analysis, sequential correction, multiplicity adjustment, clustered inference or causal identification. More bootstrap draws only reduce Monte Carlo noise; they do not create more players.

Keep operational monitoring separate from a fixed-horizon effect readout. Stop for real harm according to a declared safety rule; do not repeatedly peek at ordinary intervals and stop the first time they exclude zero. If continuous effect decisions are needed, predeclare a valid sequential method. If many metrics/variants are inspected, distinguish confirmatory results from exploratory leads and account for multiplicity before claiming a winner.

## Worked synthetic readout

Run the [fixture and helper](experiment-helper.md). It contains ten assigned players per arm, nine exposed in each arm, complete D0–D7 outcomes, and one high-value player per arm. These numbers are synthetic examples, not sample-size recommendations or commercial results.

| Quantity | Control | Treatment |
|---|---|---|
| Assigned / exposed / complete | 10 / 9 / 10 | 10 / 9 / 10 |
| Net revenue per assigned player | USD 0.60 | USD 0.70 |
| Largest player outcome | USD 4.70 | USD 5.30 |

With seed 42 and 2,000 resamples, the calculated difference is USD 0.10 per player and the 95% percentile interval is approximately USD -1.26025 to +1.48025. The relative point estimate is about +16.7%, but it is dominated by sparse high-value outcomes and has substantial uncertainty. This is not evidence to increase ad pressure. Inspect delivery and source completeness, retain the planned horizon and collect an adequate randomized sample with retention/reward guardrails.

If one player's outcome becomes `null`, the helper reports that missing record and withholds means and the primary comparison. If one arm has many missing players, do not analyze just those who reported; establish whether data loss depends on the feature. If revenue rises while retention falls, evaluate total value at mature comparable horizons and the predeclared guardrails rather than silently replacing the success metric.

## Report format

Return assignment/exposure/coverage counts; metric definitions; effect and uncertainty; diagnostics; guardrail estimates and uncertainty; supported decision; remaining threats; and the next evidence needed. “No clear effect at this precision” is not “the variants are equivalent.” Equivalence or noninferiority needs its own margin and design.
