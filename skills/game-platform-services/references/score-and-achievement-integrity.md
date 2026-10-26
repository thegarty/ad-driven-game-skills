# Scores, achievement progress and durable intent

This is an original integrity design with current native behavior linked where relevant. It does not claim that all provider APIs offer idempotency keys, historical season submission or exactly-once delivery.

## Score contract

Declare metric and unit (points, elapsed milliseconds or another explicit integer encoding), larger/smaller-is-better, allowed range, tie handling, completed-run condition, game/content/rules version, difficulty and assisted-play policy. Do not mix runs with ad revives or paid boosts into an unassisted category without explaining that rule. Decide whether rankings compare best run, cumulative progress or a season-specific result.

Record immutable run identity and authoritative completion before sending. Validate score arithmetic, feasible duration, required checkpoints, seed/content version and eligible boosts on the trusted side where possible. A client can be modified; signing a client-computed value or applying a broad score range is not authoritative gameplay validation. Native tamper protection can add a signal but is not proof of a fair result. Define review/removal/appeal handling for suspicious scores without exposing anti-abuse secrets.

Google leaderboards have configured ordering and native daily/weekly/all-time views; their reset boundary need not equal the game's local daily reset. Apple recurring leaderboards have configured occurrences. Inspect these definitions before presenting a countdown or issuing seasonal rewards. [Google leaderboard concepts](https://developer.android.com/games/pgs/leaderboards), [Apple recurring leaderboards](https://developer.apple.com/documentation/gamekit/creating-recurring-leaderboards).

For offline results, retain run completion time, board/season intent and version. If the provider cannot submit to the intended past occurrence, do not silently move yesterday's run into today's competition. Apply the declared late-submission policy and show an accurate outcome. Do not backdate results using only a mutable device clock. High-value seasonal prizes need an authoritative cutoff and finalization process separate from a cached ranking screen.

Apple's current recurring-leaderboard guide explicitly directs submission to the current occurrence and says not to submit to past occurrences. Loading a previous occurrence for display is not permission to backfill it. An offline run that missed its intended Apple occurrence therefore needs the game's declared exclusion/fallback rather than a fabricated historical submission.

## Delivery and ambiguity

Persist an outbox intent before transmission, with account/profile, logical operation identity, payload/rules version, attempts and known provider result. Understand the SDK's own offline queue before adding another retry layer. Distinguish durable local queue acceptance from remote confirmation.

For a pure best-score board, coalescing obsolete worse scores can reduce requests **only if** no challenge, attempt-count or other behavior depends on each submission. Apple's current challenge guide says to submit the recent completed-attempt score even when the board displays only a personal best. Deduplicating all non-best attempts could break the challenge experience. [Current Apple challenge reporting](https://developer.apple.com/documentation/gamekit/creating-engaging-challenges-from-leaderboards).

A connection loss after submission creates an ambiguous result. If replay is idempotent under the provider's semantics, retry with the same logical intent. If a submission counts an attempt or increments progress, inspect reconciliation support before replaying; a local UUID does not become a provider idempotency key by itself. Document the remaining guarantee when the provider cannot resolve ambiguity. Bound retry/backoff and use current [Google API usage guidance](https://developer.android.com/games/pgs/quota) rather than arbitrary universal rate limits.

For current Apple challenges, Game Center handles offline score recovery. Do
not unconditionally resubmit a completed-attempt score merely because the app
starts. Separate never-submitted game-owned intent from work already handed to
the native queue, and follow the current challenge guide's recovery semantics.

## Achievement intent and state

Map gameplay events to a stable logical achievement and version. Persist the game-side event/target before reporting; keep a local display state of pending versus confirmed if the API allows that distinction. One achievement toast is not a durable currency reward. If the game also grants a prize, use a separate immutable claim key and ledger tied to the intended account/cycle.

For monotonic progress prefer an absolute target derived from the authoritative total when supported. Google's achievement client distinguishes incremental operations from setting at least a given step count: replaying an increment can overcount, whereas a lower repeated minimum target does not reduce progress. This does not solve two-device aggregation; compute a reliable shared total or a deliberate reconciliation policy first. [AchievementsClient reference](https://developers.google.com/android/reference/com/google/android/gms/games/AchievementsClient).

For Apple, inspect current progress/completion and repeatability semantics rather than assuming every achievement is an endlessly repeatable quest. Version/cycle identities must prevent a completed achievement from repeatedly paying the game's reward on every native state refresh. [Apple achievements](https://developer.apple.com/documentation/gamekit/rewarding-players-with-achievements).

## Native reward delivery

For eligible current Play Games promotional rewards, follow the documented out-of-app purchase verification/fulfillment path. Resolve the intended in-game account before the durable grant, deduplicate by verified transaction identity, then complete through the relevant billing operation. Reconcile at startup/foreground and respect the current claim availability. Do not treat a quest-complete UI or native achievement callback as a substitute for a verified transaction. [Play Games Rewards](https://developer.android.com/games/rewards).

## Synthetic failure exercise

A player completes a run offline near a seasonal cutoff. The outbox binds it to the completed run, old season, score rules and native profile A. Before reconnecting, profile B signs in. Expected behavior: suspend A's intent, preserve the run/save, and report pending/unavailable status without posting to B or assigning it to the new season. When A returns, submit/reconcile only if the native service supports the intended occurrence and the game's declared late policy allows it. Test that reconnecting twice neither issues a second game reward nor falsely reports two confirmed submissions.
