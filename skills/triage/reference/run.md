# Run — Queue Orchestration

This is the orchestrator: discover the queue, dispatch issue threads, report handoff. Do not solve issues here.

## Steps

1. Confirm the project is set up.
   - The loop needs the playbooks under `docs/agents/`. If they are absent, tell the user to run `triage setup` and stop.
   - Read the parallelism verdict in `docs/agents/environment.md`. If it is absent, the isolation audit hasn't run — tell the user to run `triage setup` and stop.
   - Completion criterion: every playbook the loop may reach (`triage-policy`, `diagnosing-bugs`, `refactoring`, `planning`, `implementing`, `verifying`, `pr-reviewer`, `pr-fixer`, `environment`) exists and the parallelism verdict is known, or the user has been told to run setup.

2. Build the queue.
   - If the user named issue numbers or URLs, use exactly those.
   - Otherwise, select every open issue carrying the `ready-for-agent` role (per `docs/agents/triage-policy.md`) that also carries a work-type role and is not blocked by another open issue. `ready-for-agent` is the human's confirmation from grooming, so no further confirmation is needed before dispatch.
   - Issues without `ready-for-agent` are not run — they have not been groomed and released. If nothing is `ready-for-agent`, tell the user to run `triage groom` first and stop.
   - Completion criterion: the queue holds every `ready-for-agent`, unblocked issue exactly once, or the user is told to groom first / that the queue is empty.

3. Check labels.
   - `triage setup` provisions the role labels; this is a safety net. Confirm the roles in `docs/agents/triage-policy.md` still resolve to real labels — the readiness roles `run` reads (`ready-for-agent`) and the issue threads may apply (`needs-info`), and the work-type roles they route on.
   - If any are missing, create them when the available tools allow; otherwise record each as a blocker and tell the user to re-run `triage setup`.
   - Completion criterion: each required label is available or has an explicit blocker.

4. Dispatch one issue thread per queue item.
   - Create each issue thread in its own worktree under this project. Create the worktree from the base branch named in `docs/agents/environment.md`, updated to its latest remote state first — not from whatever branch is currently checked out.
   - Title each thread `triage #<issue-number>: <issue-title>`.
   - Prompt each thread with the issue URL and an instruction to follow this skill's `reference/issue-loop.md`. The skill is installed in this project, so that bundled reference is available to the thread; if the thread cannot read it, paste its contents into the prompt.
   - One issue per thread. Never batch.
   - Dispatch threads on the lead role — the most capable model reachable, per the Model staffing section of `docs/agents/environment.md` — staffing down happens inside a thread's delegated loops (verify, evidence, adversarial review), never at dispatch.
   - Honor the parallelism verdict. When it is `serialize-verification`, the threads may still be created, but only one may stand up the stack and verify at a time — tell each thread which shared resource is serialized and that it must acquire it before its verify step. When it is `parallel-safe`, threads run fully concurrently.
   - Completion criterion: every queued issue has a worktree off the current base branch with a created thread id, the parallelism constraint is passed to the threads, or an explicit creation blocker is recorded.

5. Report the handoff table.
   - One row per issue: number, title, URL, thread or pending worktree id, blocker if any.
   - Stop after handoff unless the user explicitly asks this thread to monitor the issue threads.
   - Completion criterion: every queued issue appears in the table with a terminal handoff state.
