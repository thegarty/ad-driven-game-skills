---
name: game-feel-and-onboarding
description: Improve mobile controls, feedback, accessibility, first-play teaching and failure/reward screens. Use when players struggle to understand actions, discover useful strategies or complete the first session.
license: MIT
---
# Game feel and onboarding

Make actions understandable, consequences legible and early decisions meaningful. Diagnose the obstacle before adding tutorial screens or reducing difficulty.

## Trace a real journey

Inspect the actual first launch, first action, first mistake, first success, first persistent upgrade and return. Use fresh isolated saves and representative phone sizes. Separate confusion, motor difficulty, poor feedback, performance and weak incentives; these require different fixes.

Record what information the player sees when a decision is required. Check whether they can tell what happened, why it happened and what they can try next. A model that knows all upgrade formulas is not a substitute for an uninformed player.

## Teach in context

Teach an action near its first useful moment; let the player perform it and see the consequence. Keep previously explained mechanics discoverable in contextual help. Avoid a long opening slideshow that asks a player to remember mechanics they cannot yet use.

After repeated comparable failures, consider a bounded hint tied to the observed problem. Show a relevant upgrade, counter or strategy and offer navigation to it. Navigation must not buy an upgrade or change the player's build unless the action clearly says so. Stop repeating advice when its condition no longer holds.

Use [first-play and recap review](references/first-play-and-recap.md) for a sanitised Overgrowth lesson and the compact-screen acceptance scenarios.

Use [gameplay input and feedback](references/gameplay-input-and-feedback.md) for pointer ownership, drag/commit/cancel states, interruption and contextual teach/do/check recipes. Test unaided comprehension before adding more explanation; avoid making every new feature a blocking modal.

## Improve feel without obscuring information

Inspect input latency, visual response, animation timing, audio/haptics and feedback consistency. Prefer immediate acknowledgement of an input, followed by clear result feedback. Important cues should not rely on colour, sound or vibration alone. Provide usable mute/motion/feedback choices appropriate to the game's effects and verify that reduced feedback still conveys the rules.

Protect readability during busy play: distinguish threats from rewards, effects from hitboxes, unavailable actions from loading actions, and a drag from a tap. Preserve player control through interruptions and return from full-screen service UI. Establish target-platform accessibility behaviour through current documentation and device tests; do not claim screen-reader support from visual inspection alone.

## Design the outcome screen

Show the actual outcome, already-earned progress and one attainable next action. Use stored outcomes as the source of truth; displaying a recap must not grant currency again. Clearly separate base earnings, a voluntary bonus, pending persistence and an unavailable ad. A long recap must preserve a clear route home/retry and avoid accidental offer activation while scrolling.

## Deliver and check

Use [the journey review template](assets/journey-review.md). Provide the observed obstacle, minimal change, predicted effect, evidence and remaining uncertainty. For implementation requests, change the actual interaction and verify the complete journey.

Test short/tall screens, safe areas, enlarged text where supported, muted audio, reduced effects, rapid input, scroll-to-tap transitions, loss, reward unavailability and interruption/resume. Record physical-device testing separately from synthetic input. Validate improvements through player comprehension and completion evidence; tutorial completion alone does not prove retention.
