# Run — Queue Orchestration

This is the orchestrator: discover the queue, claim it, dispatch issue threads, report handoff. Do not solve issues here. Tracker and dispatch mechanics come from `docs/agents/platform.md`; this thread is also the loop's **serialized tracker writer** — where the binding requires main-branch writes (the local binding's abort and creation writes), they happen here, never in a worktree.

## Steps

1. Confirm the project is set up.
   - The loop needs the playbooks under `docs/agents/`. If they are absent — `platform.md` included — tell the user to run `backlog setup` and stop.
   - Read the parallelism verdict in `docs/agents/environment.md`. If it is absent, the isolation audit hasn't run — tell the user to run `backlog setup` and stop.
   - Read the Model staffing section of `docs/agents/environment.md`. Apply its succession line first: a role whose model is unreachable resolves to the successor the roster names. If the section is missing, or a role stays unfilled after succession, tell the user to re-run `backlog setup` to fix the roster and stop — the fallback ladder in `reference/staffing.md` is for mid-thread surprises, not a roster known bad at dispatch.
   - Completion criterion: every `templates/*.md` in this skill has its `docs/agents/` counterpart, the parallelism verdict is known, and the staffing roster resolves in this harness — or the user has been told to run setup.

2. Build the queue.
   - If the user named issues, use exactly those.
   - Otherwise, via the tracker binding's list verb, select every open issue carrying the `ready-for-agent` role (per `docs/agents/backlog-policy.md`) that also carries a work-type role and is not blocked by another open issue. `ready-for-agent` is the human's confirmation from grooming, so no further confirmation is needed before dispatch.
   - Issues without `ready-for-agent` are not run — they have not been groomed and released; `in-flight` issues are already owned by a thread and never re-queued. If nothing is `ready-for-agent`, tell the user to run `backlog groom` first and stop.
   - A `ready-for-agent` issue lacking a work-type is skipped and reported as a grooming gap; it does not block the rest of the queue.
   - Completion criterion: the queue holds every `ready-for-agent`, unblocked issue exactly once, or the user is told to groom first / that the queue is empty.

3. Check the bindings.
   - `backlog setup` provisions the role labels and records the platform verbs; this is a safety net. Confirm the roles in `docs/agents/backlog-policy.md` still resolve on the tracker — the readiness roles `run` reads (`ready-for-agent`) and writes (`in-flight`), the ones issue threads may apply (`needs-info`), and the work-type roles they route on.
   - If any are missing, create them when the binding's verbs allow; otherwise record each as a blocker and tell the user to re-run `backlog setup`.
   - Completion criterion: each required role is available or has an explicit blocker.

4. Claim the queue.
   - Immediately before marking, re-read each queued issue via the tracker binding; skip any that changed since the queue was built — a readiness role dropped or already `in-flight` means another runner claimed it. This closes most of the concurrent-runner window; the loop accepts the residue rather than locking (`backlog-policy.md` § In-flight hygiene).
   - Mark each surviving issue `in-flight`, replacing `ready-for-agent`, recording the branch name and dispatch date per the policy playbook.
   - Local tracker binding: commit any uncommitted groomed tracker state first, then commit the `in-flight` marks — worktrees fork from a commit, so this claim commit is the fork point and every work branch is born carrying its own issue marked `in-flight` (`platform.md` § The local binding).
   - Completion criterion: every dispatched-to-be issue is marked `in-flight` on the tracker (committed, on the local binding), and skipped claims are reported.

5. Dispatch one issue thread per claimed issue.
   - Create each issue thread in its own worktree under this project, via the version-control binding's working-copy verb. Fork from the base branch named in `docs/agents/environment.md`, synced per the binding first — not from whatever branch is currently checked out. On the local tracker binding the fork point is the claim commit from step 4.
   - Title each thread `backlog #<issue-id>: <issue-title>`.
   - Prompt each thread with the issue reference and an instruction to follow this skill's `reference/issue-loop.md`, spawned per the harness binding in `platform.md`. If the binding says threads cannot read the bundled references from disk, paste the reference's contents into the prompt.
   - One issue per thread. Never batch.
   - Dispatch threads on the **orchestrator** role per `reference/staffing.md` and the roster in `docs/agents/environment.md` — staffing down happens inside a thread's delegated stages (build, verify, evidence, review), never at dispatch.
   - Honor the parallelism verdict. When it is `serialize-verification`, the threads may still be created, but only one may stand up the stack and verify at a time — tell each thread which shared resource is serialized and that it must acquire it before its verify step. When it is `parallel-safe`, threads run fully concurrently — except issues in the playbook's serialized exception lane: tell those threads they must serialize their verification on the named resource.
   - Completion criterion: every claimed issue has a worktree off the right fork point with a created thread id, the parallelism constraint is passed to the threads, or an explicit creation blocker is recorded.

6. Report the handoff table.
   - One row per issue: id, title, reference, thread or pending worktree id, blocker if any.
   - On bindings where threads write the tracker directly (GitHub), stop after handoff unless the user explicitly asks this thread to monitor; abort reports arriving later are only bookkeeping.
   - On bindings that need a serialized main writer (local), staying available *is* the handoff: this thread remains the sole tracker writer until every issue thread reaches a terminal state, applying each abort as it is reported — clear `in-flight`, set the reported role (`needs-info` for missing information, `ready-for-human` for verify caps and blockers per `backlog-policy.md`), and commit the comment on main.
   - Completion criterion: every claimed issue appears in the table, and every abort reported so far is written to the tracker; on the local binding this thread stays available as writer while threads still fly.
