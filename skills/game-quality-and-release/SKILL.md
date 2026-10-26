---
name: game-quality-and-release
description: Validate and release mobile games with evidence for gameplay, saves, device performance, native ads and store readiness. Use for release candidates, regression reviews, staged rollout and post-release checks.
license: MIT
---

# Game quality and release

Define the candidate before testing. Record the source revision, engine/export-template versions, native plugins and SDKs, configuration, app version/build numbers and resulting artifact identifiers. A passing source snapshot does not certify a different export or installed app.

## Build the evidence chain

Use the [release checklist](assets/release-checklist.md) as a working record, marking passed, failed, not applicable or unverified. Keep evidence proportional to the change; broaden testing when new failures or unresolved risks justify it.

1. **Logic and persistence:** test changed gameplay rules, reward grants, save migration and restart recovery using isolated saves. Compare the no-ad route with legal rewarded routes where economy changes warrant it.
2. **Real UI interaction:** validate small screens, safe areas, text scaling, touch/scroll distinction, readable reward copy, visible exits and screen-reader/navigation behaviour supported by the game. Screenshots alone cannot establish input correctness.
3. **Physical-device behaviour:** measure loading, frame time, memory, thermal/battery behaviour and network transitions on representative Android/iOS devices. State the tested devices and session length; choose budgets from the actual game and minimum supported hardware.
4. **Native services:** use test ads and sandbox purchases. Exercise initialization, unavailable ads, close/earn order, duplicate callbacks, background/resume, consent changes, purchase restoration and entitlement persistence as applicable.
5. **Packaging and stores:** inspect native dependencies/permissions/privacy metadata, versioning, signing, production versus test configuration and matching store disclosures. Measure the actual release package, per-device download, installed footprint and runtime memory separately against project budgets and current store limits. Verify the actual uploaded artifact and release track. If installed, `game-size-and-performance` provides focused compression and bloat analysis; this release check still applies without that optional skill.

Read [release and rollback guidance](references/release-and-rollback.md) when creating a rollout or investigating whether a fix reached users. Use [official sources](references/sources.md) for current export and store procedures.

Use the [automation and fault-injection matrix](references/automation-and-fault-injection.md) to turn changed behavior into repeatable tests with explicit failure points and expected recovery. Isolate test identities, saves and service environments before automating destructive lifecycle cases.

## Decide and roll out

Document release-blocking failures and explicit acceptance criteria before promotion. Preserve existing authorization for uploading/publishing; a skill invocation is not itself authorization to change production services or spend money. Do the authorized preparation and validation first.

Use a staged rollout where supported and appropriate. Define the observation window, minimum useful sample, guardrails and action owner from current traffic. Check crashes, ad/reward failures, save failures and early progression before interpreting revenue changes. Have a remote ad-placement kill switch or configuration rollback only if that mechanism is actually implemented and tested.

## Report precisely

Return changes, passed checks, failed/unverified checks, artifact identity, store/track status, rollout status and next observation. Distinguish source tests, simulator/desktop rendering, physical-device tests, provider readiness and production outcomes.

The Overgrowth review supplied a useful **source-tested** lesson: native-style desktop touch checks and frozen-source tests gave local confidence, but did not prove physical-phone playback or live retention/revenue uplift. Keep that boundary in every release report.
