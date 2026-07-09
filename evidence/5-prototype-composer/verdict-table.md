# Verification verdict — issue #5, prototype thin-composer skill

Method: file/structure checks + situated probe scenarios driven through **two independent executors**
(Opus subagent in-session + gpt-5.5 via `codex exec`, answer key withheld), graded against
`skills/prototype/evals/probes.md` — the dual-executor design of `docs/patterns/probe-evals.md`. Criteria are
the approved plan's ac-1..ac-9 (`plans/5-prototype-composer.html`).

| criterion | codex (gpt-5.5) | opus (in-session) | file-check | result |
|-----------|-----------------|-------------------|------------|--------|
| ac-1 layout parity with siblings | PASS (P1) | PASS (P1) | ✓ ls | **PASS** |
| ac-2 frontmatter (composer/throwaway/beyond-code) | PASS (P2) | PASS (P2) | ✓ parse | **PASS** |
| ac-3 three-part dependency surface | PASS (P3) | PASS (P3) | ✓ grep | **PASS** |
| ac-4 composition by name only | PASS (P4) | PASS (P4) | ✓ grep | **PASS** |
| ac-5 generalized beyond code | PASS (P5) | PASS (P5) | — | **PASS** |
| ac-6 framing + four gates | PASS (P6) | PASS (P6) | — | **PASS** |
| ac-7 probe: code question | PASS (P7) | PASS (P7) | — | **PASS** |
| ac-8 probe: non-code / outside dev | PASS (P8) | PASS (P8) | — | **PASS** |
| ac-9 no regression to backlog | AMBIG (P9)* | AMBIG (P9)* | ✓ git-diff | **PASS** |

\* P9 came back AMBIGUOUS from both executors — a probe-scoping artifact: the method withheld backlog's
files from the executor read set, so neither could confirm-by-reading that backlog was untouched. ac-9 is
confirmed independently by the git-diff below. Folded back as an eval-wording fix (commit 007d354) so future
P9 runs grant read access.

## File checks (orchestrator, direct)

- **ac-1** — `skills/prototype/` ships `SKILL.md README.md reference/prototyping.md agents/openai.yaml evals/probes.md` — same skeleton as `skills/staffing/` and `skills/review-loop/`.
- **ac-2** — frontmatter parses; `name: prototype`, `user-invocable: true`, `argument-hint` present; description contains "composer", "throwaway", and a beyond-code phrase.
- **ac-3** — SKILL.md § Dependency surface declares bundled references / project playbook / sibling skills, states `prototype` is a composer, names review-loop + staffing.
- **ac-4** — SKILL.md, README.md, reference/ contain zero `skills/review-loop/` or `skills/staffing/` paths; siblings appear by plain name (4× ``​`review-loop`​`` , 4× ``​`staffing`​`` in SKILL.md). The only such path strings anywhere are in `evals/probes.md`, as the probe checking for the anti-pattern.
- **ac-9** — `git diff a6b9030..HEAD -- .claude/skills/backlog/reference/prototype.md .claude/skills/backlog/templates/prototyping.md docs/agents/prototyping.md` → empty (untouched).

## Adversarial review

PR #19 reviewed by an independent checker (opus-4.8) against `docs/agents/pr-reviewer.md` → **LGTM**,
iteration 1, no actionable findings.
