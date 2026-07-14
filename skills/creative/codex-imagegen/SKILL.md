---
name: codex-imagegen
description: Generate or extract versioned raster assets through Codex's built-in image tool. Use when the user wants one raster asset with optional transparency, an asset-first layered scene with independently animatable objects, or named sprites split from a sheet.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Codex Imagegen

## Process

1. Select exactly one mode: **flat** for one raster, **layered** for a planned backdrop plus independently generated objects, or **spritesheet** for a sheet split into named assets. Use SVG/CSS/canvas instead when the deliverable is vector or code-native. Selection is complete when one mode matches both the supplied source and the requested artifact.
2. Read only the selected mode below and the references its context pointers require. Prepare every required prompt, plan, source, name, and geometry input before execution. Preparation is complete when every input named by the selected command is explicit and available.
3. Set the shell variable `SKILL_DIR` to this skill's absolute directory; the commands below use it. Run them from the working project so relative inputs and outputs stay with the user's work. Serialize image-generation commands because concurrent sessions make result matching unreliable. Execution is complete when every command exits successfully and reports its artifact path.
4. Open each reported artifact and apply every verification check for the selected mode. The run is complete only when every requested asset exists, its version family remains immutable, and visual inspection confirms usable content and edges.

## Common contract

- Treat artifacts as immutable. The first output uses the requested name; later writes use monotonic siblings such as `scene.png`, `scene-v2/`, and `scene-v3.png`. Same-stem files and directories form one version family.
- For transparency, use one flat key color. Prefer magenta for green, brown, or gray subjects; use green only when the subject contains no green.
- Use the bundled generator rather than constructing a direct `codex exec` command. It owns the required sandbox bypass and transcript extraction mechanics.

## Flat mode

Generate one keyed raster:

```bash
python3 "$SKILL_DIR/scripts/codex_imagegen.py" \
  --subject "a cozy top-down oak tree, round leafy canopy, storybook game-asset style" \
  --key magenta --size 1024 --out assets/raw/oak-tree.png
```

Use `--prompt-file FILE` for a fully authored prompt, retaining the solid-key requirements when transparency is needed. Then remove the background:

```bash
python3 "$SKILL_DIR/scripts/chroma_key.py" \
  assets/raw/oak-tree.png assets/oak-tree.png --key magenta
```

For a sequential batch, pass `--batch batch.json --outdir DIR`; the JSON shape is `[{"name":"oak-tree","subject":"..."}]`. A rerun skips the latest sufficiently large PNG. Add `--new-version` only when intentionally iterating every item.

## Layered mode: asset-first

Before writing the plan, read [the layered scene and artifact contract](reference/layered-mode.md). Plan the layers before generating. Every movable foreground/subject object gets its own image-generation request on a flat key background; the backdrop is generated separately as a full-bleed image. The composite is derived from those layer assets, never treated as their source.

```bash
python3 "$SKILL_DIR/scripts/codex_imagegen.py" \
  --layers scene.json --out assets/forest-clearing
```

The output is a versioned directory containing prompts, raw generations, transparent layer PNGs, `manifest.json`, and `composite.png`. A failed run remains on disk with `status: "failed"` so completed layers are retained as evidence.

Do not imply reconstruction fidelity: this mode does not infer hidden pixels, split a flattened source, or use Segment Anything. If the user provides only a flattened image, stop at a flat artifact or ask them to approve a future segmentation/recreation workflow.

## Spritesheet mode

Before selecting grid geometry or components, read [the slicing rules](reference/spritesheet-slicing.md). Before using `--generate`, read [the extractable-sheet prompt rules](reference/spritesheet-prompts.md). Before using `--validate` or diagnosing extraction failure, read [the validation contract](reference/spritesheet-validation.md).

Extract a regular grid:

```bash
python3 "$SKILL_DIR/scripts/extract_spritesheet.py" \
  --in sheet.png --cols 4 --rows 4 --key auto \
  --names grass,dirt,stone,sand,water,shoreline,roads,wood,lava,snow,forest,mountain,farmland,bridge,cliff,ice \
  --out assets/terrain-sprites --validate --expect 16 \
  --contact-sheet assets/terrain-preview.png
```

Use `--slice components` for separated objects in a packed sheet. Use `--generate "SUBJECT"` instead of `--in` to create the keyed source through the bundled flat generator first. The generated source is preserved inside the directory artifact under `source/`.

Read [the manifest schema](reference/spritesheet-manifest.md) when integrating extracted assets with a consumer.

## Shared keying

Flat transparency, layered foregrounds, and sprite extraction all use `scripts/image_key.py`: a distance-based alpha ramp with despill. Accepted keys are `auto`, `none`, `magenta`, `green`, or `#RRGGBB` where the caller permits them. If edges are eaten, regenerate with the other key color; if key remnants survive, adjust `--key-lo`/`--key-hi` or provide the exact color.

## Verification

For flat output, inspect subject accuracy and composition, plus every edge when keyed. For layered output, inspect every layer independently, then confirm `manifest.json` is complete and `composite.png` reflects manifest z-order and placement. For spritesheets, use `--validate`, confirm the expected asset count and names, and inspect a contact sheet. A zero exit code alone does not pass verification.

Common failures:

- An unrelated old image means the generation was sandboxed or transcript keyword matching failed.
- A checkerboard means the prompt requested transparency rather than a solid key fill.
- Holes in the subject mean the chosen key color occurred in the subject.
- A failed layered manifest is partial evidence, not permission to overwrite that directory.

## Fallback

Only when `OPENAI_API_KEY` is available and the user explicitly wants the API/CLI route, use [the API-key path](reference/api-key-path.md).

## Dependency surface

- **Bundled:** generator, immutable path allocator, shared keyer, layered compositor, sprite extractor, references, and evals.
- **Project playbooks:** none.
- **Sibling skills:** none. Sprite generation calls the bundled generator directly.
- **External requirements:** Pillow and NumPy from `requirements.txt`; Codex CLI with an authenticated ChatGPT session for generation.
