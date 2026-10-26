# Native review requests and feedback

Official documentation checked **2026-10-26**. Re-check the current supported SDK and store policy before shipping. This recipe does not prescribe a universal session count or prompt frequency.

## Eligibility and experience

Choose a quiet transition after the player has enough experience to form an opinion. Define eligibility from neutral usage conditions, app version and your own conservative request history. Defer during active play, ads, purchases, permission prompts, loading or a support conversation so the app does not pile up interruptions. Do not inspect predicted sentiment, spending or rating likelihood to decide who reaches the store flow.

Do not ask “Do you like the game?” and route only yes to a review. Do not offer coins, unlocks or prize entries for ratings/reviews. Help and a voluntary store review link should remain accessible without completing either flow. Apple requires its provided review API and disallows custom review prompts; review manipulation is prohibited. [App Review Guidelines, review and ratings provisions](https://developer.apple.com/app-store/review/guidelines/).

## Platform behavior

Google's in-app review guidance forbids opinion/predictive questions before or during the rating flow. Its quota can prevent display and can change; calling the API is not a guarantee of a visible card. A direct “rate this game” button should use an appropriate store destination rather than relying on a quota-limited prompt that may do nothing. [Google Play In-App Reviews](https://developer.android.com/guide/playcore/in-app-review?hl=en).

Apple recommends an unobtrusive moment after meaningful use; the system can suppress requests and users can disable them. Its documentation distinguishes opportunistic native requests from a user-initiated store review link. Use the selected native API appropriate to supported OS versions, not the sample's arbitrary usage count as a universal rule. [Requesting App Store reviews](https://developer.apple.com/documentation/storekit/requesting-app-store-reviews).

## Godot bridge and test contract

Discover the installed review plugin and native library versions. Confirm native activity/scene availability, foreground execution, callback semantics and release export inclusion. Wrap it in an application-owned `review_request_attempted` event if permitted, but do not label it `review_submitted`. A completed flow or return from the store cannot prove the person left a review or reveal its rating.

Test safe transition eligibility, user leaving the screen before the prompt, missing store support, suppressed prompt, plugin error, repeated scene entry and fallback link. The game must continue normally in each case. Do not automatically bombard the user with a second popup if no native card appears.

## Feedback triage and responses

Tag reviews as bug, comprehension, difficulty, value, ads, accessibility or content request; preserve a count of unclassifiable reports. Deduplicate copied reports before counting themes. Separate reported experience, reproduced problem and hypothesis. Prioritize severity and reach over rating alone, and keep unhappy feedback in the same improvement process.

Draft factual public replies without personal data or unverifiable promises. Offer a private support route for account details; do not condition recovery on editing or deleting a review. Describe a fix as released only when the intended build is available in the relevant store/market. Measure support resolution and product quality separately from review score changes.
