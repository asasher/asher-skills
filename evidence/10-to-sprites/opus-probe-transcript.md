# Opus probe transcript — issue #10 to-sprites

Executor: in-session Opus subagent (Agent tool, fresh `general-purpose`). Skill read cold from SKILL.md + references only; answer key (`evals/probes.md`), `selfcheck.py`, and the plan withheld. Verbatim answers below.

## P1 — Green 4x4 isometric sheet, 16 named tiles

**Command** (verbatim from the Command Surface example, which already matches this exact case — green sheet, 4x4, 16 names):
```sh
python3 skills/to-sprites/scripts/extract_spritesheet.py \
  --in sheet.png --cols 4 --rows 4 --key auto \
  --names grass,dirt,stone,sand,water,shoreline,roads,wood,lava,snow,forest,mountain,farmland,bridge,cliff,ice \
  --out sheet-sprites --validate --expect 16 --contact-sheet preview.png
```
`--key auto` is correct because the background is a flat green border ring: *"`auto` samples the dominant border-ring color"* (SKILL.md, Pipeline step 2). Grid order maps names row-major: *"the first name maps to row 0 col 0, the second to row 0 col 1"* (slicing.md, Grid).

**Files that should appear** — under `sheet-sprites/`: 16 assets in `<out>/assets/` (SKILL.md Pipeline step 5), a `spritesheet.json`, and the `preview.png` contact sheet. Names combine index + supplied label, e.g. `tile_01_grass.png` … through `tile_16_ice.png` (manifest.md example element `"name": "tile_01_grass"`, `"asset": "assets/tile_01_grass.png"`).

**Facts that prove it worked** — manifest: `key` records `{ "color": "#00FF00", "method": "border-sample" }` and 16 element objects, each with `sheet_rect`/`trimmed_bounds`/`anchor`/`pivot`/`css.background-position`/`frame` (manifest.md schema). Validation (all four checks must pass, else nonzero exit): exactly 16 elements via `--expect 16`, no empty cells, every asset's four corner pixels alpha 0, and no residual key-color remnants (validation.md, Checks; SKILL.md Validation).

## P2 — No source, "16 isometric terrain tiles"

**Use `--generate`**, which shells out to the sibling by subprocess, not import: *"the script shells out by command template instead of importing another skill"* (SKILL.md, Generate Source).

**Prompt constraints** (prompts.md, Grid Sheet Prompt — 16 tiles = a 4x4 grid): a fixed grid with exact rows/columns and equal cell size, no overlaps; a solid flat key background covering the whole image (pure magenta `#FF00FF` or pure green `#00FF00`); one centered element per cell with transparent-able padding; no shadows touching neighboring cells; no text, labels, checkerboard, gradients, or decorative background; and no subject pixels matching/nearly matching the key color. **Key choice: magenta** — *"Use magenta for green/brown/gray subjects such as foliage, terrain, stone"* (prompts.md, Key Choice), which fits terrain.

**Optional sibling & composition:** `codex-imagegen`, *"composed by name/subprocess only for `--generate`. The extractor imports no sibling files and degrades cleanly when the sibling is absent"* (SKILL.md, Dependency Surface). Invoked via the command template `codex_imagegen.py --subject {subject} --key magenta --out {out}` (SKILL.md, Generate Source).

**Manifest record:** `source` becomes an object, not a string — `{ "path": "...generated-source.png", "generated": true, "subject": "..." }` (manifest.md, "When `--generate` is used"; SKILL.md: *"the manifest records `source.generated: true` plus the subject"*).

## P3 — Packed non-grid sheet: empty cells + key remnants

**Extraction mode:** switch to `--slice components` — *"Use `--slice components` for packed or gridless sheets where each sprite is an isolated opaque blob after keying"* (slicing.md, Components); validation.md's "Common Fixes" for wrong count says *"for packed sheets, switch to `--slice components`."*

**Key flags to try next** for the key remnants: *"widen the ramp with a higher `--key-hi`, or regenerate on a key color that is not present in the subject"* (validation.md, Common Fixes → Key remnants); or pass an explicit `--key #RRGGBB` instead of `auto`. Note components mode also *"requires separation. Touching sprites merge into one component"* (slicing.md).

**Never overwrite:** the source — *"Open the source read-only. Never write to or over `--in`"* (SKILL.md, Pipeline step 1). (Existing outputs are also protected unless `--force`, step 5.)

**QA artifact for visual inspection:** write a contact sheet with `--contact-sheet PATH` (SKILL.md Command Surface / Output flags; Pipeline step 5).
