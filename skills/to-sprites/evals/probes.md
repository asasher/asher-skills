# to-sprites — situated dry-run probes

Method: run situated probes against both executor targets before first deployment: an Opus subagent and
`codex exec --sandbox read-only`, with `skills/to-sprites/SKILL.md` in context plus the one referenced file
named by the probe. Require citations to the deciding file/sentence and grade against this answer key before
looking at executor output. The scripted mechanics are covered by `evals/selfcheck.py`; these probes test
whether an executor chooses the right branch.

## Probes

**P1 (ac-1, ac-2, ac-5, ac-6, ac-9).** A user gives you a flat green 4x4 isometric tile sheet and asks for
named tiles: `grass,dirt,stone,sand,water,shoreline,roads,wood,lava,snow,forest,mountain,farmland,bridge,cliff,ice`.
What command do you run, what files should appear, and what manifest/validation facts prove it worked?

**P2 (ac-11, ac-14).** A user has no source sheet and asks you to start from "16 isometric terrain tiles".
What prompt constraints do you include, which sibling skill is optional, how is it composed, and how should
the manifest record the generated source?

**P3 (ac-3, ac-7, ac-8, ac-12).** A user reports that validation found empty cells and key remnants on a
packed non-grid sheet. What extraction mode and key flags do you try next, what should you never overwrite,
and what QA artifact can you write for visual inspection?

## Answer Key

- **P1:** Run `python3 skills/to-sprites/scripts/extract_spritesheet.py --in <sheet> --cols 4 --rows 4
  --key auto --names <16 names> --out <dir> --validate --expect 16` and optionally `--contact-sheet`.
  Expected observable facts: `assets/tile_01_grass.png` through 16 assets exist, `spritesheet.json` has 16
  `elements`, rows/cols are 0..3 row-major, asset corners are alpha 0, and every element has `sheet_rect`,
  `trimmed_bounds`, `asset`, `anchor`, `pivot`, `css.background-position`, and `frame`. Citing
  `SKILL.md` command surface plus `reference/manifest.md` passes.
- **P2:** Include a fixed grid, flat solid key background, isolated non-touching elements, padding, no
  checkerboard/text/gradients, and no subject pixels near the key color. `codex-imagegen` is optional and is
  composed by subprocess command template, not imported. The manifest must record `source.generated: true`
  and the subject. Citing `reference/prompts.md` and `SKILL.md` generate-source/dependency surface passes.
- **P3:** Use `--slice components` for isolated blobs; if auto sampled the wrong border, pass
  `--key #RRGGBB`, or `--key none` only when the sheet is already alpha-correct. Never write to or over the
  source and refuse existing outputs unless `--force`. Add `--contact-sheet preview.png` for inspection.
  Citing `reference/slicing.md`, `reference/validation.md`, and `SKILL.md` pipeline passes.
