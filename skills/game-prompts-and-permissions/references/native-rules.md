# Current native request constraints

Official sources checked **2026-10-26**. Request behavior varies by SDK, supported OS, region, previous choice and app configuration. Inspect the shipped engine bridge and use current official platform documentation before writing methods or deciding whether to re-request.

## Permission is not an app invitation

Keep a separate state for the player's feature preference and the OS/provider authorization. Re-query actual status on use/foreground as appropriate. A dismissed dialog, an error or a denied result does not authorize access. Only the dependent feature needs an unavailable/denied explanation; preserve unaffected gameplay.

Apple recommends requesting only necessary access in context, with a specific purpose string. If an explanatory pre-alert is needed, its guidance calls for one clearly labeled continuation to the system alert and forbids misleading imitation, incentives or annotations directing the tracking choice. Do not transplant the game's two-button sales-modal design into that pre-alert. [Apple privacy design](https://developer.apple.com/design/human-interface-guidelines/privacy).

Android runtime permission guidance requires checking current permission, explaining where appropriate, requesting at the relevant feature and degrading gracefully when denied. Rationale and re-request behavior depend on actual OS state, permission and target version; an app counter alone cannot determine whether a system prompt will appear. [Android request permissions](https://developer.android.com/training/permissions/requesting).

Where Play's prominent disclosure rules apply, provide the required in-app explanation before the governed request/access and obtain the required affirmative choice. Navigating away is not consent. Do not combine unrelated disclosures or start the restricted collection while the player is deciding. [Google Play User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311).

## ATT and ad consent

ATT is distinct from ad-provider consent and from notification permission. Read the current authorization status and the selected SDK/provider eligibility before data operations. Do not offer coins, access or discounts for agreeing to tracking, and do not imply that consent is required for unrelated gameplay.

Apple's current `requestTrackingAuthorization` documentation distinguishes denied, restricted, authorized and not-determined responses, and conditions such as active app state and another pending permission. It also describes EU re-request eligibility after one year. Consequently **neither “always ask again” nor “ATT can never be requested again” is a valid universal rule**. Discover the current OS/region behavior, respect user preferences and test the actual packaged integration. [Apple ATT request behavior](https://developer.apple.com/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:)).

AdMob UMP requires current consent-information updates and provides ad-request eligibility/privacy-option state. Use the selected platform/SDK's documented sequence and do not substitute an app-local “consent shown once” flag. Changing privacy choices can affect loaded ads as well as future requests. [AdMob UMP setup](https://developers.google.com/admob/android/privacy).

## Notifications

Ask when the player understands a specific notification's use. Apple records the first explicit notification authorization choice; repeated authorization calls do not simply reopen the same prompt. Its provisional mode is a distinct quiet-delivery option, not the same as full alert permission. [Apple notification permission](https://developer.apple.com/documentation/usernotifications/asking-permission-to-use-notifications).

Android notification permission behavior differs by OS and target SDK, with allow, denial and dismissal having distinct effects. Check current permission and channel settings rather than assuming installation or a previous API call enabled all notifications. [Android notification permission](https://developer.android.com/develop/ui/views/notifications/notification-permission). Delivery scheduling, cancellation and quiet hours need their own implementation; permission is only one prerequisite.

## Reviews

Use native review mechanisms and neutral experience eligibility. Do not ask a sentiment question before a review flow, incentivize reviews, or route only likely positive reviewers to the store. Google documents quotas and forbids opinion/predictive screening; native requests can show nothing. [Play In-App Reviews](https://developer.android.com/guide/playcore/in-app-review?hl=en).

Apple distinguishes unobtrusive native requests from a user-initiated store review link. System suppression means an attempted request does not prove a visible prompt or submitted review. Keep support independent and available to everyone. [Apple review requests](https://developer.apple.com/documentation/storekit/requesting-app-store-reviews), [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).

## Godot/native proof

Inventory the real plugin methods, exported native libraries, purpose strings/manifest declarations, supported OS levels and callback results. Normalize them into application states without relabeling ambiguous callbacks as success. Test requests while active, after background/resume, after denial/dismissal, after settings changes and with another modal pending. Verify both actual system behavior and normal gameplay fallback on a packaged device. Editor mocks establish only game-side state handling.
