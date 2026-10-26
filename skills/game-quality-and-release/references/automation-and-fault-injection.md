# Repeatable automation and fault injection

Select checks from the changed behavior and its failure impact. A small pure rules change may need a few deterministic checks; a native purchase/save change needs broader recovery evidence. Record the expected invariant before writing the test so the test can challenge the implementation rather than repeat its internal calculations.

## Test boundary and fixtures

| Layer | Useful proof | Does not establish |
|---|---|---|
| Pure rules/state model | Known economy outcomes, legal transitions, idempotency, clock policies | Actual engine serialization or native callback behavior |
| Engine integration | Scene ownership, actual save migration, signals/input, asset references | Native SDK operation on a phone |
| Native bridge probe | Method availability, payload types, callback dispatch, platform lifecycle | Successful production ad delivery or paid entitlements |
| Physical-device candidate | Actual rendering/input/performance, test ads and sandbox purchases | Store approval, every device or live uplift |
| Store/provider/live checks | Uploaded identity, availability, provider readiness, observed cohort outcomes | Causality without a suitable design and enough evidence |

Use an isolated profile/save directory, synthetic identities, explicit clock, seeded randomness and controlled service adapters. Validate the isolation path before cleanup; delete only the temporary fixture directory created for that run. Never point reset/fault tests at a normal player profile, real purchase account or production service merely because its credentials are available.

Each automated scenario needs: fixture revision, setup, action sequence, injected failure location, expected persisted state, expected visible state, telemetry expectation and timeout. Tests must exit with a failing status when their assertions fail; a process that merely launches and quits has not exercised a scenario. Keep logs and artifacts small, scrubbed and attached to the tested candidate.

## Recovery matrix

| Fault or sequence | Invariant and observable result |
|---|---|
| Reward receipt persists; wallet commit fails | Pending receipt survives; no confirmed UI grant; later settlement grants once |
| Wallet+deduplication commit succeeds; crash before acknowledgement | Restart acknowledges existing grant; wallet never increases twice |
| Save candidate truncated; backup valid | Recover coherent backup; diagnose current-save failure without mixing its ledger |
| New schema unsupported by older binary | Protect original file; controlled incompatibility outcome, no silent reset overwrite |
| Background then process termination | Recover from last committed checkpoint; do not depend on final quit callback |
| Duplicate/out-of-order callbacks, scene freed, account switched | Claims retain immutable recipient; dead view not accessed; no cross-account grant |
| Network lost during ad/config/cloud response | Game remains usable; truthful availability; no endless spinner or retry storm |
| Two offline devices spend same balance | Chosen authority/conflict policy applied; inventory and currency not naively merged |
| Device wall clock moves backward/forward; booster expires mid-absence | Explicit capped interval policy; no negative time, repeated claim or unintended extra boost |
| Invalid remote config or missing content dependency | Compatible default/last-known-good remains active; current run unchanged |
| Download interrupted or storage fills at every write stage | Old content/save intact; incomplete pack never activates; retry is bounded |
| Consent changes while old native load finishes | Stale success cannot request/show against current eligibility; earned obligations preserved |
| Store purchase pending/cancelled/duplicated/restored | Product-specific entitlement state converges once; cancellation is not purchase success |

For a save transaction, inject failures before write, during candidate write, after validation, around replacement and after commit/before acknowledgement. A synthetic exception tests the error path; an actual forced process termination tests a different boundary. Filesystem power-loss guarantees require platform-specific investigation and cannot be inferred from a passing desktop exception test.

## Godot execution recipe

Pin the exact Godot/editor/export-template versions used by CI and record `--version` output. Build a small project-owned harness that injects save storage, time and service adapters, runs named cases and returns a nonzero status on failure. Then inspect that engine build's `--help` and supported script/headless options before scripting it. Native UI, visual fidelity and audio remain device checks even when logic can run headlessly.

The [official Godot command-line reference](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html), checked **2026-10-26**, documents build-dependent options and warns that unknown command-line arguments may be ignored. Verify test execution through explicit case counts/results and exit status, not absence of a startup error. This library supplies a test-design recipe, not a Godot test runner or a tested native project.

## Report a useful result

Report unique scenarios and meaningful assertions separately. Include candidate/source identity, fixture version, engine/plugin/SDK versions, platform/device, observed recovery and unresolved limits. A skipped case is unverified. A flaky retry that later passes still needs its initial failure explained before declaring confidence. When a behavior is unsupported by the current tooling, record the manual procedure and actual outcome instead of inventing an automated pass.
