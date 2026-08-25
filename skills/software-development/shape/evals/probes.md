# Shape probes

Pre-deployment probes with only `SKILL.md` in context. Require an exact citation for each answer.

## Scenario

You are shaping ticket 142, "driver payouts." An earlier session settled the affected users and left open experience questions on the ticket. The ticket work branch exists remotely, but this machine has no worktree for it.

## Probes

**P1.** What provides continuity, and what happens to the worktree?

**P2.** What do you read before asking questions, and which questions do you avoid?

**P3.** In what order do you work the design tree?

**P4.** What happens when users, experience, and system behavior are settled?

**P5.** A vendor guarantee needs sources and a payout layout needs a working comparison. Where does each go, and what may continue meanwhile?

**P6.** A research subagent returns a dossier. Who publishes it, in what order, and what reaches the ticket?

**P7.** Shaping changes `CONTEXT.md`. Which branch carries it, when is it pushed, and which session opens the change request?

**P8.** The design frontier empties. Where does `to-spec` run, and when may the ticket become `ready-for-agent`?

**P9.** The user parks the ticket at the experience handoff. What must be durable before the session stops?

**P10.** An unrelated CSV-export idea appears. What happens to it?

## Answer key

- **P1:** "The branch carries continuity across sessions and machines; the worktree may be reused or recreated." Use `worktree` to prepare or inspect the worktree on that branch.
- **P2:** Read "the ticket, its linked artifacts, the project instruction file, and the project context files" and "Re-ask nothing the record settles."
- **P3:** Users, experience, system behavior, implementation. "Settle every decision at one level before opening the next."
- **P4:** Say, "Experience is settled. Implementation is next. This is a handoff point." The user may continue or park the ticket.
- **P5:** Dispatch `research` and `prototype` via `to-subagent`, "each fresh subagent one question and only the context it needs." A question "blocks only the decisions that depend on it."
- **P6:** Shape uses `to-branch`, then `to-web`, then adds "a ticket projection with the question, concise result, durable URL, and commit hash."
- **P7:** Commit and push the context change on the ticket work branch as it lands. "The later build continues on it and opens the ticket's single change request."
- **P8:** Run `to-spec` inline, publish through `to-branch` then `to-web`, and write the projection. Only "After the user approves that published revision" may shape record the hash and mark the ticket ready.
- **P9:** "Push the ticket branch and record every open frontier item on the ticket."
- **P10:** "Offer work outside this ticket to `to-backlog`."

Pass bar: ten of ten on both executors.
