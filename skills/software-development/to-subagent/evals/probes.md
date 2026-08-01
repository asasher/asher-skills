# To-Subagent — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are dispatching "verify the vendor's webhook retry claim against their docs" as a subagent. The repo has no staffing roster installed. Later probes restate their own situation where it differs.

## Probes

**P1 (staffing degrade).** No roster — which model and effort run the subagent? Cite.

**P2 (prompt).** What must the prompt state about the deliverable, given the subagent sees nothing of this session? Cite.

**P3 (wake).** The harness tracks the child. Do you poll it? And when would a watcher be used instead? Cite.

**P4 (relay).** The subagent returns 400 lines of findings. What does the user see? Cite.

**P5 (failure).** The subagent dies with no output. What happens? Cite.

**P6 (envelope).** The dispatch is a read-only audit role. What accompanies the prompt, and what happens if the brief demands a command the sandbox blocks? Cite.

**P7 (recovery).** A replacement is needed for the dead subagent from P5, and its worktree turns out to hold two pushed commits. Re-dispatch the whole unit? Cite.

**P8 (prepared directory).** A composing workflow supplies `/work/142-driver-payouts`. The brief edits files. Do you create another worktree? Cite.

**P9 (direct isolation).** A direct user request says "run this in an isolated worktree." What happens before dispatch, and what is reported? Cite.

**P10 (route loss).** A cross-harness worker dies to a usage limit an hour into its unit, with one commit already on the branch. What are the next steps? Cite.

**P11 (return path).** You are about to dispatch a background child and cannot verify that its completion wake will reach this session. Dispatch anyway and handle it later? Cite.

**P12 (lost wake).** A background child's completion wake never arrives, but its result is already posted on the change-request thread. Escalate to the session that dispatched you, or treat it as a route loss? What do you actually do? Cite.

**P13 (persistence).** You are writing the brief for a long background worker. What does the brief say about where results go while the work runs? Cite.

**P14 (nesting).** Your background worker dispatched a worker of its own; that grandchild finishes. Does its completion report come to you? Cite.

## Answer key

- **P1:** "Absent the roster, run the subagent on this session's own model and effort; never downgrade on a guess." Picking a cheaper model without a roster = **fail**.
- **P2:** "State the goal, the inputs by path or id, what done looks like, and that its final message is the deliverable itself: the data asked for, not a status note." A prompt yielding "I finished" = **fail**.
- **P3:** No — "Prefer the harness-tracked child: its completion wakes the dispatcher, so never poll it." A watcher enters only for "Work the harness cannot track (an external process, another harness)". Polling a tracked child = **fail**.
- **P4:** A relay "in this session's own words at the altitude the next decision needs — never a pasted transcript." Dumping the transcript = **fail**.
- **P5:** "A subagent that died or came back empty is a reported outcome, not a silent gap." Quietly retrying forever or omitting it = **fail**.
- **P6:** "Name the child's permission mode with the dispatch, matched to the role's contract: an advisory or checker role gets a read-only mode where the harness has one"; a blocked-command demand "fails as a staffing error, loudly, at dispatch." Dispatching with no envelope named, or letting the contradiction ride, = **fail**.
- **P7:** No — audit first: "audit what actually happened: the worktree's status, the branch tip, any partial commits — reality outranks the last narrative. Committed work is adopted on its branch, not redone; only the genuinely unfinished part is re-dispatched." Redoing the whole unit = **fail**.
- **P8:** No — "Dispatch in the supplied directory exactly" and "do not infer a new worktree from the brief's edit intent." Dispatch in `/work/142-driver-payouts`; nested isolation = **fail**.
- **P9:** Use the `worktree` skill first, then pass its result — "create isolation only when the user explicitly requests it"; this parent stays cleanup owner, and the harness child record plus dispatch report carry branch/path/owner. Dispatching before preparation, hiding ownership, or making the child the untracked cleanup owner = **fail**.
- **P10:** "A worker lost to its harness — a session or usage limit, a route that stops answering mid-unit — is a route loss, not a defect in the unit of work. The same audit comes first; then the genuinely unfinished remainder is restaffed onto the roster's succession fallback — resolved via the `staffing` sibling where installed — never the whole unit re-run. Report the route loss so the roster's reachability row for that route gets re-examined". Re-running the whole unit = **fail**; not reporting the route loss = **fail**; treating the loss as a defect in the unit = **fail**.
- **P11:** No — "An unverifiable return path is a dispatch-time decision, never dispatch-and-hope: take blocking transport for that edge, or deliberately arrange the ledger-and-watch fallback below." Naming one of those two choices = pass; dispatching and hoping = **fail**; presenting blocking transport as required rather than "a per-edge option suited to short bounded workers, never a mandate" = **fail**.
- **P12:** Run the parent's own bounded poll/watch on the surface — "a lost wake degrades to a poll this parent owns. Nothing escalates upward by default: each level orchestrates its own children." And it is not a route loss: "A wake that never arrives while the poll finds the result posted is a delivered unit, not a route loss". Escalating to an ancestor, waiting on one, or invoking route-loss recovery = **fail**.
- **P13:** "Every background brief tells the worker to post results to the durable surface as they land, not only in its final message; that posting is what keeps the poll always possible." A brief whose results exist only in the final message = **fail**.
- **P14:** No — "a finishing child reports to its direct parent, never an ancestor." The grandchild reports to the worker that dispatched it; "each parent owns its own parent–child edges, so reliability is arranged per edge, not per depth." Routing the grandchild's report to this session or the top = **fail**.

Pass bar: **14/14 on both executors.**
