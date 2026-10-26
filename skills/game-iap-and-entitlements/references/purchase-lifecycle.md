# Purchase lifecycle and authority

This is an implementation design, not a store API. Official behavior was checked on **2026-10-26**; see [source map](sources.md). Verify the exact SDK and product type when implementing it.

## Separate three records

| Record | Owns | Must not mean |
|---|---|---|
| Verified transaction | Store, environment, transaction/token identity, product, quantity, lifecycle state, verification time | Every callback is a new purchase |
| Fulfillment ledger | One immutable transaction-derived grant key, recipient, benefit, committed result and retry state | Local animation means delivery succeeded |
| Entitlement projection | Current access derived from validated transactions and product rules | Purchase was once seen, so access is permanent |

An original subscription chain ID groups renewals; it is not the unique identity for every renewal benefit. Store environment is part of test/production separation. Persist raw tokens only in protected storage where verification needs them, not general logs. Notifications can be delayed, duplicated or out of order; validate them and reconcile against current store state instead of trusting arrival order.

## Durable fulfillment sequence

1. Capture the transaction candidate. Pending and cancelled purchases do not earn a paid grant. Display a pending state without encouraging repeated purchases while the first one is unresolved.
2. Verify authenticity, app/environment, product, current state and recipient binding. A valid transaction for another game account is an ownership conflict, not an automatic transfer.
3. Begin a durable transaction in the authoritative ledger. If the immutable grant key is already committed, return the prior result. Otherwise record the grant, currency/benefit mutation and audit entry atomically. If a local-only save cannot commit these together, document its weaker guarantee and use a recovery journal; never claim exactly-once server behavior from a local flag.
4. Retry platform completion from the committed record. Apple finishing and Google acknowledgement/consumption differ; use the selected SDK's documented lifecycle. A lost completion response must not duplicate delivery. Monitor outstanding verified purchases against the platform's current completion deadlines.
5. Reconcile on startup, foreground, restore and verified server updates. A missing network response is not proof of revocation. Cache valid access under an explicit offline/staleness policy; retry verification without creating another grant.

Google recommends backend verification and acknowledgement; purchase tokens identify purchase records. Its one-time purchase lifecycle includes state reconciliation from notifications and client queries. These are inputs to the same fulfillment service. [Google verification](https://developer.android.com/google/play/billing/security), [one-time lifecycle](https://developer.android.com/google/play/billing/lifecycle/one-time).

Apple purchase results distinguish pending, cancelled and successful verification results. A pending purchase can complete later through transaction updates; finish verified delivery after access has been provided. [Purchase results](https://developer.apple.com/documentation/storekit/product/purchaseresult), [transaction updates](https://developer.apple.com/documentation/storekit/transaction/updates).

## Restore and account conflict

Restoration rebuilds eligible access. It must not replay historical consumable grants. Apple current entitlements exclude consumables and refunded/revoked products; non-renewing subscriptions need your own validity rules because completed transactions can be present. Do not mistake that sequence for a complete wallet history. [Apple current entitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements).

Choose and document one identity model:

- **Store-only offline game:** reconcile store access on that store account; disclose consumable/save recovery limits. Local saves cannot reliably enforce cross-device consumable uniqueness.
- **Account-backed game:** bind verified ownership to the intended game account, handle guest upgrade, and authenticate recovery. Transfer or merge only through a defined, audited policy. Do not infer ownership from a shared device.
- **Cross-platform game:** specify which benefits follow the game account, which are store-specific, and how concurrent claims deduplicate. Re-check applicable store rules before promising cross-platform purchase access.

A restore failure is not a reason to reset progress. Keep entitlement reconciliation separate from wallet migration and ordinary game saves.

## Refunds and subscriptions

Recompute current benefits after verified refund/revocation. For already-spent consumables, use a declared support/fraud policy; do not silently manufacture negative balances or delete unrelated earned progress. Keep revocation audit history without retaining unnecessary personal data.

Cancellation, expiry, payment retry, grace period and account hold have different access consequences. In particular, cancelling renewal does not necessarily end a paid period immediately. Resolve the present subscription state from the relevant store authority, including upgrades and replacement chains, before granting or removing access. [Google subscription lifecycle](https://developer.android.com/google/play/billing/lifecycle/subscriptions).

## Synthetic interruption example

Transaction `demo-tx-17` grants 200 coins. The ledger commits `demo-tx-17/coins-v1` and a new balance, then the process dies before platform completion. A foreground query returns the transaction again. The fulfillment service finds its committed key, returns the existing result and retries completion; it grants zero additional coins. If the original commit never happened, the next verified delivery commits once. This is a design scenario, not a measured production guarantee.
