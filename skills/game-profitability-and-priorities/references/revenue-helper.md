# Revenue and CPI sensitivity helper

Python 3.9+, standard library only. From this skill directory:

```bash
python3 scripts/revenue_sensitivity.py assets/revenue-example.json
```

The [fixture](../assets/revenue-example.json) is synthetic and its numbers are not benchmarks. Input JSON uses exactly the keys below. Output JSON is written to stdout; invalid input produces stderr and exit code 2.

## Input contract

- `currency`: nonempty label, shared by every monetary amount; convert externally using an explicit rate/date.
- `population`: the install population whose metrics are being combined.
- `horizon_days`: integer 1–3,650; a horizon of 30 covers day zero through day 29.
- `assumptions`: nonempty string list describing the evidence and model choices.
- `scenarios`: nonempty list with unique `label` values and all the following fields.

| Scenario field | Meaning |
|---|---|
| `input_basis` | `synthetic`, `observed` or `mixed`; caller assertion, not verified. |
| `retained_active_days_per_install` | Average active days including day zero, between 0 and horizon. Use the same population across all inputs. |
| `impressions_per_active_day` | Impressions, not requests, per active user-day. |
| `realized_ecpm` | Publisher ad proceeds per 1,000 impressions; do not deduct a network share twice. |
| `net_iap_revenue_per_install` | Net purchase proceeds through the same horizon after the deductions explicitly chosen in assumptions. |
| `variable_cost_per_install` | Serving and other per-install costs through the horizon. |
| `cpi` | Acquisition cost per install, same currency and population. |

Numeric fields must be finite and nonnegative; boolean values are invalid. Explicit zero is permitted, but missing observations must not be silently entered as zero.

Monetary comparisons use decimal arithmetic internally, including exact zero-contribution decisions. Output remains ordinary finite JSON numbers; floating-point output conversion and nonterminating ROAS division can round. The helper does not infer currency rounding rules or treat a small real loss as zero.

## Calculations

`ad proceeds/install = active days/install × impressions/active day × realised eCPM / 1,000`

`contribution before acquisition = ad proceeds + net purchase proceeds − variable cost`

`contribution after acquisition = contribution before acquisition − CPI`

`revenue ROAS = (ad proceeds + net purchase proceeds) / CPI`

ROAS returns `null` when CPI is zero. If contribution before acquisition is negative, the break-even CPI returns `null`: even free installs fail to cover the supplied variable costs. Otherwise break-even CPI equals that contribution **before fixed costs**. This does not establish company profitability or a safe bidding level.

The fixture's baseline has 15 impressions/install, 0.15 ad proceeds, 0.25 total proceeds, 0.23 contribution before acquisition and 0.03 after acquisition. Its second scenario illustrates how more daily ads can coincide with no improvement in total value when assumed return days fall. The scenario does not establish that ads caused the decline.

Outputs remain scenario arithmetic even when some inputs are observed. Prefer direct, mature cohort proceeds when available. Changing geography, format mix, consent coverage or cohort maturity can invalidate comparisons; the tool cannot detect those mismatches or estimate uncertainty from aggregate inputs.
