# Optional purchases and advertising entitlements

Define the promise before selecting products or writing a store integration.

| Promise | Required explicit decision |
|---|---|
| Remove ads | Does it remove automatic interstitials, banners and app-open ads? Are optional rewarded offers retained? |
| Ad-free rewards | Are benefits claimable without watching, granted automatically, or replaced by a different system? What are the caps? |
| Supporter/cosmetic purchase | Which items or privileges are permanent, consumable or time-limited? |
| Subscription | Which rights remain after cancellation, expiry, billing retry or refund? |

Prefer precise wording such as “Removes automatic ads; optional reward videos remain” when that is the implemented promise. Do not label a product “all ads removed” while preserving advertising. Clarify this before purchase, not after payment.

## Implementation contract

Use store-verified transactions as the authority for paid rights, not a client-only Boolean in a gameplay save. Plan a platform-specific purchase adapter and a durable entitlement ledger. Decide whether server verification is required by the selected architecture and fraud exposure; follow current store guidance.

Process verified successful transactions idempotently, commit the entitlement durably, then finish/acknowledge using the store's lifecycle. Pending purchases do not grant rights early. Restore/reconcile current entitlements on the appropriate lifecycle events and expose the required recovery UI. Never grant an ad reward merely because restoration failed.

Non-consumable restoration, consumable fulfilment and subscription renewal are different flows. Avoid promising cross-platform restoration unless account linking and entitlement reconciliation actually support it. Test reinstall, device change, offline launch, refund/revocation, interrupted fulfilment and duplicate callbacks. A temporary network failure is not evidence of a refund; define the product's cached-entitlement policy.

After an ad-removal purchase, cancel newly disallowed pending presentations and invalidate cached presentation eligibility. Preserve an already-earned reward. A previously purchased right must survive a normal game-progress reset; account deletion and store rights require an explicitly designed policy.

For current purchase lifecycles and APIs, see [Google Play Billing integration](https://developer.android.com/google/play/billing/integrate) and [Apple StoreKit](https://developer.apple.com/documentation/storekit). Recheck these when choosing SDK versions. These recipes are not a complete billing implementation.
