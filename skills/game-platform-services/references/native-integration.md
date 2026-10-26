# Godot adapter, account changes and release proof

This is an original implementation workflow. Official native references and their **2026-10-26** verification date are in the [capability map](platform-capabilities.md). All interface/state names below belong to the proposed application design; they are not invented Godot SDK methods.

## Discover before binding

Inspect Godot version, addon/plugin source, Android Gradle/export dependencies, iOS Xcode/export settings and release artifact contents. List each actual method/signal, argument type, callback meaning, threading/lifecycle requirement, native SDK version and OS availability. Do not infer support for current challenges or incremental achievement state from a plugin merely advertising “Game Center support.”

For Android use the current PGS v2 integration path and verify required application/OAuth/signing configuration for the exact distributed variant. For Apple verify Game Center capability, correct bundle/configuration, resource IDs and available native UI. Keep real identifiers and credentials out of public templates.

Measure the marginal download/installed size and launch/memory change of the native addition using comparable builds. Include only required libraries and resources; strip unused debug material from player packages while preserving private symbols. Prefer a narrow maintained bridge over an unrelated all-service SDK bundle when it satisfies the tested requirements.

## Application boundary

| State or operation | Contract |
|---|---|
| Native profile availability | Platform identity plus authentication/availability, separate from game account and purchase account |
| Show leaderboard/achievements | User intent, supported native UI, safe return/cancel and unavailable explanation |
| Submit run result | Validated completed-run identity, score contract version, board/occurrence, native profile and delivery status |
| Publish achievement progress | Gameplay-derived target/state, native achievement mapping, profile and repeat cycle if relevant |
| Reconcile pending work | Respect account binding, supported provider retry semantics, source state and limits |
| Challenge/platform reward capability | Explicit supported/unsupported/eligibility-unknown result; ordinary play remains available |

Keep one long-lived service and marshal callbacks safely to the game thread. Scene changes must not attach duplicate reporters. Coordinate native authentication/leaderboard UI with ads, store sheets and permission prompts. Follow each platform's documented automatic/authentication UX instead of inventing repeated manual login popups. A cancelled or unavailable platform service should leave unrelated gameplay usable.

## Identity changes

Store pending intent under its intended game account and native profile. On any authentication change, suspend mismatched pending work, refresh native state, then apply the project's explicit relinking policy. Never send profile A's pending score or achievement to profile B just because B is now signed in. Do not reset the local save or mint a second quest reward during relinking.

If a backend owns competitive scores, verify platform authentication using the current platform-supported server flow and keep credentials server-side. Profile names/avatars are presentation data, not authorization. Native service identity alone cannot decide ownership of an unrelated in-game account, wallet or store transaction.

## Test and release matrix

Use native test configuration/accounts and packaged devices. Test clean install, returning profile, profile creation/unavailable/declined state, guest progress, profile switch, offline play/reconnect, app kill during submission, repeated scene entry, invalid resource IDs, service error/rate limiting, lower supported OS and native UI close/back. Include the release signing and optimization configuration, because debug-only success can hide credential/export defects.

Apple's current configuration workflow includes local GameKit testing; local test state is not proof that reviewed components are live. Google's [test/publish workflow](https://developer.android.com/games/pgs/console/publish) requires appropriate test access for unpublished services and separate publication of game-service changes. Record component visibility, build distribution and representative live readback separately.

Native UI can omit a public score because of privacy, eligibility, filtering, delayed sync or configuration. Distinguish queued, accepted and visible states using what the actual API proves. Never claim the service uploaded a score merely because an application signal fired. Store source-inspected, device-tested and measured-live evidence in the [services matrix](../assets/platform-services-matrix.md).
