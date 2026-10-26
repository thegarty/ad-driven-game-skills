---
name: game-art-audio-and-content
description: Define and implement a coherent mobile game art, audio and content pipeline, including asset briefs, runtime budgets and reusable content rules. Use for production direction and integration rather than acquisition-ad creative.
license: MIT
---
# Game art, audio and content

Create a small coherent production system that supports gameplay readability and can expand within the team's budget.

## Establish direction and constraints

Inspect the current game, target devices, engine/import settings, camera, orientation and asset provenance. Preserve a deliberate existing style unless redesign is requested. Define a visual hierarchy for player, threat, interactable object, reward and decoration. State the audio purpose of each cue: acknowledgement, threat, success, ambience or music.

Use [the asset brief](assets/asset-brief.md) to specify an asset family before creating many variants. Include examples of shape language, palette roles, camera scale, motion and sound character. Verify that the style communicates at actual phone size; a large concept image is not a usability test.

## Produce a representative kit

Build one representative gameplay scene with a player/object, a threat, an interaction, an outcome, UI icons and the essential sound cues. Validate the kit in the engine before scaling production. Use placeholders for unfinished content and distinguish them from approved assets.

For generated assets, preserve the prompt/settings/source or generation receipt needed to reproduce or revise the result. Use tools available in the environment; do not assume an image, audio or 3D generator is installed. Record ownership/licensing and attribution requirements for external inputs and outputs. Generation alone does not establish permission to reuse a supplied logo, character, voice or source asset.

Generate original visual alternatives when available tools can clarify a mechanic, state or style decision. Keep interface text editable/localisable, inspect mechanical truth and coherence at phone scale, and compress the selected export against the runtime/download budget. Use [content validation](references/content-validation.md) to review generated material as part of the same pipeline as other assets; no provider is required.

## Integrate for mobile

Use [the Godot content pipeline](references/godot-content-pipeline.md) for import, performance and audio checks. Set budgets from the target device and measured representative scene. Record texture size, materials, animation/particle complexity, simultaneous audio voices and download footprint where relevant. Prefer changes that retain readability when reducing effects.

Keep stable content IDs separate from display names and asset filenames. Establish naming, pivot/scale, animation hooks, export settings and fallback behaviour so a replacement asset cannot silently break gameplay. Asset variations should communicate meaningful differences rather than introduce unreadable noise.

Provide separate music/effects controls where useful, preserve settings, and define pause/background/ad-presentation behaviour. Important gameplay information must remain available with audio or haptics disabled. Test loop boundaries, simultaneous effects, repeated UI sounds and return from interruption.

Use [the audio runtime recipe](references/audio-runtime.md) for bus routing, persistent preferences, overlapping duck/mute reasons, cue priority and voice ownership. Confirm the actual native interruption behavior on devices.

## Expand content deliberately

Build a content matrix around mechanic variation, difficulty purpose, required assets and reuse. Estimate the design, art, audio, localisation and QA effort for each new item or level. Avoid producing a large roster before validating that its differences create useful player decisions.

Use [content contracts and validation](references/content-validation.md) to separate schema/reference checks, export/runtime checks and human approval. Preserve stable IDs and define retirement/migration behavior before changing content used by existing saves.

## Deliver and check

Deliver a concise style/asset specification, a representative integrated kit or implementation plan as requested, a provenance list and measured runtime/import observations. Test legibility on the smallest supported phone, busy scenes, muted/reduced-feedback play, missing assets and representative load/resume cycles.

Separate concept approval, engine import, desktop rendering and physical-device performance evidence. A visually attractive asset is not evidence that the production pipeline or device budget is ready.
