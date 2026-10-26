---
name: game-prototyping
description: Turn an agreed mobile game loop into a playable vertical slice, or improve its implementation foundation. Use for engine structure, deterministic gameplay, saves, configuration and prototype validation rather than commercial strategy.
license: MIT
---
# Game prototyping

Build the smallest playable slice that answers the design question while preserving a clear path to a reliable mobile game.

## Inspect before selecting a stack

Read the existing project manifest, scene structure, engine version, build scripts and development instructions. Preserve a working stack unless the requested outcome requires a change. If the engine or plugin is unfamiliar, inspect its current official documentation before writing API calls. Never substitute an invented wrapper or promise mobile support based on a desktop demonstration.

Clarify only decisions that affect the slice: intended input/orientation, target devices, core loop, success/failure, persistence, content budget and observation to capture. Record unresolved matters as explicit prototype assumptions.

## Build a testable slice

1. Implement one start → play → outcome → restart cycle with placeholder assets where appropriate. Include a useful player choice and enough feedback to judge it.
2. Keep gameplay state and rules separable from rendering and menus. Store tunable values in identifiable configuration rather than scattering them through UI code. A fixed seed and injected clock should make a reported gameplay failure reproducible when randomness or timing matters.
3. Define which progress persists, the schema version and when a save becomes authoritative. Treat a failed save as a visible recoverable condition. Preserve valid prior data and do not silently reset an unreadable save.
4. Define pause, background, resume and interruption behaviour. Specify which clocks stop and whether any offline progress exists; do not infer offline rewards just because a timestamp was saved.
5. Represent external services through narrow interfaces. During prototype tests use inert adapters with explicit unavailable, success and failure outcomes. Keep real ad units, credentials and production services out of fixtures.

For a Godot project, use [the Godot slice recipe](references/godot-slice.md). It describes architectural boundaries, not a drop-in template or a mandated folder structure.

## Make performance observable

Choose a low-end target device and project-specific frame-time, loading and memory budgets. Measure representative worst-case play, including dense waves/effects and repeated restart cycles. Explain whether a result comes from a desktop, emulator or physical phone. A fast empty scene is insufficient evidence for the planned content scale.

## Deliver and validate

Use the [slice acceptance template](assets/slice-acceptance.md). Deliver the playable slice, its run instructions, the tested engine/build configuration, a concise change summary and the observation needed for the next decision.

Test the complete loop, restart, pause/background, interrupted save, reload and a representative failure path. If the slice includes an ad offer, test that normal play still works with the adapter unavailable and that a mock completion cannot grant twice. Do not broaden a prototype into production SDK integration, a store upload or a content factory just to make it appear complete.
