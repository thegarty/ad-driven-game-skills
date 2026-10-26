# Godot UI recipe

Contract recipe for Godot 4.x, not a drop-in project. Inspect the exact engine
version, stretch settings and native plugin behaviour before writing code.
Official sources checked 2026-10-26:
[containers](https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html),
[theme editor](https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_theme_editor.html).

1. Build a `Control` screen root and nested `MarginContainer`, `VBoxContainer`,
   `HBoxContainer` or `GridContainer` children according to layout needs. A
   container owns its child Controls' positioning: do not fight it with manual
   offsets. Use minimum sizes, size flags and expanding space deliberately.
2. Put shared colours, fonts, StyleBoxes and control states in an external
   `Theme` resource. Preview real screen scenes, not only isolated controls.
   Keep decorative background layers separate from focusable content.
3. Decide reference resolution and stretch behaviour. Convert the native safe
   area through the actual viewport/stretch transform once, then apply margins.
   Do not assume a desktop screenshot or physical-pixel inset is already in
   Control coordinates. Test notches, gesture bars and rotated/resized windows.
4. Use live Label/RichTextLabel text and actual Buttons. Do not flatten menus or
   instructional text into generated images. Verify font fallback, line wrap,
   maximum line growth and scroll containers. Preserve action/decline controls
   when text expands; do not shrink everything until it fits.
5. Define a screen navigator with one current route and modal stack owner.
   Keep gameplay/service state outside disposable screen nodes. Bind UI from
   a view state; clicks issue commands, then the confirmed state updates the UI.
   Disable repeat submission while a transaction is pending, without freezing
   navigation or losing recovery options.
6. Set intentional input/focus behaviour. Decorative Controls should not steal
   pointer events; modal backgrounds must block gameplay behind them. Handle
   keyboard/controller focus explicitly where supported. Restore focus to a
   valid control after closing a modal or removing a locked feature.
7. Associate timers/tweens/signals with the screen's lifetime. A delayed ad or
   save callback checks its immutable operation identity and owner validity.
   It cannot mutate a new screen that happens to reuse the same node name.
8. Provide reduced-motion and audio-independent feedback. Keep essential state
   readable after a brief animation ends. Profile effects on a low-end device;
   polished UI does not justify shader, memory or startup bloat.

Acceptance: smallest supported screen; largest supported text; long locale;
rapid open/back; overlapping callbacks; app background/resume; modal during ad
load; save failure; disabled/pressed/focused states; no pointer passthrough;
balance wider than mockup; safe-area transform under each stretch mode. Record
engine revision, device, renderer and screenshots for reproducibility. UI nodes
alone do not establish screen-reader support; inspect current platform bridges
and test assistive technology explicitly.
