---
name: codex-imagegen
description: Generate versioned raster assets through a configured CLIProxyAPI gateway, native Codex, or an explicitly authorized OpenAI API key. Use for one image, independently generated scene layers, or named sprites extracted from a sheet.
---

# Codex Imagegen

1. Choose **flat**, **layered**, or **spritesheet** mode. Use SVG/CSS/canvas for vector or code-native deliverables.
2. Select the execution backend using [backend configuration](reference/backends.md): configured CLIProxyAPI first, native Codex otherwise, direct OpenAI API last with an available Platform key and explicit user permission. Resolve this before generation; a failed or ambiguous request stops the run.
3. Run the bundled scripts from the working project, resolving script paths from this skill. Generate sequentially and preserve each reported artifact.
4. Inspect the outputs against the mode's checks below. Report the backend, requested model/size, decoded dimensions, artifact paths, and any visual limitations.

## Artifact contract

Files and directories share an immutable version family: `scene.png`, `scene-v2/`, `scene-v3.png`. Completed and partial generations remain available for inspection.

For transparency, generate against a flat key color and remove it with the bundled chroma-key script. Prefer magenta for green, brown, or gray subjects; use green for subjects without green. Pillow and NumPy ship as declared dependencies in `requirements.txt`.

## Flat

Use `scripts/codex_imagegen.py --subject "SUBJECT" --out assets/raw/name.png`. Use `--prompt-file FILE` for an authored prompt, preserving the solid-key requirements for transparency. Then run `scripts/chroma_key.py INPUT OUTPUT --key magenta`.

For sequential batches, pass `--batch FILE --outdir DIR` with `[{"name":"name","subject":"SUBJECT"}]`. Existing sufficiently large outputs are skipped; `--new-version` intentionally regenerates them. The first failed request stops the batch and preserves completed outputs.

Inspect subject, composition, decoded dimensions, and every keyed edge.

## Layered

Read [the scene plan and artifact contract](reference/layered-mode.md), then run `scripts/codex_imagegen.py --layers PLAN.json --out scene`.

Generate the backdrop separately and each movable object against its own key background. Derive the composite from these assets. Reconstruction from a flattened source is outside this mode.

Inspect each layer and the composite. Confirm manifest z-order, placement, raw dimensions, and declared resizing. Failed runs preserve their partial manifest and completed layers.

## Spritesheet

Read [slicing rules](reference/spritesheet-slicing.md) before choosing geometry, [prompt rules](reference/spritesheet-prompts.md) before generating a sheet, and [validation rules](reference/spritesheet-validation.md) before extraction.

Run `scripts/extract_spritesheet.py --in SHEET --cols N --rows N --names NAMES --out DIR --validate --expect N`. Use `--slice components` for separated packed objects, or `--generate "SUBJECT"` to generate the source through the selected backend. The source is retained inside the artifact. Backend options are shared with the flat generator; consult `--help` for optional controls.

Confirm expected count and names, and inspect a contact sheet. Read [the manifest schema](reference/spritesheet-manifest.md) when integrating the assets.

## Keying failures

Subject holes indicate a conflicting key color; regenerate with the other key. Surviving key pixels call for inspecting the edge, then adjusting `--key-lo`/`--key-hi` or supplying the exact key. Shared `scripts/image_key.py` owns the alpha ramp and despill.
