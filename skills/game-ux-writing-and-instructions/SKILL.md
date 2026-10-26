---
name: game-ux-writing-and-instructions
description: Reduce text-heavy game modals, instructions and menus while preserving comprehension and informed choices. Use to write concise microcopy, visual teaching sequences, contextual hints, reward offers or error states; research and test when players need explanation rather than assuming all text is bad.
license: MIT
---

# Game UX Writing and Instructions

Help players act and learn with the least explanation that preserves meaning.
Do not equate fewer words with better understanding or guaranteed engagement.

## Inspect before rewriting

Read the actual screen/state flow, strings, mechanic, target audience, language
and device constraints. Identify what the player knows at this point. Separate
action guidance, optional depth/lore, transaction terms and recovery messages.
Keep legal/provider consent content in its required flow; do not abbreviate it
without checking the applicable requirements.

1. List each instruction or modal with its trigger, task, required facts,
   action, dismissal and recurrence using the [copy inventory](assets/copy-inventory.md).
   Remove duplicate explanations and internal implementation language.
2. Decide whether the mechanic can teach itself through a safe, readable
   action. Read [research and limits](references/research.md) before choosing
   no tutorial, contextual help or a structured practice sequence. Complex or
   unfamiliar mechanics can need explanation; deleting it is not a strategy.
3. Use [show → try → feedback](references/visual-teaching.md): demonstrate the
   relevant action visually, let the player perform it, then show the result.
   Generate an original illustration or annotated mockup when useful and tools
   are available. Prefer editable diagrams for logic, actual screenshots for
   implementation reviews and in-engine cues for production. Keep live text
   separate from images and supply a text/accessibility equivalent.
4. Write the immediate action in plain language. Put optional explanation near
   the relevant feature behind a discoverable details/help control. Do not hide
   cost, reward conditions, loss consequences, privacy choices or purchase
   scope. Use [microcopy patterns](references/microcopy.md) for concrete examples.
5. Trigger help when needed: first encounter, demonstrated confusion or explicit
   request. Keep it dismissible/replayable where safe. Progress after the
   relevant action is understood or performed, not after tapping Next through
   a wall of text. Define how repeated failure changes the hint.
6. Test real layouts and comprehension, including text expansion, small screens,
   low literacy, colour differences, reduced motion, muted audio and returning
   players. If shorter copy causes wrong choices, restore the missing meaning
   or simplify the interaction. Avoid universal word/character limits.

## Deliver and measure

Produce a before/after copy table, visual teaching storyboard, trigger/state
rules, localisation notes and test plan. Use the
[instruction test template](assets/instruction-test.md) to record unassisted
task success, mistakes, help use and repeated understanding. Treat modal dwell
and dismissal as ambiguous: fast dismissal may mean clarity or unread text.

Measure early meaningful action, comprehension and voluntary continuation;
evaluate return retention separately with mature cohorts. Session length can
increase because players are stuck. Avoid claims about dopamine or attention
spans that the evidence does not establish. If installed, use the UI specialist
for layout and the progression specialist for when new features become useful.

No skill or image generator is a prerequisite. If generation is unavailable,
produce an editable storyboard and clear asset brief; do not claim an image was
created. Never add a heavy video or many full-resolution images merely to replace
a sentence that was already clear.
