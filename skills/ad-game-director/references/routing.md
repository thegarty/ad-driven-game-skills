# Route by the player's or team's problem

These are optional peer skills. A selected specialist remains independently
usable, and a missing specialist does not require installing the entire library.

| Request or bottleneck | Skill to load first | Concrete result |
|---|---|---|
| New concept, unclear fun or repeated choices | `game-concept-and-loops` | Concept comparison and loop specification |
| Need a playable learning build | `game-prototyping` | Bounded vertical slice and playtest questions |
| Players cannot understand/control the game | `game-feel-and-onboarding` | First-session journey and interaction changes |
| Progress stalls, rewards inflate or upgrades dominate | `game-progression-and-economy` | Sources/sinks model and strategy comparisons |
| People stop returning | `game-retention-and-liveops` | Cohort diagnosis and sustainable intervention |
| Inconsistent assets or content bottleneck | `game-art-audio-and-content` | Production brief, asset pipeline and budgets |
| Which ads, where, how often, what reward | `game-ad-monetization` | Placement matrix and test hypotheses |
| Ads fail, rewards repeat or consent changes break state | `game-ad-integration` | Integration contract, implementation and failure tests |
| Provider ready but delivery/revenue weak | `game-ad-operations` | Request-to-revenue diagnosis and verified account gates |
| Audience, consent, data or platform policy question | `game-privacy-and-platform-policy` | Current requirements and implementation implications |
| Untrustworthy metrics or unclear experiment | `game-analytics-and-experiments` | Event ownership, population definitions and experiment plan |
| Need a safe mobile release | `game-quality-and-release` | Tested build, release evidence and rollback criteria |
| Downloads/install footprint grow, memory spikes or asset/SDK bloat | `game-size-and-performance` | Measured size budget and compression/removal changes |
| Need more suitable players | `game-growth-and-acquisition` | Store/creative tests and acquisition measurement |
| Which investment is worthwhile | `game-profitability-and-priorities` | Horizon-specific economics and prioritised next work |
| Look/feel, HUDs, menus and screen layouts | `game-ui-and-navigation` | Screen/state map, visual specification and task checks |
| Long modals, unclear text or visual teaching | `game-ux-writing-and-instructions` | Brief contextual copy, storyboard and comprehension test |
| Need direct evidence from players | `game-playtesting-and-research` | Research protocol, observations and bounded conclusions |
| Levels/waves are confusing or infeasible | `game-level-design-and-difficulty` | Feasible content, difficulty diagnosis and validation |
| Language, ability or input barriers | `game-accessibility-and-localization` | Inclusive interaction and localisation test matrix |
| Gradual feature depth and early earned success | `game-progression-and-economy` | Readiness-based unlock sequence and visible progress |
| Missions, daily goals or event objectives | `game-quests-and-objectives` | Quest definitions, progress lifecycle and durable claims |
| When and how to ask players | `game-prompts-and-permissions` | Context, eligibility, prompt budget, decline and recurrence |
| Useful reminders and return messages | `game-notifications-and-messaging` | Trigger/copy/cancellation plan and holdout test |
| Apple/Google leaderboards and achievements | `game-platform-services` | Capability/identity map, native adapters and verification |
| Scenes/services or asynchronous ownership are tangled | `game-systems-architecture` | State, lifetime and command contracts |
| Saves lost, migrations unsafe or devices disagree | `game-save-and-cloud-sync` | Recovery, conflict and account-linking rules |
| Away earnings or clocks behave incorrectly | `game-offline-and-time` | Time authority, cap/boost policy and interval scenarios |
| Need tuning/content changes without breaking old clients | `game-remote-config-and-delivery` | Schema, staged activation and rollback |
| Pending/duplicate/refunded purchases or restore failure | `game-iap-and-entitlements` | Verified entitlement and recovery lifecycle |
| Score/currency/reward trust or replay abuse | `game-security-and-integrity` | Authority map and bounded abuse/failure tests |
| Production crashes, save faults or provider incidents | `game-observability-and-incidents` | Build-specific diagnosis and mitigation |
| Player complaints, lost progress or review feedback | `game-player-support-and-reviews` | Triage, recovery and recurring-issue evidence |

Typical sequences are concept → prototype → first-session review; measurement
→ retention/economy diagnosis → experiment; or ad integration → native QA →
provider readiness. Select the sequence from evidence, not a fixed ritual.

For engagement requests, inspect the journey before adding systems. A clearer
menu, useful short hint or early earned upgrade may be the right test; a quest,
notification, leaderboard or new SDK is not automatically needed. Build visuals
where they explain the decision, and keep examples distinct from observations.

Buying advertising to acquire players and showing advertising to earn revenue
are different systems. Connect them through cohort economics and attribution;
do not conflate acquisition clicks with in-game ad impressions.
