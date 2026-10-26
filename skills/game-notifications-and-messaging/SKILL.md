---
name: game-notifications-and-messaging
description: Design, implement or evaluate mobile-game reminders and lifecycle messaging, including useful triggers, concise copy, cadence, permissions, quiet hours, cancellation and incremental return. Use for notification scheduling and fatigue control, not for sending a live campaign without authorisation.
license: MIT
---

# Game notifications and messaging

Notify when there is a real, useful reason for this player to return. Determine
what to say, when it remains useful and how often the complete messaging system
may interrupt them. There is no universal optimal sending frequency.

## Establish the reason and current system

Inspect gameplay states, audience/markets, notification implementation, existing
campaigns, permission coverage and measurement before adding a schedule. Identify
all senders: local reminders, server push, event campaigns and other marketing
channels. A cap per campaign is insufficient when several can contact one player.

Define the player benefit, trigger, eligibility, earliest useful time, expiry,
completion/cancellation condition, destination and authoritative state source.
Prefer player-started tasks or explicit event preferences over a generic daily
“come back” message. A game should remain usable after refusal or opt-out. For
children or other audience-specific requirements, verify current applicable
platform/audience guidance before implementing targeting or outreach.

Use [trigger, copy and cadence design](references/cadence-and-copy.md) for a worked
synthetic schedule, concise message examples and experiment rules. Keep the
material promise clear; avoid fabricated scarcity, rewards or social activity.

## Design permission and delivery deliberately

Separate the OS authorization, in-game category preference and any applicable
consent. Ask in a relevant context, respect refusal/revocation and make controls
available later. Use [platform delivery](references/platform-delivery.md) to check
Apple, Android and Firebase behavior against the installed versions. No generic
Godot notification or Firebase plugin API is assumed by this skill.

Choose local scheduling when the device can determine the useful state and server
push when shared authoritative state is required. Identify what can become stale
while a device is offline. Do not promise immediate cross-device cancellation,
exact delivery or exactly-once display without evidence the architecture supports
it. Keep credentials and raw registration identifiers out of examples and logs.

## Make the scheduler stateful

Use [the decision and lifecycle recipe](references/scheduling-decision.md) and
[notification ledger](assets/notification-ledger.md). Track stable reason and
message identities, generation, permission/preferences, timezone, validity,
priority, quiet hours, category/global budgets and cooldowns. Reconcile on claim,
return, reset, sign-out, preference/timezone change and relevant server changes.

Apply quiet hours before dispatch, then recheck expiry. Suppress stale reasons
instead of sending a backlog after quiet hours or a service outage. Enforce a
single player-level contact policy across connected senders where identity and
consent permit it; document the weaker device-only guarantee when they do not.

Validate payload and current authorization on open. Route expired/unknown content
to a safe current screen. Opening a notification must never directly trust a
reward amount or grant an entitlement from the payload.

## Evaluate meaningful return

Predefine an eligible population, stable assignment, holdout, observation horizon,
primary useful action and fatigue guardrails. Compare return/completion in all
assigned eligible players, not only openers. Track system permission changes,
category opt-outs, complaints and retention where observable; missing delivery or
permission data is not a zero rate. Record message acceptance, delivery evidence,
open and meaningful return separately.

Deliver a trigger/copy matrix, reviewed cadence policy, lifecycle/ledger contract,
implementation or experiment plan and unresolved measurement limits. Validate
permission denial, midnight/DST/travel, expired claims, concurrent senders,
offline/cross-device state, retries and stale destinations. Live campaigns or
player contact require the user's authorization; library design and fixtures do
not send messages.
