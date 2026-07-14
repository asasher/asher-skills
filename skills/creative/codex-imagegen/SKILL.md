---
name: codex-imagegen
description: Generate immutable raster image artifacts through Codex's built-in image tool. Use for flat images and transparent assets, asset-first layered scenes with independently generated layers, or keyed sprite-sheet extraction into named assets and manifests.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Codex Imagegen

Use one of three artifact modes:

1. **Flat** — generate one raster image, optionally key it into transparency.
2. **Layered** — generate a planned background and independently generated foreground/subject assets, then derive a composite. This is asset-first only: do not segment an existing flattened image.
3. **Spritesheet** — extract a keyed sheet into named transparent assets and a manifest, or generate the sheet first and then extract it.

For vector or code-native graphics, use the project's native SVG/CSS/canvas path instead.

## Invariants

- Run image generation sequentially. Concurrent Codex image sessions make transcript matching unreliable.
- The generator must use `codex exec --dangerously-bypass-approvals-and-sandbox`; sandboxed execution can silently reuse a stale result.
- Image bytes live in `~/.codex/sessions/**/*.jsonl`, not reliably in stdout or a generated-images directory. The bundled generator extracts the new image by prompt keywords and payload size.
- Treat every artifact as immutable. The first output uses the requested name; later writes use monotonic siblings such as `scene.png`, `scene-v2/`, `scene-v3.png`. A file and directory with the same stem belong to one version family.
- Use the actual output path reported by the script. Never assume the requested path was written.
- Use one flat key color for transparent assets. Prefer magenta for green/brown/gray subjects; use green only when the subject contains no green.

All commands below are relative to this skill directory.

## Flat mode

Generate one keyed raster:

```bash
python3 scripts/codex_imagegen.py \
  --subject "a cozy top-down oak tree, round leafy canopy, storybook game-asset style" \
  --key magenta --size 1024 --out assets/raw/oak-tree.png
```

Use `--prompt-file FILE` for a fully authored prompt, retaining the solid-key requirements when transparency is needed. Then remove the background:

```bash
python3 scripts/chroma_key.py \
  assets/raw/oak-tree.png assets/oak-tree.png --key magenta
```

For a sequential batch, pass `--batch batch.json --outdir DIR`; the JSON shape is `[{"name":"oak-tree","subject":"..."}]`. Existing completed families are resumable. Add `--new-version` only when intentionally iterating every item.

## Layered mode: asset-first

Plan the layers before generating. Every movable foreground/subject object gets its own image-generation request on a flat key background; the backdrop is generated separately as a full-bleed image. The composite is derived from those layer assets, never treated as their source.

```bash
python3 scripts/codex_imagegen.py \
  --layers scene.json --out assets/forest-clearing
```

The output is a versioned directory containing the prompts and raw generations, transparent layer PNGs, `manifest.json`, and `composite.png`. A failed run remains on disk with `status: "failed"` so expensive successful layers are not lost. See [layered mode](reference/layered-mode.md) for the scene schema and artifact contract.

Do not imply reconstruction fidelity: this mode does not infer hidden pixels, split a flattened source, or use Segment Anything. If the user provides only a flattened image, stop at a flat artifact or ask them to approve a future segmentation/recreation workflow.

## Spritesheet mode

Extract a regular grid:

```bash
python3 scripts/extract_spritesheet.py \
  --in sheet.png --cols 4 --rows 4 --key auto \
  --names grass,dirt,stone,sand,water,shoreline,roads,wood,lava,snow,forest,mountain,farmland,bridge,cliff,ice \
  --out assets/terrain-sprites --validate --expect 16 \
  --contact-sheet assets/terrain-preview.png
```

Use `--slice components` for separated objects in a packed sheet. Use `--generate "SUBJECT"` instead of `--in` to create the keyed source through the bundled flat generator first. The generated source is preserved inside the directory artifact under `source/`.

Every extraction reserves a new versioned directory rather than overwriting a prior result. Read [slicing](reference/spritesheet-slicing.md), [prompting](reference/spritesheet-prompts.md), [manifest](reference/spritesheet-manifest.md), and [validation](reference/spritesheet-validation.md) when that branch applies.

## Shared keying

Flat transparency, layered foregrounds, and sprite extraction all use `scripts/image_key.py`: a distance-based alpha ramp with despill. Accepted keys are `auto`, `none`, `magenta`, `green`, or `#RRGGBB` where the caller permits them. If edges are eaten, regenerate with the other key color; if key remnants survive, adjust `--key-lo`/`--key-hi` or provide the exact color.

## Verify

Open the reported artifact, not merely the requested path. For layered output, inspect both every layer and the derived composite. For spritesheets, use `--validate` and a contact sheet. A zero exit code does not substitute for checking that the generated subject matches the request and that keyed edges are usable.

Common failures:

- An unrelated old image means the generation was sandboxed or transcript keyword matching failed.
- A checkerboard means the prompt requested transparency rather than a solid key fill.
- Holes in the subject mean the chosen key color occurred in the subject.
- A failed layered manifest is resumable evidence, not permission to overwrite that directory.

## Fallback

Only when `OPENAI_API_KEY` is available and the user explicitly wants the API/CLI route, use [the API-key path](reference/api-key-path.md).

## Dependency surface

- **Bundled:** generator, immutable path allocator, shared keyer, layered compositor, sprite extractor, references, and evals.
- **Project playbooks:** none.
- **Sibling skills:** none. Sprite generation calls the bundled generator directly.
- **External requirements:** Pillow and NumPy from `requirements.txt`; Codex CLI with an authenticated ChatGPT session for generation.
