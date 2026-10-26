# Scheduling decisions and lifecycle

This is **design pseudocode**, not an executed implementation or a guarantee from
an operating system. Adapt it to the game's storage, identity and native bridge.
Use [the ledger template](../assets/notification-ledger.md) to define real fields.

## Minimum state

Keep a stable reason ID and generation for the task/event, current validity and
expiry, category, copy version and destination. Keep user category preferences,
current known OS authorization, selected timezone/travel policy, active-state
freshness, holdout assignment and recent contact history. Registration/installation
identity is a delivery address; it is not automatically an authenticated account.

Use a durable message identity per user/reason/generation/policy decision. Separate
planned, reserved, scheduled/submitted, known-failed, unknown-result, cancelled,
expired and observed-open states. Provider acceptance is neither display nor open.
Keep attempted/accepted contacts distinct from cap reservations.

## Candidate decision

```text
evaluate(reason, player, now):
    if invalid_or_completed(reason) or now >= reason.expires_at:
        return SUPPRESS_STALE
    if not audience_allowed(reason, player): return SUPPRESS_AUDIENCE
    if not category_enabled(player, reason.category): return SUPPRESS_PREFERENCE
    if not required_authorization_known_allowed(player): return SUPPRESS_PERMISSION
    if state_too_stale_for_this_promise(reason, player): return SUPPRESS_UNCERTAIN
    if player_already_active_in_relevant_context(player): return SUPPRESS_ACTIVE
    if assigned_holdout(player, reason.policy): return SUPPRESS_HOLDOUT
    due = next_allowed_instant(max(now, reason.earliest), player.quiet_hours,
                               player.timezone, player.dst_and_travel_policy)
    if due >= reason.expires_at: return SUPPRESS_EXPIRED_AFTER_QUIET_HOURS
    return CANDIDATE(reason.identity, due, reason.expires_at, reason.priority)

reserve(candidate):
    transaction scoped to player contact policy:
        reread preferences, reason revision, contact history and reservations
        if identity already scheduled/submitted/unknown: return EXISTING
        apply global rolling caps, category caps and minimum spacing at due time
        choose among competing reasons by declared priority and usefulness
        if blocked: defer only while useful; otherwise suppress
        write reservation + durable dispatch job using stable message identity
```

Use an actual atomic store operation or equivalent serialization for concurrent
senders; checking a counter and later incrementing it is race-prone. A rolling
window must include the appropriate accepted contacts and future reservations,
not just today's calendar count. A category rename cannot reset global history.

## Dispatch and uncertain outcomes

At dispatch, re-read eligibility, preference, reason generation, expiry and the
policy reservation, then apply the decision again with current state. If stale,
cancel the job and any still-cancellable platform request. If eligible, submit
using the stable identity, explicit useful lifetime and current registration.
Record success, definite rejection or unknown outcome separately.

A network timeout after submission can mean the provider accepted the message.
Do not automatically create a fresh identity or release its budget to send another
message immediately. Reconcile where the provider/bridge allows it, otherwise use
a bounded conservative retry policy and state the duplicate risk. Database and
external delivery cannot be made exactly-once merely by writing “atomic send.”
Retain an accepted/unknown contact for fatigue accounting when display is unknown.

Local requests scheduled far ahead cannot necessarily rerun this decision at
presentation time. Reconcile while the app has execution time, cancel with stable
request IDs, and use wording/expiry choices that tolerate the remaining staleness.
For volatile server state, prefer a design with authoritative dispatch-time
checking, while still acknowledging network and OS delay.

## Reconcile changes

On task claim/cancel, event revision, preference change, return, sign-out, save
reset, registration rotation or timezone change, recompute desired requests and
cancel obsolete ones. Do not repeatedly regenerate a new message because the
same task was loaded from a save. Clear stale visible notifications/badges where
supported; a badge count should reflect actual outstanding information.

An account-aware service can coordinate task completion and message budgets across
devices. A disconnected device's already-scheduled local reminder may still appear.
If identity or offline constraints prevent global control, document device-scoped
limits and avoid running independent broad campaigns on top. Never claim an
account-level cap from unrelated device counters.

Resolve local quiet hours through timezone-aware calendar logic. Define ambiguous
repeated times and nonexistent times around DST, midnight-crossing windows and
travel behavior; test both directions. After an outage, recompute every reason and
retain at most the currently useful allowed messages, not the old backlog.

## Open safely

Parse only a versioned allowlisted payload shape. Resolve a stable content/reason
ID; do not execute arbitrary URLs, scripts, paths or reward parameters. Confirm
the current signed-in account may access the destination. After authentication,
re-resolve eligibility and content state; do not reuse an old authorization result.

Route an expired event to its available history/claim view or a current home
screen with an honest explanation. An unsupported payload/version should safely
fall back. Claim rewards through the game's ordinary authoritative, idempotent
entitlement path, never from the notification body or click alone.

## Acceptance fixtures

Use a fake clock and synthetic registrations for quiet-hour boundaries, expiry at
reschedule, two simultaneous senders, duplicate worker delivery, timeout after
acceptance, permission revocation, claimed-on-other-device, stale offline state,
DST/travel, sign-out and malicious/unknown destination. Then test the packaged
native implementation on devices. Label model walkthroughs, automated checks and
actual delivery observations separately.
