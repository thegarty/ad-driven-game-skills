# Audio runtime recipe

Godot audio documentation checked **2026-10-26**. The routing principles below are
portable; confirm engine, audio-session and native-service behavior on target
devices. The library has not executed these examples in a game build.

## Route by player control and information purpose

Create explicit groups for music, gameplay effects and interface cues as needed,
feeding a master output. Keep bus names stable and validate player references.
[Godot's audio-bus guide](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html)
describes stream-player routing and bus meters; a renamed bus can change where an
existing player routes. Test mute and level settings in the exported build after
any layout rename, not only in an editor scene.

Store the player's preferences separately from temporary attenuation. An ad,
phone interruption or pause may request a temporary mute/duck; it must not rewrite
the saved music preference. Model active attenuation reasons with stable ownership
and idempotent add/remove operations. Restore the effective mix only after all
applicable reasons have ended. Do not restore to a hardcoded full-volume value.

Synthetic overlap: the player has music muted, an ad starts, then the app loses
focus. Ad dismissal removes only the ad's attenuation reason. Music remains muted
from the preference and gameplay audio stays suppressed until the focus policy
allows it. Duplicate dismissal must not remove another reason or start duplicate
music players. Convert linear gain and decibel values deliberately at API
boundaries; adding a linear multiplier to a dB level is not a valid conversion.

## Cue lifecycle and voice policy

Give each cue a purpose, trigger, priority, category, maximum simultaneous voices,
repeat policy, spatial behavior and variant/loop rules. Derive limits from the
actual busy scene and target devices. A hundred enemies hitting at once should
not blindly instantiate a hundred full-volume copies of the same effect.
Coalesce/rate-limit low-priority repeats or choose a representative mix while
preserving important threats and player confirmations.

Play purchase/reward success from the accepted state transition. A button press
may have a lighter acknowledgement, but failed or pending operations must not
sound like completion. Include visual alternatives to every gameplay-critical
sound. Do not use audio-only cues for accessibility modes or quiet play.

Reuse or pool players only after establishing lifetime and reset rules: stopped
streams, callbacks, pitch/gain, position and bus must not leak from the previous
cue. A loop needs intentional start, transition and stop boundaries; prevent a
scene reload from layering a second persistent music instance.

## Assets and mix

Compare compression formats, sample rate, channels and streaming/decode behavior
using the same actual listening context and device. Long ambience, short attack
cues and UI clicks need different tradeoffs; apply no universal codec rule.
Trim unintended silence, inspect seamless loops, and validate decoded memory and
loading as well as file size. Avoid stereo content for a cue that gains no useful
spatial information from it, but verify the perceptual result.

Use meters and listening tests to check simultaneous cues, clipping, harsh repeats
and whether threats remain distinguishable at the user's chosen level. A limiter
cannot make an overloaded mix clear. Test device speaker, headphones and muted
play where supported; an attractive source waveform does not establish a good
phone mix.

## Acceptance scenarios

Exercise rapid actions, peak enemies, repeated retries, music transition,
background/foreground, headphone/audio-route change, full-screen ads, native
purchase UI, mute while ducked and relaunch. Verify preference persistence and
absence of duplicate/stuck loops. Confirm both audible behavior and CPU/memory
cost under representative load. Report desktop listening, native device checks
and player observations separately.
