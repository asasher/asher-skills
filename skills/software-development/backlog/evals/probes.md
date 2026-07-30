# Backlog — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**
(plus the one bundled reference a probe names), exact-sentence citation per answer. Ambiguity flagged
with a citation is valid. Key before runs.

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

**P1b (single batch).** The user approves one batch holding #10–#12. What is prepared and spawned, and
what happens to the labels? Cite.

**P2 (two dispatch shapes).** An hour later the user asks "what did the shaping threads decide, and how
are the builds going?" How does each half get answered? Cite.

**P3 (double dispatch).** `backlog build` — is #21 dispatched? What happens before #20's subagent
spawns, and via which skill does the dispatch go? Cite.

**P4 (isolation verdict).** The environment playbook records that this repo cannot provide worktree
isolation. How do #20 and #22 run? Cite.

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

**P15 (plan readability).** You are about to present the groom plan covering #10–#13 and a proposed
closure of #18. What does each ticket's line in the plan carry, and should the user need the tracker
open to follow it? For this probe, replace the earlier description of #13 with the thin body "fix the
thing" — what digest do you present for it? Cite.

**P16 (changed shaping branch).** A shaping batch's branch contains ADR and ticket-context changes.
What is presented before readiness is requested? The user then says "ready for agent." When do its
tickets become ready, and what exactly did that phrase authorize? Cite.

**P17 (clean shaping branch).** A shaping batch reaches the readiness signal without changing the
repository. What happens to its worktree and labels? Cite.

**P18 (one build directory).** #20's subagent is implementing, then verifying, opening the change
request, fixing adversarial findings, and capturing evidence. How many worktrees cover that lifecycle,
and may a downstream skill request harness-native isolation? Cite.

**P19 (prepare failure).** After the batch is marked shaping, worktree bootstrap fails before its
thread spawns. What happens to the roles, ownership record, and a worktree containing bootstrap residue?
Cite.

**P20 (setup, machine-fact classification).** During `backlog setup`, reconciling a repo's
`docs/agents/environment.md`, you find the line "Codex CLI authed (`codex --version` → 0.145.0)".
Read `reference/machine-facts.md`. Classify this fact, say what the reconciled playbook carries
instead, and name the only file that may record the CLI's version at all. Cite.

**P21 (build preflight, stale stamp).** `backlog build`'s preflight runs
`scripts/check-machine-facts.py` and it exits nonzero with `stale docs/agents/staffing.md: recorded
machine 'Other-Mac' is not this machine 'This-Mac' (probed 2026-07-26)`. What is this finding, and
what happens before any dispatch? Cite.

## Answer key

- **P1:** #10–#13 are swept ("tickets carrying **no readiness role** ... and tickets carrying the needs-shaping role") but #13
  is routed, not shaped — "a ticket whose decisions are already settled routes to the ready role". The
  rest group as subjects {#10,#11} and {#12} ("tickets whose decisions interlock form one **subject**"),
  batched together or apart by belonging. Nothing spawns or mutates yet — "until they approve, the
  tracker is untouched and no thread exists." Spawning threads or writing labels before confirmation,
  or shaping #13, = **fail**.
- **P1b:** Mark #10–#12 shaping, prepare one batch worktree, and spawn one `to-thread` session in its
  exact directory — "This is also the one-batch path: the dispatcher never shapes in the primary
  checkout." Record batch id, base, branch, path, and intended thread owner on every ticket. Running
  the batch in the dispatcher, omitting ownership, or leaving labels unmarked = **fail**.
- **P2:** Shaping: from the tracker and the thread listing — "no result flows back" for threads. Builds:
  this session supervises them — "each build's completion wakes it, and it relays the outcome". Claiming
  to know shaping outcomes directly, or having nothing to say about builds, = **fail**.
- **P3:** #21 is skipped — "a dispatched ticket must never dispatch twice". #20 is marked building,
  its worktree is prepared via `worktree`, the claim is updated with base/branch/path/cleanup owner,
  then `build` is dispatched via `to-subagent` "with that exact directory." Dispatching #21, spawning
  before marking/preparing/recording ownership, or spawning a thread = **fail**.
- **P4:** Neither runs — "a repo that cannot provide worktree isolation does not dispatch builds and
  hands the claim back with the capability gap surfaced." Running either in the primary checkout =
  **fail**.
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

- **P15:** Every named ticket carries "its id, its title, and a one-or-two-sentence digest drawn from
  its body", relations "said in words — '#12 blocks #14' ... never bare id lists"; the user "never
  needs the tracker open to follow it." For #13: no digest is invented — "A body too thin to digest is
  presented as exactly that — thinness is a groom finding, never a licence to invent a digest."
  Bare-id relationship lists, title-only lines, or a fabricated digest for #13 = **fail**.

- **P16:** Commit/propose the shaping change and present its exact current head before requesting
  readiness. The whole batch stays shaping until that request is merged, the merge is verified, and
  the worktree is removed. The later blessing "authorizes merging that shaping change only"; it does
  not authorize unrelated merges or an unpresented head. Labeling early or presenting only after the
  signal = **fail**.
- **P17:** Remove the clean shaping worktree, clean up its branch, and mark the entire batch ready —
  "a clean shaping worktree is removed, its branch is cleaned up, and the whole batch becomes ready."
  Keeping either isolation artifact or splitting batch readiness = **fail**.
- **P18:** Exactly one worktree covers the whole pipeline; "downstream skills must not create another
  worktree" and "harness-native worktrees are not requested." Creating review/evidence worktrees or
  asking the harness to isolate again = **fail**.
- **P19:** Restore the former roles and record the failure. Preserve the residue-bearing worktree and
  ownership record for recovery, surfacing its path and blocker — "If prepare or bootstrap left files,
  preserve the worktree and its ownership record for recovery while restoring the roles." Deleting the
  residue, leaving the batch claimed shaping, or falling back to primary = **fail**.

- **P20:** Verify-at-use, the default class — "The playbook records the *probe command* — one that
  exercises the capability itself (`gh auth status`, a bounded executor echo), never a version string
  standing proxy for it — and never the probe's result." The reconciled line keeps a
  capability-exercising liveness probe and drops the recorded version; the version's only home is the
  staffing playbook's probe record, as metadata — "Model and capability reachability — routes,
  dispatch aliases, effect-probe verdicts — lives only in the staffing playbook's probe record
  (`docs/agents/staffing.md`), the CLI versions its probes observed riding along as that record's
  metadata; an environment or platform playbook restating a route, an alias, or a version is drift."
  Keeping the version in environment.md, moving it to the machine-local overlay, or classifying it an
  expensive probe cache = **fail**.
- **P21:** A stale machine-record stamp — the checker's exit is the drift signal, and dispatch waits:
  "The preflight also runs this skill's `scripts/check-machine-facts.py` against the repo — a stale
  stamped record or a missing declared overlay is the same drift, fixed by re-running the owning
  setup before dispatch." Dispatching anyway, treating the finding as advisory, or hand-editing the
  stamp to match instead of re-running the owning setup = **fail**.

Pass bar: **22/22 on both executors.**
