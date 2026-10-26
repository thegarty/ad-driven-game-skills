---
name: game-privacy-and-platform-policy
description: Review or implement mobile-game audience, consent, advertising privacy and store-disclosure requirements. Use when adding SDKs, changing data use or ads, targeting children, or preparing Android/iOS releases.
license: MIT
---

# Game privacy and platform policy

Turn the actual game's audience and data flows into a verifiable implementation and disclosure plan. This skill provides engineering and platform-policy guidance; do not present a legal interpretation or checklist as legal clearance.

## Establish the applicable context

Inspect the declared and intended audience, actual imagery/gameplay, distribution markets, app-store categories, SDK inventory, account features and data use. An age rating is not a substitute for audience classification. Do not assume one country's child-age threshold applies everywhere or that a self-declared adult audience resolves a child-directed design.

Use the [policy and implementation guide](references/policy-guide.md) and its official links. Recheck primary sources for the selected platforms, markets and SDK versions. If jurisdictional obligations remain unresolved, state the specific decision requiring qualified review while continuing independent technical discovery.

## Map data and permission independently

Complete the [privacy implementation record](assets/privacy-record.md): data item, collection point, purpose, recipient, retention, control and disclosure. Distinguish gameplay analytics, advertising storage/identifiers, ad measurement, personalization, platform tracking and account functionality. A single global “consent granted” flag is insufficient.

Inspect native startup paths and automatic SDK collection, not only the game's settings screen. Determine what is initialized, what may collect/transmit and when. Validate configured defaults and persisted choices on a cold start of the exported binary.

For AdMob, implement the documented UMP update/form/privacy-options flow for the selected SDK. `canRequestAds` means the provider permits an ad request in that state; it does not certify permission for personalized advertising, ATT tracking or every analytics purpose. Apply each SDK's supported controls rather than guessing meaning from raw consent strings.

## Preserve state correctly

- Keep privacy choices independent of game-progress restoration/reset. Restoring an old save must not resurrect withdrawn permissions.
- On changes, invalidate incompatible cached ads and stale load callbacks. Do not erase legitimate already-earned rewards.
- Handle unknown, refused, restricted, error and granted states explicitly. Use the provider's documented handling of valid cached eligibility on errors; never reinterpret an error as an opt-in.
- Present available privacy controls and persist choices accurately. Report a failed preference write rather than falsely confirming it.
- Evaluate provider/account-wide settings against older deployed versions as well as the current candidate.

## Audience and release review

For child-directed or mixed-audience games, replace the adult advertising recipe with an audience-specific design review before selecting SDKs or tracking features. Verify applicable store restrictions, permitted SDKs/formats and neutral age-screen requirements using current official policy. Preserve playable behaviour when an advertising or analytics capability is unavailable.

Compare privacy policy, App Store privacy disclosures/manifests, Google Play Data safety, audience declarations and in-app controls with the final binary and SDK inventory. Readiness evidence is a tested implementation and matching disclosures, not merely a consent dialog screenshot.

Deliver the data/control matrix, platform-specific required changes, unresolved decisions, native test results and dated sources. State limits precisely; this skill does not guarantee store acceptance or legal compliance.
