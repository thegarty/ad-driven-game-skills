# Copy patterns with preserved meaning

Original synthetic examples. These are starting points for the stated feature
contract, not mandatory strings or universal lengths. Localise naturally; do
not enforce English word counts in other languages.

| Situation | Less useful | Proposed copy / presentation | Essential condition |
|---|---|---|---|
| First tower placement | A paragraph describing every tower, enemy and currency | “Place a tower” beside a legal highlighted pad, with a ghost preview | The task is safe and cancellable; further strategy is available later |
| Upgrade | “Do you wish to proceed with enhancement?” | “Damage 12 → 15” and “Upgrade · 40 seeds” | Show actual cost and currency; guard repeat submissions |
| Rewarded offer | “Claim!” on a video icon | “Watch ad · Get 50 seeds” plus “Continue” | The reward is exactly 50, earned under the disclosed completion condition |
| Ad unavailable | Modal explaining an SDK error | “No ad available. Try again later.” near the offer | Free continue stays usable; no promise of a retry time you cannot guarantee |
| Durable save failed after earning | “Success! Reward added!” | “Reward pending. We’ll retry saving.” | Use only if retry/recovery actually exists; otherwise explain the available recovery action |
| Lose run | Long list of failure statistics | “You earned 35 seeds” plus one attainable next upgrade | Display only confirmed earnings; details remain available |
| Irreversible reset | “Are you sure?” | “Delete local progress?” with exact scope and “Keep progress” / “Delete” | Clearly distinguish local progress, cloud data and purchases; describe the real consequences |
| Purchase | “Remove all ads” while rewarded offers remain | “Remove forced ads” with nearby scope covering optional rewarded offers | Use only if accurate; decide treatment of rewarded benefits and restoration before sale |

## Decide how much text is necessary

Ask: what must the player know to act correctly now? Keep that information in
the immediate surface. Put explanation of *why*, advanced strategy and optional
details one step away when the immediate decision remains informed. Use short
headings, familiar verbs, explicit amounts and consistent feature names.
Avoid both long prose and cryptic icon-only navigation.

Do not split one necessary sentence into six Next panels. Do not make each
button need another paragraph explaining it. If a mechanic needs repeated
lengthy explanation, reconsider its controls or rules. A diagram can reduce
ambiguity but can also introduce visual clutter or unfamiliar symbolism.

Preserve prices, duration, expiry, limits, conditions, destructive effects and
meaningful consent choices. Confirm the actual entitlement before naming it.
An ad reward is not “free” if the label conceals the required ad view. Use real
expiry times, not artificial urgency. Write neutral decline labels.

## Localisation and accessibility

Store strings by stable semantic keys, with translator context and plural rules.
Pass complete sentences with placeholders; do not concatenate word fragments.
Do not abbreviate important numbers ambiguously around a spend decision. Test
expanded text, right-to-left layouts, screen-reader labels and repeated exposure.
Use voice or animation as supplements, not the only instruction. Let players
pause or replay important teaching, and keep a persistent path to help.

## Trigger rules matter as much as wording

A hint should have an eligibility condition, mechanic version, completion rule,
dismissal state, cooldown and replay entry. Distinguish seen from understood.
Do not persist “mastered” simply because a prompt was displayed. An expert may
skip basics; a returning player may request a refresher. A player who repeatedly
fails needs a more useful hint or safer practice, not the same sentence louder.
