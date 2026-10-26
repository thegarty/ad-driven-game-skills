# Content contracts and validation

A content pipeline should catch invalid or inconsistent assets before they reach
a player's save. This is an authoring/release recipe; it is not a claim that the
library contains a production content validator.

## Contract before volume

For each content family, define stable ID, schema revision, display/localisation
keys, required asset references, gameplay parameters with units/ranges, unlock
requirements, compatible ruleset and fallback. Keep raw source masters, exported
runtime assets, import settings and approval status distinguishable. Asset file
names and translated labels are not durable gameplay identities.

Synthetic defender record: `defender_bramble_01` references a sprite, attack cue,
projectile scene and description key. It defines attack interval in seconds,
range in world units and an explicit targeting rule. Changing its display name
does not change ownership. Retiring it needs a save/content migration or retained
compatibility definition; deleting the file alone is not a safe retirement.

## Validate in layers

| Layer | Checks | What passing does not prove |
|---|---|---|
| Data/schema | Required fields; types; finite numeric values; units; ranges; unique IDs | The mechanic is fun or balanced |
| References | Missing assets/keys; unknown IDs; dependency cycles where forbidden; unreachable unlocks | Dynamic runtime loading works in an export |
| Import/export | Real release import succeeds; texture/audio/font settings; required resources packaged | Phone readability or acceptable memory |
| Runtime | Instantiate representative and extreme records; trigger animation hooks/cues; unload/reload | Every content combination works |
| Human review | Visual/audio coherence, silhouette/scale, access alternatives, meaning and provenance | Measured retention or commercial performance |

Choose hard invariants based on actual rules. A cycle in a recipe graph may be
intentional, whereas a cycle in required prerequisites can make an unlock
impossible. Validate references created dynamically by IDs or generated paths;
static scene traversal will miss them. Flag apparently unused assets for review
rather than deleting them solely because a text search found no caller.

## Authoring and approval

For original generated art, first specify the asset's gameplay purpose, silhouette,
state and integration constraints. Explore a bounded set of alternatives, then
inspect them in context: correct number/position of controls, truthful ranges or
mechanic diagrams, consistent perspective, recognisable states and enough visual
separation from threats. Do not ship attractive but misleading instructional art.
Keep functional text and numbers as editable/localisable UI layers instead of
baking them into an image. Record prompts/settings, input provenance, generation
receipt, edits and rights/attribution status. Retain source masters separately;
export only the needed resolution/format and verify compression at actual size.

Use a small reviewed kit to establish dimensions, pivots, layer ordering, colour
roles, animation events, sound categories and naming. Record whether an item is
placeholder, imported, gameplay-approved, access-reviewed and release-approved;
a single “done” flag hides the remaining work. Maintain provenance/licence and
required attribution with the source and export, including generated inputs.

Separate content parameters from executable scripts where practical, validate
both, and treat downloaded content/configuration as untrusted input. Bound
payload sizes and unsupported versions; verify the intended integrity controls.
A remote asset catalog is a new update, caching and security responsibility, not
free package-size reduction.

## Compatibility and rollback

Pin content/config revision to a run when a change could alter its rules or
rewards. Define how current saves resolve retired/renamed IDs, missing optional
assets and future-schema data. A fallback should remain honest: a neutral sprite
can be acceptable temporarily, while silently substituting a differently behaving
unit may change a purchase or saved build.

For a content release, test a clean install, prior save, late unlock, offline load,
missing optional asset and rollback to the last compatible catalog. Confirm
localised font/cue resources survive compression and export filtering. Keep
errors actionable for the author: record ID, violated rule and affected runtime
path, without logging sensitive player data.

## Production batch acceptance

Deliver a content manifest, validation results, human-review exceptions, measured
runtime/package deltas and compatibility notes. Sample combinatorial interactions
based on risk, especially multi-effect attacks, seasonal overrides and large
rosters. State untested combinations explicitly. A passed schema check is
source-tested validation behavior, not a playtest or a shipped-device result.
