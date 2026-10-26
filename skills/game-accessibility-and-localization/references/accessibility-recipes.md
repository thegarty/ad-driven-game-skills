# Accessibility implementation recipes

Use these original recipes with the actual game, target devices and player
needs. Official source navigation was checked **2026-10-26**; verify the engine
version and platform bridge before promising a capability.

## Information channels

List each essential fact: approaching threat, selected target, cooldown, damage,
success, failure, pending grant and unavailable action. For each, identify the
primary channel and a usable alternative. Colour plus shape, audio plus visual
cue, or motion plus a stable indicator can convey the same fact; simply adding
more effects may increase clutter.

Synthetic case: red and green pests differ only by colour, but require opposite
counters. Add a readable silhouette/icon and explicit counter description, then
verify recognition in a dense wave with effects reduced. A colour filter alone
does not establish that the gameplay distinction is now understandable.

## Input demand

Describe what the action requires: tap precision, repeated tapping, sustained
hold, drag distance, simultaneous contacts, rapid timing or device motion.
Offer suitable alternatives where the game allows them: toggle instead of hold,
tap-to-select then tap-to-place instead of precision drag, adjustable sensitivity,
or fewer repeated inputs. Preserve the meaningful decision when changing motor
demand; avoid assuming every assist must change difficulty.

For time-critical choices, consider pausing a decision menu or giving a declared
timing option when consistent with the game. Keep the option's effect on scoring
explicit. Test both activation and cancellation so an alternative does not
create unintended purchases or resource spending.

## Focus, labels and native assistive paths

Provide a logical navigation order and visible current selection. On opening a
modal, move focus to an appropriate control and restore it to a valid origin on
close. Disabled/hidden controls must not create navigation traps. Describe a
control's action and state, not only its icon. Announce a result without repeatedly
interrupting a player with unchanged information.

Godot's [focus/navigation guide](https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html)
describes Control focus modes and neighbors. Initial focus and hidden-control
behavior require deliberate handling. These engine controls do not by themselves
prove VoiceOver or TalkBack exposure; verify the actual exported app and any
native bridge with the intended assistive technology.

## Presentation settings

Keep important text readable at the smallest supported device and chosen scale.
Offer relevant motion/flash/effect and audio options, while preserving critical
information through another channel. Avoid claiming a generic “safe mode” from
an arbitrary reduced particle count. Check actual transitions, flashes and busy
sequences with appropriate evaluation methods for the intended coverage.

Place settings where a player can reach them before a blocked first-play action.
Persist them independently of a run reset. A reduced-motion setting that resets
on every scene or an audio slider that unmutes after an ad is a functional defect.

## Worked acceptance sequence

Start a fresh save with muted audio and reduced effects. Identify the next
required action, distinguish threats, pause, change a setting, finish/lose a run,
decline a rewarded offer, return home and relaunch. Repeat on the selected input
and assistive configurations. Record the point of failure and whether recovery
was possible without outside assistance.

## Official design references

- [Apple accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility)
  and [designing games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games/)
  provide platform design guidance; app-specific coverage requires testing.
- [Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines)
  offer game-specific design/review topics such as input, cues, focus and time
  limits. They are useful cross-platform questions, not a mobile certification
  checklist or a substitute for testing the intended players and technologies.
