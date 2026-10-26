---
name: game-analytics-and-experiments
description: Design mobile game telemetry, diagnose player and ad funnels, calculate retention cohorts, and evaluate experiments when a decision depends on reliable behavioural evidence.
license: MIT
---

# Game analytics and experiments

Turn a game question into a measurable decision. Inspect the existing event code, SDK ownership, privacy controls and exports before proposing more instrumentation. A dashboard value is not evidence until its population, time window and collection path are understood.

## Establish the measurement contract

1. State the decision and current uncertainty: first-session abandonment, a progression stall, missed reward offers, or whether an ad change improves cohort value.
2. Identify the population: all installs, consented analytics installs, active players or exposed experiment users. Keep these separate. Record platform, build, install cohort, market, source, reporting timezone and last complete data date.
3. Define each numerator and denominator. D7 exact-day retention is eligible installs active on calendar day seven divided by installs with a complete seventh day; it is different from rolling retention. Session duration does not establish return behaviour.
4. Assign one owner to every event. Check which lifecycle, purchase and ad revenue events the actual SDK already emits before adding custom events. Keep SDK revenue events separate from game reward grants.
5. Trace representative events from gameplay through the native bridge to the export, including denied consent, backgrounding, retries and duplicate callbacks. Missing or delayed data is unknown until diagnosed.

Start with the [event dictionary](assets/event-dictionary.md). For AdMob/Firebase integration and experiment setup, read [measurement recipes](references/measurement-recipes.md). Use [the cohort helper](references/cohort-helper.md) when an install roster and activity export are available; it reports maturity and denominators explicitly.

## Diagnose a funnel

Map first launch → meaningful action → first success/failure → next goal → return. For optional ads, distinguish eligible opportunity → visible offer → selection → request/load → presentation → earned callback → durable grant. A rewarded completion count cannot reveal how many eligible offers were never seen.

Segment by progression stage and placement before changing reward amounts. Compare the same cohorts and app versions; a new market mix, privacy rollout or tracking repair can change the measured rate without changing player behaviour. Retain raw counts and reporting coverage beside percentages.

## Run a useful experiment

Use the [experiment plan](assets/experiment-plan.md). Choose a primary outcome, assignment unit, inclusion rule, minimum meaningful effect, observation window and guardrails before exposure. Use stable assignment and log actual exposure; avoid mixing variants across reinstalls/accounts without documenting that limitation.

Check assignment balance, missing events, contamination and cohort maturity before interpreting effects. Analyse revenue at the randomisation unit, not as independent impressions. Report uncertainty using a method suited to the metric and design; do not manufacture significance from aggregate totals. Repeated peeking, many variants and changing the stopping rule need an explicit analysis strategy.

When traffic is small, return a diagnosis or an inconclusive experiment with the next evidence needed. Product observations and simulated economies can prioritise a hypothesis; they cannot substitute for a causal retention result.

Use the [worked experiment readout](references/experiment-analysis.md) for assignment versus exposure, sample-ratio checks, missingness, skew and stopping rules. With a complete participant-level roster, the [experiment helper](references/experiment-helper.md) calculates reproducible uncertainty while preserving nonexposed players and withholding comparisons with incomplete outcomes. It does not decide whether to ship.

## Deliver

Produce the measurement contract, the smallest instrumentation changes needed, a reproducible calculation or query, and a decision with limitations. If changing code, verify event ownership and one real sample of each changed path in an appropriate test environment. Publishing a remote configuration experiment is a separate operational action governed by the user's scope.
