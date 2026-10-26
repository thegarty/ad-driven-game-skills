# Release evidence and recovery

## Candidate identity

Freeze or record the candidate's source/configuration and dependency lock state before expensive device tests. If changes occur afterwards, identify which results remain applicable and rerun the affected checks. Verify an exported artifact through build identifiers and an appropriate manifest/hash receipt, without publishing signing material or service credentials.

Record the installed build in the actual device test. A launcher shortcut can point at an old packaged snapshot; rebuilding in a source folder does not update that snapshot automatically.

## Save and economy compatibility

Use isolated fixtures representing real supported save versions. Include interrupted atomic writes, a corrupt current save with a valid backup, partially completed research, pending rewards and restored paid entitlements. Test wallet and reward-deduplication state together.

For changed balance, preserve the declared policy for in-progress timers, purchased rights and already-promised rewards. Decide whether a migration recomputes values or retains historical snapshots. Avoid evaluating a “new player” cohort using a fixture carrying later-game bonuses.

## Native service confidence

Keep a ladder of evidence:

1. Mocked callback/state tests.
2. Actual engine/plugin bridge probes.
3. Exported binary on representative physical devices, using test ads/sandbox billing.
4. Uploaded build identity and store availability.
5. Provider readiness and observed production delivery.
6. Comparable live player cohorts and business outcomes.

Passing one level does not automatically satisfy a later level. Record unsupported tests plainly and avoid inflating assertion counts by repeatedly counting the same scenario.

## Rollout and rollback

Choose guardrails that can be measured with current traffic: crash-free sessions, failed saves, failed grants, unexpected ad exposure and progression failures. Distinguish absence of telemetry from absence of errors. Compare compatible versions/cohorts and allow for reporting delays.

A store rollout halt stops further distribution; it does not remove the build from already-updated devices. A binary downgrade may be unavailable or incompatible with migrated saves. Plan forward-fix and remote configuration options only where they exist. A configuration rollback must also preserve already-earned rewards and paid rights.

When an ad placement is disabled remotely, verify default offline behaviour and cached-config expiry. Do not depend on a network call to repair a broken startup path. Record owner, trigger, action and recovery verification in the release checklist.

For a small first launch, the correct outcome may be “technical delivery observed; retention and revenue not yet established.” Do not delay fixing clear correctness failures while waiting for a statistical experiment.
