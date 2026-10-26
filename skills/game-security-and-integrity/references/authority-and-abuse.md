# Authority, replay and abuse recovery

## Start with what needs protection

| Resource | Reasonable authority choice | Claim that must not be assumed |
|---|---|---|
| Offline solo progression | Local coherent save, explicit modifiability limit | Encryption makes a player-controlled device a trusted server |
| Cloud copy of local progress | Authenticated account ownership plus save/conflict validation | Cloud storage automatically validates the economy |
| Shared currency or tradable value | Server-owned transaction ledger | Owner-only document writes prevent self-minting |
| Competitive score | Trusted simulation/validation appropriate to the competition, with limits stated | A signed-in client or plausible range proves a run happened |
| Purchased rights | Verified store/account entitlement lifecycle | A Boolean in an old backup establishes current rights |
| Rewarded benefit | Chosen local or server authority with one durable claim | Client earn plus server notification means two grants |

Avoid increasing architecture, latency and support costs for a threat that does not affect other players or the business. Conversely, do not introduce trading or competitive rewards while retaining an undocumented client-trusted economy. A new feature can change the required authority boundary.

## Inspect one protected transaction end to end

Original conceptual contract, not a provider API:

```text
receive intent and stable operation identity
authenticate caller using verified session/token context
derive account; check access to the target object
validate schema, allowed fields, bounds, state revision and eligibility
verify external proof where the operation requires it
transaction:
    find existing result by account-scoped operation identity
    if present, return it without applying again
    enforce unique external transaction/claim where relevant
    calculate effect from trusted rules and current state
    apply effect and persist operation result together
return authoritative result and revision
```

Bind a reused operation ID to the original normalized request. Reject the same ID with a different amount, target or action; otherwise a retry can silently change meaning. Use unique database constraints or equivalent serialization to handle concurrent arrivals. An in-memory set is insufficient across restarts or multiple server instances. Audit legitimate reversals and adjustments as new linked operations instead of deleting evidence of the original grant.

For purchases and provider-verified rewards, validate the application/product/unit and account binding as well as the signature/status. Preserve one external transaction identity across all delivery paths. A provider-signed payload containing client-supplied custom data does not make that custom data a trusted reward table. Use maintained verification libraries and official key/rotation guidance; do not invent cryptography.

## Firebase boundary checklist

Choose the actual product first: Firestore, Realtime Database and Storage have distinct rules and capabilities. Inventory every path and operation, including list/query, create, update, delete and uploads. Start with no unintended access, then grant only the required paths and fields. Check ownership on existing data and prevent changing protected owner/role fields. Apply size/type restrictions and keep authoritative balances, purchases and privileged roles writable only through the intended trusted service.

Test unauthenticated, owner, other-account and privileged-service cases. Include a legitimate read/update as well as denied cross-account access, self-assigned admin role, direct currency change and overly broad query. Use the selected product's local emulator/rules test tooling in an isolated project; a UI that hides a button is not an access-control test.

Cloud Firestore server libraries bypass its Security Rules and use server credentials/IAM. Therefore review backend authorization and least-privilege credentials separately; passing client rules tests does not prove the server endpoints enforce ownership. Verify the actual deployed rules/version as well as the repository copy. The [source list](sources.md) identifies the relevant official starting points.

## Attestation without unfair enforcement

An app/device authenticity verdict is a signal about the request environment, not a user account, an economic proof or a complete behavior history. Bind request verification to the intended action using the selected platform's current supported mechanism. Do not cache a convenient old positive verdict indefinitely or treat a debug/test provider as production enforcement.

Define outcomes per protected operation: allow ordinary solo play, hold a high-value claim pending, request a supported recovery action, or deny a verified unauthorized request. Missing network, unsupported OS, quota exhaustion, provider outage and a genuinely invalid signature are distinct categories. Preserve already-confirmed rights and give support enough scrubbed evidence to resolve legitimate failures.

Before enforcement, inspect representative device/distribution coverage and observed error categories. Stage the change, monitor invalid/unavailable proportions and legitimate-action success, and provide an operational disable/repair path that does not grant arbitrary authority. False positives are a product defect to investigate, not proof of abuse. A temporary outage policy must specify which server-sensitive actions remain pending and how they later reconcile.

## Content, secrets and diagnostics

Set maximum serialized and expanded sizes, collection depths/counts and allowed identifiers. Reject paths escaping the destination and unknown executable content. Verify signed/authenticated manifests where the design requires authenticity; a file hash alone is not its source's identity. Avoid secrets in clients or downloadable configuration. Separate public client configuration from credentials that authorize privileged operations.

Log bounded operation IDs, version, phase, category and outcome sufficient for reconciliation. Exclude full tokens, receipts, signing keys, callback URLs and unnecessary account/device data. Keep a clear retention/access policy for diagnostics. Rate limits and quotas should reduce abusive cost without turning transient mobile retries into permanent account damage.

These controls need concrete implementation and tests in the game's stack. The recipe is defensive design guidance, not a certification, complete security assessment or assertion that all abuse is prevented.
