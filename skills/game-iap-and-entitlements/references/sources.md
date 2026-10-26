# Purchase sources

Official documentation checked **2026-10-26**. Re-check against the actual product type, SDK and supported OS before implementation. These links establish platform behavior; the ledger, account conflict and test designs are original engineering guidance.

| Source | Use |
|---|---|
| [Google Billing integration](https://developer.android.com/google/play/billing/integrate) | Billing client flow, purchase processing and completion |
| [Google purchase verification](https://developer.android.com/google/play/billing/security) | Backend verification, purchase-token uniqueness and abuse boundaries |
| [Google one-time lifecycle](https://developer.android.com/google/play/billing/lifecycle/one-time) | Pending/completed states and reconciliation |
| [Google subscription lifecycle](https://developer.android.com/google/play/billing/lifecycle/subscriptions) | Current subscription authority, grace/hold/cancellation/expiry |
| [Apple purchase result](https://developer.apple.com/documentation/storekit/product/purchaseresult) | Pending/cancelled/verified result and finishing after delivery |
| [Apple transaction updates](https://developer.apple.com/documentation/storekit/transaction/updates) | App-lifetime observation and transactions completed elsewhere |
| [Apple current entitlements](https://developer.apple.com/documentation/storekit/transaction/currententitlements) | Current access and exclusions; not consumable wallet restoration |
| [Godot Android plugin architecture](https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html) | Native adapter and export lifecycle discovery |
| [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) | Re-check purchase presentation and product rules for current storefronts |
