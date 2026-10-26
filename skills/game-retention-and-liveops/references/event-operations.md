# Event operations and fair competition

An event is a versioned temporary ruleset with durable player consequences.
Establish a normal gameplay reason for it and estimate its complete authoring,
localisation, QA, support and operational cost before choosing a cadence.

## Event contract

Record an immutable event instance ID, content/config revision, supported builds,
eligibility, authoritative clock, start/end, entry cutoff, late-claim deadline,
scoring rules, progression, reward definitions and rollback owner. Distinguish
eligibility to enter, ability to continue an existing run and ability to claim an
already-earned reward. These often end at different times.

Use explicit states: scheduled → active → ended/claimable → archived. Define
entry/run behavior at each boundary. Freeze a run's compatible rules on entry so
a background configuration refresh cannot change its promised reward halfway
through. Validate required content before accepting a ticket or debiting a cost.
Keep a compatible fallback for unsupported builds rather than advertising an
event that cannot load.

Synthetic event: three challenge tiers unlock cosmetic leaves. Entries close at
18:00 UTC; already-started runs may finish within a declared grace period; earned
claims remain available until a displayed later deadline. A player returning
during that claim window sees the actual earned tier and can claim once. A
player returning after archival sees history and the stated expired-claim policy,
not a misleading active countdown. These dates are project rules, not platform
requirements.

## Durable progress and claims

Persist progress and reward entitlement with stable event/player/reward identity.
The claim operation must be idempotent across double taps, relaunch, retries,
network timeouts and duplicate completion callbacks. UI animation is not the
grant authority. If the claim is pending, show that state and reconcile; do not
retry by generating a fresh reward identity.

Define offline scoring, clock trust and conflict resolution before allowing
offline competitive progress. An offline-friendly solo event may accept local
progress with stated limitations; a shared prize board needs an authoritative
validation strategy. Never label device-clock ordering as cheat-proof. A failed
sync should not erase locally earned progress without an explicit reconciliation
policy and recoverable evidence.

On config/content failure, stop unsafe new entries, preserve completed outcomes
and publish the in-game status appropriate to the project. A compensation policy
needs eligibility, one grant identity and a cost estimate; do not improvise a
repeatable grant on every error. Rehearse ending, reopening, extension and rollback
with fixtures before operating the event.

## Social and competitive options

Start with the smallest system supporting the goal: personal best, opt-in friend
comparison, asynchronous challenge, shared target or seasonal leaderboard. Each
adds identity, moderation, privacy, abuse and support costs. This reference does
not implement multiplayer networking, authoritative combat or matchmaking.

For comparisons, decide whether runs with ad revives, paid boosts, accessibility
assistance or different content versions are comparable. Publish the rules and
separate incompatible scoring categories where needed. Do not remove basic
accessibility support to protect a score; define scoring around the supported
experience. Avoid placing new players in a leaderboard against unreachable
lifetime accumulation without explaining the category.

Tie rules, season reset, score submission retries, suspicious-score review,
display-name abuse and blocked users need owners. If ranks award scarce prizes,
freeze eligibility and audit score integrity before finalising awards. A local
prototype board with synthetic scores must be labelled as such.

## Release and evaluate

Dry-run with before-start, active, boundary, late, offline, duplicate-claim,
unsupported-build and rollback fixtures. Inspect both entitlement and displayed
state. Measure eligible exposure, entry, meaningful completion, return, claim
success and cost; raw event participation can simply displace normal gameplay.
Use comparable cohorts and the declared horizon before attributing retention or
revenue movement to the event. Carry forward lessons only at their evidence level.
