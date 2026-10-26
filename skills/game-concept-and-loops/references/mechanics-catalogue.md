# Mechanics catalogue

These are design patterns and synthetic examples, not evidence of commercial
performance. Start from the decision a player enjoys, then choose compatible
progression and content. Combining genres adds explanation, balance and QA cost.

| Pattern | Fits when the enjoyable decision is… | Main production/balance risk | Useful first observation |
|---|---|---|---|
| Idle/incremental | Choosing which bottleneck to remove and when to reinvest | Waiting replaces decisions; growth makes rewards meaningless | Can a player explain the next useful investment? |
| Prestige/reset | Trading current capability for a different future route | Reset loss is unclear or repeated early play becomes a chore | Can a player predict what resets, persists and improves? |
| Tower defence | Allocating scarce coverage, counters and upgrades against readable threats | A hidden counter or one dominant build makes choice illusory | Can players change one decision after identifying why a wave failed? |
| Puzzle | Discovering a rule, relationship or sequence | Difficulty comes from ambiguity, inaccessible information or unsolvable boards | What information led to a solution or dead end? |
| Merge/board economy | Managing space, combinations and competing objectives | Random drops fill the board with no useful recovery path | Can players recover from an unhelpful drop without paying? |
| Survivors/roguelite | Movement/positioning and building a synergistic run from uncertain choices | Visual overload and runaway combinations obscure causal feedback | Can players name which choice changed their run? |
| Short casual challenge | Improving timing, aim, route or another compact skill | Cosmetic variation fails to create a new decision | Does a retry involve a deliberate adjustment? |

## Idle investment and prestige

Synthetic greenhouse: growers create seeds, processors turn seeds into compost,
and plots consume compost for unlocks. If processors are saturated, buying a
grower does not improve compost output. Show the limiting stage and the effect
of an upgrade before expecting players to discover the chain by trial and error.
Give active interaction a meaningful role such as selecting the next crop; a
mandatory repetitive tap is not inherently depth.

Define offline production separately from active production: eligible machines,
rate snapshot, resource caps, maximum credited interval, clock authority and
when the grant becomes durable. Display the credited result, not a promise that
every minute away always generates the currently displayed rate.

Prestige is useful when a reset creates a new strategy or materially changes the
route back through familiar content. Specify lost balances, retained unlocks,
permanent currency and the next threshold. Offer a preview and an explicit
decision. Do not require reset merely because numbers grew too large. Prototype
one full reset and return journey; testing only the initial accumulation misses
the cost of repeating it.

## Tower defence

Choose the scope of the player's influence: placement/coverage, target priority,
upgrade order, unit composition or active abilities. Add complexity in a sequence
where each counter can be learned before multiple threats require it together.
Distinct attack shapes, speed, armour and pathing should create different useful
responses, not merely larger health bars.

Synthetic wave: fast enemies punish slow single-target attacks; clustered enemies
give splash a role. A mixed wave asks whether to cover both routes or specialise
and spend a temporary ability. If the only available splash unit unlocks after
this wave, the sequence has a dependency problem. Trace the unlock path before
solving the failure with a larger ad-funded bonus.

Separate run resources from permanent upgrades. A loss can teach a counter and
still award the clearly earned persistent resource. Record loss point, available
counters, chosen loadout and whether the player saw the relevant cue; a win-rate
change alone does not identify why difficulty changed.

## Puzzle and merge

Choose what the player knows and controls: visible queue versus random drops,
unlimited moves versus a move budget, reversible moves versus commitment, fixed
board versus procedural generation. Explain the consequence before irreversible
actions. A hint should reveal the missing relationship in stages before giving
away the answer; a shuffle must preserve the intended solvability contract.

Synthetic merge board: combining three sprouts creates one tree and frees two
cells. If a drop can fill the last cell without forming a merge, define a normal
discard, undo, queue or failure/retry route. A rewarded shuffle may be optional,
but it cannot be the sole undisclosed escape from an unavoidable invalid board.
Specify whether higher-tier merges consume lower-tier quest items and whether a
player can lock a valuable item against accidental combination.

Track board dead ends, undo use, move reasons and hint stage, not only completion
time. A faster solution may reflect familiarity with a repeated board. A solvable
generator is not proof that the puzzle is interesting or understandable.

## Survivors and roguelite runs

Separate the movement/combat loop, within-run build and persistent progression.
Make the offer pool conditional on eligibility and define duplicate handling,
upgrade caps and guaranteed escape from an unusable choice set. Synergies should
be discoverable through description and feedback; a formula hidden from players
cannot support an informed selection.

Synthetic build: projectiles gain pierce while an item increases bounce. Decide
whether a hit can bounce back to the same enemy and how simultaneous modifiers
compose. Test an ordinary build and extreme combinations against the real rules.
Do not claim balance from a spreadsheet that ignores enemy contact, movement or
frame-rate-dependent damage.

A revive or reroll changes the run's difficulty and score comparability. Define
eligibility, revive location/invulnerability, remaining attempts and assisted
score rules before adding the offer. Players should understand when a run is
finished and what they earned without taking the offer.

## Combine patterns deliberately

For every proposed mechanic, specify the player decision, information required,
immediate consequence, persistent consequence, failure/recovery path and one
observation that could show the mechanic is not working. An idle meta layer can
support a defence run, but it may also make strategy irrelevant if permanent
power overwhelms counters. Model both and test the intended learning sequence.

Map advertising only after the normal loop works: an optional acceleration,
retry or reroll needs a clear value, a bounded effect and an acceptable no-ad
path. Neither adding a prestige system nor placing an offer at a natural pause
establishes a retention or revenue improvement.
