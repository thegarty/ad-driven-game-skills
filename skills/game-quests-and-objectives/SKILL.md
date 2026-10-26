---
name: game-quests-and-objectives
description: Design and implement mobile-game quests, missions, objectives and challenge chains with meaningful actions, gradual feature discovery, durable progress and fair expiry. Use for onboarding, main, side, recurring or event objectives and their reward state, not native platform-service setup.
license: MIT
---

# Game quests and objectives

Give a player a clear, useful goal and an honest account of progress. Connect
objectives to learning, mastery, experimentation or expression; a checklist is not
inherently engagement and a completion count is not evidence of enjoyment.

## Choose a purpose and available path

Inspect current mechanics, unlocks, resources, audience, save/clock rules and
player evidence. Define what each quest helps the player understand or choose.
Use [quest design and the worked chain](references/quest-design.md) to distinguish
onboarding, main, side, daily/weekly and event purposes. Cadence must fit the
content and player context; do not prescribe a universal task count or schedule.

Check feasibility before assignment. Required content, input/access alternatives,
resource capacity and ordinary no-ad paths must be available. A quest should not
require an unavailable ad, a purchase, a social connection or a particular access
mode unless that optional purpose is explicit and a viable ordinary route remains.
Keep settings, privacy, recovery and exit outside quest gates.

## Define exact objective semantics

Use [objective state and transactions](references/objective-state.md) and the
[definition example](assets/quest-definition.json). Specify stable definition and
revision, instance/period identity, eligibility, objective type, filters, target,
counting population, retroactivity and completion/claim rules. Separate counting
unique events, summing eligible deltas and observing an authoritative snapshot.
A displayed counter is not a sufficient event contract.

Version definitions and pin assigned instances where a change affects progress or
reward. Describe reset timezone/authority, start/end, entry cutoff, completion
cutoff, grace/claim window, offline acceptance and late-event policy. Preserve
already-earned progress and entitlements through corrections and migrations.

## Make progress and rewards durable

Validate and deduplicate semantic game events before updating progress. Commit
completion entitlement with progress atomically; grant a claim using stable
instance/reward identity through the game's normal durable economy transaction.
Retry, relaunch, duplicate callbacks or opening the quest panel must not add a
second grant. UI celebration follows committed state.

Treat native achievements or platform progress as an optional projection of the
appropriate game-owned facts. Keep a reconciliation queue and provider identity
mapping when needed; signing out of a platform service must not erase local quest
progress. The separately installable game-platform-services skill can guide native
integration, but is not required to use this skill.

## Deliver and validate

Provide the quest purpose/chain, definitions, objective-event dictionary,
state/clock contract, reward ledger and [test matrix](assets/quest-test-matrix.md).
Implement the requested slice with deterministic fixtures before adding a large
quest catalog. Validate repeated/reordered events, interrupted claims, expiry,
offline return, old saves, content retirement and unavailable optional services.

Measure eligibility → understanding → useful action → completion → claim and the
next meaningful choice. Separate assisted, abandoned, rerolled and expired quests.
Report synthetic examples, source checks, executed tests and live outcomes
accurately; more completed chores do not establish stronger retention.
