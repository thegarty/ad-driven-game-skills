# Server verification, reconciliation and mediation

## Choose the reward authority

Server verification adds infrastructure and delayed/repeated delivery states. Use it when the game's account economy or fraud exposure justifies that cost. A local-only game still needs durable idempotent grants; adding a webhook without a coherent ledger does not supply them.

Write down one of these contracts before implementation:

| Contract | Client earned callback | Verified server notification | Player experience |
|---|---|---|---|
| Local authority with server audit | Grants once to local durable claim | Reconciles/audits the same claim; never independently grants | Immediate local reward; stated local trust limitations |
| Server authority, pending UI | Creates pending claim; no authoritative spendable credit | Atomically grants once on server; client fetches state | Clear pending status and recovery if delayed |
| Server authority, provisional credit | Grants a documented provisional benefit associated with the same claim | Confirms/reconciles that claim, with a predefined failure policy | Product explicitly handles unavailable verification and any already-spent provisional credit |

The third option has substantial economy and support costs. Do not implement it by adding the reward once on each callback or silently removing a spent benefit later. Decide what happens offline before advertising the offer.

## Shared identity and settlement

Create a server-bound claim before presentation where server authority requires it. Bind the opaque claim to the account, intended ad placement/unit, immutable promised benefit, eligibility and lifetime. If a provider's custom data mechanism is used, verify the actual SDK/plugin supports it and do not include personal information or secrets. A verified provider signature authenticates what the provider returned; it does not make arbitrary client-supplied reward amounts authoritative.

On the server, verify the provider request using its documented algorithm and maintained cryptographic tooling. Preserve the signed representation and handle official key rotation; do not hand-roll signature verification. Then validate the expected application/ad unit, transaction identity and claim/account binding before settlement. Apply a replay/delay policy consistent with legitimate callbacks rather than treating any late notification as fraud.

Use provider transaction identity and internal claim identity as separate uniqueness constraints. A transaction must not fund two claims; a claim must not grant twice when the client callback, provider retry and reconciliation request race. In one real database transaction, record the verified event, apply the intended reward and mark the claim settled. Resolve a duplicate by returning the existing outcome. Follow the provider's documented acknowledgement and retry contract; acknowledging receipt and completing the economic transaction are distinct decisions that need a durable queue if separated.

Client reconciliation reads the authoritative claim outcome and associated state revision. Reconnect, scene changes and app restarts must converge on the same result. A signed-out or switched account must not receive the prior account's claim in the current wallet; retain the proper account-scoped pending record under the chosen data policy. Closing a scene or timing out a UI must not erase an earned obligation.

## Native and mediated failures

For each mediated source, record SDK/adapter versions, required settings, initialization state, privacy support and observed callback order. Test every configured source with its supported test tools where possible. One successful Google-served test ad does not exercise the other adapters.

| Failure | Required behavior |
|---|---|
| Late load from old consent/account generation | Discard stale ad; cannot restore eligibility |
| Activity/view controller recreated between load and show | Validate current presentation context; recover without consuming an unshown opportunity |
| Show fails after reservation | Release only that presentation reservation under the opportunity rules; no reward without earn evidence |
| Close precedes valid earn | Presentation identity survives UI close; reward routes to original claim |
| Plugin registers duplicate listeners after scene reload | One owner; duplicate callbacks still settle once |
| Bridge payload is malformed or wrong type | Reject with bounded diagnostics; never default to successful earning |
| Server notification precedes client callback | Client recognizes already settled claim; no second grant |
| Verification service unavailable | Explicit pending/local-policy outcome; game remains usable |

Keep minimal structured diagnostics for phase, attempt, SDK/adapter version and error category. Do not publish raw callback URLs, account identifiers or unrestricted device logs. Paid-impression revenue events have their own deduplication identity and owner; an earned reward is not proof of an impression's final revenue.

## Official references and evidence limits

Checked **2026-10-26**:

- [AdMob server-side verification](https://developers.google.com/admob/android/ssv) documents signed callbacks, transaction identity, supported verification tooling and a provider testing tool. Use the current platform-specific setup and original signed bytes.
- [AdMob rewarded ads](https://developers.google.com/admob/android/rewarded) currently includes the legacy Android SDK example, its main-thread requirement and mediation-dependent callback ordering. Select the documented SDK family matching the installed native plugin.

The authority choices and ledger protocol above are original design guidance. No backend, cryptographic verifier, mediated source or physical-device playback is bundled or validated by this reference. Use synthetic state tests first, then provider verification tests and physical-device test ads before making delivery claims.
