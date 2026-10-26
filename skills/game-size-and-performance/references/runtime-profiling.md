# Runtime profiling and sustained performance

Official documentation checked **2026-10-26**. Select tools for the actual engine,
renderer, OS and device; API or profiler availability differs by version. These
are measurement recipes, not universal frame-rate or memory requirements.

## Reproduce the workload

Record source/build/config revision, release/debug mode, engine/renderer, device,
OS, viewport, refresh-rate mode, quality options, battery/charging state and
network/native-service state. Use the same save, scene, seed and scripted actions
for comparisons. Keep cold launch, warm scene entry, steady play, peak combat,
menu transition, ad presentation and return as separate phases.

Choose a product frame target and explicit quality/access tradeoff. A hypothetical
60 frames/second implies 1000/60 ≈ 16.67 milliseconds per frame; this is arithmetic,
not a recommendation that every game must target 60. Record frame times and
stall counts/distribution, not only average FPS. A mean hides a few disruptive
frames; report the sampling window, frame count and percentile definition with
p50/p95/p99 when there is enough data to interpret them.

## Locate the bottleneck

[Godot's debugger panel](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html)
separates script/physics profiling from rendering CPU/GPU profiling. The visual
profiler does not represent all CPU work. Keep viewport and rendering settings
comparable, and check support for the active renderer/platform. Use native traces
when the cost lies in SDKs, drivers, scheduling or work outside script visibility.

[Godot CPU optimisation](https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html)
explains profiling bottlenecks and the cost of instrumentation. Compare a diagnostic
capture with a representative build without the profiler; do not call an editor
profile a release-performance measurement. Missing time in a script report may
be waiting or work outside that report, not proof the CPU is idle.

| Suspected cause | Discriminating check | Candidate change to test |
|---|---|---|
| Per-frame gameplay work | Script/physics time and call counts during the same crowded wave | Remove redundant searches/allocations; update only changed state |
| Rendering submission | Rendering CPU time and draw/material workload | Reduce avoidable state changes or batch compatible content |
| Fill/overdraw/shader cost | GPU time; compare a controlled effects/resolution change | Reduce unnecessary transparent coverage, expensive passes or resolution |
| Loading/compilation/I/O | Stall aligned with first asset use or scene entry | Prepare required resources at an appropriate boundary; measure memory cost |
| Native service transition | Native trace and ad/load/resume markers | Fix lifecycle or defer nonessential simultaneous work without hiding errors |

[Godot GPU optimisation](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html)
describes how rendering costs depend on hardware and scene structure. A lower
triangle count or smaller archive alone does not prove a GPU improvement. Test one
plausible change against the diagnosed bottleneck and retain visual readability.
Do not rewrite the architecture or add pooling everywhere without measured need.

## Memory and lifecycle

Track engine resource/object counters and process/native memory separately where
tools permit. Some allocations and GPU resources will not appear in a script
memory total. Record peak and stable state for repeated load/play/unload cycles,
large reward recaps, ad loads, locale changes and background/foreground.

Synthetic diagnostic: memory rises on the first encounter, then plateaus through
repeated identical runs. That could be intentional caching. A growing post-unload
baseline across identical cycles suggests retained resources worth tracing, but
is not by itself a proven leak. Inspect ownership, signal/callback references,
resource caches and release timing. Validate a cache cap/eviction strategy against
reload time and offline behavior instead of indiscriminately clearing everything.

A smaller compressed texture can still decode to the same or greater memory.
Keep package-size wins and runtime-memory wins as distinct measured claims.
Avoid taking native service memory peaks as permanent game allocations without
phase-aware evidence.

## Thermal and battery behavior

Run long enough to represent the intended session and sustained load, with the
duration declared. Record cool-start and sustained performance separately and
repeat under comparable conditions. Charging, ambient conditions and prior device
load can alter results; retain these limitations. A short burst benchmark is not
proof that the game maintains that behavior throughout play.

[Android's game optimisation overview](https://developer.android.com/games/optimize/overview)
points to profiling and dynamic-performance tooling, including thermal-aware
performance work. Select supported tooling from current documentation rather
than assuming every device exposes the same counters. Adaptive quality should
use bounded levels, stable transitions and hysteresis where appropriate; it must
preserve readable threats, input, timing rules and access settings.

Test a sustained busy scene, navigation and return from native UI at the selected
quality levels. Record battery/power using a defined device method and window;
a subjective “phone felt cooler” is an observation with limited precision, not
measured energy savings.

## Deliver a comparison

Use [the runtime profile record](../assets/runtime-profile.md). Include workload,
measurement provenance, baseline/candidate distributions, peak/stable memory,
loading, sustained behavior, visual/access acceptance and remaining uncertainty.
Keep per-device outcomes separate before summarising. A source change is not a
performance result; a device result is not proof of retention or revenue uplift.
