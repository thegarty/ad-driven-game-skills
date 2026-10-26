---
name: game-iap-and-entitlements
description: Design, implement or debug mobile game purchases, remove-ads products, durable entitlements, pending transactions, restoration and refunds. Use when purchase promises must survive retries, reinstalls or account changes.
license: MIT
---

# Game IAP and entitlements

Make the product promise and verified access rules agree. Inspect the store products, shipped billing bridge, server ownership, save model and customer-facing copy before writing purchase code. Treat a callback as input to reconciliation, not permission to mint another grant.

## Define the contract

1. List consumables, permanent unlocks and subscriptions separately. Record product IDs privately in the project; use synthetic IDs in reusable examples. State the delivered quantity, duration, recurrence, renewal benefits and refund handling.
2. Define exactly what “remove ads” means. If voluntary rewarded offers remain, say so before purchase. If rewards become claimable without ads, define their eligibility and limits independently. Never let restored ad removal erase earned currency or force a previous purchaser to watch an ad.
3. Identify the entitlement authority: verified store transaction, backend ledger, game account or bounded offline cache. Resolve store-account and game-account mismatch explicitly. A device ID, screenshot, local boolean or receipt-shaped string is not verified ownership.
4. Map pending, cancelled, verified, grant committed, acknowledgement pending, current entitlement, expired and revoked states using the [purchase lifecycle recipe](references/purchase-lifecycle.md). Purchase state and current access state are related but different records.

## Implement and prove recovery

Use the [Godot and native bridge recipe](references/godot-billing.md) after discovering the exact engine, plugin and native SDK versions. Reuse one durable fulfillment path for direct callbacks, foreground queries, restoration and server notifications. Preserve immutable transaction and grant identities across restarts. Finish, acknowledge or consume through the appropriate platform flow only after verified delivery is durably recorded.

Test interruption before delivery, after delivery but before acknowledgement, duplicate callbacks, pending approval after relaunch, restore after reinstall, account switch, expiry and refund. Include missing network, missing product metadata, disk-full save failure and an old build reconnecting to a newer backend. Use sandbox/test purchase accounts and the packaged native build; a mocked editor success does not establish store behavior.

## Deliver

Return the [entitlement contract and verification matrix](assets/entitlement-contract.md), implementation changes, test evidence and unresolved account/recovery limits. Show purchasing, restoring and verification as separate UI states with retry/support routes. Keep secrets and signed purchase material out of analytics and public bug reports. Record whether each claim is source-inspected, tested on a packaged build, simulated or measured live.

This skill includes its own [official source map](references/sources.md). Re-check policy, SDK support and store deadlines for the target platform before release. Monetization experiments need assignment-level outcomes; increased purchase conversion alone does not establish increased total player value.
