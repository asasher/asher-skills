# Probe-eval verdict — issue #1, `staffing` skill

Captured against branch `1-extract-staffing` final HEAD `1f05997` (post adversarial-review fix), after the Reviewer's `LGTM` at iteration 2.

**Method:** the 14 situated probes in `skills/staffing/evals/probes.md` driven through both deployment-target executors per `docs/patterns/probe-evals.md` — an Opus in-session subagent and gpt-5.5 via `codex exec -s read-only`. The answer key was withheld from both executors; each answered from the skill files and had to cite the deciding sentence. Graded pass/fail against the key in `probes.md`.

**Result: 28/28 PASS (14 probes × 2 executors). Zero ambiguity flags.**

| Criterion | Probe(s) | Opus (in-session) | gpt-5.5 (`codex exec`) |
|-----------|----------|-------------------|------------------------|
| ac-1 self-contained + frontmatter | P1 (+ grep) | PASS | PASS |
| ac-2 dependency surface (3 kinds) | P2 | PASS | PASS |
| ac-3 roles + fallback preserved | P3 | PASS | PASS |
| ac-4 rankings vs capabilities separate + taste gate | P4, P6, P14 | PASS | PASS |
| ac-5 task-pins distinct from ranking | P5 | PASS | PASS |
| ac-6 machine-audit, not hardcoded | P7, P8 | PASS | PASS |
| ac-7 two-layer install, delta-only | P9 | PASS | PASS |
| ac-8 scope-decision both branches | P10, P11 | PASS | PASS |
| ac-9 LLM-audit reconcile, no stamps | P12 (+ grep) | PASS | PASS |
| ac-10 Codex compatibility | P13 (+ YAML parse) | PASS | PASS |
| ac-11 probe eval green + verdict table | this eval | PASS (28/28 dual-executor) | — |

**Structural checks (file-level, both PASS):** no cross-skill file imports (grep clean); no `vNN`/version stamps introduced (grep clean — the only matches are the skill's own prose stating it deliberately uses none); `agents/openai.yaml` parses with `interface` + `policy.allow_implicit_invocation: false`; the machine-audit example table carries its "Example of audit output (illustrative only — NOT the shipped roster)" label.

Full executor transcripts: `opus-transcript.md`, `gpt55-transcript.md` (this directory).
