---
name: codex-imagegen
description: Generate real raster images headlessly through the Codex CLI's built-in image_gen tool (no OPENAI_API_KEY — runs off the ChatGPT login), then chroma-key them into transparent PNGs. Use to produce game/app assets, sprites, textures, icons, or illustrations from a coding agent that has no image model of its own.
argument-hint: "[subject] [--key magenta|green] [--out path]"
---

# Codex Image Generation (headless)

Codex CLI can generate real bitmap images via its built-in `image_gen` tool, authenticated by the user's **ChatGPT login — no `OPENAI_API_KEY` required**. The catch is that from `codex exec` the tool is easy to get wrong: with the sandbox on it silently no-ops and reuses a previous image, and even on success it never writes a file — the PNG is base64 inside the session transcript. This skill encodes the recipe that actually works, recovered by trial.

Use it when a coding agent needs raster art (sprites, tiles, textures, mockups, illustrations) and has no image model. For vector/icon work that should stay code-native, don't use this — draw SVG.

## The five things that make it work

1. **Bypass the sandbox.** `codex exec --dangerously-bypass-approvals-and-sandbox`. With `-s read-only`/`workspace-write` the image tool cannot run; codex will claim it "generated inline" and then hand back a *stale* earlier image (or nothing). This one flag is the difference between real output and silent failure.
2. **The bytes are in the session transcript, not a file.** After a run, the image is a base64 string inside `~/.codex/sessions/**/*.jsonl` on a payload of `type: "image_generation_call"` (PNG base64 starts with `iVBORw0KGgo`; sometimes a `data:` URL or JPEG `/9j/`). It is NOT written to disk, NOT in `--json` stdout, NOT reliably in `~/.codex/generated_images/` under exec.
3. **Sequential only.** Never run two codex image generations in parallel — concurrent processes write overlapping sessions and the fresh-session detection breaks. Batch = a sequential loop.
4. **Disambiguate by prompt keywords, not recency.** Other codex processes pollute recent sessions. Match the extracted image's `revised_prompt` against subject keywords; fall back to the largest payload. Never "grab the newest session."
5. **Flat key background, then key it out yourself.** Codex fakes "transparent" requests by painting a checkerboard, so ask for a **solid flat key color** and remove it locally. Pick the key by subject: **magenta `#FF00FF`** for green/brown/grey subjects (trees, rock, wood, buildings); **green `#00FF00`** only when the subject has no green (and never for pink/magenta subjects). Green-on-green eats foliage edges.

## Generate one asset

```
python3 scripts/codex_imagegen.py \
  --subject "a cozy top-down oak tree, round leafy canopy, storybook game-asset style" \
  --key magenta --size 1024 --out assets/raw/oak-tree.png
```

`--subject` wraps your text in a prompt that pins the flat key background, dimensions, and "no checkerboard / no text / no pure-key pixels in the subject". For full control pass `--prompt-file FILE` instead (you own the whole prompt, but keep the flat-key-background clause). The script marks the time, runs codex with the bypass flag, then extracts the freshest matching image from the session transcript and writes it to `--out`. Runs take ~1–3 min.

## Make it transparent

The generated PNG has a flat key background. Remove it:

```
python3 scripts/chroma_key.py assets/raw/oak-tree.png assets/oak-tree.png --key magenta
```

This keys the flat color, despills the fringe, feathers the edge, and trims to content bounds. (Codex also ships an equivalent at `~/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py`.)

## Batch (sequential)

```
python3 scripts/codex_imagegen.py --batch batch.json --outdir assets/raw --key magenta
```

`batch.json` is `[{"name": "oak-tree", "subject": "..."}, ...]`. The script loops **one at a time**, skips names whose output already exists (resumable), and logs progress. For N assets budget ~1.5–2 min each.

## Verify — silence is not success

Always open the result. Failure modes to check for:
- **Stale image**: you asked for X and got a prior unrelated image → the bypass flag was missing, or keyword matching failed. Re-run; confirm `matched_kw > 0` in the log.
- **Checkerboard background**: you asked for transparency instead of a flat key color → re-prompt with a solid key fill.
- **Keyed holes**: the subject contained the key color (green foliage on a green key) → regenerate on the other key color.

## Fallback: the CLI path (needs a key)

Only when an `OPENAI_API_KEY` is available *and* the user asks for the CLI/API path (a fully scriptable, deterministic `image_gen.py` with true transparency). See [api-key-path](reference/api-key-path.md).
