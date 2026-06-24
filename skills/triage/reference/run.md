# Run — Queue Orchestration

This is the orchestrator. Keep this thread focused on discovering the issue queue, dispatching issue threads, and reporting handoff state. Do not solve issues here.

## Steps

1. Confirm the project is set up.
   - The loop needs the playbooks under `docs/agents/`. If they are absent, tell the user to run `triage setup` and stop.
   - Completion criterion: every playbook the loop may reach (`diagnosing-bugs`, `refactoring`, `planning`, `implementing`, `verifying`, `pr-reviewer`, `pr-fixer`, `environment`) exists, or the user has been told to run setup.

2. Build the queue.
   - If the user named issue numbers or URLs, use exactly those.
   - Otherwise, fetch every open GitHub issue in the current repo with no labels.
   - Completion criterion: the queue holds every in-scope issue URL exactly once, or the user is told the queue is empty.

3. Check labels.
   - The loop needs `bug`, `enhancement`, `refactor`, and `needs-info`.
   - Create missing labels when the available tools allow; otherwise record each missing label as a blocker for the issue threads.
   - Completion criterion: each required label is available or has an explicit blocker.

4. Dispatch one issue thread per queue item.
   - Create each issue thread in its own worktree under this project. Create the worktree from the base branch named in `docs/agents/environment.md`, updated to its latest remote state first — not from whatever branch is currently checked out.
   - Title each thread `triage #<issue-number>: <issue-title>`.
   - Prompt each thread with the issue URL and an instruction to follow this skill's `reference/issue-loop.md`. The skill is installed in this project, so that bundled reference is available to the thread; if the thread cannot read it, paste its contents into the prompt.
   - One issue per thread. Never batch.
   - Completion criterion: every queued issue has a worktree off the current base branch with a created thread id, or an explicit creation blocker.

5. Report the handoff table.
   - One row per issue: number, title, URL, thread or pending worktree id, blocker if any.
   - Stop after handoff unless the user explicitly asks this thread to monitor the issue threads.
   - Completion criterion: every queued issue appears in the table with a terminal handoff state.
