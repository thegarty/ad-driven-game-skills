# Cloud identity and conflicting progress

## Choose authority per field

| Field | Potential policy | Failure to avoid |
|---|---|---|
| Settings | Last explicit choice under a defined ordering | Stale device unexpectedly re-enables an option |
| Best score | Validated maximum, if attempts/rules remain comparable | Accepting untrusted or incompatible scores |
| Cosmetic collection | Union only for independently valid immutable grants | Treating invented client items as verified ownership |
| Currency / consumed inventory | Authoritative ledger, single-writer lease, or choose one complete branch | Adding balances or taking the maximum after both devices spent |
| Progress gates | Product-specific complete-state or validated milestone policy | Combining mutually exclusive states into an impossible campaign |
| Paid entitlement | Current verified store/account entitlement authority | Old save revokes or fabricates a purchase |
| Privacy permission | Current platform/privacy controller | Save restore resurrects withdrawn permission |

The table suggests decisions to make; it does not choose a provider or guarantee
that a client-only game can prevent tampering.

## Concrete conflicting-spend example

Two devices start from the same 100-unit snapshot. Device A buys a 60-unit item;
device B buys an 80-unit item while offline. Their remaining balances are 40 and
20. Summing balances, taking 40 and unioning purchases, or summing both grants
does not reconcile the original budget.

Choose and disclose one design: preserve one complete branch after a player
choice; enforce a single authorized writer/lease; or submit idempotent commands
to an authoritative service which validates ordering and rejects/reconciles
unfunded operations. If offline provisional purchases exist, specify what the
player sees and how rejected operations are resolved before introducing them.
Preserve both original candidates during conflict handling.

## Transport and linking

Use authenticated account identity and revision preconditions in the actual
provider's supported interface. On conflict, fetch the current candidate and
resolve; do not blindly retry a stale replacement. An acknowledgement should
identify which revision is stored, and UI should distinguish local saved,
upload pending, cloud confirmed and conflict states.

For guest-to-account linking, inspect both states before assignment. Clearly
present progress, relevant content/version and last-play information without
pretending a local clock is an authoritative ordering. Scope in-flight responses
to the originating identity. On logout, cancel/reject account-bound work without
discarding already-durable local progress.

Deletion needs a server-recognized deletion generation or equivalent protocol
if old devices can reconnect. Define retention, recreation and reconciliation
with legitimate store rights; do not equate deleting gameplay with refunding a
purchase. Avoid storing or printing unnecessary personal information in fixtures.

## Sources and implementation limits

Verified **2026-10-26**:

- [Google Play Games cloud save guidance](https://developer.android.com/games/pgs/savedgames): account linking and conflict-resolution scenarios.
- [Apple GKSavedGame reference](https://developer.apple.com/documentation/gamekit/gksavedgame): platform-specific saved-game API entry point. Its interactive page requires further inspection of the current API documentation before implementation.

Provider capabilities and account availability differ. These recipes do not
claim that cloud blobs automatically merge transactions or support cross-platform
accounts. Test the selected provider's real identity/conflict behavior separately.
