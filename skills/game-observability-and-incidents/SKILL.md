---
name: game-observability-and-incidents
description: Instrument and investigate mobile game crashes, ANRs, startup failures, reward incidents and live regressions. Use to correlate failures with exact builds and configuration, mitigate impact and verify recovery.
license: MIT
---

# Game observability and incidents

Establish what players are experiencing, which deployed versions are affected and which evidence is missing. Preserve saves and earned value while diagnosing. A successful source test is not proof that the fixed code reached devices.

## Establish impact

1. Record incident onset, reporting timezone, last complete observation, affected platforms/builds, configuration revisions and deployment history. Compare rates with exposure denominators, not issue counts alone.
2. Distinguish fatal crash, nonfatal exception, Android ANR, memory termination, failed network operation and gameplay logic error. Route to the [native diagnostics recipe](references/native-diagnostics.md); one SDK does not necessarily observe every failure class.
3. Identify affected player actions: launching, loading a save, presenting/closing an ad, granting a reward, purchasing or downloading content. Link sanitized state transitions to an incident ID and build identity without exposing purchase tokens or personal content.
4. State severity from user harm, reach and recoverability. An issue that corrupts saves or duplicates currency can need faster containment than a larger count of recoverable UI errors. Define thresholds for this project and baseline; do not copy a generic crash-rate target.

## Contain and investigate

Use the [incident runbook](references/incident-response.md). Preserve representative evidence, assign an owner and bound the affected population before changing live settings. Use a previously tested kill switch, rollout pause or feature disable where the user's scope authorizes it. Explain what older installed clients actually support; stopping a rollout does not remove the bad build from existing devices.

Reproduce on the affected packaged version and a representative device. Inspect symbolicated native stacks alongside engine logs, SDK adapter versions, low-memory conditions, consent, background/resume and remote configuration. Change the smallest implicated path, then test the original reproduction and its recovery edges. Avoid speculative broad SDK upgrades during an incident without evidence and a rollback path.

## Verify recovery

Maintain four separate statements: source fix present, artifact built, correct artifact distributed, observed device/live behavior. Compare repaired build cohorts with mature windows and reporting coverage; absence of new reports in a tiny or unreported population is inconclusive. Record mitigation versus permanent repair separately.

## Deliver

Return the [incident record](assets/incident-record.md), impact bounds, evidence links, tested mitigation/repair, exact deployed artifact identity, monitored recovery criteria and remaining unknowns. Feed recurring failures into engineering and support priorities. Instrument only actionable data and apply retention/access controls; diagnostics are not an excuse to collect full saves, identifiers or chat logs.
