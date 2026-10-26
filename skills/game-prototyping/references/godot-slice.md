# Godot mobile slice recipe

Use the engine version already selected by the project. Verify APIs and export/plugin compatibility against that version. This recipe is an original architecture recommendation, not extracted Overgrowth code.

## Practical boundaries

| Responsibility | Minimum contract | Useful isolated check |
|---|---|---|
| Gameplay rules | Explicit state + action + elapsed active time → next state/outcomes | Fixed-seed replay; invalid action does not mutate state |
| Presentation | Render current state; convert input to actions | Touch target/drag behaviour and readable failure feedback |
| Configuration | Versioned content IDs and tunable values | Missing/invalid content ID gives a useful error |
| Persistence | Load/migrate/validate; durably save a candidate state | Restart, corrupt input, disk-write failure, previous-save recovery |
| Service adapter | Availability + request identity + bounded outcomes | Unavailable, delayed, duplicate and stale responses |

Use ordinary Godot nodes/scenes for presentation and separate script objects/resources for rules/configuration where that fits the project. Avoid a large autoload singleton that owns combat, UI, save writes and provider callbacks: the problem is shared mutable ownership, not the presence of an autoload itself.

## Save protocol to specify

Before writing code, list the persistable fields, stable IDs and any pending transactions. A save operation should validate the candidate, write a new file, and use a platform-appropriate replacement/recovery strategy. Verify the exact filesystem guarantees available on the target platform; a rename alone is not a universal durability guarantee. Record success only after the persistence operation reports success. Preserve a recoverable previous version and keep an unreadable source for diagnosis when practical.

Gameplay state, display state and permissions have different owners. A restored gameplay save must not overwrite current platform consent. Earned currency and its receipt/acknowledgement must commit together. If cloud saves are introduced, define conflict ownership explicitly rather than combining two balances.

## Time and test seams

Distinguish simulation delta, active-play time and calendar time. Record the policy for backgrounding, pausing, time zone changes and device clock changes. Inject a clock into tests. An offline-production cap is a product rule requiring an explicit value; do not invent one as an implementation shortcut.

For a prototype, model ad availability without loading a provider SDK. Give each offer a stable opportunity ID and simulate earned/closed as separate outcomes. The service can fail while the gameplay loop still completes.

## Sources and limits

Official documentation verified **2026-10-26**:

- [Godot saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html): serialization and persistence building blocks. The tutorial is not a complete transactional save system.
- [Godot general optimisation](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html): profile bottlenecks and compare results on relevant hardware. The budgets in a new project remain project-specific.

These sources establish engine capabilities and measurement guidance. The ownership, recovery and transaction recommendations above are design decisions to validate in the implementing project.
