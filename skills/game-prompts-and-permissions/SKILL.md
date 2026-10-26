---
name: game-prompts-and-permissions
description: Decide when and how a game should ask for ads, purchases, ratings, feedback, sign-in or system permissions. Use to design contextual requests, respectful decline and recurrence rules, and one coordinated interruption budget.
license: MIT
---

# Game prompts and permissions

Ask when the player understands the benefit and can make a clear choice without losing their current task. Inspect all request surfaces together: a carefully timed purchase panel can still be the fifth interruption after consent, notifications, sign-in and a review request.

## Design each ask

Use the [prompt decision guide](references/prompt-design.md) to specify the player need, relevant moment, eligibility, exact benefit/cost, action, decline path, recurrence rule and stale-context expiry. A milestone can make an ask eligible; it does not mean an interruption must occur. Preserve some earned successes as uninterrupted celebrations.

Choose the least intrusive surface that works: an available in-context button, a small explanatory panel or a modal only when the decision needs it. Do not use fake urgency, guilt, hidden dismissals or a purchase/permission requirement unrelated to the feature. A smart ask optimizes informed useful participation and retained experience, not acceptance at any cost.

## Coordinate across systems

Create one [ask ledger](assets/ask-ledger.md) and a shared coordinator. Re-check current screen, foreground state, native modal activity, consent/entitlement, decline history and relevance immediately before presentation. Prioritize the player's requested action and necessary recovery/disclosure; defer optional requests under a declared global burden budget. Expire deferred opportunities rather than presenting a backlog on the next launch.

Separate app invitation, system request attempted, actual authorization result and completed feature action. Each has a different event meaning. Permission status must come from the current OS/provider authority, not a cached local “asked” flag. Never interpret closing a disclosure or dismissing a system prompt as consent.

## Apply platform-specific rules

Read [native permissions and review rules](references/native-rules.md) before writing UI. Tracking, ad consent, notifications, store reviews and account authentication are separate decisions. Native prompts can be suppressed or have version/region-specific re-request rules. Respect denied/restricted states, preserve the usable fallback and re-query when returning from settings.

Do not incentivize tracking authorization or reviews, gate reviews by sentiment, or convert a privacy decision into a sales bargain. Child-directed or mixed audiences need audience-specific requirements before eligibility/copy is finalized. Discover exact engine/plugin/native SDK APIs; do not invent a common Godot request-permission interface.

## Validate and deliver

Return the decision table, copy, ledger/coordinator behavior and [journey test plan](assets/prompt-journey-plan.md). Exercise first session, return, repeated decline, settings changes, offline/unavailable service, simultaneous eligibility, backgrounding and accessibility. Use the [worked journeys](references/prompt-design.md) as design examples, not proven conversion recipes.

For experiments, assign before eligibility, report the full eligible/assigned population and count requests, actual responses, completed benefits, abandonment and return behavior. An improved accept rate does not prove a better game or valid consent. Separate guidelines, synthetic examples, observed behavior and experimental results.
