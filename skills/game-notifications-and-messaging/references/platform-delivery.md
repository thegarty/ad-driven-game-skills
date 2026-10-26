# Platform delivery and documentation discovery

Official sources checked **2026-10-26**. Inspect the project's installed engine,
plugin, OS target and Firebase SDK/API versions before implementing. The platform
facts below are bounded summaries; the scheduler, copy and experiment recipes in
this skill are original design guidance, not platform-prescribed frequency rules.

## Apple

[Authorization guidance](https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications)
covers contextual authorization and checking current notification settings. Honor
the actual allowed presentation types; a category preference does not grant OS
permission. Do not repeatedly request the same system prompt after refusal or
treat provisional authorization as permission for an intrusive alert. Verify the
chosen flow and system-settings return on a device.

[Local scheduling](https://developer.apple.com/documentation/usernotifications/scheduling-a-notification-locally-from-your-app)
uses request identifiers and time/calendar triggers, with cancellation by request
identity. Persist the identifier needed to cancel an obsolete task reminder.
Keep app state and notification state reconciled. The operating system's delivery
and focus/summary behavior means a scheduled date is not proof of exact display.

## Android

[Notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
documents `POST_NOTIFICATIONS` for Android 13/API 33 and later, with behavior
influenced by target SDK and user choice. Check current system and relevant
channel state; a stored permission flag can become stale. Request at a useful
moment, such as enabling a chosen task reminder, and preserve a usable refusal
path. Use the current platform scheduling documentation for the selected bridge;
ordinary game reminders do not justify inventing exact-time guarantees.

## Firebase delivery

[Message types](https://firebase.google.com/docs/cloud-messaging/customize-messages/set-message-type)
distinguishes SDK-displayed notification payloads from application-handled data
payloads. Foreground/background and API-version behavior affect whether client
logic can suppress presentation. Check the installed integration, including
current Android migration guidance, instead of assuming a pre-display callback
always runs. Do not rely on silent background execution for critical reward or
save correctness.

[Message lifespan](https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-lifespan)
explains deferred delivery, platform-specific expiry and time-to-live behavior.
Set lifespan from the reason's remaining useful time; the service default may be
much longer. A collapse key can replace obsolete transport messages where
supported, but is not a global contact cap or an exactly-once reward mechanism.
Test the chosen transport fields against the active SDK/API reference.

[Registration management](https://firebase.google.com/docs/cloud-messaging/manage-tokens)
covers registration freshness and cleanup. At this check date its guidance
describes both FID-based registrations and legacy tokens; verify what the actual
client/server versions use. Track refresh and invalidation, bind addresses to the
correct signed-in context, and stop targeting stale/invalid registrations. Keep
server credentials off the client and raw delivery identifiers out of analytics
exports and public examples.

## Integration proof

Define a narrow engine adapter for permission state/request, schedule/cancel,
registration changes and opens. These are interface responsibilities, not named
Godot APIs. Use a test provider/fake clock for business rules and then the actual
native plugin for device acceptance. Pin plugin/native SDK versions and inspect
maintenance, dependency footprint and platform compatibility before adoption.

Exercise fresh install, denial, later enable/revocation, foreground/background,
terminated app, offline return, expiry, local cancellation, duplicate opens,
registration refresh, sign-out and stale content. Store service acceptance,
device-observed presentation and player action as separate evidence. Recheck
sources when OS targets, SDKs, plugins or delivery modes change.
