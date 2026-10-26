---
name: game-ad-operations
description: Diagnose live mobile-game ad readiness, requests, match and show rates, app-ads.txt, mediation and revenue reporting. Use for provider operations and delivery problems after identifying the actual app and build.
license: MIT
---

# Game ad operations

Separate provider configuration, installed implementation and observed delivery. Begin with a read-only baseline of the exact platform/app, store listing, build, provider app/ad units, date range, time zone and currency. Use connected tools if available; otherwise ask for a scoped export or use the authorized console. Do not treat old screenshots or development notes as current provider state.

## Locate the failure

Trace the funnel in order using the [diagnostic guide](references/diagnostic-guide.md):

1. **Eligible opportunities:** does the game reach a valid placement, and is the user permitted to request ads?
2. **Requests:** does the packaged SDK actually request the intended format/unit on the intended platform?
3. **Matched requests:** is there eligible demand, subject to geography, consent, policy, floors and mediation?
4. **Shown impressions:** are loaded ads presented at the right time, or lost to expiry, lifecycle or callback errors?
5. **Revenue records:** are events, currencies, precision and reporting windows reconciled correctly?

Record actual provider definitions before calculating rates. The denominator for show rate may be matched requests; it is not automatically all requests. Empty, delayed, unavailable and zero are different observations.

## Check readiness and supply

- Read current account/app approval and serving-limit statuses, policy issues and store linkage. A store approval does not prove full ad serving, and a test-ad response does not prove live demand.
- Verify the public developer-domain relationship, root app-ads.txt content and provider crawl/verification status. Use the publisher's current authorized seller lines; do not invent identifiers or copy another app's entries.
- Check actual packaged SDK/adapter versions, ad-unit/format mapping and whether expected impression-level revenue reporting is enabled and implemented.
- Segment by platform, country, app version, ad format and source where sample sizes permit. Aggregate eCPM can change solely because traffic mix changed.

## Make a bounded change

Recommend the smallest intervention supported by the baseline: fix an integration mismatch, resolve a readiness prerequisite, recover a show opportunity, or test a floor/mediation change. New mediation adds SDK size, startup cost, privacy obligations and operational dependencies; it is not a guaranteed improvement.

For authorized provider changes, record the original setting, affected apps/versions, exact change and rollback. Account-level privacy or demand settings may affect older installed builds too. Re-read the setting after mutation and verify outcomes after the provider's processing window. Do not invent a universal wait interval or promise a revenue lift.

For new demand or inconsistent dashboards, use [mediation onboarding and funnel reconciliation](references/mediation-and-reconciliation.md). It includes a worked eCPM-versus-delivery example, SDK size/performance costs, source fan-out denominators and a [source onboarding record](assets/mediation-onboarding.md).

Use [the operations record](assets/operations-record.md) to return evidence, diagnosis, actions, verification and remaining unknowns. Read [sources](references/sources.md) for current Google procedures and [the Overgrowth lesson](references/overgrowth-lesson.md) for evidence boundaries.
