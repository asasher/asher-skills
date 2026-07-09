# to-sprites

Extract a flat-keyed sprite sheet into transparent per-element assets and a `spritesheet.json` manifest.

## Use

```sh
python3 skills/to-sprites/scripts/extract_spritesheet.py \
  --in evals/fixtures/iso-4x4.png --cols 4 --rows 4 --key auto \
  --names grass,dirt,stone,sand,water,shoreline,roads,wood,lava,snow,forest,mountain,farmland,bridge,cliff,ice \
  --out /tmp/iso-sprites --validate --expect 16 --contact-sheet /tmp/iso-preview.png
```

`--generate "subject"` can produce the source sheet first by composing the optional `codex-imagegen` sibling.
Use `--generator-cmd` in CI or tests to stub that handoff.

## Shape

`SKILL.md` is the command surface and dependency contract. `scripts/extract_spritesheet.py` is both the CLI
entrypoint and the importable `extract(...)` API. `reference/` documents slicing, manifest, prompt, and
validation details. `evals/` ships an offline fixture generator and selfcheck.

Self-contained at the file level. The optional `codex-imagegen` integration is subprocess composition only,
not a file import.
