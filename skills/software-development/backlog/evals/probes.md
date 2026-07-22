# Backlog — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `backlog` skill in a repo with a bound tracker. Tickets: #10 and #11 carry
needs-shaping (their decisions interlock), #12 carries needs-shaping alone; #20 is ready and unblocked,
#21 is ready but already marked building, #22 is ready and unblocked.

## Probes

**P1 (groom grouping).** `backlog groom` — how many threads spawn, seeded with what, and what happens
to the tickets' labels? Cite.

**P2 (two dispatch shapes).** An hour later the user asks "what did the shaping threads decide, and how
are the builds going?" How does each half get answered? Cite.

**P3 (double dispatch).** `backlog build` — is #21 dispatched? What happens before #20's subagent
spawns, and via which skill does the dispatch go? Cite.

**P4 (isolation verdict).** The environment playbook records that this repo cannot isolate worktree
stacks. How do #20 and #22 run? Cite.

**P5 (missing playbook).** There is no `docs/agents/platform.md`. What happens on `backlog build`? Cite.

**P6 (merge boundary).** Both builds produced change requests with LGTM. Do you merge them? Cite.

## Answer key

- **P1:** Two threads: one for the {#10,#11} subject, one for #12 — "Group tickets whose decisions
  interlock into one subject; the rest stay one subject each" — each subject marked shaping ("a subject
  never gets two threads") and "seeded with the ticket ids and the instruction to run the `shape` skill
  on them." Three threads, one thread, or unmarked subjects, = **fail**.
- **P2:** Shaping: from the tracker and the thread listing — "no result flows back" for threads. Builds:
  this session supervises them — "each build's completion wakes it, and it relays the outcome." Claiming
  to know shaping outcomes directly, or having nothing to say about builds, = **fail**.
- **P3:** #21 is skipped — "a dispatched ticket must never dispatch twice." #20 is marked building per
  the label roles first, then "dispatch the `build` skill on it via the `to-subagent` skill, in its own
  worktree." Dispatching #21, spawning before marking, or spawning a thread instead, = **fail**.
- **P4:** One at a time in the main checkout — "a repo that can't isolate builds one ticket at a time in
  the main checkout." Spawning both in parallel worktrees = **fail**.
- **P5:** Stop and run setup — "Missing playbooks: run `backlog setup` first — don't improvise them."
  Guessing tracker commands = **fail**.
- **P6:** No — "Merging the resulting change requests waits for explicit authorization." Merging on
  LGTM = **fail**.

Pass bar: **6/6 on both executors.**
