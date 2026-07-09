# Evidence — #27 Harden setup-asher-skills audit-mode

Verified against branch HEAD `64bb459`. The skill is prompt-driven, so the proof is a
**probe-eval transcript + pass/fail table** (`docs/patterns/probe-evals.md`), not a screenshot.

## Method

Each behavioral probe (P7–P11) plus a regression probe (R) was run **cold** — no answer key —
through **both** deployment executors, per the skill's dual-executor design (`environment.md`
§ Model staffing, checker role):

- **Claude in-session** (Opus) via the Agent tool, reading the skill's files.
- **gpt-5.5** via `codex exec -s read-only --skip-git-repo-check`.

Every answer had to cite the exact file + sentence. A probe passes **only if both executors pass**,
graded against `skills/setup-asher-skills/evals/answer-key.md`. This repo is the fixture: it exhibits
all five gaps live (skills-but-no-block; `.claude/skills/*` symlinked to `.agents/skills/*`;
`writing-great-skills` from `mattpocock/skills`; is the source repo).

The gpt-5.5 executor's cold answers are captured verbatim in
[`gpt55-executor-transcript.md`](./gpt55-executor-transcript.md).

## Verdict

| Criterion | Gap | Probe | Claude (Opus) | gpt-5.5 | Result |
|---|---|---|---|---|---|
| ac-1 | A routing | P7: skills installed, no block → setup or audit? | audit; cites 3-state routing; notes Missing-map writes the block | audit; same citation; flags "traceable to this repo" nuance | ✅ PASS |
| ac-2 | B `.agents/` scan | P8: skill only under `.agents/skills/` — seen? | reads both harness dirs at both scopes; sees it | same; cites audit-mode.md step 2 | ✅ PASS |
| ac-3 | C overlap | P9: same skill in `.claude`+`.agents` (symlinked) — drift? | not drift; note-only vs divergent-copies flagged | same; cites symlink-resolution + Overlap bullet | ✅ PASS |
| ac-4 | D foreign | P10: `writing-great-skills` from `mattpocock/skills` | Foreign-source finding; advise-only; no reinstall | same; checked local `skills/`, concludes honest "we don't ship it" | ✅ PASS |
| ac-5 | E self-catalog | P11: auditing the source repo, branch ahead | local `skills/` as catalog; states ahead-of-origin | same; cites step-1 self-host | ✅ PASS |
| ac-6 | regression | R: greenfield route? drift mechanism? | greenfield → setup; drift by model-read, no version stamp | same; cites SKILL.md greenfield + no-stamp section | ✅ PASS |

**All six criteria PASS on both executors.**

## Supplementary file-checks (ac-6 invariants)

- Diff is Markdown-only across `SKILL.md`, `audit-mode.md`, `interview.md`, `probes.md`, `answer-key.md`
  — no script, server, or runtime added.
- No version stamp / `vNN` / content-hash introduced (grep over the implementation diff); the no-stamp
  invariant and the prompt-driven posture hold.
- Probes P1–P6 and their answer keys are untouched.
