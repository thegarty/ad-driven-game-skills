# Godot purchase bridge recipe

Checked **2026-10-26**. Godot is the game layer; do not invent a universal Godot StoreKit or BillingClient API. Discover the maintained plugin, native SDK version and exported methods/signals in the project. For another engine, repeat discovery against that engine's current official documentation before translating the contract.

## Before writing glue code

Inspect engine version, Android Gradle dependencies/export plugin, iOS exported Xcode dependencies and plugin source. Record which native capabilities are actually exposed: product loading, purchase, pending state, verification result, transaction identity, product quantity, restore/query, completion, errors and lifecycle callbacks. A plugin that emits only `purchase_succeeded(product_id)` cannot support reliable transaction-level deduplication without extension.

Current Godot Android plugin architecture provides native lifecycle hooks and build integration. Use the documentation matching the installed Godot version; an editor addon being enabled does not prove its native library is in the release export. [Godot Android plugins](https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html).

## Adapter boundary

Define a game-owned interface with normalized **application events**, not assumed SDK methods:

| Application event | Required behavior |
|---|---|
| Product catalog available | Display store-provided localized price/title; unavailable products are unavailable, not free |
| Purchase pending/cancelled | Record UI state; grant nothing; allow ordinary gameplay |
| Transaction candidate received | Send protected verification inputs to the authority; do not emit purchase revenue yet |
| Verified fulfillment committed | Apply the authoritative entitlement/wallet revision once and acknowledge UI success |
| Completion retry needed | Retry platform finish/ack/consume without re-granting |
| Ownership refreshed | Update current access, including expiry/revocation; preserve unrelated progress |

Marshal native callbacks to the appropriate Godot thread and use one long-lived service rather than scene-owned listeners. Reopening the shop must not attach another fulfillment handler. Separate UI timeouts from transaction state: a dismissed spinner does not cancel a pending store purchase.

For Android, follow the selected [Google Billing integration](https://developer.android.com/google/play/billing/integrate): reconnect/query where needed, verify completed state and complete the relevant purchase type. For Apple, handle the direct purchase result as well as the long-lived [transaction updates](https://developer.apple.com/documentation/storekit/transaction/updates) listener. Refresh access independently using current verified entitlements. A Godot signal name can differ from every native API name.

## Packaged-device exercise

Use two sandbox accounts and a clean device/install. Record the release-like build hash, plugin/native SDK versions, store test environment, transaction correlation alias and expected state at each interruption. Never publish the original token or signed payload.

1. Complete a purchase and reopen the shop repeatedly: one fulfillment, one revenue owner.
2. Approve a pending transaction while the game is closed, then reopen: late delivery reconciles.
3. Interrupt after grant commit but before completion: redelivery returns the existing balance.
4. Reinstall and restore: permanent access returns; historical consumables do not all reappear.
5. Switch game account while the store account stays constant: the declared ownership conflict policy executes.
6. Simulate refund, expiry and renewal using supported store test tools: access updates correctly and distinct renewal benefits use distinct grant keys.
7. Disable network and fill storage: no fabricated successful grant or destructive reset.

Report each row as source-inspected, sandbox device-tested or still untested. Sandbox success is evidence for the exercised path, not proof of live billing, tax, settlement or account configuration.
