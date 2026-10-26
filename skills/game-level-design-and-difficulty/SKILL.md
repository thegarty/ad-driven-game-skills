---
name: game-level-design-and-difficulty
description: Design or audit mobile-game levels, waves, encounters, puzzle sequences and procedural content for learnability, solvability and fair difficulty. Use for challenge authoring and validation rather than economy pricing or broad concept selection.
license: MIT
---

# Game level design and difficulty

Make each challenge teach, test or combine a meaningful player decision. Work
from the actual controls, mechanics, available tools and progression state;
difficulty cannot be inferred from enemy health or move count alone.

## Establish the challenge contract

Inspect implemented rules, content definitions, unlocks, seeds and telemetry.
Identify the intended audience, player tools available on entry, success/failure,
information shown, retry cost and what persists. Separate lack of knowledge,
execution demand, resource shortage, randomness, poor readability and technical
performance. They can produce similar completion rates but require different fixes.

Use [the level specification](assets/level-spec.md) and
[authoring recipes](references/authoring-recipes.md). Give every level or wave a
learning/challenge purpose, not simply a larger number. Establish an introduction
→ practice → combination sequence for new rules. A counter must be available
and discoverable before a mandatory challenge requires it.

## Author and compare

For wave/combat games, define threat roles, arrival timing, routes, target rules,
counter availability and recovery windows. Compare pressure over time, not only
the total enemy count. An overlap of individually fair threats can remove every
legal response. For puzzles, define the skill tested, solution constraints,
possible dead ends and the information a hint reveals. Do not equate a solver's
shortest path with a novice's experienced difficulty.

Keep authored values separate from outcome measurements. Use synthetic profiles
for invariants and strategy exploration, and human playtests for understanding,
execution and enjoyment. Report assisted and unassisted outcomes separately.

## Validate procedural and changing content

Record generator/configuration version and seed. Define hard invariants before
quality scores: reachable objectives, legal placements, available resources,
valid references and at least one feasible route under the stated rules.
Bound generation attempts and supply a known-valid fallback when appropriate.
Failed or timed-out solver searches are not automatically proof of impossibility.

Test content with the actual game's rule implementation, including required
upgrade/loadout states. A content change must preserve stable IDs and explain
how existing runs/saves are handled. A live configuration change must not silently
replace a challenge midway through a committed run.

## Tune with interpretable evidence

Read a funnel from entry → attempt → failure reason → retry → completion. Segment
by prior progression, strategy and assistance when the population supports it.
Include time to understand, damage/pressure context, hint use and abandonment;
do not optimise completion percentage without considering the desired experience.

Compare baseline/candidate on the same seeds and starting states, then observe
players on the revised content. Change one explanatory dimension where possible.
Adaptive difficulty, when chosen, needs an explicit goal, inputs, bounds and
reset policy; it must not secretly manufacture failure to induce an ad or purchase.

Deliver authored specs or implemented content, validation receipts, representative
failure replays and the next real-player question. Label simulated solvability,
source-tested rules and observed human outcomes separately; none guarantees
retention or revenue uplift.
