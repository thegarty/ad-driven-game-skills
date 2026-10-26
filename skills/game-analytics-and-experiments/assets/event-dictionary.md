# Game event dictionary

Fill this in for the selected project; the example names below are game-level proposals, not guaranteed SDK APIs.

- Decision supported:
- Population and consent eligibility:
- Reporting timezone / collection lag / last complete date:
- Identity and reinstall policy:
- Build and schema version:

| Event or fact | Trigger and owner | Required bounded dimensions | Identity / deduplication | Used for |
|---|---|---|---|---|
| First open / session | Verify automatic SDK ownership | platform, build | documented SDK behaviour | install and active populations |
| Tutorial step | Game: first successful completion | step ID, outcome | one completion per tutorial attempt | onboarding funnel |
| Run end | Game: final persisted outcome | stage ID, outcome, duration bucket | run ID | progression and failure analysis |
| Reward offer shown | Game: eligible offer actually visible | placement, progression bucket | opportunity ID | offer denominator |
| Reward selected | Game: player chooses Watch | placement | opportunity ID | selection conversion |
| Ad load / show outcome | Adapter: callback or explicit terminal timeout | placement, outcome, bounded error class | request and opportunity IDs | supply and presentation loss |
| Reward earned | Adapter: provider earned signal | placement, reward type | opportunity ID | earned evidence |
| Reward granted | Game: successful durable transaction | placement, reward value/type | opportunity ID / transaction ID | grant correctness |
| Ad impression revenue | One verified SDK/provider owner | currency, value, source, format | provider-supported identity | revenue |
| Currency earned/spent | Game: committed economy transaction | currency, amount, bounded reason | transaction ID | sources and sinks |

For each row define retention period, permitted collection conditions, expected volume, validation query and the owner who can fix discrepancies. Do not send personal details, free text, full save files or unnecessarily high-cardinality data. Document whether IDs are test-only, local diagnostic IDs, or permitted analytics identifiers.

## Metric definitions

| Metric | Numerator | Denominator | Window and exclusions |
|---|---|---|---|
| Offer selection rate | selected opportunities | visible eligible opportunities | same placement and cohort |
| Load success rate | successful loads | requests | retries separately identified |
| Grant completion rate | durably granted rewards | earned rewards | allow documented callback delay |
| Dn exact-day retention | installs active on install date + n | installs with complete day n | one declared calendar timezone |
| Cohort revenue/install | revenue attributable to cohort through horizon | all included cohort installs | same maturity, currency and consent coverage |
| ARPDAU | daily revenue | daily active users | matching population, date and revenue scope |

Keep monetisation-provider totals and consented-user analytics totals as separate views until their populations and definitions reconcile.
