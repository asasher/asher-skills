# Round-2 Claude executor transcript (sonnet, in-session subagent) — final answer verbatim

# Probe Answers — `backlog` SKILL.md dry-run

**P1 (groom sweep & gate).**
Grooming sweeps in the unlabeled and needs-shaping tickets: "Sweep the tracker for unlabeled tickets and tickets carrying the needs-shaping role, or take the ids given." That means #10, #11, #12 (needs-shaping) and #13 (no readiness label) enter the sweep; #20/#21/#22 already carry the ready role and are out of scope for groom.

Routing plan: #13's description "reads fully settled," so it routes to ready — "a ticket whose decisions are already settled routes to the ready role... — the rest are shaping work." #10/#11/#12 are shaping work. Grouping: "Group that rest twice: tickets whose decisions interlock form one **subject**; subjects that belong together (same subsystem, same domain area) form one **batch**, sized to what one thread can hold." #10+#11 interlock → one subject; #12 is its own subject but same subsystem, so it joins #10/#11's subject into one batch.

Before the user says anything: nothing exists yet but the plan — "**Confirm before anything changes.** Present the plan — which tickets, which batches, what each is about, and every proposed tracker mutation... The confirmation is the gate for all of it: until they approve, the tracker is untouched and no thread exists."

**P1b (single batch).**
Nothing spawns as a separate thread: "A single batch spawns nothing: this session becomes the shaping thread and runs the `shape` skill itself." Labels: per the general execute step, "mark its tickets shaping per the label roles — a ticket never gets two threads" — so #10, #11, and #12 are all marked shaping before this session runs `shape` on them itself.

**P2 (two dispatch shapes).**
The shaping half can't be answered from this session's own memory — "Grooming is interactive — human-in-the-loop work fans out as threads the user attends, and no result flows back" — so it's answered via "status on request comes from the tracker and the harness's thread listing" (check the tickets' specs / attach to the threads). The build half is answered directly, since "This session babysits the fleet: each build's completion wakes it, and it relays the outcome" — the dispatcher already knows and reports build status itself.

**P3 (double dispatch).**
#21 is not dispatched — it is already marked building, and "a dispatched ticket must never dispatch twice." Before #20's subagent spawns: the run's preflight happens first — "Preflight once per run: the platform verbs and credentials the builds will lean on answer a cheap live read — a dead one is drift, fixed by re-running `backlog setup` before any dispatch spends a build discovering it" — then #20 is marked building with a claim comment: "mark it building per the label roles... and the claim comment carries this runner's identity per the policy's § Building hygiene." Dispatch goes "via the `to-subagent` skill, in its own worktree": "then dispatch the `build` skill on it via the `to-subagent` skill, in its own worktree."

**P4 (isolation verdict).**
They run one at a time in the main checkout, not in separate worktrees: "a repo that can't isolate at all builds one ticket at a time in the main checkout." (This follows from "Isolation and concurrency follow the environment playbook's verdicts.")

**P5 (missing playbook).**
Build does not proceed on its own improvised bindings — the top-level rule fires: "Missing playbooks: run `backlog setup` first — don't improvise them." Since `platform.md` binds the very nouns *ticket*, *label*, *change request* ("Nouns are roles: *ticket*, *label*, *change request*... bound to this repo's real tracker, review surface, and version control by `docs/agents/platform.md`"), its absence means `backlog setup` runs first.

**P6 (merge boundary).**
No. "Merging the resulting change requests waits for explicit authorization."

**P7 (resume).**
Before any new dispatch: "on resume, reconcile the claims this runner owns against live worktrees and branch tips before dispatching anything new." #30's claim names this runner, so it falls under that reconciliation — its worktree and branch tip (`30-x`) get checked against the claim before anything new is dispatched. #31's claim is from a different actor, so it is not "the claims this runner owns" — the text gives no instruction for reconciling or touching another actor's claim, so it is left outside this reconciliation step. Flagging ambiguity: SKILL.md never states what (if anything) happens to a claim owned by a different actor; only "the claims this runner owns" are named for resume reconciliation.

**P8 (wedged build).**
It gets checked, then respawned or reported: "a build past it with no completion is checked — worktree, branch tip, process — and respawned or reported, so a wedged build surfaces instead of sitting silent."

**P9 (squash-merged, clean).**
The 40-x worktree is torn down as a teardown candidate — reaped without asking, since its tree is clean. Evidence for "merged" is explicitly not the ancestor check: "detect merged squash-proof — the branch's upstream gone, or the change request's own recorded state — never a merge-base ancestor check, which squash merges defeat." Here the branch's upstream is gone, which is exactly the squash-proof signal, so it's called merged despite the ancestor check saying "not merged." Since the tree is clean: "A candidate with a clean tree is reaped without asking, environment before working copy per the environment playbook's teardown row" — so removal order is environment (docker stack) first, then working copy (the worktree) second.

**P10 (merged, dirty).**
It is not torn down automatically: "a dirty tree is surfaced for the user's confirmation and never silently deleted — it may hold unpushed work, the same rule the policy's branch-gone orphan sweep applies, and that sweep runs alongside this direction on its own quiet horizon." So 41-y is surfaced for the user's confirmation, not deleted.

**P11 (live branch).**
It's left alone: "A worktree whose branch is live with its change request open is left alone."

**P12 (label-orphaned stack).**
Yes, the sweep still sees it, but through a different check than the worktree-listing path — the worktree-based enumeration ("Enumerate from git's worktree listing joined with each branch's change-request state — never a directory scan") wouldn't catch a directory that's already gone, but there's a dedicated further step keyed off the compose label itself: "Where the environment playbook records container stacks, sweep one direction further: containers whose compose working-dir label points at a path that no longer exists are orphaned stacks — surface them for teardown too." So it is surfaced for teardown via this separate container-label check. Flagging ambiguity: the text says "surface... for teardown" without specifying whether this is reaped automatically (like a clean tree) or requires the user's confirmation (like a dirty tree) — SKILL.md doesn't state which regime an orphaned stack falls under.
