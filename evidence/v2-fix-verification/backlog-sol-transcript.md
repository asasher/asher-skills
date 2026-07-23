1. **P1 — groom sweep and gate**

Tickets #10, #11, #12, and unlabeled #13 enter grooming. #13 is routed toward the ready role because its decisions are settled. The remaining shaping work forms two subjects—#10/#11 together and #12 alone—combined into one batch because they share a subsystem. Before approval, only the proposed plan exists: no tracker changes and no thread.

Citations:

> “Sweep the tracker for unlabeled tickets and tickets carrying the needs-shaping role, or take the ids given.”

> “Route first — as a plan, not as writes: a ticket whose decisions are already settled routes to the ready role…”

> “Group that rest twice: tickets whose decisions interlock form one **subject**; subjects that belong together (same subsystem, same domain area) form one **batch**…”

> “The confirmation is the gate for all of it: until they approve, the tracker is untouched and no thread exists.”

2. **P1b — single batch**

After approval, #10–#12 are marked with the shaping role according to the label policy. Since there is only one approved batch, no separate thread spawns; the current session becomes the shaping thread and runs `shape` on the two subjects.

Citations:

> “Then execute the approved mutations and, per approved batch: mark its tickets shaping per the label roles — a ticket never gets two threads…”

> “A single batch spawns nothing: this session becomes the shaping thread and runs the `shape` skill itself.”

3. **P2 — two dispatch shapes**

For shaping, I report the relevant threads and attachment instructions, using the tracker and harness thread listing for current status. To learn the actual decisions, I direct the user to the shaping thread or the specs it placed on the tickets; shaping results do not flow back automatically.

For builds, I report each subagent’s relayed outcome—either its review-ready change request or failure—and use tracker claim/outcome comments as the durable run record.

Citations:

> “Grooming is interactive — human-in-the-loop work fans out as threads the user attends, and no result flows back.”

> “Report each thread and how to attach; status on request comes from the tracker and the harness's thread listing.”

> “Inside the thread, shaping ends with a spec on each ticket…”

> “This session babysits the fleet: each build's completion wakes it, and it relays the outcome — the review-ready change request, or the failure, with a died-silent build reported, never dropped.”

> “**The tracker is the run ledger**: the claim comment and the outcome comment are its events…”

4. **P3 — double dispatch**

#21 is not dispatched again because it is already marked building. Before spawning #20’s worker, I run the one-time live preflight; if it passes, I mark #20 building and add the runner-identity claim comment. I then dispatch `build` through `to-subagent`, in its own worktree if the environment permits.

Citations:

> “Preflight once per run: the platform verbs and credentials the builds will lean on answer a cheap live read…”

> “For each ticket: mark it building per the label roles — a dispatched ticket must never dispatch twice, and the claim comment carries this runner's identity…”

> “…then dispatch the `build` skill on it via the `to-subagent` skill, in its own worktree.”

5. **P4 — isolation verdict**

#20 and #22 run sequentially, one ticket at a time in the main checkout. They do not run concurrently in separate worktrees.

Citation:

> “Isolation and concurrency follow the environment playbook's verdicts (`docs/agents/environment.md` § Worktree isolation, § Parallelism): a repo that can't isolate builds one ticket at a time in the main checkout.”

6. **P5 — missing playbook**

I stop before build dispatch and run—or instruct the user to run—`backlog setup`; I do not invent platform bindings.

Citation:

> “Missing playbooks: run `backlog setup` first — don't improvise them.”

7. **P6 — merge boundary**

No. LGTM and review-ready change requests do not authorize merging. I wait for explicit merge authorization.

Citation:

> “Merging the resulting change requests waits for explicit authorization.”

8. **P7 — resume**

Before dispatching anything new, I reconstruct the run from tracker claims and outcomes, then reconcile claims owned by this runner against live worktrees and branch tips.

For #30, I inspect branch `30-x`, its worktree, and branch tip to determine whether its existing build is live, completed, wedged, or needs recovery; I do not create a duplicate dispatch.

For #31, I do not take over or redispatch it because its claim belongs to another actor. The skill is slightly ambiguous about whether to report, ignore, or separately verify foreign claims; it only explicitly requires reconciliation of claims “this runner owns.” The no-double-dispatch rule still prevents another dispatch.

Citations:

> “The tracker is the run ledger: the claim comment and the outcome comment are its events, so a dispatcher that dies or compacts mid-fleet reconstructs from there…”

> “…on resume, reconcile the claims this runner owns against live worktrees and branch tips before dispatching anything new.”

> “…a dispatched ticket must never dispatch twice…”

9. **P8 — wedged build**

I inspect #20’s worktree, branch tip, and process. Based on that evidence, I either respawn the build or report it as failed/wedged so it cannot remain silently stuck.

Citation:

> “Each dispatch also gets a deadline (the policy's quiet horizon, or tighter): a build past it with no completion is checked — worktree, branch tip, process — and respawned or reported, so a wedged build surfaces instead of sitting silent.”
