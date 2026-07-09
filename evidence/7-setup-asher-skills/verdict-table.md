# Verification — setup-asher-skills (#7)

Skill = a prompt; "running it" = an executor model reading it and doing the right next thing
(`docs/agents/environment.md` § Driving the app). Two seams: structure/grep checks and dual-executor
situated probes (`docs/patterns/probe-evals.md`). A probe passes only if **both** executors pass it.

- Executors: **Claude (Opus)** in-session via the Agent tool, and **gpt-5.5** via `codex exec -s read-only
  --skip-git-repo-check`.
- Answer key written before runs: `skills/setup-asher-skills/evals/answer-key.md`.
- Transcripts: `probe-eval-opus.md` (Claude), `probe-eval-codex.txt` (gpt-5.5). Structure checks:
  `structure-checks.txt`.
- Adversarial review: **LGTM with one optional nit** (orthogonal `-g`/`-y` flag phrasing); nit applied in
  commit `d1a82db` before evidence.

## Per-criterion

| AC | Criterion | Seam | Opus | gpt-5.5 | Result |
|----|-----------|------|------|---------|--------|
| ac-1 | SKILL.md frontmatter (name/description/argument-hint/user-invocable) | structure | — | — | PASS |
| ac-2 | three-part `## Dependency surface` | structure | — | — | PASS |
| ac-3 | full file layout present | structure | — | — | PASS |
| ac-4 | every install command targets asasher/asher-skills only | grep | — | — | PASS |
| ac-5 | closure rules stated in catalog | grep | — | — | PASS |
| ac-6 | no version-stamp mechanism in audit-mode | grep | — | — | PASS |
| ac-7 | probes.md ≥6 probes, both executors, key separate | structure | — | — | PASS |
| ac-8 | P1 three-part audit (repo/machine-via-staffing/user) | probe | PASS | PASS | PASS |
| ac-9 | P2 one-decision interview + dependency-guarantee (plan⇒+review-loop+staffing, announced) | probe | PASS | PASS | PASS |
| ac-10 | P3 pull-from-this-repo-only (refuse external, offer ours or say we don't ship it) | probe | PASS | PASS | PASS |
| ac-11 | P4 `## Agent skills` block + delegated playbook writes, no ask-asher router | probe | PASS | PASS | PASS |
| ac-12 | P5 audit-mode on re-invoke, drift by LLM read not stamps | probe | PASS | PASS | PASS |
| ac-13 | P6 project-first scope, global only for staffing (consent) | probe | PASS | PASS | PASS |

**13/13 PASS.** Both executors 6/6 on the probes; all 7 structure/grep checks pass.

Deliberately unchecked (per plan § How it will be checked): the subjective quality of the interview copy —
left to human review on the presentation surface, not mechanically graded.
