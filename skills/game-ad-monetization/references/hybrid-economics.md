# Ads and purchases in the same economy

This is an original decision framework. The numeric examples are **synthetic projections**, not observed results, price recommendations or universal benchmarks. Use the [purchase contract](purchases-and-entitlements.md) before testing an offer.

## Make the product executable

| Promise | Forced interruptions | Voluntary reward offers | Required implementation |
|---|---|---|---|
| Remove forced ads | Removed for eligible entitlement | May remain with clear advance disclosure | All forced placement checks use the same entitlement, including restored users |
| All ads removed | Removed | No advertising remains under that promise | Define whether rewards are claimable, replaced or absent; communicate before purchase |
| Claim rewards without watching | Removed if included in the product | Non-ad claims under explicit limits | Stable claim keys, eligibility and durable grants without fabricated ad events |
| Cosmetic/supporter pack | Whatever the store promise specifies | Whatever the store promise specifies | No implied ad removal or undisclosed repeat benefit |

Do not advertise “all ads removed” while keeping voluntary ad offers. Resolve the promise or product implementation before launch. Paid players still need a coherent progression route: removing reward access can make an apparent benefit harmful; unlimited ad-free rewards can collapse sinks. Test no ads/no purchases, ordinary ad participation, maximum legal ad participation and every paid entitlement.

If the mismatch is already live, honour existing purchasers' promised rights.
Changing wording for future sales does not narrow the entitlement already sold.
Version the product/entitlement contract and test restored legacy purchasers as
well as new buyers; keep any agreed remediation explicit and recoverable.

## Measure total contribution at one horizon

For the same eligible assigned population and horizon H:

`contribution_H = publisher_ad_revenue_H + net_IAP_proceeds_H - variable_service_and_support_cost_H - acquisition_cost`

Specify currency, reporting completeness, refunds/taxes/fees already deducted, costs included and fixed costs excluded. Do not subtract store fees twice from net proceeds. Do not add purchase price to an ad-LTV forecast that still assumes the buyer watches all displaced ads. Subscription renewal projections need stated renewal/churn assumptions and benefits/costs over the same horizon.

Compare offers using stable assignment before purchase, not purchasers versus nonpurchasers. Purchasing players select themselves and may have different engagement even without the offer. A buyer's lost ad revenue is a useful mechanism estimate; it does not identify the causal effect of selling the offer to everyone.

## Synthetic 30-day sensitivity

All numbers below are projected USD per acquired player over 30 days, with identical assumed CPI of USD 0.30. They are arithmetic scenarios, not an experiment.

| Component | Baseline assumption | Offer assumption |
|---|---|---|
| Publisher ad revenue | 0.42 | 0.34 |
| Net purchase proceeds | 0.08 | 0.20 |
| Variable service/support cost | 0.03 | 0.04 |
| Contribution before acquisition | 0.47 | 0.50 |
| Contribution after acquisition | 0.17 | 0.20 |

Projected improvement is USD 0.03 per acquired player, although purchase proceeds rise USD 0.12. The difference reflects displaced ads and costs. If offer purchase proceeds are only USD 0.15 with other assumptions unchanged, contribution after acquisition is USD 0.15, below baseline. Sensitize conversion, retained active days, refunds, displaced formats, reward issuance and support cost together; these quantities can move with the product.

## Test and reconcile

Predeclare the primary total-value metric and mature horizon, retention and failed-entitlement guardrails. Inspect refund/revocation, restore completion, unwanted forced-ad exposure among entitled users and reward claims by progression stage. Revenue recorded before an unresolved refund window is provisional; later reconciliation may change the result.

Keep three ledgers: verified purchase transactions, earned/claimed game benefits and publisher ad earnings. One purchase can unlock many future claims; those claims are not new purchases. A paid no-ad claim generates a reward event but no ad impression/revenue event. Retain immutable transaction/claim identities and never double-report auto-collected purchase events with custom revenue events.

Return the exact player-facing promise, entitlement table, free/paid economy scenarios, observed-versus-projected contribution model, instrumentation ownership and bounded experiment proposal. Check current billing/product rules using the skill's [official sources](sources.md).
