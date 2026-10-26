# Mediation onboarding and funnel reconciliation

Official SDK sources checked **2026-10-26**. Select the actual native platform and SDK family in the documentation: current AdMob pages distinguish Android next-generation and legacy SDKs. Do not mix initialization or callback recipes between them.

## Add demand as a bounded hypothesis

Start with an observed gap: eligible geography/format has insufficient matches, existing demand is concentrated, or a supported source might improve total delivered value. Adding every available network increases operating burden without establishing incremental revenue. Recover broken requests/presentation first.

For each candidate, complete the [source onboarding record](../assets/mediation-onboarding.md):

1. Verify account access, app/format support, target markets, audience restrictions, store linkage, commercial eligibility and expected reporting support. Record unknown prerequisites rather than assuming the console entry proves readiness.
2. Inspect the provider's current integration guide, supported adapter/SDK pair, minimum OS, native dependencies, privacy/consent propagation and test mode. Keep secrets and publisher IDs in project configuration, not public examples.
3. Measure incremental download/installed size, launch time, memory and network work using comparable packaged builds. Record a named owner, recurring maintenance and removal route. Shared dependencies mean marginal size must be measured, not estimated by adding download archives.
4. Configure a bounded platform/format/market group, map ad units correctly and verify its effective settings. Record the prior state, eligible installed builds, settings version and rollback. An old app without the adapter cannot be assumed to participate successfully.
5. Test initialization, consent changes, unavailable demand, background/resume, show failure, reward identity and paid-event ownership using test devices. Use [Ad inspector](https://developers.google.com/admob/android/ad-inspector) for adapter/ad-unit/privacy diagnosis where the selected SDK supports it. Test success demonstrates the exercised path, not live fill or commercial lift.
6. Measure comparable live cohorts/traffic with mature windows, reporting completeness and retention/performance guardrails. Retain or remove the source based on incremental contribution and cost, not its isolated eCPM.

Follow [AdMob mediation setup](https://developers.google.com/admob/android/mediation) and each selected network's official adapter guide for initialization and privacy requirements. Review the partner list and actual consent propagation. Changing mediation order or floors cannot fix an adapter absent from the distributed binary.

## Match the metric to the stage

| Stage | Evidence and denominator | Interpretation boundary |
|---|---|---|
| Eligible opportunity | Placement/entitlement/audience-valid game transitions | Not every active player reaches a placement |
| Visible offer and opt-in | Offer shown, then player selection | Hidden offers cannot be diagnosed from completed ads |
| App request | Format/ad-unit request with outcome | Retries and network fan-out can create more provider requests than opportunities |
| Match/load | Provider-defined match and app load result | A server match does not prove a successfully retained ready ad |
| Show/impression | Presentation state and provider-defined impression | A loaded ad may expire or miss the natural transition |
| Earned/committed reward | SDK eligibility callback and durable grant record | Ad revenue and reward ownership are separate events |
| Paid value/reporting | Provider value, precision, currency, source and report date | Estimates and settlement are not interchangeable |

Do not sum every mediation-source request and use that as the app request denominator. Network bidding/waterfall fan-out and fallback can make source-level metrics overlap. Write the provider's current definitions beside every rate before comparing dashboards.

## Synthetic decomposition

Assume one comparable platform/format/day population with 1,000 **app requests**, 800 matched requests, 600 shown impressions and USD 3 publisher revenue. If these provider definitions align, match rate is 80%, show rate per match is 75%, impression rate per app request is 60%, realized eCPM is USD 5 and revenue per app request is USD 0.003.

A hypothetical higher floor yields 500 matches, 400 impressions and USD 2.80 revenue from the same 1,000 requests. Realized eCPM rises to USD 7 while revenue falls. These are synthetic arithmetic scenarios; live comparisons also need traffic mix, latency, eligibility and cohort-value effects. Raising the floor because eCPM rose would ignore lost delivery.

## Reconcile revenue without inventing precision

Maintain one owner for each impression's revenue reporting path. Where the selected SDK provides an identity, preserve it through ingestion/retry. Otherwise define an app-owned presentation/event identity and document its coverage limits; do not use only a timestamp or placement ID as a globally unique impression key. Reward IDs and ad presentation IDs are not interchangeable.

Impression-level data includes monetary value, currency and precision; preserve these attributes and convert units once. Keep unknown value distinct from a genuine zero, and avoid inventing user-level settlement precision from estimated callbacks. Use the selected SDK's [impression-level ad revenue guide](https://developers.google.com/admob/android/impression-level-ad-revenue).

Reconcile source ledgers by platform, build, ad unit/format, date/timezone, currency and source. Compare app paid-event totals, analytics totals and provider reports separately. Account for retries/duplicates, automatic SDK events, missing consent/telemetry, report lag, currency conversion, adjustments and unsupported networks. Reconcile ad impressions independently of reward grants: a reward may legitimately complete later. Record unexplained residuals and next evidence; never spread a residual across users and call it observed revenue.

## Decision record

Return the onboarding record, effective configuration, device proof, funnel counts/definitions, revenue reconciliation and cost/performance deltas. Declare whether a claim is source-inspected, test-device behavior, synthetic arithmetic or measured live. Keep the demand change bounded until its own evidence supports expansion.
