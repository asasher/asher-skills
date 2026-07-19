# Goodwork v3 pre-ship eval — runner brief

For a **fresh session** (clean context — do not run from the session that authored the rework). Preferred
surface: Claude Code desktop, repo worktree `asher-skills-worktrees/goodwork-viz`, branch `goodwork-polish`
(if this session is cloud-cloned, make sure that branch is pushed first). Discipline:
`docs/agents/probe-evals.md`. Assets under test: `skills/personal/goodwork/` on this branch.

## Order

**Tier 2 first (cheap, mechanical):**
```
bash skills/personal/goodwork/evals/dryrun.sh
```
Record the full output. Any FAIL stops the eval — fix mechanics before spending on probes.
(Authoring baseline 2026-07-19: 12/12 pass.)

**Tier 1 — situated probes, dual-executor.** Probes: `skills/personal/goodwork/evals/probes.md`.
Key: `skills/personal/goodwork/evals/key.md` — **grader-only; never in any executor's context.**

For each probe, run both executors with ONLY the context the probe's tag names ([S] = SKILL.md;
[S+R] = SKILL.md + the one named reference):
1. **Claude executor:** a fresh general-purpose subagent. Paste the context files' contents into its
   prompt (do not let it browse the repo — context fidelity is the point), then the probe verbatim, then:
   "Answer with your next concrete action(s). Cite the file and exact sentence that decided it. If the
   skill is genuinely ambiguous here, say so — that is a valid answer."
2. **Codex executor:** `codex exec --sandbox read-only` from the worktree root with the same rule: name
   the context file paths it may read, the probe, the citation requirement. If codex is unavailable,
   record the direction as unavailable and proceed asymmetrically — do not fake the second executor.

Grade each answer pass/fail against the key. Collect every flagged ambiguity verbatim — those are
findings, not noise.

**Verdict table:** probe × executor → pass/fail/ambiguity, with one-line evidence per fail. Write it plus
raw executor transcripts to `goodwork-workspace/eval/runs/<date>-v3/`. Ship bar: all probes pass both
executors (or the wording gets fixed and the failed probes re-run — record both rounds).

**Tier 3 — human-in-the-loop:** hand the human `goodwork-workspace/eval/walkthrough/WALKTHROUGH.md`
(seeded workspace beside it). This tier is judged by the human; your only job is to leave the seed
untouched until they start.

## Report

End with: Tier-2 count, Tier-1 table, ambiguity findings list, and — after the human runs Tier 3 — their
station verdicts, all in the run directory. No fixes from this session: findings route back to the
authoring branch as issues, not live edits mid-eval.
