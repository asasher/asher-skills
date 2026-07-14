# Codex Imagegen probe answer key

Written before executor runs.

- **P1:** Choose asset-first layered mode. Write a JSON scene plan with one `background` and independently described subject/foreground layers, shared `art_direction`, z-order, anchors, and positions; run `python3 scripts/codex_imagegen.py --layers scene.json --out <artifact>`. Passing evidence is a newly versioned directory with raw inputs, separate processed PNGs, a complete manifest, and a composite derived from those layers.
- **P2:** State that layered mode cannot recover an existing flattened composition or infer occluded pixels. Keep the PNG flat and ask for approval/context for a future segmentation-plus-recreation workflow; never promise original-layer or hidden-pixel fidelity.
- **P3:** Run `python3 scripts/extract_spritesheet.py --in <sheet> --cols 4 --rows 4 --key auto --names <16 names> --out <dir> --validate --expect 16`, optionally with a versioned `--contact-sheet`. Expect a new directory artifact containing 16 assets and `spritesheet.json`; manifest elements include source/frame/bounds/anchor/pivot metadata, and validation passes count, empty-cell, alpha-corner, and key-remnant checks.
- **P4:** Write `assets/scene-v3.png`. Neither `scene.png` nor `scene-v2/` may be overwritten or deleted because same-stem files and directories form one immutable version family.
- **P5:** Use `--slice components` for separated packed objects. Because inspection establishes that border auto-keying is wrong, pass the exact `--key #RRGGBB` (`none` is valid only for already-correct alpha); tolerance tuning alone cannot correct the wrong sampled color. Preserve the source and every prior output directory; the retry reserves a later directory. Write a contact sheet for visual QA and rerun validation.
