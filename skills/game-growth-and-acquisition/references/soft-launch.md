# Soft launch gates and learning budget

Use a soft launch to resolve defined uncertainties in a real distribution environment. The gates below are an original planning framework, not universal performance thresholds. Set each threshold from the game's economics, audience, baseline variability and available runway.

## Choose a population that answers the question

A low-cost market can help exercise infrastructure but may not represent target languages, devices, payer behavior, ad demand or creative appeal. Record the reason for every market/platform choice and what cannot generalize. Child-directed audiences require their specific product, privacy, advertising and recruitment rules; do not treat them as ordinary acquisition segments.

Declare the learning question, maximum spend/time, permitted campaign changes, build/config, cohort windows and stop conditions before recruiting. Buying volume cannot compensate for broken attribution or unavailable ads. A plan is not authorization to start campaigns; use the user's actual approved scope for live actions.

## Stage gates

| Gate | Question | Minimum decision evidence | If inadequate |
|---|---|---|---|
| Distribution and integrity | Does the intended build run, save and report correctly? | Store/test install proof, startup/first-session completion, native consent/ad/reward/purchase exercises, event ownership, crash symbols | Repair before increasing exposure |
| Product comprehension | Do intended players understand the loop and want another attempt? | Observed play sessions, first-session funnel, failure reasons, return goals, device/accessibility coverage | Change one testable product obstacle; playtest again |
| Return behavior | Do mature cohorts return for understandable reasons? | Defined exact/rolling retention, source/market/build cohorts, complete windows, uncertainty and content exhaustion | Diagnose progression/content/quality and collect missing evidence |
| Monetization integrity | Are willing opportunities delivered and rewards trusted? | Eligible→offer→opt-in→load→show→grant funnel, entitlement correctness, reconciled publisher/IAP revenue | Recover delivery and reporting before adding pressure |
| Unit economics | Is there plausible contribution at an actionable acquisition cost? | Observed value through H, net proceeds/costs, CPI, attribution limits, projected tail sensitivity | Continue bounded learning, revise, or stop; do not call projected LTV measured |
| Expansion readiness | Can operations support a larger population? | Size/performance budgets, incident/rollback plan, support capacity, consent/store declarations, compatibility and content cadence | Fix the limiting dependency before scaling |

Gate evidence can overlap; the table does not require six separate launches. Include the actual ad/purchase experience early enough to evaluate it. A clean prototype with no monetization does not establish retention under the intended commercial experience.

## Decide continue, revise or stop

For each gate write: baseline, practical success condition, minimum maturity/coverage, uncertainty method, maximum learning cost and exact next action. Predeclare the difference between operational harm (stop now), lack of precision (collect until the planned limit), and evidence against a viable concept (revise/stop).

Avoid repeatedly extending an unfavorable test until it becomes favorable. Preserve successful and failed hypotheses. If a change affects several systems, log it as a new build/cohort and separate the effects you cannot identify.

## Synthetic example

A prototype has complete first-session instrumentation and positive observed playtest comprehension, but paid installs are only two days old. D7 retention and 30-day payback are unavailable. Ad delivery testing can continue, and early failures can justify a repair, but neither projected D30 revenue nor a low current CPI establishes scalable acquisition. Keep spending inside the agreed learning ceiling; collect the planned mature cohorts or revise the plan transparently. No universal target or result is implied.

## Current platform references

Checked **2026-10-26**: [Apple product-page optimization](https://developer.apple.com/app-store/product-page-optimization/) and [Play listing experiments](https://play.google.com/console/about/store-listing-experiments/) offer platform-specific store tests. Their conversion and retention definitions/populations are not automatically interchangeable. [Apple attribution](https://developer.apple.com/app-store/ad-attribution/) describes privacy-preserving attribution capabilities; delayed/limited postbacks do not create a complete person-level revenue join. Re-check the actual account, SDK and OS coverage before planning a measurement contract.

Complete the [soft-launch scorecard](../assets/soft-launch-scorecard.md) with observed, projected and unknown values visibly separated.
