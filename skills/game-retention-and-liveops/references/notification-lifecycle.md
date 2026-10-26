# Notification lifecycle

Platform documentation checked **2026-10-26**. Recheck the actual target OS and
native bridge before implementation. A scheduled request is not proof of delivery
or a player seeing it, and operating systems can delay or suppress presentation.

## Model a useful reason

A notification represents a currently valid reason to return, such as a completed
player-started task. Define a stable reason ID, reason generation/version, intended
recipient/device scope, earliest useful time, expiry, destination and cancellation
condition. Copy should describe a real state without inventing urgency, an earned
reward or a player relationship. The destination must still be valid when opened.

Choose local scheduling for a state the device can know; use server push when the
reason depends on shared authoritative state. State the tradeoff: a local request
may become stale until the app can cancel it, while a server needs permission,
token lifecycle, delivery handling and operational infrastructure. Do not promise
cross-device deduplication without an account/device reconciliation design.

## Permission and preferences

[Android's notification permission documentation](https://developer.android.com/develop/ui/views/notifications/notification-permission)
describes `POST_NOTIFICATIONS` for Android 13 and later. Use a relevant context,
check current permission state, and let the game remain useful after refusal.
An in-game preference cannot override an OS denial. Verify the actual plugin's
permission and settings behavior on a device rather than inventing Godot APIs.

Record separate preferences where the project distinguishes task reminders,
events and other message purposes. Request only the permissions needed for the
chosen behavior. Do not repeatedly prompt after a refusal or schedule messages
under a preference the player has turned off. Avoid exact-alarm privileges just
to deliver an ordinary game reminder.

## Quiet hours and expiry

Represent quiet hours in the player's selected/local timezone with a clear travel
policy. A window from 22:00 to 08:00 crosses midnight; implement it as that window,
not a simple same-day numeric comparison. Re-evaluate pending reasons when the
timezone, daylight-saving offset, preferences or relevant game state changes.

Synthetic rule: a harvest becomes ready at 23:10 and expires at 07:00; quiet hours
end at 08:00. Suppress the reminder because postponing it would describe an expired
benefit. If the harvest remains useful past 08:00, one postponed reminder may be
appropriate. Do not release every suppressed request at quiet-hours end. Apply a
project-defined overall budget across categories, with explicit deduplication and
priority; no universal sending frequency is justified.

## Reconcile, cancel and open

Persist desired requests by stable ID, compare with scheduled requests where the
platform supports inspection, and reconcile idempotently. Returning to the game,
claiming the resource, cancelling a task, changing an event, signing out, resetting
the save or disabling a preference can invalidate a reason. Cancel both pending
requests and outdated visible messages where the platform supports it.

[Apple's local-notification guide](https://developer.apple.com/documentation/usernotifications/scheduling-a-notification-locally-from-your-app)
uses notification request identifiers and supports cancelling pending requests.
Use the installed bridge's documented equivalent, and retain the identity needed
to cancel the earlier request. Do not confuse rescheduling a task with a new
permission grant.

On open, validate the payload and current state, then route to an available game
screen. An expired event should show a useful current destination or a clear
historical result. Never grant currency merely because a notification was opened.
Treat payload data as untrusted and keep sensitive/player-identifying detail out
of lock-screen copy and analytics unless necessary and authorised.

## Test and interpret

Exercise permission granted/refused/revoked, notification category disabled,
quiet hours crossing midnight, travel/DST, task claimed elsewhere, app reinstall,
duplicate scheduling, offline open, expiry and stale deep links. Record request
creation, platform acceptance, open and meaningful return separately; do not
infer delivery from acceptance or retention impact from opens alone.

Drafting the lifecycle is implementation work. Starting a live messaging campaign
or contacting players still requires the user's authorization for that action.
