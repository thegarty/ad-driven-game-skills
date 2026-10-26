# Measurement recipes

## Godot → native SDK → export

Keep gameplay event intent behind a small analytics adapter. Pass bounded dictionaries with documented names/types; native bridges translate into the selected SDK API. Detect the real bridge capabilities and normalise returned types rather than assuming desktop mock behaviour matches Android/iOS.

Test the same event with collection permitted, denied and changed at runtime. Collection settings must follow the project's native consent authority, independently of gameplay save restoration. Use development destinations and synthetic identities. Inspect the export for schema, currency units, timestamp, build and duplicate counts before marking instrumentation complete.

Firebase documents automatic AdMob revenue measurement when the required app integration/linking is established. Verify that path before manually logging `ad_impression`; a second owner can duplicate revenue. Other mediation paths may require explicit impression-revenue logging. See [Firebase revenue measurement](https://firebase.google.com/docs/analytics/measure-ad-revenue), verified 2026-10-26.

Map economy transactions to the SDK's supported events only after inspecting current parameters. Keep source/sink reasons bounded and distinguish an offered reward from a committed grant. See [GA4 recommended events](https://developers.google.com/analytics/devguides/collection/ga4/reference/events), verified 2026-10-26.

## Remote configuration experiments

Expose an allowlisted, versioned configuration with safe local defaults. Record the configuration actually activated for the session. Update at a suitable transition; do not change difficulty or reward promises midway through an active offer. Keep a revert path that does not invalidate earned entitlements.

Firebase supports an activation event to restrict results to exposed users; fetched values still reach targeted users outside that reporting subset. Verify activation timing and current console requirements before starting an experiment. See [Firebase Remote Config experiments](https://firebase.google.com/docs/ab-testing/abtest-config), verified 2026-10-26.

## Overgrowth-derived example

**Evidence: source-inspected, with separate source-tested callback paths in the 25 October 2026 review.** Started/completed reward events left uncertainty about losses before playback. The reusable lesson is to instrument offer visibility, selection and request outcomes, while maintaining one revenue-event owner. This observation did not prove a production telemetry failure or a retention/revenue uplift. Use synthetic fixtures when recreating the scenario.

## Before trusting a result

Reconcile SDK and provider dates, reporting timezone, estimated versus final revenue, currency conversions, consent coverage and ad-format scope. An unavailable console or a not-yet-processed postback is not a zero. Preserve those states in reports rather than coercing them into numeric inputs.
