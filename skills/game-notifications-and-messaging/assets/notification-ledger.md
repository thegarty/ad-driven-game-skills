# Notification policy and ledger

- Game/build/engine/plugin/native SDK versions:
- Audience, markets and authorization requirements:
- Reason and actual player benefit:
- Local/server authority; offline/cross-device limits:
- Policy version and owner; integrated channels/senders:
- Quiet hours, timezone source, travel and DST rules:
- Global rolling cap, category caps, cooldown and reason for each:
- Holdout/assignment unit, meaningful-return action and observation horizon:
- Stop/reduce criteria for fatigue, opt-outs and other guardrails:

| Trigger/reason ID | Generation | Category/preference | Earliest useful time | Expiry | Completion/cancel condition | Title/body keys | Destination and fallback |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Keep the following in the production ledger as needed; use synthetic IDs in
fixtures and documentation. Do not copy raw tokens or private player identifiers.

| Field | Meaning and handling |
|---|---|
| Subject reference / scope | Pseudonymous player or installation reference; account vs device guarantee |
| Message ID / reason ID / generation | Stable deduplication and cancellation identity |
| Policy / copy / payload version | Reproducible decision and compatible open route |
| Preference / authorization / state revision | Decision inputs with freshness timestamp |
| Timezone / earliest / due / expires | UTC instants plus timezone-aware scheduling intent |
| Reservation / cap window | Atomic ownership of a contact slot and cooldown |
| Provider request reference | Reference held securely for reconciliation; not exposed raw in reports |
| State / decision reason | Planned, reserved, scheduled/submitted, unknown, failed, cancelled, expired |
| Attempt / accepted / observed delivery / open | Separate timestamps and evidence provenance |
| Meaningful action / observation maturity | Defined outcome, elapsed horizon and missingness |
| Retention/deletion policy | Minimum necessary fields, authorised access and cleanup |

- Concurrent-sender and unknown-outcome handling:
- Claim/activity/sign-out/reset cancellation and badge cleanup:
- Payload validation, authentication and expired-event route:
- Test fixtures, packaged/device observations and limitations:
- Actual experiment population/results/uncertainty; no-message comparison:
