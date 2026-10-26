# Firebase telemetry ownership

Define the event contract before adding callbacks. Google documents [AdMob ad-revenue measurement through Firebase](https://firebase.google.com/docs/analytics/measure-ad-revenue). For the actual linked SDK configuration, establish whether `ad_impression` is automatic before emitting a manual equivalent. Multiple listeners can make the same impression look like two revenues.

An illustrative ownership table:

| Event class | Owner | Purpose |
|---|---|---|
| SDK lifecycle and supported automatic ad revenue | Configured native SDK integration | SDK-managed observations |
| Offer visible and offer selected | Game UI, after real visibility/input | Player exposure and choice |
| Load requested/result, show requested/result | Ad broker/adapter | Delivery diagnostics |
| Reward earned | Presentation callback router | Provider earned event |
| Reward granted | Durable reward store, after commit | Actual game fulfilment |

Use stable placement IDs and bounded parameters for format, progression band, outcome and experiment variant. Keep native provider errors in an appropriately restricted diagnostic channel; avoid passing arbitrary error strings, advertising IDs or personal data into game analytics.

Specify the join key and deduplication owner for each event. Do not use timestamps alone as identity. The funnel may branch or arrive out of order: keep eligibility, load, presentation and reward counts distinct instead of forcing every callback into a single chronological pipeline.

Ad reporting and analytics may have different time zones, currencies, processing delays, consent populations and revenue precision. Reconcile them explicitly. Do not infer all-player retention from the measurable opt-in population, or treat a missing dashboard metric as measured zero.

Consent eligibility for gameplay analytics, advertising measurement, ad storage, personalized ads and platform tracking can differ. Use the actual configured privacy controller and SDK documentation. See [Firebase collection configuration](https://firebase.google.com/docs/analytics/configure-data-collection); the existence of a provider consent dialog is not evidence that every Firebase purpose is authorized.

Verified source links: **2026-10-26**. Recheck automatic-event behaviour and consent APIs for the chosen integration before implementation.
