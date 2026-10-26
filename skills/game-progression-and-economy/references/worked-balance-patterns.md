# Worked balance patterns

All numbers below are **synthetic assumptions** used to show reasoning. They are
not recommended prices, growth factors, retention targets or live outcomes. The
bundled economy helper models fixed-rate earning/affordability only; it does not
execute these combat, prestige or dynamic-rate systems.

## Cost curves and marginal value

Suppose upgrade purchase index `n` starts at zero and its unrounded cost is
`10 × 1.5^n` coins. The first three costs are 10, 15 and 22.5; their unrounded sum
is 47.5. In general the unrounded sum of `N` purchases is
`10 × (1.5^N − 1) / (1.5 − 1)`. Define integer rounding per purchase before using
the total in the game. Rounding only the final sum can produce a different debit.

At a constant 5 coins/minute and a zero starting balance, the first two purchases
require 5 minutes of earning in total. That statement assumes earning continues
unchanged and ignores gameplay constraints. If the first purchase increases
earning, integrate each phase with its new rate; do not divide the complete cost
by the final, faster rate. Record rate, time, balance and purchases per phase.

Compare cost to the marginal benefit and the decision it unlocks. An exponential
price with a linear benefit can create a deliberate soft cap or an accidental
wall. Inspect late-stage cost, numeric precision, content caps and whether
players still have a useful alternative. Use the game's exact integer/decimal or
large-number representation and test its boundaries rather than relying on a
displayed abbreviated number for affordability.

## Complementary upgrades and dominance

Synthetic attack has damage 10 and two attacks/second, giving an idealised
20 damage/second. Upgrade A adds 5 damage; B adds one attack/second. Either alone
gives 30 damage/second; both give 45. With equal costs, their interaction matters:
buying both is not equivalent to adding two isolated gains of 10.

That arithmetic still omits armour, overkill, target acquisition and travel time.
Against five-health targets, additional damage may be wasted; against a per-hit
armour rule, attack speed may be less effective. Compare the actual encounter
rules for uninformed single-stat investment, a plausible complementary build and
an efficient build. A dominant option across every relevant encounter can
justify reworking a mechanic or price; one option being good in its intended
counter situation is not a balance failure.

For regeneration/health, model damage arrival and time alive, not just displayed
stats. If regeneration exceeds incoming damage, a small increase can change a
finite survival time into a stable state. Record the threshold and counterplay;
linear extrapolation from below that threshold will mislead.

## Prestige with an explicit ledger

Illustrative rule: cumulative prestige entitlement is
`floor(sqrt(lifetime_eligible_resource / 100))`. A separate durable ledger stores
prestige already granted. At lifetime resource 900 the entitlement is 3; at 1600
it is 4. A player previously granted 3 earns **one additional unit**, not four.

Define which resource earns lifetime credit, whether purchases or ad bonuses
count, and which balances/unlocks reset. Do not add spending back to lifetime
credit or reset the granted ledger. If lifetime credit can be corrected downward,
define a correction policy; do not silently erase a previously earned reward.
The preview must show the actual incremental grant, losses, retained benefits and
next threshold. A zero-increment reset should be explicitly explained or blocked
according to the design.

Commit the reset and entitlement grant as one durable game transaction with a
stable operation identity. Reloading, retrying confirmation or replaying a
callback must return the same outcome, not apply another reset/grant. Preserve a
recoverable pre-reset save until the new state has been validated. Simulate the
journey back to a meaningful choice and check whether repeated early steps are
still useful before calling the prestige loop ready.

## Rewards by progression stage

Assume early ordinary earning is 2 coins/minute and later earning is 100/minute.
A flat 10-coin reward represents five early minutes but 0.1 late minutes. These
are projections from assumed rates; actual earning may be intermittent and vary
by strategy. Report what a typical useful purchase costs at each stage as well as
time value. A reward can be a large time saving yet fail to unlock anything.

An illustrative reward `min(30 × stage_rate, 500)` would be 60 coins early and 500
late: 30 and five minutes respectively under those same assumptions. This is a
demonstration of the cap's effect, not a recommendation for a 30-minute reward.
Choose units and caps from the intended player decision. Test low/high rates,
zero earnings, capped progression and temporary boosts. Snapshot the promised
reward when the player accepts it so a mid-offer rate/config change cannot alter
what was agreed.

Compare no-ad, occasional voluntary-ad and frequent voluntary-ad paths with
explicit opportunity, availability and completion assumptions. Do not price
mandatory progression around perfect ad availability. If a stage-scaled reward
becomes exploitably large after a temporary bonus, define eligibility and cap
rules plainly rather than silently reducing it at claim time.

## Report a useful model

Return the formula and units; balance/ledger definitions; tested stage profiles;
rounding, caps and timestamps; source of each input; ordinary and optional paths;
and the behavior the model omits. State whether results came from hand arithmetic,
a fixture executing game rules, simulation or live measurement. Specify the next
player observation needed, such as discovering a counter or understanding a reset,
instead of presenting an affordability improvement as retained users.
