# Deterministic economy scenario helper

Python 3.9+, standard library only. From this skill directory:

```bash
python3 scripts/economy_scenario.py assets/economy-example.json
```

Input is a JSON object with exactly the keys in the [synthetic example](../assets/economy-example.json). The helper writes a JSON report to stdout and errors to stderr with exit code 2. It reads no game files and contacts no service.

| Field | Meaning |
|---|---|
| `currency` | Nonempty currency label; all amounts share this unit. |
| `steps` | Integer 1–10,000. |
| `active_minutes_per_step` | Positive finite active minutes, excluding menus/offline time. |
| `normal_income_per_active_minute` | Nonnegative finite fixed earning rate. |
| `initial_balance` | Nonnegative starting currency. |
| `optional_earned_rewards_per_step` | Nonnegative integer of assumed earned rewards; no selection/load model. |
| `optional_reward_value` | Nonnegative finite amount per reward. |
| `optional_reward_cap_total` | Nonnegative integer ceiling across the entire scenario, not a daily cap. |
| `spends` | Ordered list of `{step, label, cost}`; repeated step purchases execute in list order. |
| `milestones` | Unique `{label, cost}` entries for affordability inspection. |
| `assumptions` | Nonempty list of explanatory strings; make clock, strategy and reward assumptions explicit. |

Per step, the model adds normal income and capped assumed rewards, records milestones affordable at that point, then processes scheduled spends. An unaffordable spend is reported and skipped, not retried automatically. Initial affordability is step 0. Milestones do not deduct currency or grant unlocks. Scheduled purchases do not alter the fixed income rate.

Amounts use decimal arithmetic internally, so a balance of 0.3 can pay scheduled costs of 0.1 and 0.2 exactly. Output remains ordinary finite JSON numbers; conversion to floating-point output can round very small or highly precise values. The helper does not apply an affordability tolerance or infer a currency's smallest unit.

The fixture yields 40 normal currency, 10 reward currency, 20 spent and a closing balance of 30. The first milestone becomes affordable at step 2; the second never becomes affordable. Set assumed rewards and cap to zero for a free-route comparison. Compare scenarios using the same active-time budget and disclose that successful ad availability and human choices were assumed.

This small arithmetic model is a planning aid. For combat, compound production, prestige, offline timers or adaptive strategies, create project-specific simulations against actual game logic and validate their clocks, caps and stopping conditions. Do not extrapolate this output into retention or revenue.
