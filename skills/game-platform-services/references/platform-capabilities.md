# Current platform capability map

Official sources checked **2026-10-26**. Availability is conditional on target OS/SDK, account/program eligibility, configuration and the actual engine bridge. This map is documentation-backed; it is not a report that any project's integration has been tested.

| Capability | Apple Game Center / GameKit | Google Play Games Services | Game responsibility |
|---|---|---|---|
| Native profile/authentication | Authenticate the local Game Center player and handle unavailable state | Current PGS v2 platform authentication is distinct from in-game authentication | Preserve game identity, saves, inventory and guest/account transitions separately |
| Leaderboards | Classic and recurring configurations; current GameKit score/reporting APIs | Configured leaderboards with daily, weekly and all-time views | Define comparable metric, valid runs, reset boundary and assisted-play rules |
| Achievements | Configured achievement progress/completion, with current feature options | Standard/incremental achievement operations and native UI | Own gameplay intent, deduplicate events and separate any game reward |
| Friend competition | Current leaderboard-backed challenges; configuration/review/minimum-version requirements | Verify current program/feature support rather than assume GameKit parity | Design fair, eligible modes and fallback UI |
| Platform quests/rewards | Challenges are competitions, not the game's general quest claim ledger | Current Level Up quests/rewards have program and fulfillment requirements | Keep custom daily/weekly quests independent; verify any external reward exactly once |
| Saved progress | A native gaming profile alone does not define the game's conflict/restore policy | PGS is not the primary game inventory/progress identity system | Specify storage authority, account ownership, migration and recovery |

## Apple

Use [Initializing and configuring Game Center](https://developer.apple.com/documentation/gamekit/initializing-and-configuring-game-center) for capability/configuration, local testing and deployment discovery. [Leaderboards](https://developer.apple.com/documentation/gamekit/encourage-progress-and-competition-with-leaderboards) and [recurring leaderboards](https://developer.apple.com/documentation/gamekit/creating-recurring-leaderboards) describe native score and occurrence behavior. [Achievements](https://developer.apple.com/documentation/gamekit/rewarding-players-with-achievements) describe progress and configuration. Verify the symbol availability for the project's supported OS range; a new API in documentation may be absent in its Godot bridge or oldest device.

Current [GameKit challenges](https://developer.apple.com/documentation/gamekit/creating-engaging-challenges-from-leaderboards) use an associated leaderboard. Configuration can declare a minimum game version; players participating in a challenge use the leaderboard's score submissions. [App Store Connect challenge management](https://developer.apple.com/help/app-store-connect/configure-game-center/manage-challenges/) describes review/configuration and distinguishes the legacy deprecated challenges setting. Do not implement a current feature by copying legacy challenge APIs without checking availability.

Choose a mode with comparable attempts. Apple's [leaderboard selection guide](https://developer.apple.com/documentation/gamekit/choosing-a-leaderboard-for-your-challenges) distinguishes repeatable/nonrepeatable challenges and classic/recurring leaderboards. It also describes hidden Game Center leaderboards alongside a custom service. Such mirroring is two delivery paths, not proof of atomic cross-service consistency.

## Google

[Platform authentication](https://developer.android.com/games/pgs/platform-authentication) describes PGS v2's platform layer and the developer-owned in-game account. PGS profile authentication does not automatically back up or restore the game's wallet. Use supported authentication and, where needed, [server-side access](https://developer.android.com/games/pgs/android/server-access) instead of trusting a client-provided player ID as an authentication credential.

The current [PGS overview](https://developer.android.com/games/pgs/overview) describes Level Up program engagement features including quests; eligibility must be verified for the actual title. This does **not** revive the old Quests API. The [2017 official retirement announcement](https://android-developers.googleblog.com/2017/04/focusing-our-google-play-games-services.html) is historical context, not a guide to today's program capabilities. Also check the current SDK migration requirements rather than choosing a PGS v1 plugin from an old tutorial.

[Play Games Rewards](https://developer.android.com/games/rewards) currently describes out-of-app purchase fulfillment for eligible quest rewards, including startup/foreground reconciliation, verification, grant and completion. It also requires resolving the intended in-game identity when several exist, and describes account matching and claim availability. Re-check current eligibility/window rather than promising every player a reward. A platform promotional reward is not automatically a cash purchase or publisher ad impression; its revenue classification must reflect the actual transaction.

Use [leaderboard concepts](https://developer.android.com/games/pgs/leaderboards), [Android achievements](https://developer.android.com/games/pgs/android/achievements), [achievement operation reference](https://developers.google.com/android/reference/com/google/android/gms/games/AchievementsClient), [API usage limits](https://developer.android.com/games/pgs/quota) and [test/publish guidance](https://developer.android.com/games/pgs/console/publish) for current implementation details. Publishing the game binary and publishing native service configuration are separate readiness checks.
