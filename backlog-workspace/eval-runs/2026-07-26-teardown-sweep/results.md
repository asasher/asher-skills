# Probe run — backlog teardown sweep (ticket #83)

Method: `docs/agents/probe-evals.md` Tier 1, dual-executor per the staffing repo delta. Prompt:
`prompt.md` (scenario + 13 probes + SKILL.md verbatim, no answer key). Key: written in
`skills/software-development/backlog/evals/probes.md` before any run. Executors: an in-session Claude
subagent (sonnet, the Claude-side floor) and gpt-5.6-sol via
`codex exec -s read-only --skip-git-repo-check` (`run-codex.sh`; transcript
`run-codex-gpt-5.6-sol.txt`).

Three rounds were run, 13/13 on both executors in every round. Round 1 hit the pre-polish wording of
one groom sentence (its tail clause "(that direction and its quiet horizon continue unchanged
alongside)" was rewritten for authoring-context leakage before review). Round 2 ran the shipped
SKILL.md text but a probe fixture named the leave-alone worktree's branch `20-z`, colliding with
ticket #20's pre-dispatch state in the base scenario (verifier finding); the fixture was renamed
`42-z`. Round 3, on the shipped text and corrected fixture, is the run of record; its transcripts are
the ones stored here.

## Round 3 verdicts (shipped text, corrected fixture)

| Probe | Decision point | key demands | codex gpt-5.6-sol | claude sonnet |
|---|---|---|---|---|
| P1 | groom sweep & gate | plan only; #13 routed not shaped | pass | pass |
| P1b | single batch | no spawn; mark shaping | pass | pass |
| P2 | dispatch shapes | tracker/threads vs supervised fleet | pass | pass |
| P3 | double dispatch | skip #21; mark then to-subagent | pass | pass |
| P4 | isolation verdict | one at a time, main checkout | pass | pass |
| P5 | missing playbook | stop, run setup | pass | pass |
| P6 | merge boundary | never merge on LGTM | pass | pass |
| P7 | resume | reconcile own claims; other actor's untouched | pass | pass |
| P8 | wedged build | check worktree/branch/process; respawn or report | pass | pass |
| P9 | squash-merged clean tree | auto-reap; upstream-gone/CR-state, never ancestor check; env before working copy | pass | pass |
| P10 | merged dirty tree | surface for confirmation, never silent delete | pass | pass |
| P11 | live branch | leave alone | pass | pass |
| P12 | label-orphaned stack | seen despite absent worktree; surfaced, not auto-removed | pass | pass |

**Result: 13/13 on both executors — pass bar met.**

Valid flagged ambiguities (not failures, both with correct actions taken): the respawn-vs-report
choice for a wedged build is left to judgment; another actor's dead claim is groom's concern, not
build's; whether a surfaced label-orphaned stack is then auto-reaped or confirmed is unstated — every
executor still surfaced it rather than removing it, the behavior the key demands.
