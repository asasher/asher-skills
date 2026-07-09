# Pre-deployment evals: situated probes + scripted dry-runs

## Problem

A skill is a prompt. Before deploying (or after reworking) one, the cheap question that predicts failure is
not "is the skill well written" but "does an executor model, situated mid-task, do the right next thing?"
Live smoke tests answer this too late and too expensively.

## When to use

Before first deployment or after any substantial rework of a skill — especially stateful skills whose
mistakes compound across sessions. Two tiers, run in order:

- **Tier 1 — situated probes**: tests whether executor models *comprehend* the skill's wording.
- **Tier 2 — scripted dry-run**: tests whether the skill's *tool mechanics* (git protocols, servers,
  worktrees) actually work, in a sandbox, with no model in the loop.

## Tier 1: situated dry-run probes

Validated 2026-07-04 (triage skill, 20/20) and reused since (bayes 20/20 before ship; maquette). The rules:

1. **Situated probes, not quiz questions.** "You are at step X, criterion 3 fails — what is your next
   concrete action?" beats "what does the skill say about X".
2. **Context fidelity.** Run separate sessions per real deployment context: a command-surface session
   (SKILL.md in context) vs a dispatched-thread session (only the dispatch prompt, no SKILL.md). This tests
   whether disclosed references stand alone.
3. **Require citations.** "Cite the file and exact sentence that decided it" makes pointer-following
   observable instead of vibes.
4. **Answer key written before any runs.** Grade pass/fail against it.
5. **Executors are the actual deployment targets.** An Opus subagent via the Agent tool, plus
   `codex exec --sandbox read-only` for the Codex side. (~115k tokens total for 4 sessions × 5 probes.)
6. **Ambiguity is a valid answer.** Instruct executors to flag it — the flagged ambiguities are routinely
   the most valuable findings.

Canonical written-out example: `skills/maquette/evals/probes.md` (probes + method header; key kept
separate until runs are graded).

## Tier 2: scripted dry-run

When the skill's risk is in tool mechanics rather than wording, script the whole protocol against a
sandbox and assert invariants at every step.

Canonical: `skills/fair-deal/eval/protocol-dryrun.sh` — exercises the full two-party negotiation protocol
with a bare local repo standing in for the remote and two clones playing the partners; 35 checks (privacy
firewall, turn alternation, shared-state integrity); scaffolds into a fresh `mktemp` dir each run and
never touches this repo; exits non-zero on any FAIL.

## How to adopt

1. Create `evals/` (or `eval/`) in the skill and ship the assets in-repo — probes, answer key, and any
   dry-run script live with the skill so reworks re-run them (shadixfy and maquette both do this).
2. Write probes for the moments the skill is most likely to be misread: first user message, an ambiguous
   user answer, a mid-loop failure, a resume after a gap.
3. Run Tier 1; fix wording until executors pass; only then spend on a Tier 2 sandbox run if the skill has
   tool mechanics worth scripting.

## Gotchas

- Writing the answer key *after* seeing model output invalidates the eval — you'll grade toward whatever
  the model said.
- Don't probe only the happy path; the value is in failure-branch and resume probes.
- Billing: Claude executors run in-session (Agent tool), never via `claude -p`; Codex executors run via
  `codex exec` on the subscription. See CLAUDE.md § Staffing.

## Instances

triage (method origin), bayes, maquette (Tier 1); fair-deal (Tier 2); shadixfy (`evals/evals.json`
harness shipped in-skill); skill-loop consumes these harnesses as its eval input.
