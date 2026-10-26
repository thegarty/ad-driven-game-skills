# Capability and output map

Choose skills by the next decision, not by loading the whole library. The
[catalogue](../CATALOG.md) lists every standalone entry; installation
[profiles](../profiles.json) are additive conveniences, not dependencies.

| Work | Primary skills | Reviewable output / verification |
|---|---|---|
| Concept to first enjoyable action | concept, prototyping, feel, playtesting | Small playable loop, observable learning questions and test record |
| Look, menus and layouts | UI/navigation, art/audio, accessibility/localisation | Annotated screens, reusable tokens, real-device task checks |
| Short instructions and visual teaching | UX writing, UI, playtesting | Copy inventory, show/try/feedback storyboard, unassisted comprehension |
| Gradual depth and progress | progression, level design, quests | Readiness-based unlock schedule, feasible content, durable quest claims |
| Ads and optional purchases | ad monetisation/integration/operations, IAP | Explicit offers, native adapter contracts, receipt/reward recovery |
| Smart asks and reminders | prompts/permissions, notifications, retention | Eligibility and suppression rules, concise copy, holdout evaluation |
| Native player features | platform services, security, saves | Apple/Google capability map, identity and score/achievement reconciliation |
| Durable game systems | architecture, save/cloud, offline/time, remote config | Ownership contracts, migration/conflict policies and failure cases |
| Lean reliable releases | size/performance, quality/release, observability | Artifact budget, device profiling, rollout/incident evidence |
| Evidence and commercial decisions | analytics, growth, profitability | Cohorts, experiment readout, soft-launch gates and sensitivity ranges |
| Player trust | privacy/policy, support/reviews, accessibility, security | Current audience/data rules, fair recovery, accessible choices |

Names above are abbreviated for readability; use exact names in the catalogue.

## Runnable local helpers

All use Python 3.9+ and the standard library. Each lives inside its independently
copyable skill with input documentation and examples.

| Helper | Answers | Does not establish |
|---|---|---|
| `economy_scenario.py` | Fixed-assumption earnings/spends and milestones | Adaptive player strategy or an optimal economy |
| `cohort_retention.py` | Exact-day retention with mature install denominators | Causal reasons for return or missing-player behaviour |
| `revenue_sensitivity.py` | Revenue/cost/CPI scenarios over an explicit horizon | Unobserved lifetime value or a spend recommendation |
| `artifact_size.py` | Local artifacts, largest files and selected byte budgets | Store-produced download/installed size or RAM |
| `offline_accrual.py` | Proposed interval settlement with caps/boosts/dedup | Actual durable grants, trusted clocks or cloud authority |
| `experiment_readout.py` | Assigned-unit descriptive comparison and bootstrap uncertainty | Valid randomisation, absence of bias or permission to stop early |
| `contrast_check.py` | Opaque sRGB colour-pair contrast | Complete native accessibility or actual device legibility |

The [validation record](validation.md) distinguishes automated checks, independent
scenario evaluations, generated illustrations and client smoke tests.

## Scope boundaries

This release covers mobile ad-funded games, with optional purchases. Engine
principles are portable; Godot recipes are contracts and implementation steps
that require checking the installed plugin/native SDK, not a bundled production
adapter. Native Game Center/Play Games features require actual account, build
and device verification. Complex real-time multiplayer, matchmaking, player
trading, user-generated-content moderation and jurisdiction-specific legal
opinions need additional specialist work. The library identifies those boundaries
rather than pretending a general checklist implements them.

Comprehensiveness means a useful path through common design, build and operation
decisions, with recoverable failure states and evidence limits. It does not mean
every game should ship every system, every SDK or every visual asset.
