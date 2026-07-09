---
name: to-sprites
description: Extract flat-keyed sprite sheets into transparent per-element PNG/WebP assets plus spritesheet.json manifests. Use when Codex needs to slice generated or hand-made sprite sheets, remove a chroma key background by auto border sample or supplied hex color, trim and name tiles, produce CSS/engine frame metadata, validate extraction quality, create a contact sheet, or optionally start from a prompt by composing the codex-imagegen sibling skill before extraction. Codex-first asset pipeline for game, web, and prototype sprites.
argument-hint: "[--in sheet.png | --generate subject] [--cols N --rows N] [--names a,b,...]"
---

# to-sprites

`to-sprites` turns a flat-background sheet into usable sprite assets: key the background, slice the sheet,
trim each element, export transparent assets, and write `spritesheet.json`. It is a deterministic asset
pipeline, not an image generator. When the starting point is a prompt, `--generate` delegates the source
sheet to the optional `codex-imagegen` sibling and then runs the same extractor.

This skill intentionally uses Python 3 with `numpy` and `Pillow`. That is a plan-sanctioned deviation from
the repo's usual stdlib-only default because image work needs Pillow; the sibling `codex-imagegen` has the
same dependency floor. Install with `pip install -r skills/to-sprites/requirements.txt` when needed.

## Command Surface

Run the bundled entrypoint:

```sh
python3 skills/to-sprites/scripts/extract_spritesheet.py \
  --in sheet.png --cols 4 --rows 4 --key auto \
  --names grass,dirt,stone,sand,water,shoreline,roads,wood,lava,snow,forest,mountain,farmland,bridge,cliff,ice \
  --out sheet-sprites --validate --expect 16 --contact-sheet preview.png
```

Use `--help` for the full argparse surface. The core flags are:

- Source: `--in PATH` or `--generate "SUBJECT"`; `--generator-cmd` stubs or overrides generation.
- Slicing: `--slice grid|components`, `--cols`, `--rows`, `--tile WxH`, `--margin L,T`, `--spacing X,Y`.
- Keying: `--key auto|none|#RRGGBB`, `--key-hi`, `--key-lo`.
- Output: `--out DIR`, `--format png|webp|both`, `--names`, `--pad`, `--anchor`, `--force`,
  `--contact-sheet PATH`.
- Verification: `--validate` and `--expect N`.

The script is also importable:

```python
from extract_spritesheet import extract

manifest = extract("sheet.png", cols=4, rows=4, key="auto", out_dir="sheet-sprites")
```

## Pipeline

1. Open the source read-only. Never write to or over `--in`.
2. Key the flat background unless `--key none`: `auto` samples the dominant border-ring color; `#RRGGBB`
   uses a supplied key. Alpha is a Euclidean RGB distance ramp with despill on semi-transparent fringe pixels.
3. Slice by grid or connected components. Load [slicing](reference/slicing.md) when choosing or debugging a
   slicing mode.
4. Trim each element to opaque content, keep optional transparent `--pad`, assign row-major names, anchors,
   pivots, CSS metadata, and frame metadata.
5. Refuse to overwrite existing output files unless `--force`, then write assets under `<out>/assets/`,
   `spritesheet.json`, and an optional contact sheet.

## Manifest

`spritesheet.json` records the source, sheet size, slicing parameters, key method, and one element object per
extracted sprite. Each element carries `name`, `index`, `row`, `col`, `sheet_rect`, `trimmed_bounds`, `asset`,
`size`, `anchor`, `pivot`, `css.background-position`, and `frame`. Load
[manifest](reference/manifest.md) for the full schema and consumer notes.

## Generate Source

With `--generate "SUBJECT"`, the script shells out by command template instead of importing another skill:

```sh
python3 skills/codex-imagegen/scripts/codex_imagegen.py --subject {subject} --key magenta --out {out}
```

The generated source is handed into the normal pipeline, and the manifest records `source.generated: true`
plus the subject. If `codex-imagegen` is absent or the generator command fails, `--generate` exits with an
actionable error; file-input extraction still works. Load [prompts](reference/prompts.md) before asking for a
new sheet, because the same flat-key prompt rules make generation and extraction reliable.

## Validation

`--validate` checks asset count, empty grid cells, transparent asset corners, and residual key-color remnants.
`--expect N` makes the count check exact. Any failed check exits nonzero. Load
[validation](reference/validation.md) when interpreting a failure or tightening a sheet prompt.

## Dependency Surface

- **Bundled references** — this skill's own contract, shipped in-directory: [slicing](reference/slicing.md),
  [manifest](reference/manifest.md), [prompts](reference/prompts.md), and
  [validation](reference/validation.md), plus `scripts/extract_spritesheet.py` and the offline evals.
- **Project playbooks** — none. `to-sprites` does not install repo-specific playbooks.
- **Optional sibling skill** — `codex-imagegen`, composed by name/subprocess only for `--generate`. The
  extractor imports no sibling files and degrades cleanly when the sibling is absent.
