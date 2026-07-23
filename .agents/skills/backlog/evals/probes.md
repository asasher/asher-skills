# Backlog — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `backlog` skill in a repo with a bound tracker. Tickets: #10 and #11 carry
needs-shaping (their decisions interlock), #12 carries needs-shaping alone (same subsystem as #10/#11);
#13 carries no readiness label and its description reads fully settled; #20 is ready and unblocked,
#21 is ready but already marked building, #22 is ready and unblocked.

## Probes

**P1 (groom sweep & gate).** `backlog groom` — which tickets enter grooming, how are they grouped, and
what exists before the user says anything? Cite.

**P1b (single batch).** The user approves one batch holding #10–#12. What spawns, and what happens to
the labels? Cite.

**P2 (two dispatch shapes).** An hour later the user asks "what did the shaping threads decide, and how
are the builds going?" How does each half get answered? Cite.

**P3 (double dispatch).** `backlog build` — is #21 dispatched? What happens before #20's subagent
spawns, and via which skill does the dispatch go? Cite.

**P4 (isolation verdict).** The environment playbook records that this repo cannot isolate worktree
stacks. How do #20 and #22 run? Cite.

**P5 (missing playbook).** There is no `docs/agents/platform.md`. What happens on `backlog build`? Cite.

**P6 (merge boundary).** Both builds produced change requests with LGTM. Do you merge them? Cite.

**P7 (resume).** The previous dispatcher session died mid-fleet. This fresh session runs `backlog
build` and finds #30 marked building with a claim comment from this runner naming branch `30-x`, and
#31 marked building with a claim comment from a different actor. What happens with each, and what runs
before any new dispatch? Cite.

**P8 (wedged build).** #20's build passes its deadline with no completion signal. What happens? Cite.

## Answer key

- **P1:** #10–#13 are swept ("unlabeled tickets and tickets carrying the needs-shaping role") but #13
  is routed, not shaped — "a ticket whose decisions are already settled routes to the ready role." The
  rest group as subjects {#10,#11} and {#12} ("tickets whose decisions interlock form one **subject**"),
  batched together or apart by belonging. Nothing spawns or mutates yet — "until they approve, the
  tracker is untouched and no thread exists." Spawning threads or writing labels before confirmation,
  or shaping #13, = **fail**.
- **P1b:** Nothing spawns — "A single batch spawns nothing: this session becomes the shaping thread and
  runs the `shape` skill itself" — after marking #10–#12 shaping per the label roles ("a ticket never
  gets two threads"). Spawning a thread for the lone batch, or leaving labels unmarked, = **fail**.
- **P2:** Shaping: from the tracker and the thread listing — "no result flows back" for threads. Builds:
  this session supervises them — "each build's completion wakes it, and it relays the outcome." Claiming
  to know shaping outcomes directly, or having nothing to say about builds, = **fail**.
- **P3:** #21 is skipped — "a dispatched ticket must never dispatch twice." #20 is marked building per
  the label roles first, then "dispatch the `build` skill on it via the `to-subagent` skill, in its own
  worktree." Dispatching #21, spawning before marking, or spawning a thread instead, = **fail**.
- **P4:** One at a time in the main checkout — "a repo that can't isolate at all builds one ticket at a
  time in the main checkout." Spawning both in parallel worktrees = **fail**.
- **P5:** Stop and run setup — "Missing playbooks: run `backlog setup` first — don't improvise them."
  Guessing tracker commands = **fail**.
- **P6:** No — "Merging the resulting change requests waits for explicit authorization." Merging on
  LGTM = **fail**.
- **P7:** "**The tracker is the run ledger**: the claim comment and the outcome comment are its
  events" — "on resume, reconcile the claims this runner owns against live worktrees and branch tips
  before dispatching anything new." #30 is this runner's to reconcile; #31 belongs to the other actor
  (the policy's § Building hygiene governs whose claim is whose). Re-dispatching #31, or dispatching
  new work before reconciling, = **fail**.
- **P8:** "a build past it with no completion is checked — worktree, branch tip, process — and
  respawned or reported, so a wedged build surfaces instead of sitting silent." Waiting indefinitely
  on the completion wake = **fail**.

Pass bar: **9/9 on both executors.**
