---
name: game-remote-config-and-delivery
description: Implement or audit remote game configuration, staged rollout, kill switches and optional content delivery. Use for safe defaults, version compatibility, activation boundaries, rollback and offline resilience in Godot or other mobile engines.
license: MIT
---

# Game remote config and delivery

Make remote changes predictable, recoverable and optional for core play. Inspect the engine, provider/plugin, configuration consumers, save schema, content manifests and existing deployment permissions before proposing a new service. A small game may need only bundled configuration and app releases; add remote delivery when its operational value justifies the extra states and maintenance.

## Define the contract

1. Inventory every key's owner, type, unit, bounds, default, dependency and activation boundary. Reject invalid values and incompatible combinations as a configuration unit; silently clamping a broken economy can create a different experiment. Define permitted unknown fields and missing-field behavior.
2. Separate downloaded, validated, staged and active versions. Check supported config schema, client version, save compatibility and required content version before staging. A successful fetch is not permission to change a live run.
3. Bundle usable defaults. Keep a verified last-known-good version only while it remains compatible with this client. Bound startup waits; offline, timeout, invalid data and provider failure must have explicit fallback behavior. Report the active version and fallback reason without exposing secrets or personal data.
4. Activate at a named safe transition. Snapshot rules for a run, quoted purchase or ad opportunity; a new multiplier must not rewrite an accepted offer. Specify narrowly scoped emergency disabling behavior separately from ordinary balance changes. Already earned valid rewards remain obligations.
5. Treat client configuration as inspectable and modifiable. It must contain neither secrets nor authority to grant valuable server-owned entitlements. Do not use a remote data mechanism to deliver executable code without evaluating platform requirements and the actual delivery system.

Use the [config contract](assets/config-contract.md) and [activation recipe](references/activation-and-rollout.md). For Godot, wrap the inspected native provider in an app-lifetime adapter that exposes typed snapshots to game logic. The recipe describes interfaces to implement, not a supplied Firebase Godot API.

## Deliver content and operate changes

Read the [optional content recipe](references/optional-content.md) when assets leave the base package. Keep required first-play content available; show optional download size and truthful availability. Validate a complete compatible content set before activation, handle interrupted downloads and storage exhaustion, and budget cached assets as part of the installed footprint.

Stage configuration through development and release-candidate environments. Preview affected audiences and dependent keys, preserve the previous compatible version, and define observable failure conditions and the person who can roll back. Choose rollout size and observation window from traffic and risk. Record assignment and actual exposure separately; changed config alone is not evidence that a player experienced a treatment.

Test cold offline launch, incompatible caches, malformed values, old clients, missing assets, mid-run fetch, account switch, partial delivery and rollback. A server template rollback does not undo purchases, consumed currency, save migrations or a downloaded file already activated on an offline device. Design recovery for those consequences before launch.

Return the typed contract, fallback/activation state diagram, content and storage budgets, version compatibility table, rollout/rollback record and tests. Distinguish local fault simulation, device verification and observed production delivery.
