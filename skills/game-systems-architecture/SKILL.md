---
name: game-systems-architecture
description: Design or refactor mobile-game state ownership, Godot scenes, services, native bridges and asynchronous lifetimes. Use when features interfere, callbacks outlive screens, startup order is fragile or a prototype needs a maintainable architecture.
license: MIT
---

# Game systems architecture

Make a player's action have one understandable path to authoritative game state.
Preserve a working engine and suitable architecture; do not replace a small game
with a framework merely because more features are planned.

## Inspect ownership and lifecycle

Read the engine/version, startup scene, autoloads, state models, native plugins,
save boundaries and representative UI actions. Trace one purchase/upgrade, one
run transition and one delayed external callback. Record who can mutate each
field and who lives long enough to receive the result. Use the
[system contract](assets/system-contract.md) to capture current and proposed ownership.

Separate responsibilities where they have different lifetimes or correctness
requirements: simulation rules; presentation/input; saved progression; remote
configuration; time; native services; consent; and reward/entitlement settlement.
An autoload can be appropriate for an application-lived service. The problem is
uncontrolled shared mutation or scenes depending on hidden startup state.

## Define the boundaries

Read [Godot ownership and async recipes](references/godot-ownership.md) before
changing service startup, scene ownership or native callback dispatch.

- A gameplay command carries validated intent and identity. The rules owner
  decides whether it is legal, mutates once and returns an outcome.
- Presentation observes outcomes and renders state. A destroyed scene must not
  own the only receipt for a valid earned reward or completed purchase.
- Services expose explicit unavailable/loading/ready/failure outcomes. Optional
  ads or telemetry must not block the ordinary playable loop indefinitely.
- Configuration is a validated snapshot bound to the run or offer where needed.
  A late fetch must not alter a reward already promised to the player.
- Native adapters normalize documented payload types and marshal work to the
  engine's supported execution context. App-owned interface names are contracts,
  not claims that a particular Godot plugin already provides those methods.

Make illegal transitions reject without partial mutation. Define command IDs,
attempt generations and cancellation ownership where retries or delayed results
exist. Cancellation of a view's interest is different from cancellation of a
durable transaction. Avoid a global event bus whose consumers all write the same
balance or trigger one another recursively.

## Build in slices

Choose the smallest seam that fixes the observed problem. Preserve save/content
IDs and player promises; migrate state explicitly if the refactor changes them.
Use a composition point to provide dependencies, inject clocks/randomness for
replay, and replace external providers with inert adapters in logic tests.
Retain an explicit bootstrap order with bounded failures and recovery behavior.

For each change, test command rejection, duplicate submission, scene replacement,
late callback, pause/resume, startup failure and ordinary play with optional
services unavailable. Trace the old versus new result for representative saved
states. Measure allocations/loading where moving ownership changes performance.

Return the ownership map, chosen contracts, changed implementation, compatibility
decisions and observable tests. A diagram alone is not an implemented boundary;
a desktop fake is not validation of native threads or exported mobile binaries.
