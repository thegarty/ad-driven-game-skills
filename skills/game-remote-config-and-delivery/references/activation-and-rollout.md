# Activation and rollout recipe

## One state owner

Keep configuration fetching outside gameplay scenes. A simple lifecycle is `bundled default -> compatible cached active -> fetched candidate -> validated staged -> activated snapshot`. Fetch failure changes availability diagnostics, not the currently active valid snapshot. Reject a stale response from an earlier account/environment generation. Serialize publication so two asynchronous fetches cannot activate in the wrong order.

The candidate envelope should identify a config revision, schema version, supported client range, content revision and integrity/provenance information appropriate to the transport. Each key has a type and units. Validate cross-field rules as well as individual bounds: a reward cannot reference a nonexistent currency; a level cannot reference a missing enemy; minimum difficulty cannot exceed maximum difficulty. These are product-defined fields, not Firebase-reserved names.

Example synthetic compatibility table:

| Candidate | Installed client's contract | Decision |
|---|---|---|
| Schema 2, content pack 7, known currencies | Schema 2 and content 7 present | Stage for next menu transition |
| Schema 3 | Client supports schema 2 only | Retain compatible active/default; record rejection |
| Schema 2, content pack 8 unavailable | Required content 8 missing | Wait with existing content; do not expose broken level |
| Known schema, negative upgrade cost | Nonnegative cost required | Reject candidate; do not turn invalid data into a free purchase |

The exact numbers are illustrative. Version ordering alone is insufficient: an older schema may still contain unsupported content identifiers. Avoid changing a downloaded asset in place while retaining the same version identity.

## Bind snapshots to accepted actions

At run creation, retain the relevant immutable config snapshot or a recoverable version identity. At offer creation, retain the exact promised reward. A later activation affects new actions according to the contract. Do not recalculate a completed reward from today's table. Configuration history must remain available long enough to settle in-flight claims; storing a compact normalized offer can be simpler than retaining every remote template.

For an emergency ad disable, stop new eligible requests/presentations according to the documented privacy/provider constraints and allow legitimate in-flight settlements to complete. A kill switch is effective only after clients receive and apply it. Offline devices still require safe local behavior; do not describe the switch as immediate global control.

## Release record and rollback

Before publishing, capture old/new revisions, semantic diff, targeted population, compatible clients, dependent content, expected change, guardrails and owner. Use a stable assignment appropriate to the account/install model and record actual exposure at use. Keep staged environments and provider permissions separate from production. Avoid distributing admin credentials in the game or automation fixtures.

Monitor configuration acceptance/rejection and crash/save/reward failure rates before interpreting commercial metrics. A rollback restores compatible rules for future actions. It cannot reverse previously granted items, migration writes or downloads on unreachable devices. For such changes, design a forward repair or compensating transaction with an audit trail rather than replaying an old file blindly.

## Official implementation sources

Checked **2026-10-26**:

- [Firebase loading strategies](https://firebase.google.com/docs/remote-config/loading) separates fetching and activation and discusses choosing when fetched values affect users. Match the chosen SDK/plugin's actual supported calls; these pages do not provide a built-in Godot binding.
- [Firebase templates and versioning](https://firebase.google.com/docs/remote-config/templates) documents versioned templates and management. Provider template history is not your game's save, transaction or content rollback mechanism.

The validation, ownership and compatibility contracts above are original architectural recommendations. They need implementation and project-specific tests; reading provider documentation does not prove them in a shipped client.
