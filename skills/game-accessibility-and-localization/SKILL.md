---
name: game-accessibility-and-localization
description: Implement or audit inclusive mobile-game interaction, scalable UI, assistive access and localisation workflows. Use for input/feedback alternatives, text expansion, translation, plurals, fonts, RTL and device validation rather than visual styling alone.
license: MIT
---

# Game accessibility and localisation

Make the intended game actions and information available across the supported
players, languages and devices. Treat accessibility and localisation as
implementation behavior with explicit coverage, not a badge inferred from a
colour palette or translated menu.

## Establish the access contract

Inspect core actions, time pressure, input precision, visual/audio/haptic cues,
text density, device orientation and existing engine/native accessibility support.
Record supported languages, scripts, locales and assistive methods. Use
[the coverage matrix](assets/coverage-matrix.md) to track verified, unsupported
and unverified paths. Do not claim screen-reader support because a desktop
Control node has a label or a screenshot appears readable.

Use [accessibility implementation](references/accessibility-recipes.md) for
redundant cues, input alternatives, focus and meaningful difficulty/assistance
choices. Check the actual platform, engine version and native bridge before
promising assistive integration. Include players with relevant access needs in
evaluation rather than relying exclusively on simulations.

## Build localisation into content

Use [the localisation workflow](references/localization-workflow.md). Keep stable
content IDs separate from translated display text. Externalise complete messages
with context, named placeholders, plural rules and translator notes. Preserve
the meaning of rewards, purchases, privacy and decline/exit controls across
languages; never hide a qualification by truncating its translation.

Design layouts for expansion, wrapping and appropriate ordering. Test actual
target scripts, font fallback, bidirectional text and input fields in exported
builds. Pseudolocalisation finds useful problems but is not proof of CJK glyph
coverage or correct RTL behavior. Respect locale-specific numeric/date formats
without confusing translated display values with stored identifiers or amounts.

## Make choices persistent and understandable

Offer the relevant control, audio, motion, text and language settings early
enough to make the game usable. Preserve choices across normal scene changes
and app restarts. Define defaults and reset behavior explicitly. Confirm that
reducing effects or disabling sound does not remove the sole warning of a threat.

Separate an accessibility option from a monetised advantage. If assisted modes
affect a competitive score, explain the rule without removing access to ordinary
progression. Do not gate a necessary input alternative or readable instruction
behind an ad.

## Verify and communicate coverage

Test first launch, settings, core play, pause, defeat, reward offers, purchases,
privacy controls and error recovery with the relevant settings enabled. Include
small screens, large supported text, muted audio, reduced motion, focus navigation,
long translations and actual RTL/CJK strings where supported. A lost focus or
clipped decline control can block a player even when the main game works.

Deliver the implemented changes, language/access coverage, test devices and
remaining gaps. Distinguish content review, automated layout/string checks,
engine behavior and physical-device assistive tests. Current platform guidance
is a source for design and implementation; this skill does not certify legal
compliance or universal accessibility.
