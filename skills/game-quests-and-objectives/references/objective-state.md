# Objective state, time and transactions

The included definition is an illustrative schema contract, not a standard engine
API or a production server. Adapt it to the actual game-owned event and save
system. Record schema versions and reject unsupported definitions predictably.

## Three progress semantics

| Type | Meaning | Example | Deduplication/ordering rule |
|---|---|---|---|
| Unique event count | Count each eligible semantic action once | Finish three distinct eligible runs | Stable event/run identity; duplicate transport receipt adds zero |
| Sum of eligible deltas | Add explicit earned changes from allowed sources | Earn 100 ordinary-play seeds during this instance | Stable transaction identity; filter origin; never sum both transaction and replay notification |
| Authoritative snapshot | Evaluate a current or high-water fact | Own three eligible defenders; or reach lifetime milestone | Versioned source snapshot and explicit current-vs-high-water semantics; ignore older revisions |

Define whether spending, refunds, ad rewards, gifts, compensation and prestige
count. An “earn” quest usually needs gross eligible earned deltas, while a “hold”
quest needs current balance; they are not interchangeable. Never derive an earned
delta from the change in a UI label or subtract two snapshots without accounting
for spending/reset/migration.

Current-state predicates can become false before completion. Specify exactly when
completion is evaluated. Once a quest has durably earned an entitlement, a later
spend should not silently revoke it. If a legitimate correction affects progress,
use an explicit reviewed migration/correction policy and preserve the audit trail.
Do not call a current snapshot monotonic merely to simplify the counter.

## Event contract

A semantic event needs event ID, type/schema revision, run/transaction identity,
subject scope, occurrence time with clock authority, received time, source revision
or sequence and typed payload with units. Validate it against the actual game
operation before counting. A client-supplied “wave won” message is not authoritative
for competitive rewards merely because it contains an ID.

Prefer accepted domain actions such as committed upgrade or settled run outcome
to button presses, rendered screens or SDK callbacks. Define event eligibility at
instance start, including whether already-completed facts can satisfy it. Store
that decision; loading the panel must not reinterpret the full lifetime ledger
under a changed filter.

## Instance and time identity

A definition ID names the quest template. A revision pins its meaning. An instance
ID names one assignment to a player; a period ID names a specific recurring/event
window. Display names, localised dates and weekday labels are not identities.
Keep the UTC boundaries plus the intended timezone/reset rule for calendar periods.
Travel must not create an extra reward period or erase an existing assignment.

Define entry cutoff, completion cutoff and claim deadline separately. State which
clock owns competitive/calendar rewards, what offline progress is allowed and how
late arrivals are handled. A trusted event occurring before completion cutoff but
received in a claim grace window may be accepted under a stated rule; receipt
after the grace deadline should follow the stated late policy. A device timestamp
alone cannot prove an event occurred before a server deadline.

For offline solo play, choose a bounded deterministic policy and document trust
limits. Preserve locally recorded eligible progress through reconciliation;
separate pending from accepted. Avoid silently giving different deadlines when a
player changes locale, changes the system clock or launches on another device.

## Durable processing and claims

```text
on_domain_event(event):
    validate event schema, authority and subject
    transaction on objective state:
        if event identity already processed: return stored result
        select eligible pinned instances and enforce occurrence/receipt policy
        update progress according to each objective's declared semantics
        when completion becomes true, write durable completion entitlement
        record event identity and state revision with progress
    publish UI feedback from committed state

claim(instance_id, reward_id):
    transaction on economy and entitlement:
        require earned, claimable entitlement owned by this subject
        operation_id = stable(instance_id, reward_id)
        if operation_id already granted: return original outcome
        validate reward destination/overflow and apply the immutable grant
        record grant and claimed state atomically
    project committed outcome to UI and optional platform services
```

If economy and objectives use different services/stores, a single local transaction
cannot span them by assertion. Use a durable outbox/retry workflow with idempotent
receivers and explicit pending state. Do not mark claimed before a durable grant,
or retry with a new identity after a timeout. Retain processed identities for the
full possible replay window, or use a proven ordered checkpoint design; deleting
them arbitrarily reintroduces duplicate progress.

A multi-objective quest must define all/any/sequence logic and when counters start.
For sequence objectives, decide whether actions before the preceding stage count.
Do not accidentally backfill them from unrestricted lifetime totals. Repeated
open/claim callbacks and interrupted celebration animations affect display only.

## Versioning, retirement and projections

Pin active instances and rewards to their accepted revision. Changing a target
from three to five after assignment must not silently move the goal. Preserve
earned access and entitlements when content is retired; provide a compatible
replacement or explicit migration with recorded reason. Handle old saves and
unsupported future schema without corrupting either.

Native achievements may represent a subset of durable facts. Store provider ID
mapping and sync status separately. Reconcile duplicate/late platform responses
without incrementing game-owned quest state again. A recurring quest should not
reuse a one-time native achievement as its resettable progress database. Verify
current platform capabilities separately; this reference makes no provider API
or native reset guarantee.
