# Optional content without a fragile first launch

Deliver remote assets only when the benefit exceeds the operational cost. A few tightly compressed base assets can be simpler and more reliable than a downloader, cache manager and unavailable-content UI. Measure download, installed/cache and runtime-memory budgets separately.

## Manifest and transaction

For each immutable pack define its logical identifier, version, supported client/content schema, expected files, individual and aggregate byte bounds, digests, content types and dependencies. Treat all remote paths as untrusted: resolve only allowlisted logical paths inside the pack, reject traversal/absolute paths and duplicates, limit file count and expansion size, and do not execute content as code. Hashes check bytes against a manifest; authenticity requires an authenticated manifest/transport and an appropriate trust design. A hash beside a tampered file is not authentication.

1. Confirm the pack is optional or provide an existing playable alternative. Present the expected transfer and storage requirement when it affects the player's decision.
2. Check available space for old pack, staged download, temporary expansion and rollback reserve. Account for OS/runtime reporting uncertainty; handle a write failure even after the check passes.
3. Download to an isolated staging location using the selected platform's supported mechanism. Preserve a bounded resumable record if supported. Revalidate partial files; resuming a transfer is not proof of integrity.
4. Verify length, digest, schema, dependencies and any authenticity requirements before unpacking/activating. Bound decompression, validate paths and reject unknown asset types. Never let a missing texture become a partially active level.
5. Activate a complete set at a safe scene boundary by switching its manifest reference. Hold files referenced by active scenes until unloaded. Keep a compatible previous set while rollback is required.
6. Clean up failed staging and unused cache entries according to policy. Never evict the active pack, a pending transaction's necessary asset or a player-created save. Record storage savings and newly created startup/network cost.

The exact transport, signing, filesystem and activation guarantees must be selected and verified for the engine/platform. This is a protocol checklist, not an implementation of platform asset delivery.

## Failure acceptance table

| Injected failure | Required observable outcome |
|---|---|
| Offline on first launch | Bundled core loop remains playable, or a clearly justified required-download screen can retry without losing progress |
| Network interruption halfway | Existing pack stays active; incomplete data is never loaded |
| Valid download, incorrect hash | Candidate rejected and recoverable; no silent fallback to unverified bytes |
| Disk fills during expansion | Previous content/save preserved; bounded cleanup and understandable retry |
| Config references missing pack | Candidate remains staged or rejected; level offer stays unavailable truthfully |
| App dies during activation | Restart chooses one complete compatible manifest; no mixed pack |
| Rollback after new save fields written | Compatible recovery/forward repair chosen explicitly; old client is not assumed to understand new state |

Store delivery limits and allowed content mechanisms change. Before shipping a specific Android/iOS delivery mechanism, inspect its current official documentation and record the platform, date, quotas and measured candidate artifacts. Do not substitute this general recipe for current store policy or treat remote downloads as exemption from installed-size budgets.
