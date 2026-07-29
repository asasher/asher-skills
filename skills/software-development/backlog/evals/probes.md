# Backlog — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are running the `backlog` skill in a repo with a bound tracker. Tickets: #10 and #11 carry
needs-shaping (their decisions interlock), #12 carries needs-shaping alone (same subsystem as #10/#11);
#13 carries no readiness label and its description reads fully settled; #20 is ready and unblocked,
#21 is ready but already marked building, #22 is ready and unblocked.

For the teardown probes (P9–P12): git's worktree listing shows, besides the main checkout, a worktree
on branch `40-x` whose change request was **squash-merged** last week (its upstream is gone; a
merge-base ancestor check against the base branch reports *not merged*) with a clean tree; a worktree
on branch `41-y` whose change request is merged but whose tree holds uncommitted changes; and a
worktree on branch `42-z` whose change request is open with review in progress. The environment
playbook records per-worktree docker stacks; `docker ps` shows a compose project whose working-dir
label points at a directory that no longer exists on disk.

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

**P9 (squash-merged, clean).** During `backlog groom`, what happens to the `40-x` worktree — and on
what evidence do you call its change request merged, given the ancestor check says otherwise? In what
order does removal proceed? Cite.

**P10 (merged, dirty).** What happens to the `41-y` worktree? Cite.

**P11 (live branch).** What happens to the `42-z` worktree? Cite.

**P12 (label-orphaned stack).** The compose project whose working-dir label points at a nonexistent
directory — does the sweep see it (its worktree is not in git's listing), and what happens to it? Cite.

**P13 (friction, retro present).** The `retro` sibling is installed. While confirming the groom plan the
user corrected the same batching mistake twice; later, a build outcome relay mentions the subagent
needed a workaround for a stale playbook row. When is each recorded, and via what? Then retro's note
verb replies "noted; 6 open entries — a retro pass is due." Do you run the pass? Cite.

**P14 (friction, retro absent).** Same stumbles, but the `retro` sibling is not installed. What happens?
Cite.

## Answer key

- **P1:** #10–#13 are swept ("tickets carrying **no readiness role** ... and tickets carrying the needs-shaping role") but #13
  is routed, not shaped — "a ticket whose decisions are already settled routes to the ready role". The
  rest group as subjects {#10,#11} and {#12} ("tickets whose decisions interlock form one **subject**"),
  batched together or apart by belonging. Nothing spawns or mutates yet — "until they approve, the
  tracker is untouched and no thread exists." Spawning threads or writing labels before confirmation,
  or shaping #13, = **fail**.
- **P1b:** Nothing spawns — "A single batch spawns nothing: this session becomes the shaping thread and
  runs the `shape` skill itself" — after marking #10–#12 shaping per the label roles ("a ticket never
  gets two threads"). Spawning a thread for the lone batch, or leaving labels unmarked, = **fail**.
- **P2:** Shaping: from the tracker and the thread listing — "no result flows back" for threads. Builds:
  this session supervises them — "each build's completion wakes it, and it relays the outcome". Claiming
  to know shaping outcomes directly, or having nothing to say about builds, = **fail**.
- **P3:** #21 is skipped — "a dispatched ticket must never dispatch twice". #20 is marked building per
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
- **P9:** Reaped without asking — "A candidate with a clean tree is reaped without asking, environment
  before working copy per the environment playbook's teardown row". Merged is called on upstream-gone
  or change-request state — "detect merged squash-proof — the branch's upstream gone, or the change
  request's own recorded state — never a merge-base ancestor check, which squash merges defeat."
  Trusting the ancestor check (leaving `40-x` alone as unmerged), asking the user before reaping a
  clean tree, or removing the working copy before the environment, = **fail**.
- **P10:** Surfaced for confirmation, not deleted — "a dirty tree is surfaced for the user's
  confirmation and never silently deleted — it may hold unpushed work". Auto-reaping `41-y` = **fail**.
- **P11:** Left alone — "A worktree whose branch is live with its change request open is left alone."
  Reaping or surfacing `42-z` as a candidate = **fail**.
- **P12:** Yes — the label direction exists precisely because git's listing can't see it: "Where the
  environment playbook records container stacks, sweep one direction further: containers whose compose
  working-dir label points at a path that no longer exists are orphaned stacks — surface them for
  teardown too." Missing it because it's absent from the worktree listing, or auto-removing it rather
  than surfacing, = **fail**.

- **P13:** The groom stumble is recorded "the moment it shows via the `retro` sibling's note verb"; the
  build-relayed workaround is swept at latest at run end — "a run's end is the sweep for anything
  unnoted, stumbles relayed in build outcomes included." The pass is not run: "relay that report and
  stop — running the pass is never this dispatcher's call." Deferring all noting to run end without the
  in-the-moment note, or launching the pass = **fail**.
- **P14:** "Absent the `retro` sibling, friction goes unrecorded: say so once when there was something
  worth noting, then move on." Saying nothing, improvising a ledger by hand, or repeating the complaint
  = **fail**.

Pass bar: **15/15 on both executors.**
