# Authoring levels, waves and procedural challenges

The examples below are synthetic design reasoning. Their values are not
difficulty benchmarks or recommended production defaults.

## Learning sequence

Use a small matrix: prerequisite knowledge, new decision, information supplied,
failure explanation and next combination. Introduce one meaningful rule in a
low-noise context, practise it with variation, then combine it with known rules.
Vary routes, timing or tradeoffs when they create a new decision; a recoloured
enemy with the same response is mainly content presentation.

Example sequence for a defence prototype:

| Challenge | Intended learning | Required entry capability | Evidence to inspect |
|---|---|---|---|
| Slow single-lane threat | Placement changes coverage | Basic attack available | Player notices where attacks connect |
| Fast threat with clear cue | Slow effects buy attack time | Slow option available and explained | Player identifies the counter without coaching |
| Two routes with unequal pressure | Allocate rather than duplicate a build | Both prior tools usable | Choice changes which route survives |
| Shield plus fast threat | Sequence counters and target priorities | Shield counter introduced earlier | Failure can be attributed to a recoverable decision |

If the shield counter is unlocked only after this final challenge, the content
contract is broken regardless of an expert debug loadout's success.

## Wave pressure rather than enemy totals

Write a spawn timeline including enemy role, count, interval, path, speed,
durability, support effects and time in the player's effective range. Separate
an enemy's individual threat from interactions such as protection, healing or
blocking. A single scalar “threat budget” is an authoring aid, not a proof of
fairness; validate combinations in the real simulation.

Synthetic example: both waves contain eight ordinary enemies and one shield
carrier. The first spaces the ordinary enemies away from the carrier; the second
clusters them behind it. Equal counts and total health do not imply equal difficulty because effective damage,
targeting and response time differ. First compare a timeline/replay. Do not
compensate by globally reducing every enemy's health.

Check at least these strategies where relevant: plausible uninformed, focused
single-stat, complementary, efficient and deliberately adversarial. A dominant
build may reveal missing counterplay; a weak build's failure is not by itself a
bug. Explain which viable choices the design intends to support.

## Puzzle sequences and hints

State the legal moves, win condition, move/time/resource constraints and whether
the puzzle is deterministic. An exhaustive search can establish existence of a
solution only within its actual encoded rules and explored state space. Store
the solution trace and rule version with the seed. A timeout means “unresolved
within this search budget,” not “unsolvable.”

Test a teaching sequence against the mental operation required: recognise a
pattern, plan an irreversible move, combine rules or manage a scarce resource.
Measure where players diverge from a viable path, not only how many moves they use.

Use a hint ladder: restate the goal → highlight relevant information → identify
a useful relation → suggest a next action. Specify whether hints reveal
information or execute moves. If a rewarded hint is declined/unavailable, the
ordinary puzzle route must still follow its promised rules. A hint that solves
the entire interesting step can improve completion while reducing satisfaction.

## Procedural generation contract

Separate generation, invariant validation, optional difficulty estimation and
selection. For every accepted item, retain seed, generator/config version and
validation result. Test seed ranges and boundary configurations; also inspect
repetition, layout variety and player-readable affordances.

Bound retries. If validation cannot establish a playable result, use a known-valid
fallback or surface a controlled unavailable state according to the product.
Never spend a player's scarce entry token before the challenge can be delivered.
A random seed is insufficient for reproducibility when content tables, RNG
algorithm or call order changed; capture the relevant version/state too.

## Difficulty changes and live compatibility

Define whether an active run keeps its starting configuration. Preserve its
content revision through resume and reward settlement. A fresh-run difficulty
change may be acceptable while changing an already-started purchased/earned
challenge is a different product decision.

For adaptive difficulty, document inputs, intended experience, adjustment limits,
evaluation window and reset conditions. Distinguish an accessibility assist
chosen by the player from hidden adaptation. Record assisted-score eligibility
when competition exists. Do not conflate a fair challenge with a monetisation
funnel that withholds the required counter.

## Acceptance scenarios

- Required counter absent, affordable but undiscovered, and correctly used.
- Low/high supported progression, no-ad and supported assisted runs.
- Same threat count with different timing/interaction patterns.
- Invalid generator output, exhausted search budget and known-valid fallback.
- Save/resume after content update; removed or renamed stable content IDs.
- Pause, low frame rate, small screen and reduced-effects settings.
- A player explains a failure and identifies a different plausible next action.
