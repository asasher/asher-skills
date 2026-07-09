# Probe eval — maquette sign-off gates via review-loop (issue #3)

Captured against branch `3-maquette-review-loop` HEAD `45afb8c` (final, post-review — no fixer commits).
Primary test per `docs/agents/verifying.md`: the changed skill's probe scenarios driven through two
independent executors and graded against the answer key in `skills/maquette/evals/probes.md`.

Probes P11/P12 target the retrofitted sign-off **mechanism** (proves ac-1, ac-3, ac-7).

| Probe | Executor #1 (Opus) | Executor #2 (codex / gpt-5.5) | Answer-key criterion |
|-------|--------------------|-------------------------------|----------------------|
| P11 (BRIEF sign-off) | PASS | PASS | Render BRIEF.md → HTML w/ stable ids, serve+await via `review-loop`, branch on verdict; proceed only on approve; request_changes → revise + ledger + re-serve. Cite SKILL.md phase-1 gate + sign-off.md. |
| P12 (JOURNEYS sign-off) | PASS | PASS | Present JOURNEYS.md through `review-loop` before phase-4 data design; no self-approval. Cite SKILL.md phase-3 gate + sign-off.md. |

## Executor #1 (Opus) — answers + citations
- **P11 — PASS.** Action: render `BRIEF.md` to self-contained HTML with stable ids, serve+await through the
  `review-loop` skill, branch on the exit-code verdict; proceed only on approve. Cited `SKILL.md` phase-1
  gate ("present `BRIEF.md` for sign-off through the `review-loop` skill … proceed only on an approving
  verdict") and `references/sign-off.md`.
- **P12 — PASS.** Action: `JOURNEYS.md` sign-off goes through `review-loop` before phase-4 data design; no
  self-approval. Cited `SKILL.md` phase-3 gate and `references/sign-off.md`.

## Executor #2 (codex / gpt-5.5, read-only) — answers + citations
- **P11 — PASS.** "Render BRIEF.md … then serve/await it via review-loop", cited `sign-off.md`.
- **P12 — PASS.** "JOURNEYS.md must get review-loop sign-off with an approving verdict before phase 4",
  cited `SKILL.md` phase-3 gate.

## Static eval-coherence checks (ac-7)
- `evals/probes.md`: P11/P12 present with answer keys; Scoring line reads "12 probes × executors" (was 10).
- `evals/build-eval.md` hard gate #1: "Approved means a review-loop approve verdict: each deliverable is
  rendered, served through the `review-loop` skill, and awaited."

Result: both executors PASS both probes; eval coherence confirmed.
