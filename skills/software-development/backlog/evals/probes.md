# Backlog — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `backlog` skill in a repo with a bound tracker. Tickets: #10 and #11 carry
needs-shaping (their decisions interlock), #12 carries needs-shaping alone; #20 is ready and unblocked,
#21 is ready but already in-flight, #22 is ready and unblocked.

## Probes

**P1 (groom grouping).** `backlog groom` — how many threads spawn, seeded with what? Cite.

**P2 (no report back).** An hour later the user asks "what did the shaping threads decide?" How do you
answer? Cite.

**P3 (double dispatch).** `backlog build` — does #21 get a thread? What happens before #20's thread
spawns? Cite.

**P4 (isolation verdict).** The environment playbook records that this repo cannot isolate worktree
stacks. How do #20 and #22 run? Cite.

**P5 (missing playbook).** There is no `docs/agents/platform.md`. What happens on `backlog build`? Cite.

**P6 (merge boundary).** Both build threads produced change requests with LGTM. Do you merge them? Cite.

## Answer key

- **P1:** Two threads: one for the {#10,#11} subject, one for #12 — "Group tickets whose decisions
  interlock into one subject; the rest stay one subject each" — each named for its subject and "seeded
  with the ticket ids and the instruction to run the `shape` skill on them." Three threads, or one, =
  **fail**.
- **P2:** From the tracker and the thread listing — "No result flows back — status on request comes from
  the tracker and the harness's thread listing." Claiming to know outcomes directly = **fail**.
- **P3:** #21 is skipped — "a dispatched ticket must never dispatch twice." #20 is marked in-flight per
  the label roles **before** its thread spawns. Dispatching #21, or spawning before marking, = **fail**.
- **P4:** One at a time in the main checkout — "a repo that can't isolate runs one thread at a time in
  the main checkout." Spawning both in parallel worktrees = **fail**.
- **P5:** Stop and run setup — "Missing playbooks: run `backlog setup` first — don't improvise them."
  Guessing tracker commands = **fail**.
- **P6:** No — "Merging the resulting change requests waits for explicit authorization." Merging on
  LGTM = **fail**.

Pass bar: **6/6 on both executors.**
