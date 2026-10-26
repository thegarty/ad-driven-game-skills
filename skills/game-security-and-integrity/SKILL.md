---
name: game-security-and-integrity
description: Protect mobile-game progress, account data, rewards, purchases and competitive outcomes through explicit authority, validation and replay protection. Use for defensive game-integrity reviews, Firebase access rules, attestation rollout or abuse recovery without treating every solo game as a server-authoritative economy.
license: MIT
---

# Game security and integrity

Protect the resources the game actually exposes. Inspect accounts, saves, cloud services, purchases, ads, leaderboards, remote content and native dependencies. Trace a legitimate upgrade, reward and account read through the client and any backend. Identify observed weaknesses and plausible failure paths before adding an anti-cheat service or another SDK.

## Establish proportionate authority

Use the [trust map](assets/trust-map.md) and [authority recipe](references/authority-and-abuse.md). A local solo game can accept that players control their own device and protect progress mainly against accidental corruption. Shared currency, competitive scores and server-owned entitlements require different validation. State the chosen trust model and remaining limits.

For a backend action, derive the owner from verified authentication/session context. A submitted account ID, local save flag or attestation token is not permission to access that account. Check object ownership, operation eligibility and field-level authority independently. Calculate authoritative prices, rewards and transitions from trusted rules; do not accept a replacement wallet or client-selected entitlement as fact.

Give retryable economic operations stable identities. Validate provider purchases and rewarded-ad verification using their current official flows, then deduplicate the external transaction and internal claim in one coherent grant. Repeated client callbacks, server notifications and reconciliation must converge on the same result. An authenticated request can still be a replay or an impossible game action.

## Apply the controls at the actual boundary

- For Firebase, inspect the selected product's Security Rules, privileged service credentials and direct client access. Authentication alone must not let any signed-in player edit every profile. Owner-only access alone must not let an owner mint server-authoritative currency.
- Use App Check, Play Integrity or App Attest as complementary authenticity/risk signals where justified. They do not replace authentication, authorization or economic validation and do not guarantee the absence of cheating. Verify platform/plugin support and server-side verification requirements before adding calls.
- Treat downloadable content, cloud saves and callback payloads as bounded input. Validate types, sizes, paths, versions and allowed transitions before allocation or mutation. A checksum detects changed bytes against a trusted expectation; local encryption or a client-held key does not make local claims authoritative.
- Keep service credentials, signing secrets and admin tokens out of the app, public repository, remote config and logs. Use supported secure storage for legitimate device credentials, least-privilege server access and an explicit rotation/revocation procedure.

## Operate fairly and verify

Separate invalid signatures or unauthorized writes from network errors, provider outages and unsupported devices. Define pending/retry or limited-feature behavior for uncertain states while preserving legitimate progress and confirmed purchases. Do not permanently ban or erase a player from a single unavailable signal. Observe enforcement before broad rollout, provide useful recovery and monitor false positives alongside prevented abuse.

Test with synthetic accounts and isolated environments: cross-account access, changed owner fields, forged balances, duplicate/concurrent grants, expired sessions, malformed content and attestation failures. Confirm both rejection of unauthorized requests and success of legitimate ones. Use [current sources](references/sources.md) for provider specifics; no cryptographic verifier or backend is bundled here.

Return the trust map, concrete changes, negative and positive test results, rollout/recovery policy and remaining risk. Distinguish source inspection, local rule tests, provider/device tests and production observations; never call an untested architecture secure or tamper-proof.
