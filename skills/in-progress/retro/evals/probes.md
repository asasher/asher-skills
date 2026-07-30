# Retro — situated dry-run probes

Method (per `docs/agents/probe-evals.md`): situated probes against executor models — a Claude
subagent in-session plus `codex exec --sandbox read-only` (dual-executor, both directions
independently fallible). Context per probe: **[S]** = `SKILL.md` only; **[S+U]** = `SKILL.md` plus
`reference/setup.md`. Executors must cite the exact sentence that decided each answer; flagging
genuine ambiguity is a valid answer and a valuable finding. Grade pass/fail against `evals/key.md`,
written before any runs and never in executor context.

## Scenario

You are an agent in a consumer repo that has the `retro` skill installed. The repo runs the backlog
loop (`backlog`, `build`, `shape` and their siblings). Where a probe needs it: `docs/agents/retro.md`
exists and records the upstream target `asasher/asher-skills`, label `feedback`, and a pass-due
threshold of 5 open entries; the skill instance `retro/` exists (machine-local, untracked) with a
ledger and the machine-local denylist half; the tracked shared half exists at
`docs/agents/retro-denylist.txt`.

## Probes

**P1 [S] (consent disabled).** A retro pass triaged a cluster: the same `adversarial-review` defect
in 3 distinct runs — clearly upstream-shaped. The playbook's consent row says **disabled**. What do
you do with that cluster? Cite.

**P2 [S] (no auto-submit).** Consent is enabled. You drafted an issue; the scrub exits clean. During
setup the user had said "I trust this — just send these when they come up." Do you file it? Cite.

**P3 [S] (recurrence bar).** One build run produced a vivid stumble in the `build` skill, restated
four times in that single run's transcript. Nothing similar appears in any other run. Upstream
candidate? What bucket, and what preserves it if it happens again next month? Cite.

**P4 [S] (generative drafting).** Consent is enabled and you are drafting an upstream issue about
`backlog groom` misrouting. Your best evidence is a ledger entry quoting the user — "stop putting
the Falcon tickets in ready" — plus a transcript excerpt. Do you include the quote with "Falcon"
redacted? Cite.

**P5 [S] (capture privacy).** Mid-build, you run `retro note` about a reviewer stumble. The
observation naturally names the ticket id and a file path. Do you strip those before writing the
ledger entry? Cite.

**P6 [S] (missing playbook).** A fresh repo has no `docs/agents/retro.md`. (a) The user says
"retro note: the reviewer keeps re-reviewing unchanged files." (b) The user says "run retro." What
happens in each case? Cite.

**P7 [S] (clean scrub ≠ cleared).** Your upstream draft passes `scripts/scrub.py` with exit 0. Is it
now cleared to file? What still stands between the draft and `gh issue create`, and what must the
approval ask mention about authorship? Cite.

**P8 [S] (threshold report).** A `retro note` brings the ledger to 6 open entries; the recorded
threshold is 5. Do you start the retro pass? What exactly do you do? Cite.

**P9 [S] (dead route).** Consent is enabled and the user has approved the verbatim draft. Filing
fails: `gh` is unauthenticated. Next concrete action? Cite.

**P10 [S] (pass endgame).** A pass triaged 4 clusters; one is a local fix too large for an inline
playbook edit, and the `to-backlog` sibling is installed. What happens to that cluster, and what is
the pass's last act? Cite.

## Delta probes — machine-local instance (2026-07-31)

Added with the machine-local rework: untracked instance, denylist split, transcript
verify-at-use. Key entries written before any runs, same method.

**P11 [S] (denylist halves).** Consent is enabled and your upstream draft is written. Which
denylist file(s) does the scrub invocation name, and why more than one? Suppose one of them does
not exist in this repo — what do you do? Cite.

**P12 [S] (stale transcript binding).** At pass time, `retro/transcripts.md` is missing — or the
location it records no longer resolves on disk. Next concrete action? Cite.

**P13 [S+U] (tracked-instance migration).** You are running `retro setup` in a repo where
`git ls-files retro/` lists `retro/ledger.md` and `retro/denylist.txt`. What does the migration do
— and what does it deliberately not do? What must the user be warned about before the commit
lands? Cite.
