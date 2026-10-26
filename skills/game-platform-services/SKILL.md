---
name: game-platform-services
description: Integrate or audit Apple Game Center and Google Play Games Services for native identity, leaderboards, achievements, challenges and eligible platform rewards. Use when the game needs reliable native progress features without confusing platform profiles with saves or inventing cross-platform APIs.
license: MIT
---

# Game platform services

Start with the player experience and verify the actual native capability. A leaderboard can create a useful near-term goal, but global rank alone is not proof of retention. Choose fair modes, visible personal progress and an ordinary play route when native services are unavailable.

## Establish the platform contract

1. Inspect engine/plugin/native SDK versions, supported OS versions, signing, app identifiers, console configuration and published components. Use the [current capability map](references/platform-capabilities.md), then discover exact APIs before writing glue code.
2. Separate Game Center/Play Games profile, store billing account, game account and local save identity. Define linking, guest progress and account-switch behavior; never merge wallets or overwrite saves just because a native profile changes.
3. Define score metric, units, direction, allowed range, game/content version, assistance/paid-boost policy, reset/season semantics and validation authority. Native time filters are not a substitute for the game's own season contract.
4. Define each achievement's intent, monotonic progress or repeatability, completion conditions, identity and any game reward. Native achievement confirmation and durable game-currency delivery are separate operations.

## Implement reliable native behavior

Follow the [Godot/native integration recipe](references/native-integration.md). Use a narrow adapter with explicit unavailable, authenticating, ready, queued, confirmed and failed states. Bind pending operations to the intended native profile and game account. Do not replay one account's offline achievements into another account after a switch.

Use the [score and achievement integrity recipe](references/score-and-achievement-integrity.md) for interruption recovery, ambiguous acknowledgements, seasonal boundaries and abuse controls. Native score submission does not independently validate gameplay. API success or local queue acceptance does not prove a public ranking is visible to every player.

## Challenges and quests

Apple's current challenges build on configured leaderboards and have their own availability/configuration requirements. Google's current Level Up quests and Play Games Rewards are distinct from the retired legacy Quests API; verify eligibility and current delivery integration. Neither is a universal cross-platform quest engine. Keep the game's daily/weekly quest logic and claims authoritative in the game's own system, with native integrations as explicitly supported surfaces.

## Deliver

Return the [platform services matrix](assets/platform-services-matrix.md), exact bindings/source dates, identity and scoring contracts, implementation changes and packaged-device evidence. Test service unavailable/declined, offline sync, duplicate callbacks, account switching, season rollover, invalid scores and UI return paths. Verify configuration publication separately from binary distribution. Record added SDK download/installed size, startup/memory cost and why the native feature merits that cost.

Label source-inspected, simulated, packaged-device tested and measured-live claims distinctly. This skill's references contain current official sources; no live account or production capability is assumed from documentation alone.
