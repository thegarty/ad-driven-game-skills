# Evidence and decisions

Record the basis for a claim separately from its project validation. Primary
research supports findings in its original population and task; official
requirements support a platform contract; expert design guidance supplies a
starting heuristic. An original design proposal has no result yet. Preserve the
source URL, verification date, method, context, actual supported finding and
limits. Then record the project hypothesis, outcome, guardrails and test.

| Label | What it supports | What it cannot establish alone |
|---|---|---|
| Source-inspected | A behavior or risk visible in a particular revision | Runtime correctness or live impact |
| Source-tested | Observed results from stated tests/environment/revision | Native delivery if mocked, or human retention |
| Simulated | Outcomes under specified model inputs and stopping rules | Human choices, ad availability or causal uplift |
| Measured live | Observed production/provider outcomes for a stated population and time | Causality without a suitable comparison |

A hypothesis or proposed experiment has no result label yet. A live descriptive
observation is not automatically an experiment. Record uncertainty, missing
coverage and whether results use consented analytics users, all installs or ad
requests. Do not mix these denominators.

For revenue decisions, state the cohort acquisition date, maturity, currency,
gross/net basis, costs and evaluation horizon. Measured cumulative revenue to
day N is not lifetime value. Tail extrapolation needs explicit assumptions and
a sensitivity range. Distinguish equal-time comparisons from changing content,
acquisition mix, inventory or instrumentation.

For simulation, disclose upgrade legality, strategy, clock semantics, initial
save, ad success/choice assumptions and artificial retirement rules. Testing a
reward does not demonstrate players will choose it. A deterministic scenario
can reveal a dead end without predicting population retention.

For mutable SDK/policy requirements, inspect the installed version and current
official documentation when doing the work. If access is unavailable, state the
last verified date and avoid asserting current compliance. Use first-party
sources for implementation facts; treat design advice as hypotheses to test.

For game experience, separate active play, idle time, reading/navigation, ads
and loading. Longer sessions do not by themselves establish enjoyment. Shorter
instructions are useful if players understand and can transfer the action;
fast modal dismissal alone may mean they skipped it. Early earned success and
progressive unlocks are design hypotheses, not measured dopamine effects.
Generated mockups, synthetic numbers and suggested timing schedules must be
labelled. Do not turn a guideline or a study of different games into a claim of
retention uplift in this game. A/B tests require valid assignment, a defined
outcome window and analysis that handles missing data and repeated peeking.
