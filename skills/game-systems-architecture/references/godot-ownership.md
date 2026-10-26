# Godot ownership and asynchronous work

## A practical ownership map

| State or action | Typical lifetime | Contract to make explicit |
|---|---|---|
| Current run simulation | Run | State plus valid command and active delta produces one outcome |
| Menus and scene nodes | View/scene | Render snapshots; translate input into commands |
| Saved progression and applied claims | Account/local profile | Validate, migrate and commit a coherent snapshot |
| Native ad/billing bridge | Application | Retain request/presentation identities across view changes |
| Consent and platform permissions | Device/platform | Reconcile independently of ordinary gameplay restore |
| Config/content snapshot | Compatible version or run | Validate before activation; preserve bound promises |

This is a starting design, not a required class hierarchy. A small game can
combine responsibilities when ownership stays clear and tests remain possible.

## Async contract

Every operation that can finish after navigation needs an owner, operation ID,
expected generation, terminal outcomes and cleanup behavior. A view can stop
listening without destroying the transaction result. Before applying a callback,
validate its payload and match it to the original operation. Do not use the
currently selected screen, currency or run as its destination.

For app-owned native adapters, document argument/return types, null/error
representation, callback thread, ordering guarantees actually supplied by the
SDK and ownership of retained native objects. Normalize wrapper-specific numeric
and Boolean representations deliberately. Reject malformed values; do not treat
truthy strings as permission or success.

An original example of a typed application contract, expressed as pseudocode:

```text
UpgradeIntent:
    command_id: nonempty opaque string
    profile_id: known local/account identity
    expected_revision: nonnegative integer
    upgrade_id: supported stable content ID

UpgradeOutcome:
    command_id: original identity
    status: applied | already_applied | rejected | retryable_failure
    revision: authoritative state revision
    reason: defined reason code, never an arbitrary success-like string
```

The command owner obtains price and eligibility from its authoritative rules,
checks the expected revision, and atomically applies the spend and upgrade.
A scene supplies intent, not a trusted price or replacement balance. Repeated
command IDs return the existing outcome; a stale expected revision requires
reconciliation rather than a second spend. A local profile may use a coherent
snapshot instead of a backend, but needs the same explicit ownership.

Keep concurrent full-screen services behind one presentation coordinator. One
operation may pause gameplay/audio without making an unrelated service's close
callback resume the game prematurely. Model overlapping reasons to pause, such
as application background plus native modal, rather than one toggled Boolean.

## Bootstrap and teardown

1. Load minimum local configuration and recoverable game state.
2. Establish the playable scene with explicit optional-service availability.
3. Reconcile privacy/platform prerequisites and initialize required adapters in
   their documented order. Inspect native auto-initializers too.
4. Activate compatible remote data at a safe boundary; publish state changes to
   presentation without mutating an in-progress promise.
5. On background, checkpoint already-valid progress within the platform's actual
   budget. Do not assume a final shutdown callback will run.
6. On scene disposal, disconnect view-owned listeners and invalidate view work.
   Keep application-owned pending settlements recoverable.

The order is a design to adapt after inspecting the game's services. A backend,
dependency-injection framework or reactive event system is not inherently needed.

## First-party sources

Verified **2026-10-26**; check against the chosen engine release:

- [Godot scene organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html): scene dependencies and relationships.
- [Godot thread-safe APIs](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html): active scene-tree access is not generally thread-safe; use supported handoff mechanisms and verify resource sharing.
- [Godot quit and pause handling](https://docs.godotengine.org/en/stable/tutorials/inputs/handling_quit_requests.html): mobile termination can occur while backgrounded.

The lifecycle/ownership contracts here are original engineering guidance. They
are not a tested native plugin or guarantees supplied by those documentation pages.
