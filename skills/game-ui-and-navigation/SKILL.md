---
name: game-ui-and-navigation
description: Design or improve a mobile game's look and feel, HUD, menus, screen layouts, navigation and visual hierarchy. Use for interface audits, screen specifications, Godot UI implementation or confusing player choices; include visual examples and test comprehension on real devices.
license: MIT
---

# Game UI and Navigation

Make the next useful action understandable and the world enjoyable to interact
with. A polished screenshot is a design proposal, not evidence of engagement.

## Start with the player's task

Inspect screenshots, scenes, input handling, theme resources, audience, locale,
orientation and smallest supported device. Trace first launch, play, pause,
loss, upgrades and return. Identify what players must see, decide and do on each
screen. Keep decorative art separate from interactive controls. If no project
exists, state the assumed device and make a small coherent screen set.

1. Use the [screen and state inventory](assets/screen-inventory.md) to map entry,
   exit, back, failure, loading, empty and recovery states. Start with task flow,
   then choose layout. Keep settings, accessibility and privacy discoverable.
2. Define a visual direction and reusable [UI tokens](assets/ui-spec.md): type,
   spacing, surfaces, semantic colours, icons, press/focus/disabled states,
   motion and audio. Use [look and layout patterns](references/look-and-layout.md)
   for concrete home, HUD, result and upgrade examples.
3. Produce a screen map and annotated wireframes before detailed art. When art
   materially helps understanding, generate or commission an original mockup
   using the available tools. Keep production text as live localisable text;
   give diagrams captions or text equivalents. Mark illustrations as untested
   examples, with no invented analytics. Do not add decorative images everywhere.
4. Show one clear primary task per state, with visible alternatives. Keep
   frequently used controls reachable and away from system gestures. Express
   status through text/shape as well as colour. Preserve enough space for long
   translations, large text, changing currency values and safe areas.
5. For Godot, use the [container/theme recipe](references/godot-ui.md). For other
   engines, discover their current layout, safe-area, focus and accessibility
   APIs before implementing. A CSS or Godot layout recipe is not a native API.
6. Test the task on touch devices: initial comprehension, accidental taps,
   back/focus recovery, text expansion, no-fill, save failure, interruption and
   modal stacking. Use [evidence and measurements](references/evidence.md) to
   separate usability observations from retention effects.

## Decisions and constraints

Use an inline status for routine progress and recoverable service failure;
reserve a blocking modal for a decision that genuinely needs interruption. Keep
instructions brief and beside the relevant action. If installed,
`game-ux-writing-and-instructions` supplies detailed copy/teaching workflows.
Never hide decline, price, reward conditions or destructive consequences to
make a screen cleaner. Do not render a grant as completed before it is durable.

Use the [contrast helper](references/contrast-helper.md) for opaque colour-pair
checks, then inspect actual rendered text and dynamic backgrounds. It is not a
complete accessibility audit. The accessibility specialist covers broader
input, localisation and assistive-technology work when available.

## Deliver

Provide the screen/state map, annotated layouts or implementation, token sheet,
brief copy, device checks and one measurable hypothesis. Keep visual approval,
functional correctness and player outcomes separate. Prefer clearer decisions,
fewer unintended actions and voluntary replay to longer time spent navigating.
