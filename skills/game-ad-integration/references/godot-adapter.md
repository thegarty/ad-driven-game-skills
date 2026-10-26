# Godot, AdMob and native bridge recipe

**Status:** architecture recipe reviewed against official documentation on 2026-10-26. No plugin implementation is bundled or claimed to have passed physical-device ad tests.

## Inspect before selecting a plugin

Record Godot version, Android/iOS export templates, renderer, target OS versions, plugin version/source/licence, native Google Mobile Ads SDK family/version, UMP version and Firebase version. Confirm that the plugin implements the required callbacks and privacy lifecycle for both targets. A functioning Android plugin does not imply iOS support.

Use Godot's [Android plugin documentation](https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html) and [iOS plugin documentation](https://docs.godotengine.org/en/stable/tutorials/platform/ios/ios_plugin.html) to verify native registration and export packaging. For SDK APIs follow the selected version's Google reference. Do not invent a built-in Godot `AdMob` singleton.

## Suggested boundaries

| Component | Responsibility |
|---|---|
| Gameplay service | Decide placement eligibility and freeze the promised reward |
| GDScript ad broker | Coordinate state, Watch intent, generation IDs and callback routing |
| Android/iOS adapter | Convert engine calls to supported native APIs, own ad objects and thread dispatch |
| Privacy controller | Read provider/runtime permission state; invalidate stale requests |
| Reward store | Atomically update game state and applied claim IDs |
| Analytics bridge | Emit consent-eligible game events with a clear ownership table |

Define app-owned methods such as `prepare(placement, claim)`, `present(claim)` and `availability(placement)` in your adapter contract. These names are suggestions, not plugin APIs. Expose load failure, show failure, shown, closed and earned as distinct signals with the original attempt/presentation identity.

On the native side, use the UI thread for APIs that require it and marshal callbacks to the engine's supported execution context before mutating scene/game state. Hold native activity/view-controller references safely across lifecycle changes. Confirm actual bridge types: a native Boolean, integer or serialized payload may not arrive as the same GDScript Variant across wrappers. Normalize documented representations deliberately and reject malformed data.

Avoid using method introspection intended for a normal Godot object as proof that a native singleton supports a method. Check the plugin contract and execute a small device bridge probe. Preserve unsupported-platform behaviour: an inert desktop adapter reports unavailable and cannot create production requests.

## Native export checks

1. Inspect the exported merged Android manifest and dependencies or iOS generated project/frameworks. Verify required app identifiers privately, test-ad configuration, privacy manifests/permissions and supported architectures.
2. Inspect SDK startup paths and auto-initializers. Calling a privacy gate from GDScript is too late if another native component already initiated prohibited collection. Exact ordering depends on the selected SDK family/version.
3. Verify cold launch, returning launch, privacy refusal/change, offline/no-fill, ad close, late callbacks and scene changes on physical Android and iOS devices using test ads.
4. Confirm game audio, timers, touch input, safe areas and orientation after a full-screen ad. Test a save/write failure independently of playback.
5. Record source revision, build number, device/OS, plugin/SDK versions and observed results. A desktop fake and a successful export are different evidence levels.

Do not migrate a working SDK family solely to match a recipe. Read release notes, compatibility and current store requirements, then make an explicit migration plan when needed.
