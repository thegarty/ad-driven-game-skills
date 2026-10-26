---
name: game-ad-integration
description: Implement or debug mobile game ad loading, presentation, earned rewards, callbacks and recovery. Use for SDK adapters and reliable reward delivery, including Godot; use separate analysis for placement strategy or live provider optimisation.
license: MIT
---

# Game ad integration

Implement the ad lifecycle as an explicit, testable service boundary. Start by inspecting the game's engine, native plugins, exact SDK versions, save model, existing privacy controller and placement contract. Preserve the chosen engine and provider; for an unfamiliar stack, locate maintained official documentation and inspect its actual adapter before writing API calls.

## Establish the implementation contract

- Separate gameplay eligibility, privacy eligibility, SDK readiness, ad availability, presentation and reward settlement. A single `ads_enabled` flag cannot express these states.
- Define immutable opportunity identity before showing. Bind reward amount, type, placement, run/claim identity and eligibility to that opportunity. Never route a late callback to the currently visible screen's offer.
- Choose one owner for each SDK callback and each analytics event. Use official test ads or registered test devices in development, with an inert adapter for offline/unit tests.
- Document source version, plugin/SDK family and platform. Do not mix Android legacy and Next-Gen API examples; verify migration guidance and the chosen plugin's compatibility.

Read the [state and reward contract](references/state-and-rewards.md) before changing callbacks, persistence, retry behaviour or consent invalidation. Read the [Godot recipe](references/godot-adapter.md) for engine/native boundaries and [telemetry recipe](references/firebase-telemetry.md) for Firebase event ownership. These are implementation recipes, not a pretested SDK plugin.

## Implement and validate

1. Put the provider behind an adapter. Keep gameplay reward calculation and persistent grant logic outside native SDK listeners.
2. Refresh the relevant privacy state using the provider's documented flow; evaluate permitted requests before initializing/requesting where applicable to the selected SDK. Inspect native auto-initializers and plugin behaviour. Do not infer personalized-ad permission from an ad-request eligibility Boolean.
3. Preload only for eligible opportunities, with bounded retry/backoff. Surface unavailable/loading/ready/error states truthfully. No-fill and initialization failures must leave the game usable.
4. Revalidate the opportunity immediately before display. A successful load or Retry action must not silently become an ordinary rewarded-ad opt-in. Prevent concurrent full-screen presentations.
5. Handle earned callbacks separately from close/failure callbacks. Commit a reward and its deduplication marker atomically, then acknowledge the local pending receipt. Preserve pending earned receipts across navigation, reset decisions and recovery as specified by the product.
6. Apply privacy changes to future requests and cached ads; stale load callbacks cannot restore old permissions. A previously earned valid reward remains deliverable.
7. Add tests at the state/persistence layer and device checks at the native layer. A desktop fake proves neither live playback nor store readiness.

## Completion evidence

Return the adapter contract, changed files, privacy and telemetry ownership, tests passed and failure cases still requiring devices. Demonstrate duplicate/out-of-order callbacks, late earn after close, restart, failed save, no-fill, timeout, background/resume and consent changes. State precisely whether validation reached source tests, native test ads or production observation.

Use [official sources](references/sources.md) for current platform APIs. The [Overgrowth lesson](references/overgrowth-lesson.md) supplies failure cases without making its implementation a universal dependency.
