---
name: game-save-and-cloud-sync
description: Implement or repair mobile-game saves, schema migrations, backup recovery, guest-account linking and multi-device cloud conflicts. Use when progress can be lost, duplicated or overwritten; preserve separate consent and store-entitlement authorities.
license: MIT
---

# Game saves and cloud sync

Protect legitimate progress while making ownership and conflicts explicit.
Inspect the existing save format, write path, schema/content versions, cloud
provider, account identity and release compatibility before changing data.

## Specify what a save means

Use the [save and conflict contract](assets/save-contract.md). Identify the
authoritative fields and the smallest transaction containing mutually dependent
state. Currency, consumed items, applied reward claims and offline checkpoints
must not be restored or committed independently if that permits duplication.

Read [local durability and migration](references/local-durability.md) for write,
load and rollback behavior. Distinguish a file that parsed from a state that is
valid for this build. Stable content IDs need a migration/remapping policy; node
paths or array positions alone are fragile long-term identities.

Validate bounded input before allocation or mutation. Preserve an unreadable or
future-version save for recovery. Do not quietly reset a player because a parser
or migration failed. Return a useful recovery state while avoiding repeated
destructive attempts on the only source copy.

## Design cloud and account transitions

Read [identity and conflict handling](references/cloud-conflicts.md) before
adding cloud sync. A cloud blob upload does not establish an authoritative
economy or solve two-device offline spending.

- State which profile/account owns each save, revision and pending operation.
  Reject responses for an account the player has since left.
- Do not automatically overwrite either meaningful guest progress or an
  existing linked account. Preserve both candidates while resolving the choice.
- Classify mergeable fields. A high-score maximum or set union may be appropriate
  only when the product's rules make the operation safe; balances and consumed
  resources cannot be merged that way.
- Choose explicit single-writer, branch-selection or server-ledger reconciliation
  for mutable economies. Explain the tradeoff to offline and cross-device play.
- Keep retry IDs, revision preconditions and conflict results stable. Transport
  retry must not replay a grant or purchase.

Consent, platform permissions and verified store rights have separate authorities.
An old game backup must not restore withdrawn permissions or cancel a valid
purchase. A gameplay reset, logout, guest link and account deletion need distinct
policies; a deletion tombstone/version must prevent stale devices resurrecting
deleted cloud progress within the chosen system's retention policy.

## Implement and demonstrate recovery

Use synthetic saves and isolated accounts. Exercise each supported old schema,
interrupted writes/migrations, insufficient storage, corrupt candidate/backup,
unsupported future versions, duplicate responses, two offline spends, account
switch during sync, logout/reinstall and deletion followed by an old-device sync.

Deliver the schema/authority contract, actual migration and recovery paths,
conflict behavior and verification evidence. Preserve the original source until
the new state is durably validated. Document whether tests used mocks, native
filesystem behavior or a provider sandbox; none alone proves all three.
