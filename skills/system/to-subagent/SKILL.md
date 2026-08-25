---
name: to-subagent
description: Dispatch one unit of non-interactive work to a subagent as a blocking call. Use whenever work should run outside this session without the user attending it.
argument-hint: "<the unit of work to dispatch>"
metadata:
  optional: [staffing]
---

# To Subagent

Dispatch one unit of non-interactive work as a blocking call. Give the subagent one self-contained brief: objective, required inputs, exact supplied directory, constraints, checkable completion condition, and promised deliverable. It sees none of this conversation.

Use `staffing` when available to select the model, effort, harness, and execution method; otherwise choose and disclose them. Pass the supplied directory exactly. The workflow that prepared it owns isolation and worktree lifecycle.

For a cross-harness call, wait for the process and close stdin (`</dev/null`); an open pipe can keep the harness waiting for EOF. Enforce a caller-supplied deadline as the process timeout.

On return, compare the promised deliverable with the completion condition. Process success without the promised result is failure. Preserve caller-requested deliverables unchanged; summarize only the outcome and implications in the parent's words.
