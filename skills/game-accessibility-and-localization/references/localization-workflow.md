# Localisation workflow

Official Godot documentation checked **2026-10-26**. Select the documentation for
the game's actual engine version; do not copy stale font or text API examples
without checking the installed version.

## String contract

Maintain a stable key, source message, context, named placeholders, plural needs,
screen/interaction reference and reviewer status. Translate complete messages;
assembling fragments in English order can fail in another language. Keep a
placeholder's type and meaning fixed, and validate that translations retain all
required placeholders without adding unsupported ones.

Synthetic example: key `reward.claim_summary` has a message meaning “Claim
{amount} {currency_name}.” Its context says that the displayed amount is the
already-earned base reward, not an extra video bonus. A separate key explains
the optional bonus. This prevents a translator from merging two different
promises into an ambiguous “double reward” action.

Do not use translated names as save keys, purchase product IDs or content IDs.
Keep player-entered names as data rather than translation keys. Treat rich-text
markup as a constrained interface: validate tags and avoid allowing translated
content to create unintended interactive behavior.

## Layout and language behavior

Allow container growth/wrapping where appropriate and prioritise actions when
space is constrained. Test long legal/purchase/reward qualifications with the
same care as buttons. Do not shrink all text until a screenshot fits or truncate
the only explanation of a purchase's limits. Use expandable details when needed
while keeping the material promise available before the action.

Verify real target scripts, shaping, font fallback and line breaking in the
exported binary. Mirror UI ordering where language convention requires it, but
do not blindly mirror diagrams, gameplay coordinates, numeric strings or every
directional symbol. Test mixed-direction player names, numbers and messages.

Keep locale formatting at the display boundary. Store amounts and timestamps in
their defined representation; do not parse a formatted label back into game
logic. Store-provided purchase pricing should retain its authoritative localized
presentation rather than being reconstructed from a guessed exchange rate.

## Godot workflow

The [internationalisation guide](https://docs.godotengine.org/en/stable/tutorials/i18n/internationalizing_games.html)
covers translation resources, message contexts, plurals, text expansion testing
and bidirectional UI. Named placeholders help translators reorder a message;
plural rules are not universally an English singular/plural condition.
Pseudolocalisation is useful for untranslated keys and expansion, but actual
target scripts still need testing. Validate any required text-server/font data
in release exports, especially after size optimisation.

Use the installed version's supported translation import format and extraction
workflow. Keep source text, translations, translator context and reviewed export
artifacts versioned together. When source meaning changes, mark translations for
review rather than silently reusing their former approval.

## QA and rollout

Test missing-key fallback, unsupported locale, runtime language change, restart,
expanded text, placeholders at zero/one/many values, actual target fonts and
mixed-direction text. Check all monetisation/privacy/exit controls at the
smallest supported viewport. Confirm that a language setting does not reset game
progress and that accessibility settings remain intact.

Record linguistic review separately from layout/engine checks. A fluent review
does not prove the exported font is present; pseudolocalisation does not prove
the copy is correct. Release only the locales that meet the declared coverage,
and make fallback behavior deliberate rather than showing raw internal keys.
