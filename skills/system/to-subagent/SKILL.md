---
name: to-subagent
description: Dispatch one unit of non-interactive work to a subagent and wait for its validated result. Use when work should run outside this session without the user attending it.
metadata:
  optional: [staffing]
---

# To subagent

Dispatch one bounded unit and wait for its return. Supply a self-contained brief: objective, required inputs, exact directory, constraints, absolute deadline, checkable completion condition, and promised deliverable. Include immutable refs for revision-specific work. Assume no conversation context is inherited.

Use `staffing` when available to choose the model, effort, harness, and execution method; otherwise choose and disclose them. Pass the directory exactly. The workflow owns isolation and worktree lifecycle.

Carry the execution permissions in the dispatch configuration: the session's authorized mode and tool restrictions, with read-only access for read-only work where supported. A prompt cannot grant filesystem or tool permissions. Before a cross-harness builder starts, validate that its configured route can write a disposable probe in the supplied directory, then remove the probe. A denied capability returns a blocker; never broaden permissions to bypass it.

Resume a previous worker for a fix when the harness supports it and the worker's role and directory still match. Supply the new findings and refs explicitly. Otherwise dispatch a fresh worker with the implementation report and persisted findings. Verification and review use independent contexts from the builder and fixer.

For a cross-harness process, close stdin (`</dev/null`) and set its timeout from the remaining deadline. For a native asynchronous API, wait for completion within that deadline and cancel on expiry. Confirm timed-out work has stopped before returning control to a workflow that may start another writer. Return an unconfirmed stop as a blocker; the directory remains occupied.

On return, check the deliverable against the completion condition. Process success without the promised result is failure. Return the report, worker resume reference when available, observed revisions, and completion or timeout status. Preserve requested deliverables unchanged; summarize only the outcome and implications in the parent's words.
