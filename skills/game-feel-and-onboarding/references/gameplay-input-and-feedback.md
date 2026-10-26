# Gameplay input and feedback

Godot input documentation checked **2026-10-26**. Use the installed engine and
native bridge documentation for exact event fields. These state recipes are
engine-neutral; they are not a tested drop-in touch implementation.

## Give each gesture an owner

A placement gesture can use idle → pressed → dragging → committed/cancelled.
Capture the active pointer identity, start position, candidate target and relevant
game-state revision. A second finger must not steal the first finger's ownership
or commit its action. Choose and document whether multi-touch is supported,
ignored or cancels the gesture. Use a device-appropriate drag threshold tested
at actual scale, not an unexplained universal pixel constant.

| Input/state | Expected behavior |
|---|---|
| Press on valid gameplay target | Acknowledge selection; capture this pointer; do not spend yet |
| Move past drag threshold | Preview a candidate using current validity rules |
| Move over blocked UI or invalid terrain | Show invalid placement; do not activate a covered control |
| Release with valid ownership and target | Revalidate affordability/rules; commit once; show accepted outcome |
| Release elsewhere, cancellation, focus loss or scene replacement | Clear ownership/preview; no resource debit |
| Release from an old pointer after return from service UI | Ignore; a fresh gesture is required |

The exact release policy depends on the mechanic: a hold-to-fire control may stop
on release, while tap-to-select/tap-to-confirm can provide an alternative to drag.
The invariant is that a gesture has one clear owner and cannot leak into another
screen. Reset armed gameplay input when backgrounding or presenting an ad/store
surface. Never resume an old press as a purchase, attack or placement.

[Godot's InputEvent guide](https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html)
explains the event pipeline and InputMap. Gameplay handled after GUI interception
can avoid treating a GUI action as a world action. Use the documented event
consumption path; polling a held input independently can bypass that protection.
Inspect both paths when one tap triggers two systems.

## Separate acknowledgement from outcome

Immediate selection/press feedback confirms receipt. Successful placement,
resource debit, hit and persistent reward are different outcomes. Emit their
feedback from the accepted operation rather than from a speculative button press.
A rejected move should explain the local reason without pretending it succeeded.
Keep sound, visual and haptic cues consistent with actual state and avoid using
one channel as the sole rule explanation.

Synthetic tower example: dragging previews range; releasing on a valid tile
atomically places a tower and spends the cost. A concurrent economy change can
make it unaffordable at release; remove the preview and show the current reason,
without playing the same celebratory cue as a successful placement. A second
release callback cannot buy a second tower.

## Tune the control loop

Measure input receipt, simulation response and visible feedback separately where
instrumentation permits. A smooth animation can hide a slow decision path; it
cannot make an unresponsive input correct. Test movement and attack rules at
different frame rates, with pause/resume and delayed frames. Use the engine's
appropriate fixed-step/elapsed-time mechanisms rather than counting frames for
wall-time gameplay rules. Never extrapolate a desktop input result to a phone.

Tune anticipation, impact, recovery and camera motion around readable outcomes.
Use a clear hierarchy: dangerous threat, player's important action, result, then
decoration. Repeated particle bursts must not conceal hitboxes or a useful counter.
Provide reduced-motion/effect choices that preserve information, and test an
intense scene with those settings and muted audio.

## Teach through the next useful action

At the first useful moment, provide one contextual cue, let the player try, then
show the consequence. Remove the cue when its condition is met; keep help
recoverable. Test whether the player can repeat the action unaided before adding
more explanation. Do not turn every feature into a blocking modal or impose a
generic word limit regardless of comprehension or language expansion.

Synthetic counter teaching: a shielded enemy first appears in a recoverable wave.
Point to the shield and available counter, allow the selection, then make its
effect visible. On the next comparable wave, observe the player's choice without
coaching. If the counter is still missed, distinguish cue visibility, label
understanding, input difficulty and lack of perceived value before adding text.

## Acceptance journey

Test rapid repeated taps, two fingers, drag-to-tap, drag across UI, invalid target,
background while held, ad dismissal, scene transition, changed affordability,
low frame rate, alternate input and reduced feedback. Verify both game state and
what the player sees. Record automated event injection separately from physical
touch tests and comprehension observations. Correct input behavior is not proof
of enjoyment or improved retention.
