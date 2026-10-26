# Delivery diagnosis and optimisation

## Read the funnel before tuning yield

| Observation | First checks | Avoid concluding |
|---|---|---|
| No requests | Eligible gameplay, consent gate, platform adapter, exported build, unit mapping, network | No advertiser demand |
| Requests but few matches | Readiness/limits, provider errors, geography, audience restrictions, format, floors, adapters | More placements will solve demand |
| Matches but few impressions | Stale/expired ad objects, scene changes, missed transitions, presentation failures | The network's bid prices caused the loss |
| Impressions but missing revenue events | Revenue integration, event ownership, delay, linking, precision, reporting population | The impressions earned exactly zero |
| eCPM rises but total revenue falls | Requests, filled impressions, active users, exposure, mix and cohort age | Higher eCPM means a winning change |

Use provider request IDs and sanitized error codes where supported. Avoid logging raw consent strings or advertising identifiers to broad analytics. Reproduce integration problems with test ads; never click live ads to test payment or attribution.

## Store and app-ads.txt chain

Confirm the actual public store entry points to the publisher's developer website, that the expected root app-ads.txt is accessible with correct text content, and that the provider shows it crawled/verified. A successful HTTP fetch is one gate; provider verification is another. Check redirects, robots restrictions, caching and the selected host against current provider guidance. Keep existing authorized sellers when updating a multi-network file.

AdMob [readiness guidance](https://support.google.com/admob/answer/10564477) describes publication, supported-store linkage and review as conditions for full serving. Its [app-ads.txt guide](https://support.google.com/admob/answer/9363762) explains discovery through the store's developer website. Record live status instead of assuming those conditions completed with a successful source build.

## Mediation and floors

Establish a baseline with compatible cohorts before introducing a source. Record bidding/waterfall configuration, supported countries/formats, SDK compatibility, test results, consent handling and revenue ownership. Follow each selected provider's own maintained integration guide; this library does not prescribe a universal waterfall or network ranking.

A higher floor can reduce matches and total revenue. Measure served impressions and revenue per eligible player alongside eCPM. A source with attractive yield can also introduce latency or failures. Compare performance and player outcomes, and define rollback criteria before rollout.

## Revenue reconciliation

Record provider estimated earnings, finalized earnings where available, impression-level paid values and game analytics separately. Normalise currency and time zones deliberately; preserve the original values and any conversion date/rate. Report provider adjustments and data latency rather than forcing reports to agree through undocumented multipliers.

If a mediation callback and Firebase automatic event both represent the same impression, pick one reporting path or a clearly defined deduplication process. Ad revenue, purchase gross revenue, purchase net proceeds and acquisition spend have different definitions. Do not subtract store commission from an ad-revenue value without evidence that the fee applies.

## Deliverable

Provide a prioritized diagnosis with evidence confidence, expected mechanism, affected population, cost/complexity and next observation. For sparse traffic, prefer fixing clear correctness issues and collecting adequate evidence over “optimizing” noise. Do not extrapolate a small launch sample to a sustainable CPI.
