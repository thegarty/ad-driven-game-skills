---
name: game-retention-and-liveops
description: Diagnose mobile game drop-off and design return goals, content cadence, events or re-engagement. Use for retention and replayability work; separate returning players from longer sessions and separate observations from hypotheses.
license: MIT
---
# Game retention and live operations

Find why players leave or return, then choose the smallest intervention that addresses that cause.

## Establish comparable evidence

Define the install/first-play cohort, retained action, time zone, day boundary, platform, version, market, acquisition source and consent/measurement coverage. Distinguish exact-day retention from rolling return and active play from time left in the background. Exclude immature cohorts from a retention window's denominator; missing measurement is not zero retention.

Inspect crashes, loading, save loss, confusing requirements, progression stalls and ad failures alongside content exhaustion. Segment by stage and exposure when data permits. Revenue rising while retention falls requires comparable cohorts and net value over a common horizon; it does not establish that more ads helped the business.

When data is unavailable, produce a hypothesis map and a minimal instrumentation/player-observation plan. Do not fabricate a retention curve or recommend a universal daily ad cap.

## Choose a return reason

Use [return systems and diagnosis](references/return-systems.md). Match the system to the game's appeal and the team's ability to sustain it:

- Mastery: a new strategy or challenge worth trying.
- Progression: a visible reachable unlock or build choice.
- Collection: meaningful combinations or expression, with clear duplicate handling.
- Content: levels, threats or modifiers that change decisions.
- Social/competitive: a fair reason to compare or cooperate, with moderation and operational costs accounted for.

A longer session is not always desirable: add save/resume or a satisfying stopping point when players cannot finish comfortably. A return timer should make sense in the game's economy and explain what changes while away.

## Design an operable intervention

Use [the retention experiment brief](assets/retention-experiment.md). Specify audience, eligibility, start/end rules, rewards, clock, late/offline behaviour, content cost and a rollback path. Preserve earned progress when an event ends and explain unclaimed rewards. Avoid a streak design that unexpectedly erases permanent progress when a day is missed.

Use [event operations and fair competition](references/event-operations.md) for versioned event states, late claims, durable reward identity and comparable scoring. Choose social features with an explicit identity, moderation and support plan; a leaderboard reference is not a multiplayer implementation.

For reminders, define the actual player benefit, relevant consent/preferences and a cancellation condition when the reason disappears. Design and measure the reminder first; creating a live notification campaign is a separate action requiring the user's authorisation. Check current platform requirements before implementation.

Use [the notification lifecycle](references/notification-lifecycle.md) for permission, quiet hours, expiry, cancellation, travel and stale-destination handling. Scheduling, delivery, opening and meaningful return are separate outcomes.

## Measure and iterate

Choose a primary outcome that matches the cause, plus guardrails for crashes, completion, frustration/support signals, ad exposure and revenue over an explicit horizon. Define variant assignment and sample maturity before interpreting results. A source-tested feature can be ready to measure while its commercial effect remains unknown.

Deliver a prioritised diagnosis, one bounded intervention, implementation/operation requirements and a measurement decision. Separate the release status, observed behaviour and inferred effect. Stop or revise an intervention that harms the agreed guardrails rather than rationalising the result from a single improving metric.
