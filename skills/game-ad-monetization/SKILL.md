---
name: game-ad-monetization
description: Design or audit in-game advertising formats, placements, reward values, exposure limits and purchase interactions for mobile games. Use for monetization decisions; buying acquisition ads is a separate task.
license: MIT
---

# Game ad monetization

Produce a placement design that supports a playable free route and can be evaluated against retention and cohort value. Establish whether the task is a new design, a placement audit or a measured experiment before recommending changes.

## Establish the decision

Inspect the actual game loop, current placements, progression stages and purchase promises. Find the intended audience, platforms, markets, average run structure, available analytics and current ad-provider constraints. Ask only for missing information that would change the design. Label assumptions when data is unavailable.

Map three different quantities: opportunities created by gameplay, opportunities the player chooses or is eligible to see, and ads actually delivered. More requests do not establish more impressions, and more impressions do not establish higher lifetime revenue.

## Design the placements

1. Use the [format and reward guide](references/formats-and-rewards.md) for choosing formats and evaluating reward value. Ordinary rewarded ads require an explicit offer and affirmative choice; treat rewarded interstitials as a separate format with their own rules.
2. Describe the natural gameplay transition for every interruptive placement. A time threshold may make a player eligible; it must not itself interrupt active play. Check current provider/store rules before adopting a format.
3. Specify a clear offer, stable placement ID, reward definition, eligibility, first-session treatment, exposure cap, cooldown, unavailable-ad behaviour and exit route in the [placement matrix](assets/ad-placement-matrix.md).
4. Evaluate reward value at early, middle and late progression. Compare ordinary earning time, the next useful purchase, competing offers and maximum daily issuance. Check both players who decline all ads and those accepting every legal offer.
5. Define interactions with purchases using the [entitlement guide](references/purchases-and-entitlements.md). The product copy and executable entitlement rules must agree.
6. Specify one primary experiment question and player-experience guardrails. Examples include cohort cumulative net revenue with retention, crash rate and abandoned sessions as guardrails. Set analysis windows and practical decision thresholds from the project's data and constraints, not generic benchmarks.

## Diagnose before adding pressure

Check whether available offers are hidden, unrecoverable, poorly explained, technically failing or worthless at the player's stage. Include offer exposure, opt-in, load, show, earned reward and durable grant in the measurement plan. For interstitials include eligible transitions and successful presentations.

Compare experiment arms at the same cohort age and across relevant geography, platform, acquisition source and progression stage. Avoid changing reward values and exposure frequency simultaneously unless the test is explicitly designed to separate their effects. Sparse results should produce a learning plan, not a winning variant.

## Deliver

Return the completed placement matrix, free-route and maximum-exposure economy checks, purchase semantics, instrumentation gaps and a bounded experiment recommendation. Distinguish implemented behaviour, proposed changes and outcomes still needing measurement.

Read [sources](references/sources.md) when verifying policy-sensitive decisions. Read the [Overgrowth lesson](references/overgrowth-lesson.md) when prioritising opportunity recovery or evaluating late-game reward relevance. Other skills are optional; this workflow must remain usable by itself.
