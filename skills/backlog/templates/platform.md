# Playbook: Platform Bindings

> Project playbook for this repo. Shared — read by every subcommand that touches the tracker (`groom`, `run`, the issue loop), proposes or edits a PR (the create-PR step, `adversarial-review`, `evidence`), or creates and publishes working copies (`run`, `implement`, the fixer). The skill's references speak in **role nouns** — issue, label, PR, branch, worktree, push — and this file binds each role to this repo's real platform. Bindings are prose contracts, not adapter code: each verb records the working command (or harness tool call) proven by `backlog setup`'s smoke test. A recorded command that no longer exists is drift — re-run `backlog setup`.

## Tracker — where issues live

- Binding: _<github | local | gitlab | custom>_.
- Verbs — record the verified command for each:
  - List open issues with their labels: _<e.g. `gh issue list --state open --json number,title,labels`; local: read the frontmatter of `.backlog/issues/*.md`>_.
  - Read one issue — title, body, comments, labels: _<e.g. `gh issue view <n> --comments`; local: read the issue file>_.
  - Comment: _<e.g. `gh issue comment <n> --body ...`; local: append a `## <date> — <author>` section>_.
  - Set / clear a role label: _<e.g. `gh issue edit <n> --add-label/--remove-label`; local: edit the `state:`/`work-type:` frontmatter>_.
  - Create an issue: _<e.g. `gh issue create`; local: new file per the shape below — created only by a serialized main-branch writer>_.
  - Close an issue: _<e.g. `gh issue close <n>`, or via the close linkage below; local: flip `state: closed` — on the work branch when a PR carries it, on the main branch otherwise>_.
  - Dependencies and duplicate links: recorded per `backlog-policy.md` § Dependencies.
- Close-on-merge linkage: _<github: `Closes #<n>` in the PR body closes the issue at merge; local: the issue file's `state: closed` flip is committed on the work branch and lands with the merge — closure is atomic with the change by construction; custom: state how closure follows a merged change, or that it is manual>_.

## Change review — where a change is proposed and reviewed

- Binding: _<github | local | gitlab | custom>_.
- Verbs:
  - Open a PR (ready for review, with a body per `pr.md`): _<e.g. `gh pr create --title ... --body-file ...`; local: commit `.backlog/reviews/<issue-id>-<slug>.md` on the work branch, body per `pr.md`, and set the issue's `state: in-review`>_.
  - Edit the PR body: _<e.g. `gh pr edit --body-file ...`; local: edit the review file and commit>_.
  - Read review comments since a SHA: _<e.g. `gh pr view --comments` / `gh api .../comments`; local: read the review file's appended review sections>_.
  - Post a review comment / reply: _<e.g. `gh pr comment`; local: append to the review file — Reviewer and Fixer each sign their sections>_.
  - Signal approval: _<an exact `LGTM` comment via the comment verb>_.
  - Merge: _<who merges and how — e.g. human merges on GitHub; local: human merges the branch; the loop never merges>_.
- Where the review conversation persists: _<github: the PR thread; local: the review file, which merges with the change as its durable record>_.

## Version control — working copies and publication

- Binding: _<git | jj (colocated or native) | custom>_.
- Verbs:
  - Create an isolated working copy off the base branch: _<e.g. `git worktree add <path> -b <branch> <base>`; jj: `jj workspace add`>_.
  - Name a line of work: _<git: branch, per `environment.md` § Branching; jj: bookmark>_.
  - Sync the base before forking: _<e.g. `git fetch && git update-ref` / pull; local-only repo: none — the tracker commit below is the fork point>_.
  - Publish a line of work: _<e.g. `git push -u origin <branch>`; local-only repo: none — the branch is already visible; jj: `jj git push` or none>_.
  - Tear down a working copy: _<e.g. `git worktree remove <path>`; jj: `jj workspace forget`>_.
- Pinned-SHA semantics: _<how a commit is referenced durably for plans and evidence — git/jj: the commit SHA/change-id; note any history-rewrite policy that can orphan pins>_.

## Harness — how threads are spawned

- Binding: _<e.g. Claude Code | Codex | other — usually the harness the loop runs from; the model roster per harness is in `environment.md` § Model staffing>_.
- Create an issue thread with a prompt and a working directory: _<e.g. the harness's task/agent tool with `isolation: worktree`, or `codex exec --cd <worktree> ...`>_.
- Can a spawned thread read this skill's bundled references from disk? _<yes at <path>; if no, the dispatcher pastes the reference into the prompt>_.
- Durable monitor / wakeup for review round-trips: _<the harness mechanism `adversarial-review` may use, or "polling only">_.

## The local binding — tracker contract

> Applies only when the tracker binding is `local`. This is the full contract; the verbs above summarize it.

- **Shape** — one file per issue: `.backlog/issues/<id>-<slug>.md`. Frontmatter: `state` (readiness role verbatim), `work-type`, `deps` (issue ids), and, while in flight, `branch` and `dispatched` (date). Body first, then comments as appended `## <date> — <author>` sections. Roles are the frontmatter values themselves — the role→label mapping in `backlog-policy.md` is the identity.
- **No index, no moves** — state changes flip frontmatter; closed issues stay in place. Agents and humans find issues by reading frontmatter, not a derived index. File moves on branches invite rename conflicts.
- **Three write classes** — every tracker write falls in exactly one:
  1. *Grooming writes* (labels, clarifications, dependencies, dedup) — on the main branch, in the primary checkout, committed before `run` dispatches. Groom never edits an in-flight issue's file; changes for one go through the run thread or wait.
  2. *PR-bound lifecycle writes* (state → `in-review` → `closed`, plan and review links) — committed on the issue's own work branch, landing with the merge. A branch edits only its own issue file, so parallel worktrees cannot conflict.
  3. *Abort writes* (`needs-info` plus its open question, blockers, clearing `in-flight`) — never written from a worktree: the issue thread reports to the run thread, the sole serialized writer to main.
- **ID allocation** — new issues are created only by the serialized main-branch writers (groom, or the run thread on behalf of an issue thread), so sequential ids never collide.
- **Commit-before-fork** — `run` commits the groomed tracker state, marks its queue `in-flight`, commits again, and creates every worktree from that commit; each work branch is born carrying its own issue marked `in-flight`.

## Custom bindings

For a platform this skill has no shipped default for, `backlog setup` derives the binding interactively: name the tool or API, exercise every verb above live, and record only commands that worked. A verb the platform cannot express is recorded as a gap with its fallback (e.g. no close-on-merge → the run thread closes issues after merge), so downstream steps inherit the degradation explicitly rather than discovering it.
