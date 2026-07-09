# Verification verdict — issue #10, `to-sprites` skill

Captured against branch `10-sprite-sheet-extractor` final HEAD `3c86490` (post adversarial-review fix), after the Reviewer's `LGTM` at review iteration 2.

Two independent verification surfaces, both green:

## 1. Mechanical — `selfcheck.py` (real image I/O)

`evals/selfcheck.py` drives the real extractor against the committed deterministic fixture `evals/fixtures/iso-4x4.png` and asserts each acceptance criterion on the returned manifest + written files (Pillow reads back corner alpha, counts, schema). **Result: ALL PASS (15 assertions across ac-1…ac-14), exit 0.** Full run: `selfcheck-transcript.txt`.

| Criterion | What selfcheck asserts | Verdict |
|-----------|------------------------|---------|
| ac-1 keyed→transparent→assets | every exported PNG's 4 corners alpha=0 | PASS |
| ac-2 4×4 grid → 16 elements | 16 assets; manifest 16 elements; row/col 0–3 row-major | PASS |
| ac-3 non-destructive + `--force` | re-run w/o `--force` refuses; source bytes unchanged (hash) | PASS |
| ac-4 documented CLI | `--help` lists every flag | PASS |
| ac-5 manifest completeness | each element has all required keys incl `css.background-position` + `frame` | PASS |
| ac-6 `--validate`/`--expect` | passes on `--expect 16`, fails on `--expect 99` | PASS |
| ac-7 key modes | `auto`, `#00FF00`, and `none` all work | PASS |
| ac-8 connected components | `--slice components` extracts >1 blob (16 on fixture) | PASS |
| ac-9 naming + order | `tile_01_grass.png` present; deterministic across two runs | PASS |
| ac-10 WebP/PNG alpha | `--format webp` and `both` preserve alpha | PASS |
| ac-11 documented prompts | prompt guidance present in `reference/prompts.md` | PASS |
| ac-12 contact sheet | `--contact-sheet` writes a valid image | PASS |
| ac-13 Codex surface | `agents/openai.yaml` present + well-formed | PASS |
| ac-14 generate-source composition | stubbed `--generator-cmd` records `source.generated`+subject; bogus cmd fails cleanly | PASS |

Plus a sanity assertion: every `trimmed_bounds` lies within its `sheet_rect`.

## 2. Dual-executor situated probes (does the skill communicate itself?)

The 3 situated probes in `evals/probes.md` driven through **both** deployment-target executors per `docs/patterns/probe-evals.md` — an Opus in-session subagent and gpt-5.5 via `codex exec -s read-only`. The answer key was withheld from both; each answered from the skill files (SKILL.md + references) and cited the deciding sentence. Graded pass/fail against the key in `probes.md`.

**Result: 6/6 PASS (3 probes × 2 executors).**

| Probe (criteria) | Answer-key essentials | Opus (in-session) | gpt-5.5 (`codex exec`) |
|------------------|-----------------------|-------------------|------------------------|
| P1 (ac-1,2,5,6,9) | grid command + `--key auto` + `--validate --expect 16`; 16 named assets, manifest fields, alpha corners | PASS | PASS |
| P2 (ac-11,14) | `--generate`; flat-key/isolated/no-key-in-subject prompt rules; magenta for terrain; codex-imagegen optional, subprocess-composed; manifest records `source.generated`+subject | PASS | PASS |
| P3 (ac-3,7,8,12) | `--slice components`; explicit `--key #hex` / higher `--key-hi`; never overwrite source; `--contact-sheet` | PASS | PASS |

Both executors independently chose magenta as the correct key for terrain (P2) and both identified `source` becoming an object with `generated`+`subject`. Full transcripts: `opus-probe-transcript.md`, `gpt55-probe-transcript.md`.

## Visual artifacts (no browser — manifest + contact sheet)

Headless-Chrome screenshots are blocked in this environment; the observable output surface is the manifest and the generated files. `spritesheet.json` (this dir) is the fixture's full 16-element manifest; `c12-contact-sheet.png` is the QA contact sheet of all 16 extracted transparent tiles (proves ac-2 + ac-12 visually).
