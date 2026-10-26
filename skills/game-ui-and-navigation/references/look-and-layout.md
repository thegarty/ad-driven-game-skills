# Look, hierarchy and screen patterns

These are original starting patterns, not universal conversion findings. Adapt
them to input, age, genre and art direction. A landscape strategy game needs a
different arrangement from a portrait puzzle game.

## Establish a coherent visual language

Choose two or three qualities players should feel, such as calm, tactile and
curious. Translate each into decisions: soft low-detail backgrounds, crisp
interactive silhouettes, gentle short feedback. Record counterexamples: a
flashing reward panel would break a calm direction. Compare two moodboards on
readability and fit, not on the number of decorative elements.

Define tokens for body/action/display text, spacing, surfaces, outlines, corners,
and motion. Semantic colour names such as `action`, `danger`, `selected`, and
`unavailable` prevent arbitrary screen-by-screen styling. An illustrated button
still needs a readable label, a generous hit region and a visible press state.
Do not use the same glowing treatment for every option. Reserve strong emphasis
for the current task. Avoid claiming that a particular colour increases revenue.

Use recognisable silhouettes for important entities, a restrained background
behind the HUD, consistent currency icons and explicit units. Preview at actual
device size with art motion enabled. A beautiful desktop composition may hide
small text, thumb occlusion or busy combat on a phone.

## Screen anatomy: synthetic portrait game

```text
HOME                       PLAY                       RUN RESULT
safe area                  safe area                  safe area
Profile     Settings       Health   Wave     Pause    Run complete
World / next goal          Compact run objective     Earned progress
Continue / Play            Playfield                  Next attainable goal
Progress   Collection      Contextual hint, if needed Upgrade preview
optional event entry       Action controls            Continue
safe area                  safe area                  Optional ad offer
```

The examples describe relative hierarchy; they do not specify raw pixel sizes.
Apple recommends a general 44×44pt hit region, Android guidance recommends
48×48dp. These are different platform logical units, not interchangeable Godot
pixels. Validate density, display scaling, margins and actual touch behaviour.
Sources checked 2026-10-26: [Apple UI tips](https://developer.apple.com/design/tips/)
and [Android accessible views](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views).

**Home:** emphasise the next playable action. Preserve a returning player's
resume state. Do not greet players with a queue of news, rewards, sales and
permission modals. Show secondary notices in a readable inbox or contextual
entry. Newly unlocked features may receive one discoverable cue, not a forced
tour on every launch.

**HUD:** put rapidly changing combat information close enough to the playfield
to read without hiding threats. Put controls where fingers do not obscure the
decision. Separate status, controls and optional offers. Pause must remain
available during learning. Do not make an ad button look like a combat action.

**Run result:** show what was earned and the next achievable action. A reward
grant has `pending`, `saved`, and `recovery needed` states; only `saved` displays
a confirmed balance increase. A voluntary ad reward has a labelled offer and a
usable continue option. Continue must not silently become an ad CTA when an
async load completes underneath a player's finger.

**Upgrade:** show current effect, next effect and cost together. A preview might
say “Damage 12 → 15 · Cost 40 seeds”. Explain an unavailable upgrade beside it
(missing currency, prerequisite or service), with a clear way back. Reveal deep
formula details on demand. Avoid dumping the full economy manual into a modal.

**Settings:** group audio, motion/input, language, privacy, restore purchases and
support logically. Preserve readable labels even if icons are used elsewhere.
Keep state and consequences explicit for account linking, reset and deletion.

## Navigation and interruption

```text
Home → Play → Result → Upgrade → Home
        ↕ Pause                    ↕ Settings
Offer → Presenting → Reward pending → Result (same run)
  ↘ unavailable → Result, free continue remains available
```

Specify back from each state, focus restoration and scroll retention. Use a
single modal owner; queue or dismiss lower-priority notices instead of stacking
blocking overlays. Protect against a tap passing through a dismissed overlay.
On resume, reconcile state before accepting another purchase/reward action.
An ad dismissal must not discard the saved run or replay its reward animation.

## Review output

Annotate a wireframe with task, primary/secondary action, hit regions, reading
order, overflow strategy and failure state. Add one realistic long translation
and one small-device view. Test recognition of the intended action and the
meaning of disabled states; do not call visual preference a retention result.
