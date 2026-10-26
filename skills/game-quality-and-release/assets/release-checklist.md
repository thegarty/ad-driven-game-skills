# Mobile game release checklist

Record each check as **passed / failed / not applicable / unverified**, with evidence. A blank checkbox is not a passed result.

## Candidate

- Source revision and configuration:
- Engine / export templates / plugin / native SDK versions:
- Android and iOS version/build identifiers:
- Build/artifact receipt and installed device build:
- Changes since the previous verified candidate:

## Gameplay and persistence

- [ ] Changed rules and progression paths verified with legal fixtures.
- [ ] Free route and maximum legal rewarded route remain viable as designed.
- [ ] Versioned save migration, atomic writes and backup recovery checked.
- [ ] Pending reward, duplicate callback and failed-save settlement checked.
- [ ] In-progress timers, clock semantics and promised benefits preserved.
- [ ] Purchase entitlements remain separate from ordinary progress reset.

## User interface and performance

- [ ] Small screens, safe areas, text scaling and orientation checked.
- [ ] Real touch scrolling does not activate reward/purchase controls accidentally.
- [ ] Decline/exit actions and unavailable-ad messaging are visible.
- [ ] Supported accessibility controls verified.
- [ ] Representative physical devices, session duration and performance budgets recorded.
- [ ] Release archive, per-device download, installed footprint and peak memory measured separately against project budgets.
- [ ] Current store size limits verified for the actual delivery format and target devices; size regression versus previous build recorded.
- [ ] Unused assets, duplicate imports, debug content and unnecessary native dependencies excluded; compression quality checked on device.
- [ ] Background/resume, audio, memory pressure and offline transitions checked.

## Native services and packaging

- [ ] Physical-device test ads exercised; no live ad clicks used for QA.
- [ ] Ad close/earn order, no-fill, retries, privacy changes and stale callbacks checked.
- [ ] Sandbox purchase, pending/failed payment, restore and revocation paths checked where applicable.
- [ ] Native initialization order, permissions, frameworks and privacy metadata inspected.
- [ ] Test/debug configuration excluded from the release candidate where required.
- [ ] Store disclosures, audience declarations and purchase promises match the binary.
- [ ] Uploaded artifact identity, track and review status independently verified.
- [ ] Provider readiness/store linkage verified separately from upload success.

## Rollout

- Stage / audience / observation window:
- Primary technical and player-experience guardrails:
- Minimum useful sample and measurement gaps:
- Stop / rollback / forward-fix triggers and owner:
- Existing remote configuration or kill switch and offline behaviour:
- Actual rollout/read-back evidence:
- Production delivery observed:
- Retention/revenue conclusions supported so far:
- Outstanding checks and next action:
