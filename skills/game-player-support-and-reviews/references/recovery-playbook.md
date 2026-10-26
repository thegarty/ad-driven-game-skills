# Recovery without duplicate value or destructive resets

This is original operational guidance. Store facts were checked **2026-10-26** in the sources linked below. Engine save and ad behavior must be inspected in the actual project.

## Minimal case evidence

Collect a case alias, platform/build, approximate local time/timezone, action, expected benefit and reproducible steps. Attach only relevant redacted screenshots/logs with consent and retention controls. Avoid publishing transaction tokens, account identifiers, raw telemetry or saves. Authenticate through the product's established account system when a recovery changes account value.

| Report | Trace | Safe next step | Do not infer |
|---|---|---|---|
| Watched ad, missing reward | Offer/opportunity identity → show → earned callback → durable grant → UI refresh | Replay committed result or retry an eligible pending grant through its original key | Ad close or provider revenue proves that player's reward was earned |
| Ad unavailable | Eligibility → load state → SDK error → retry/fallback | Preserve player action and explain availability; permit ordinary progression | No fill is the player's fault or another purchase is required |
| Lost progress | Local/cloud save revisions, migration, last valid backup, account | Preserve copies, compare schema/revision and restore under a declared conflict rule | Largest timestamp is safest, or reinstall is harmless |
| Paid, no access | Store state, verified ownership, grant ledger, game account | Reconcile/restore eligible entitlement, with pending state explained | Screenshot alone is verified ownership or every past consumable should be replayed |
| Reward credited twice | Repeated callback/claim identity and ledger | Stop duplicate path and apply declared correction policy | Deleting the whole save is an acceptable correction |

## Three recovery types

**Replay:** a committed grant exists but UI/cache is stale. Return that same ledger result. Do not insert another grant.

**Reconciliation:** verification establishes a legitimate unfulfilled benefit. Commit it through the original immutable transaction/grant identity; concurrent devices and support retries must converge. Repairing a pending entitlement is not a new purchase or a second revenue event.

**Goodwill:** evidence cannot establish the original grant, but a documented support policy permits compensation. Record an independent case-derived key, amount, reason and authority, and enforce a uniqueness constraint. Label it compensation rather than falsifying an earned-ad event. Offer a safe explanation when the product has no authenticated recovery channel.

Local-only games may not have enough trustworthy identity or server history to reconstruct a wallet. State that limitation. Do not add an unrestricted client-facing “grant coins” endpoint to solve support. Maintain an authenticated support path with least privilege, bounded grants, audit history and replay protection.

## Purchases and saves

Store restoration and save recovery are separate processes. Google purchase verification should establish valid ownership before granting access; use current store state and supported verification, not a pasted order number alone. [Google purchase security](https://developer.android.com/google/play/billing/security).

Apple current entitlements cover eligible current access but exclude consumables and refunded/revoked products. They cannot reconstruct all historical consumable spending. [Apple current entitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements).

Before a save recovery, record which copy will be replaced, preserve the prior copy and validate schema and grant-ledger consistency. Never merge two wallets by summing balances. If reverting to an earlier save would forget already-used grant IDs, retain authoritative grant history or the same purchase/ad may mint value again.

## Response and learning loop

A useful response states the acknowledged symptom, what is verified, the next safe action and the remaining limit. Example draft: “Your reward was recorded, but the balance display did not refresh. We restored the recorded balance once. Please reopen the results screen. We are still investigating why that build missed the refresh.” Use that wording only if each action actually occurred.

For each weekly theme, retain report count, reporting population limits, affected build, reproduced cause, player impact, owner and change outcome. A support fix is source-tested or device-tested until a declared live window shows whether reports or failures changed. Review sentiment can generate hypotheses, not substitute for telemetry or controlled comparisons.
