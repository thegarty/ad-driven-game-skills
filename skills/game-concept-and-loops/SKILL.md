---
name: game-concept-and-loops
description: Design or compare mobile game concepts, core mechanics, session loops and return loops; define a bounded prototype and evidence needed to continue. Use before building a new concept or when the central play loop needs redesign.
license: MIT
---
# Game concept and loops

Turn a concept into a testable player experience. Start with the player's decisions and the intended production budget, then identify where optional monetisation could fit.

## Establish the design problem

Inspect an existing game or brief before requesting more context. Establish audience, genre, orientation, engine constraints, team capacity, expected play context, accessibility needs and whether the request concerns a new game or an existing one. Distinguish stated constraints from assumptions. Age/audience and target platforms affect later monetisation choices; do not assume a child-directed game can reuse a general-audience ad recipe.

Use [genre patterns](references/genre-patterns.md) for idle/incremental, tower defence, puzzle and casual concepts. Treat these as design options, not evidence that a genre will achieve a particular retention or revenue result.

Use the [mechanics catalogue](references/mechanics-catalogue.md) when choosing idle/prestige, tower-defence, puzzle/merge or survivors/roguelite patterns. It connects player decisions to rewards, failure/recovery and observations, including the costs of combining genres.

## Build three connected loops

- **Moment-to-moment:** the player's action, information available, tradeoff, feedback and skill they learn. Describe the meaningful decision; tapping by itself is an input, not a complete mechanic.
- **Session:** starting state, escalating challenge, success/failure, earned outcome and a satisfying stopping point. Explain what persists after a loss.
- **Return:** an unresolved goal, new choice, collection, mastery or completed task that makes a later session interesting. Separate active gameplay from time-gated progress.

Write a short playable sequence rather than a list of features. For example: choose a defensive layout, observe a wave, change an upgrade priority, finish the run, then select one persistent unlock. Identify a player choice that changes the outcome and a clear reason to try a different strategy.

For concept comparison, use a small table of audience fit, input clarity, depth, content cost, device performance risk, natural ad opportunities and the cheapest experiment that could disprove the idea. Do not invent a market-size, CPI or retention score to make the table look quantitative.

## Specify the prototype

Use the [game brief](assets/game-brief.md). Choose the smallest playable slice that answers the largest uncertainty. State the content deliberately excluded, test participants or synthetic scenarios, the observation to capture, a time/effort cap and the decision after testing: continue, revise or stop. Any numeric success target is a project hypothesis with its rationale, not an industry default.

Keep the normal play loop understandable and useful when ads are unavailable or declined. At this stage, describe candidate placement moments and reward purposes; an ad SDK is unnecessary to test whether the central mechanic works. Represent a reward offer with an inert control when needed for the experiment.

## Deliver and check

Produce a brief with the three loops, core rules, one concrete play sequence, prototype scope and the experiment decision. If asked to implement, build the agreed slice using the existing project's conventions; do not expand to a full economy, content catalogue or acquisition campaign without a reason.

Check that a novice can identify the next action, failure teaches something actionable, a session can end cleanly, and return motivation does not rely solely on collecting a timer reward. Report prototype observations separately from commercial hypotheses.
