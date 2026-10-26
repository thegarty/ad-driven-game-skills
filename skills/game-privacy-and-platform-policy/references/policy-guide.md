# Policy and implementation guide

Official sources checked **2026-10-26**. Recheck at implementation and release; this document gives navigation and engineering decisions, not a timeless compliance certificate.

## Apple

Read [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/), especially the current sections addressing Kids Category, advertising, purchases and privacy. Apple places additional restrictions on third-party analytics/ads in children's apps; permitted exceptions must be verified against the actual product and current policy. Advertising must suit the app's audience, avoid deceptive interactions, and provide required dismissal/reporting controls.

[User Privacy and Data Use](https://developer.apple.com/app-store/user-privacy-and-data-use/) explains ATT, privacy labels and third-party SDK disclosure. Determine whether the implemented data flows meet Apple's definition of tracking. ATT authorization is separate from a publisher's own privacy choices and from other applicable consent requirements. Do not bypass a denied/restricted ATT state through fingerprinting or alternative identifiers. Keep current privacy manifests and required-reason API declarations aligned with SDK contents.

## Google Play and AdMob

Read [Google Play Families policies](https://support.google.com/googleplay/android-developer/answer/9893335) when children are among the intended audiences. Its SDK, personalization and mixed-audience requirements depend on the actual audience. Check the current permitted/certified SDK list and applicable format rules rather than treating ordinary AdMob integration as sufficient.

For UMP, follow the current [Android guide](https://developers.google.com/admob/android/privacy) or [iOS guide](https://developers.google.com/admob/ios/privacy), including launch-time consent-information updates and a privacy-options entry point when required. Maintain a deliberate error path; a failed refresh is neither an automatic new grant nor proof that every previously valid provider state is unusable.

Use documented provider APIs for consent interpretation and ad request controls. When composing multiple consent writers, define ownership and ordering. Avoid one SDK silently overwriting the user's choices or a stale callback re-enabling a disabled purpose. Verify raw protocol interpretation only when the official provider contract actually requires it; never infer permission from an arbitrary missing field.

## Firebase and telemetry

[Firebase collection configuration](https://firebase.google.com/docs/analytics/configure-data-collection) documents controls that must be reconciled with native initialization and app choices. Check each enabled SDK separately: disabling Analytics does not prove every other SDK stops collecting. Consent to gameplay metrics does not automatically permit remarketing or advertising identifiers.

Create a bounded event dictionary with data minimization. Do not attach raw date of birth, email, precise location, ad IDs or raw CMP strings merely to segment gameplay. Explain measurement gaps introduced by collection restrictions; do not silently generalize consented-user metrics to all users.

## Native test matrix

Test a clean install, returning install, unknown/refused/restricted state, permitted state, offline/error path, expired consent, change/withdrawal, failed preference write, game reset, restored save and app upgrade. Test platform tracking denial independently from the CMP state. Include audience branches actually supported by the product.

Inspect logs/network behaviour and packaged native metadata where feasible. A unit-test mock only demonstrates the game's interpretation of a state; it does not prove what a real SDK transmits. Keep test devices and debug geographies out of release configuration.

## Overgrowth engineering lesson

**Source-inspected, 2026-10-26:** Overgrowth kept privacy state outside ordinary gameplay saves and explicitly invalidated stale advertising callbacks. Its exact age rules and consent mapping were product-specific. The reusable lesson is separation of state and ownership, followed by native verification. This record does not establish compliance or validate subsequent releases.
