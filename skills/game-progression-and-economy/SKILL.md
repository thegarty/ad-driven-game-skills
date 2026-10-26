---
name: game-progression-and-economy
description: Design or audit mobile game difficulty, progression gates, upgrades, currencies, timers and reward value. Use for balance models, economy simulations and progression stalls; distinguish synthetic results from player retention.
license: MIT
---
# Game progression and economy

Connect challenge, earned resources and new choices. Model what players can do at each stage before changing a price, reward or gate.

## Establish the real economy

Inspect the implemented formulas, configuration, save schema and content caps. Enumerate currencies, sources, sinks, one-time grants, repeatable grants, entitlements and unlock requirements. Preserve distinct ledgers: earned lifetime currency, current balance, paid currency and achievement credit are not interchangeable.

Use [the progression model](assets/progression-model.md) to record each rule and its source. Distinguish active-play time, wall time, calendar resets and offline accrual. Specify how pause, backgrounding, clock changes and saved entitlements behave. Use current player saves only when authorised; default to isolated fixtures.

## Diagnose the bottleneck

Compare a first-time, an uninformed, a plausible engaged and an efficient strategy. Include no-ad and optional-ad scenarios with explicit assumptions about availability, selection and completion. An optimal strategy reaching a gate does not prove a novice can discover it.

For a stall, determine whether the cause is unclear requirements, a hidden counter, inaccessible controls, a dominant upgrade, a broken grant or an intended challenge. Consider clearer feedback and a relevant strategy hint when the player has a useful available choice. Do not silently compensate with currency or slow the normal route to create ad demand.

Use [economy reasoning and Overgrowth lessons](references/economy-reasoning.md) when interpreting strategy, clock or reward-value differences.

Use [worked balance patterns](references/worked-balance-patterns.md) for cost curves, complementary upgrades, prestige ledgers and stage-sensitive rewards. Recalculate their synthetic assumptions against the game's actual rules; they are not suggested production defaults.

For a gradually opening game, use [feature unlocks and satisfying payoffs](references/feature-unlocks-and-payoffs.md) and [the unlock schedule](assets/unlock-schedule.md). Sequence complexity from readiness, useful context and earned competence; keep basic access and settings available, preserve earned unlocks, and treat first-session timing as a hypothesis to test.

## Evaluate a change

Express value in context: time of ordinary earning, progress toward a useful purchase and the choice it unlocks. Compare early, middle and late stages separately. A flat reward can be valuable early and irrelevant later; a percentage reward can dominate after long runs. Calculate both the ordinary path and the proposed optional bonus.

Check source/sink balance, upgrade dominance, dead-end states, legal caps, repeat claims and whether a temporary benefit remains useful after a session ends. Define rounding and transaction ownership. Preserve earned entitlements and stable content IDs during migrations; changing a display threshold must not silently redefine an existing achievement.

For a bounded arithmetic scenario, run [the economy helper](references/economy-helper.md), which documents [the script](scripts/economy_scenario.py) and [synthetic example](assets/economy-example.json). It is not a gameplay simulator. For combat, solvability or strategy claims, use the real rules with deterministic seeds and clocks, and retain invalid fixtures separately from accepted results.

## Deliver and validate

Provide the rule inventory, tested profiles, bottleneck diagnosis, proposed changes, predicted tradeoffs and the next real-player measurement. Label evidence as source-inspected, source-tested, simulated or measured live. Report inputs, stopping rules and uncertainty with every simulation result.

Test fresh/late saves, zero earnings, affordability boundaries, capped upgrades, repeat reward claims, background/expiry and migration behaviour. A simulation must not issue real ads or assume every opportunity converts. Treat improved modelled progression as a hypothesis about player experience, not a retention or revenue forecast.
