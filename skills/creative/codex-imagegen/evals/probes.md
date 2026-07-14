# Codex Imagegen — situated probes

Run each probe in a fresh read-only executor session with `SKILL.md` and only the reference named by that probe. Require the executor to cite the deciding file and exact sentence. Grade against `probe-answer-key.md`, which must exist before any run.

## P1 — choose layered rather than segmentation

A user supplies a scene description—forest backdrop, one hero, and two foreground plants—and says every element must animate independently. No flattened source image exists. Which mode and command do you choose, what plan do you write, and which output facts demonstrate that the workflow preserved real layers? Cite `SKILL.md` and `reference/layered-mode.md`.

## P2 — reject a recovery claim

A user supplies only a finished flattened PNG and asks layered mode to recover the original hidden pixels behind its central character. What is the next concrete action, and which promise must you avoid? Cite `SKILL.md` and `reference/layered-mode.md`.

## P3 — extract a regular sheet

A user gives a flat green 4x4 isometric tile sheet and 16 names. What command do you run, what files should appear, and what manifest/validation facts prove it worked? Cite `SKILL.md` plus `reference/spritesheet-manifest.md` and `reference/spritesheet-validation.md`.

## P4 — preserve versions across modes

`assets/scene.png` and `assets/scene-v2/` already exist. The user asks for another flat generation at `assets/scene.png`. Which path may be written, and may either existing artifact be changed? Cite `SKILL.md`.

## P5 — recover from extraction failure

A packed sheet produces empty cells, key remnants, and inspection shows that `--key auto` sampled a non-key border color. Which slicing/key changes do you try, what artifact must remain immutable, and what QA output helps visual inspection? Cite `SKILL.md`, `reference/spritesheet-slicing.md`, and `reference/spritesheet-validation.md`.
