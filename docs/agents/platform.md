# Playbook: Platform Bindings

> Project playbook for this repo. Shared — read by every subcommand that touches the tracker (`groom`, `run`, the issue loop), proposes or edits a PR (the create-PR step, `adversarial-review`, `evidence`), or creates and publishes working copies (`run`, `implement`, the fixer). The skill's references speak in **role nouns** — issue, label, PR, branch, worktree, push — and this file binds each role to this repo's real platform. Bindings are prose contracts, not adapter code: each verb records the working command (or harness tool call) verified by `backlog setup` — live at binding time, end-to-end when the smoke test runs. A recorded command that no longer exists is drift — re-run `backlog setup`.

## Tracker — where issues live

- Binding: **github** — repo `asasher/asher-skills`, via the `gh` CLI (authed as `asasher`, https protocol).
- Verbs — verified against the repo at `backlog setup` time:
  - List open issues with their labels: `gh issue list --state open --json number,title,labels,body`.
  - Read one issue — title, body, comments, labels: `gh issue view <n> --comments`.
  - Comment: `gh issue comment <n> --body '...'` (or `--body-file`).
  - Set / clear a role label: `gh issue edit <n> --add-label <role> --remove-label <role>`.
  - Create an issue: `gh issue create --title '...' --body '...' --label <work-type>,<readiness>`.
  - Close an issue: `gh issue close <n>` — or, preferentially, via the close-on-merge linkage below.
  - Read an issue's unresolved blockers (so `run` skips blocked work): GitHub has no native blocker field, so parse the `- [ ] depends on #N` task-list lines in the body (`backlog-policy.md` § Dependencies); an unchecked line whose target is still open is an unresolved blocker. (A tracker with a native relation — Jira `is blocked by`, Linear `blocked-by` — would bind that link's list-blockers API call here instead.)
  - Write a blocker link: append a `- [ ] depends on #N` task-list line to the blocked issue's body via `gh issue edit <n> --body-file`.
  - Duplicate links: recorded per `backlog-policy.md` § Dependencies.
- Close-on-merge linkage: a `Closes #<n>` line in the PR body closes the issue when the PR merges — the loop's default; direct `gh issue close` only for issues no PR carries.

## Change review — where a change is proposed and reviewed

- Binding: **github** — pull requests on `asasher/asher-skills`.
- Verbs:
  - Open a PR (ready for review, with a body per `change-description.md`): `gh pr create --title '...' --body-file <file>`.
  - Edit the PR body: `gh pr edit <n> --body-file <file>`.
  - Read review comments since a SHA: `gh pr view <n> --comments`; for inline threads `gh api repos/asasher/asher-skills/pulls/<n>/comments`.
  - Post a review comment / reply: `gh pr comment <n> --body '...'`.
  - Signal approval: an exact `LGTM` comment via `gh pr comment`.
  - Merge: the human merges on GitHub — the loop never merges.
- Where the review conversation persists: the PR thread on GitHub.

## Version control — working copies and publication

- Binding: **git** (GitHub remote `origin`, https). Sequential parallelism verdict — one work branch at a time, worktrees optional.
  - Create an isolated working copy off the base branch: `git worktree add <path> -b <branch> main` (used only if a thread wants isolation; sequential runs may work the primary checkout on a branch).
  - Name a line of work: a git branch, `<issue-number>-<slug>` per `environment.md` § Branching.
  - Sync the base before forking: `git fetch origin && git checkout main && git pull --ff-only`.
  - Publish a line of work: `git push -u origin <branch>`.
  - Tear down a working copy: `git worktree remove <path>`.
- Pinned-SHA semantics: the commit SHA references a change durably for plans and evidence. No history-rewrite policy — force-pushes after evidence capture orphan pinned blob URLs (`evidence.md` § GitHub binding covers re-pinning).

## Harness — how threads are spawned

- Binding: **Claude Code** — the loop runs from Claude Code; the model roster per harness is in `environment.md` § Model staffing.
- Create an issue thread with a prompt and a working directory: the Agent tool (`subagent_type: claude` or `general-purpose`), `isolation: 'worktree'` when a thread must isolate; Codex (gpt-5.6-sol) threads run via `codex exec --cd <dir>`, held by a wrapper subagent so the orchestrator watches them like any other thread (Codex mechanics in `CLAUDE.md` § Staffing → Mechanics; the wrapper detail is in `environment.md` § Model staffing).
- Can a spawned thread read this skill's bundled references from disk? Yes — at `.claude/skills/backlog/reference/` and `docs/agents/` in the checkout.
- Durable monitor / wakeup for review round-trips: `ScheduleWakeup` / `Monitor` for polling; the review loop awaits `scripts/review-await.py`. The watch is **held on a dedicated staffing-resolved watcher subagent that loops-until-verdict**, not the orchestrator inline — contract in `skills/review-loop/reference/watch.md` (applies to both the approval gate and the PR-merge watch).

## The local binding — tracker contract

> Applies only when the tracker binding is `local`. This is the full contract; the verbs above summarize it.

- **Shape** — one file per issue: `.backlog/issues/<id>-<slug>.md`. Frontmatter: `state` (readiness role verbatim), `work-type`, `deps` (issue ids), and, while in flight, `branch` and `dispatched` (date). Body first, then comments as appended `## <date> — <author>` sections. Roles are the frontmatter values themselves — the role→label mapping in `backlog-policy.md` is the identity.
- **No index, no moves** — state changes flip frontmatter; closed issues stay in place. Agents and humans find issues by reading frontmatter, not a derived index. File moves on branches invite rename conflicts.
- **Three write classes** — every tracker write falls in exactly one:
  1. *Grooming writes* (labels, clarifications, dependencies, dedup) — on the main branch, in the primary checkout, committed before `run` dispatches. Groom never edits an in-flight issue's file — changes for one go through the run thread or wait — with one exception: the human-confirmed orphan reset (`backlog-policy.md` § In-flight hygiene), safe because the claim is dead.
  2. *PR-bound lifecycle writes* (state → `in-review` at PR-open, → `closed` once review converges — the one post-LGTM commit besides evidence, per `reference/issue-loop.md` step 7; plan and review links) — committed on the issue's own work branch, landing with the merge. A branch edits only its own issue file, so parallel worktrees cannot conflict.
  3. *Abort writes* (`needs-info` plus its open question, blockers, clearing `in-flight`) — never written from a worktree: the issue thread reports to the run thread, the sole serialized writer to main.
- **ID allocation** — new issues are created only by the serialized main-branch writers (groom, or the run thread on behalf of an issue thread), so sequential ids never collide.
- **Commit-before-fork** — `run` commits the groomed tracker state, marks its queue `in-flight`, commits again, and creates every worktree from that commit; each work branch is born carrying its own issue marked `in-flight`.

## Custom bindings

For a platform this skill has no shipped default for, `backlog setup` derives the binding interactively: name the tool or API, exercise every verb above live, and record only commands that worked. A verb the platform cannot express is recorded as a gap with its fallback (e.g. no close-on-merge → the run thread closes issues after merge), so downstream steps inherit the degradation explicitly rather than discovering it.
