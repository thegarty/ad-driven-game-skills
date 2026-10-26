# Ad lifecycle and durable rewards

This is a provider-independent design contract. Adapt it to actual SDK callbacks and the game's persistence architecture; do not pretend every SDK has these method names.

## State ownership

| Domain | Example states | Owner |
|---|---|---|
| Privacy | refreshing / request permitted / request restricted | Native privacy controller, reconciled with provider |
| SDK | not initialized / initializing / ready / retryable failure | Provider adapter |
| Opportunity | eligible / reserved for presentation / used / expired | Gameplay and durable opportunity record |
| Ad object | empty / loading / ready / showing / consumed | Adapter; one-shot objects follow SDK lifecycle |
| Reward | not earned / pending receipt / durably granted / acknowledged | Durable reward service |

Use separate records rather than one enormous enum. Privacy generations can invalidate load callbacks while a presented opportunity retains its own reward identity.

## Opportunity identity

Create a unique claim ID from the actual run/transaction opportunity, not only the placement name. Snapshot the promised benefit and entitlement conditions before display. Record a separate load-attempt ID or generation; retrying a load must not manufacture an extra reward opportunity.

When showing an ad, capture the immutable claim in the callback closure or native presentation record. A later UI selection cannot change its recipient. Reward type and amount from callbacks should be checked against the intended product contract; never let an arbitrary callback payload select a wallet account.

## Grant transaction

Conceptual pseudocode, **not executable Godot or SDK code**:

```text
on_provider_earned(presentation_id):
    opportunity = lookup_presented_opportunity(presentation_id)
    reject unknown or invalid presentation
    persist_pending_receipt(opportunity.claim_id, opportunity.reward)
    settle_pending(opportunity.claim_id)

settle_pending(claim_id):
    transaction:
        if claim_id not in applied_claims:
            apply the snapshotted reward to the intended game state
            add claim_id to applied_claims
            commit both changes durably as one unit
        else:
            verify the applied marker belongs to the current durable snapshot
    acknowledge local pending receipt after either confirmed durable outcome
```

`transaction` means a real database transaction or an atomic versioned game snapshot containing both the benefit and applied-claim ledger. Two unrelated file writes are insufficient. If commit fails, do not display a confirmed grant or remove the pending receipt. Retry settlement without replaying the ad.

After a crash between grant and acknowledgement, replay finds the claim already applied and safely clears the pending receipt. Restore a compatible ledger with game-state backups; rolling a wallet back independently from its deduplication state can lose or duplicate rewards. Set retention/pruning rules around actual replay windows, not arbitrary deletion on every session.

There is no guarantee of durable recovery if receipt persistence itself fails and the process dies before any recoverable record exists. Expose an honest pending/error state, retain in-memory evidence, and consider server-side verification where the product's value/fraud exposure justifies it. If SSV and client callbacks coexist, define a single entitlement authority and shared idempotency key; do not grant independently on both paths.

Closing or dismissing an ad is not proof of earning. Callback order can differ through mediation: support a valid earn arriving after close. The presentation record must outlive the full-screen UI. A cancelled/unearned ad must not receive the promised reward unless an explicit, separately accounted goodwill policy authorizes it.

## Recovery and privacy

- **Load/init failure:** clear only the failed attempt; retry with bounded backoff while the opportunity remains valid. No permanent session lockout from a transient error.
- **No-fill:** continue the free route; show accurate availability and avoid an infinite retry loop.
- **Consent change:** invalidate cached/load eligibility, increment the load generation and discard stale load results. Re-evaluate before any new presentation. Preserve legitimate pending earned claims.
- **Save recovery:** re-evaluate an unclaimed opportunity from the restored run record, rather than awarding or displaying automatically.
- **Foreground/background:** keep game audio/time behaviour deliberate; resume only when the actual full-screen lifecycle allows it.
- **Expiry during presentation:** fulfil the reward promised by a valid presentation according to its snapshot; do not retroactively change the deal because a menu timer expired.

## Required scenarios

| Sequence | Observable result |
|---|---|
| Ready → Watch → Earn → Earn → Close | One durable reward |
| Ready → Watch → Close → Earn | Valid late reward credited once |
| Earn → save failure → retry settlement | No lost receipt; one grant after successful commit |
| Grant committed → crash before acknowledgement → restart | No duplicate grant; pending receipt cleared |
| Loading → privacy change → old load success | Old ad never becomes eligible for display |
| Showing → privacy withdrawal → valid Earn | No further restricted requests; earned reward retained |
| Init timeout → retry → ready | Valid opportunity returns; ordinary rewarded show needs Watch |
| Start a new run → callback from previous run | Reward follows original immutable claim |
| Restore backup / migrate save | Wallet and claim ledger stay consistent |
