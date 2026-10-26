# Compression and clean packaging recipes

Official Godot sources checked **2026-10-26**. Select documentation matching the
game's installed engine version and renderer. Apply changes to a representative
asset group first, retain source masters, reimport and compare release builds.

## Textures

In Godot's Import dock, `Process > Size Limit` caps the longest dimension while
preserving aspect ratio. Choose dimensions from the largest actual on-screen
use, including UI scaling, rather than shipping every source at authoring size.

`Compress > Mode` separates disk and GPU-memory behavior. `Lossy` can reduce disk
size without reducing decoded VRAM; `VRAM Compressed` targets GPU memory too.
`Basis Universal` trades encoding/load transcode and quality for small packaged
textures. Test detailed UI, alpha edges, normal maps and pixel art before broad
conversion. Match ASTC/ETC2 and high-quality options to actual renderer/device
support. Atlas and material reuse should preserve correct padding and filtering.

Source: [Godot image import](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html).
The source image extension is not a reliable description of the imported runtime
representation. Keep mipmaps when needed to avoid shimmering; measure their cost
instead of disabling them indiscriminately.

## Audio

For WAV imports, inspect `Force > Mono`, `Force > Max Rate` and compression
choices only where listening tests support them. Preserve stereo cues where
they carry useful information. Avoid forcing 8-bit audio as a blanket reduction.
Use compressed long-form music/ambience when its decoding cost is acceptable;
short frequently overlapping effects may have different CPU/latency needs.
Trim unnecessary silence and duplicates, verify loop seams and loudness, and
test peak simultaneous playback on the target phone.

Source: [Godot audio import](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html).
Do not promise that a smaller encoded file uses proportionally less playback
memory, CPU or battery.

## Models and animations

Reuse materials/textures and inspect whether each exported GLB embeds duplicate
copies. Remove unused animation tracks, excessive keys and hidden authoring
geometry after checking gameplay attachments and dynamic references. Compare
mesh precision/compression against silhouettes, skinning and animation at phone
scale. `Generate > LODs` in
[advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html)
can reduce rendered complexity, but extra LOD data is not automatically a smaller
download. Keep package and rendering budgets separate.

## Export only the intended game

Godot's Resources export modes include selected scenes/resources with dependencies
and an exclusion mode. Review the actual export inventory. Script-constructed
paths, JSON content tables and optional scenes need explicit coverage; an orphan
report alone is not permission to delete an asset. Verify all dynamically loaded
content in the exported build. Source PSD/Blend masters, alternative generations,
marketing videos and test reports should not leak in through broad export filters.

Source: [Godot export resources](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html).
Keep `.import` settings/versioned source metadata required for reproducibility;
do not randomly delete import configuration to make the repository look smaller.
Godot may legitimately export generated imported resources: inspect the shipped
artifact before classifying them as junk.

## Engine and native dependencies

Measure a release export with no game content to understand the engine/SDK floor.
Inspect Gradle/native frameworks and every mediation adapter's incremental cost;
do not include multiple libraries doing the same job without a reason. Verify
dependency removals through actual ad, purchase, privacy and startup paths.
Keep debug symbols for crash analysis outside the consumer payload where the
platform supports that separation; do not delete the symbol archive.

If engine code dominates, consider a reproducible custom release template with
only required features. Godot documents `optimize=size` / `size_extra`, LTO and
build profiles in [build-size optimisation](https://docs.godotengine.org/en/stable/engine_details/development/compiling/optimizing_for_size.html).
Feature detection can miss runtime use. Profile performance and test all content,
languages and native integrations; do not remove text shaping, codecs or 3D
features merely because the opening scene does not use them. Version and retain
the build profile/toolchain for future releases.

## Maintain a size ledger

Attribute each material increase to a player benefit, asset group or dependency.
Compare identical device variants and tooling before/after. Review largest files
and byte growth in CI, with separate manually recorded store/device measurements.
A new compression dependency must save enough in the final artifact to justify
its own code, maintenance, startup and runtime cost.
