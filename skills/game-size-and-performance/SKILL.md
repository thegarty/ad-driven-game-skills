---
name: game-size-and-performance
description: Reduce mobile-game download size, installed footprint and asset/SDK bloat while protecting quality and runtime performance. Use for compression, app-store size limits, Godot import/export tuning and release size regressions.
license: MIT
---

# Game size and performance

Keep the shipped game lean through measured budgets and deliberate content
choices. Work from the actual release artifact, engine/SDK versions and supported
devices; a small source repository does not prove a small installed game.

## Establish the baseline

Record the source revision, release/debug configuration, export preset, engine,
SDKs, architectures, languages and delivery configuration. Separate four measures:

- Upload/archive size: the local AAB, IPA, APK or other container.
- Per-device compressed download: store-generated variant and optional content.
- Installed footprint: app plus downloaded assets, caches and saved data.
- Runtime footprint: peak CPU/GPU memory, loading time and frame-time behavior.

Read [current store limits and measurement](references/store-limits.md) before
asserting eligibility. Its dated limits are ceilings, not product budgets. Set
project-specific budgets using the [size-budget record](assets/size-budget.md):
initial play, full optional content, update growth and representative low-end
device behavior. State bytes or clearly distinguish MB from MiB.

Use [artifact inventory](references/artifact-inventory.md) to find large files
and gate local artifact growth. It can inspect ZIP-based AAB/APK/IPA containers
without extracting them, but it cannot establish store download size or runtime
memory. Confirm those with store tooling and device measurements.

## Reduce the largest justified cost

Use [Godot and content recipes](references/compression-recipes.md) for concrete
import/export options. Inspect shipped resources and dependency reports before
changing codecs or adding another optimisation library.

1. Exclude unused content, duplicate exports, source masters, marketing media,
   fixtures and development-only dependencies from release packaging. Preserve
   source work and separately archived debugging/symbolication artifacts.
2. Right-size images, audio and models for actual phone presentation. Compare
   compression changes at the same quality, device and gameplay moment.
3. Review the incremental package, startup, memory and privacy cost of each
   native SDK/mediation adapter. Remove a dependency only after tracing its
   runtime use, transitive dependencies and required bridge behavior.
4. Evaluate optional delivery only when content is genuinely optional. Keep the
   promised first-play/offline route available; handle interrupted downloads,
   cache eviction, versioning and space checks honestly.

Do not equate stronger archive compression with lower RAM. A texture can be
small on disk and large when decoded. LODs can improve rendering while adding
packaged data. Better compression can add CPU/load cost. Measure the tradeoff.

## Make the improvement stick

For slow frames, memory growth, loading stalls or thermal degradation, use
[runtime profiling](references/runtime-profiling.md) and the
[runtime profile record](assets/runtime-profile.md). Separate CPU, GPU, native
service, memory and sustained-load evidence before choosing an optimisation.

Compare before/after release builds using the same variant and measurement tool.
For update budgets, measure the actual transfer when upgrading from the previous
installed release through the intended delivery route. Archive-size differences
are not patch-download sizes. Avoid unnecessary reimports or repacking of
unchanged assets, and verify whether delivery tooling preserves that benefit.
Test visual readability, audio loops, dynamic resource loads, localization,
native services, clean install/update, offline play and representative long
sessions. Record savings in absolute bytes and percentage with the denominator.

Add a size regression check to release validation using agreed budgets and an
explicit exception rationale. Do not silently raise budgets to pass CI. Return
the largest contributors, changes, measured deltas, quality/device results and
remaining unverified store measurements. No retention or revenue uplift follows
automatically from reducing bytes.
