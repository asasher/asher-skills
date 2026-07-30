# Playbook: Platform Bindings

> Project playbook for this repo. Shared — read by every stage that touches the tracker (`backlog groom`, `backlog build`, the `build` sibling's pipeline), proposes or edits a PR (the `build` skill's create-PR step, `adversarial-review`, `prove-your-work`), or creates and publishes working copies (`backlog build` dispatch, `implement`, the `adversarial-review` fixer). The skill's references speak in **role nouns** — issue, label, PR, branch, worktree, push — and this file binds each role to this repo's real platform. Bindings are prose contracts, not adapter code: each verb records the working command (or harness tool call) verified by `backlog setup` — live at binding time, end-to-end when the smoke test runs. A recorded command that no longer exists is drift — re-run `backlog setup`.

## Tracker — where issues live

- Binding: **github** — repo `asasher/asher-skills`, via the `gh` CLI (authed as `asasher`, https protocol).
- Verbs — verified against the repo at `backlog setup` time:
  - List open issues with their labels: `gh issue list --state open --json number,title,labels,body`.
  - Read one issue — title, body, comments, labels: `gh issue view <n> --json title,body,labels,comments`. (The bare `gh issue view <n>` / `--comments` form is **broken** on this repo — GitHub's Projects-classic deprecation makes its GraphQL `repository.issue.projectCards` fetch fail; the `--json` field list avoids that path. Verified live 2026-07-25, asher-skills#98.)
  - Comment: `gh issue comment <n> --body '...'` (or `--body-file`).
  - Set / clear a role label: `gh issue edit <n> --add-label <role> --remove-label <role>`.
  - Create an issue: `gh issue create --title '...' --body '...' --label <work-type>,<readiness>`.
  - Close an issue: `gh issue close <n>` — or, preferentially, via the close-on-merge linkage below.
  - Read an issue's unresolved blockers (so `backlog build` skips blocked work): `gh api repos/asasher/asher-skills/issues/<n> --jq '.issue_dependencies_summary'`; `.blocked_by > 0` defers the issue. Verified live against this repo's native GitHub dependency summary — note this is repo-specific: in `pipelines` the same summary read is a known-stale gotcha; bindings are verified per repo, never copied.
  - Write a blocker link: resolve the blocker's numeric database id with `gh api repos/asasher/asher-skills/issues/<blocker> --jq '.id'`, then `gh api -X POST repos/asasher/asher-skills/issues/<blocked>/dependencies/blocked_by -F issue_id=<numeric-id>`. The native write and subsequent summary read were verified in the issue run; do not substitute task-list prose.
  - Read an issue's open children (so the build sweep skips an unfinished parent, per `backlog-policy.md` § Dependencies — open children block the parent): `gh api repos/asasher/asher-skills/issues/<n>/sub_issues --jq '[.[] | select(.state=="open")] | length'`; any nonzero count defers the issue. The quicker `--jq '.sub_issues_summary'` read on the issue itself is fine for display but **eventually consistent** — observed lagging a child's closure by seconds (verified live 2026-07-29 on scratch #138/#139); dispatch decisions use the direct list.
  - Attach a child issue to a parent: resolve the child's numeric database id with `gh api repos/asasher/asher-skills/issues/<child> --jq '.id'`, then `gh api -X POST repos/asasher/asher-skills/issues/<parent>/sub_issues -F sub_issue_id=<numeric-id>`. Effect-verified live 2026-07-29 (scratch #138/#139: attach, summary total incremented, child listed).
  - Duplicate links: recorded per `backlog-policy.md` § Dependencies.
- Close-on-merge linkage: a `Closes #<n>` line in the PR body closes the issue when the PR merges — the loop's default; direct `gh issue close` only for issues no PR carries.

## Change review — where a change is proposed and reviewed

- Binding: **github** — pull requests on `asasher/asher-skills`.
- Verbs:
  - Open a PR (ready for review, with a body per `change-description.md`): `gh pr create --title '...' --body-file <file>`.
  - Edit the PR body: `gh api -X PATCH repos/asasher/asher-skills/pulls/<n> -F body=@<file>`. (The `gh pr edit <n> --body-file <file>` form is **broken** on this repo by the same Projects-classic GraphQL deprecation — it fails on `repository.pullRequest.projectCards`; the REST PATCH avoids GraphQL entirely. Verified live 2026-07-25, asher-skills#98.)
  - Read review comments since a SHA: `gh pr view <n> --json title,body,comments`; for inline threads `gh api repos/asasher/asher-skills/pulls/<n>/comments`. (The `gh pr view <n> --comments` form is **broken** by the same deprecation — same `--json`-avoids-GraphQL fix as the issue read above. Verified live 2026-07-25, asher-skills#98.)
  - Post a review comment / reply: `gh pr comment <n> --body '...'`.
  - Signal approval: an exact `LGTM` comment via `gh pr comment`.
  - Merge: the human merges on GitHub, or explicitly authorizes the `merge-changes` skill (`gh pr merge <n> --squash` — **no `--delete-branch`**: the build worktree still holds the local branch, so that flag's local delete fails and aborts the command before the remote branch is deleted; five-for-five reproduction across PRs #124/#125/#126/#130/#131, asher-skills#133. Branch cleanup is the skill's step-7 teardown, after `git worktree remove`: `git branch -D <branch>` then `git push origin --delete <branch>`, verified gone with `git branch --list <branch>` and `git ls-remote --heads origin <branch>` both returning nothing — delete and query verbs verified live against this repo's `origin` with a throwaway branch, 2026-07-27, asher-skills#133) — the automated loop itself never merges. Near-simultaneous review-ready PRs land as an explicitly-authorized **batch** through `merge-changes`, which orders, merges, and reconciles them; in-flight builds never rebase onto each other (`environment.md` § Parallelism verdict).
- Where the review conversation persists: the PR thread on GitHub.

## Version control — working copies and publication

- Binding: **git** (GitHub remote `origin`, https). Parallel-safe verdict with a standing **parallel, uncapped** dispatch preference (`environment.md` § Parallelism verdict) — every ready, unblocked ticket fans out into its own worktree by default; a per-run override narrows to a width or to sequential.
  - Prepare an isolated working copy off the base branch: the project-owned `worktree` skill, rooted
    at `../asher-skills-worktrees`, with `origin/main` as the base. It creates the branch and working
    copy in one guarded operation, inspects git's registration before reuse, and never switches the
    primary checkout.
  - Enumerate live working copies: `git worktree list` plus branch/PR state — never a directory scan (`environment.md` § Worktree isolation).
  - Name a line of work: a git branch, `<issue-number>-<slug>` per `environment.md` § Branching.
  - Sync the base before forking: `git fetch origin`; resolve `origin/main` directly without checking
    out or updating the primary checkout. If required work exists only on an unpublished local base,
    publish it or stop.
  - Publish a line of work: `git push -u origin <branch>`.
  - Tear down a working copy: the `worktree` skill after environment teardown; it refuses the primary
    checkout, dirty worktrees, and unregistered paths.
- Pinned-SHA semantics: the commit SHA references a change durably for plans and evidence. No history-rewrite policy — force-pushes after evidence capture orphan pinned blob URLs (`evidence.md` § GitHub binding covers re-pinning).

## Harness — how threads are spawned

- Binding: **outermost active harness** — T3 Code, Claude Code, or Codex. The dispatch skill resolves
  explicit system/runtime host metadata before an embedded Codex/Claude runtime; product-native tools
  corroborate that host context but their mere installation does not establish ownership. Model
  staffing per harness is in `environment.md` § Model staffing.
- Create an interactive issue coordinator with the route already selected and an exact prepared
  directory: T3 uses `to-thread`'s local authenticated HTTP adapter against the loopback runtime
  (`thread.create` then `thread.turn.start`, with temporary credentials revoked); Claude and Codex use
  their native thread/session mechanisms. T3 Code 0.0.30 is the latest effect-verified build as of
  2026-07-30, an observation rather than a version pin — dispatch gates on runtime capabilities and
  fails visibly if they drift. No route requests harness-native worktree isolation.
- Create a non-interactive coordinator: native subagent dispatch receives the exact prepared
  worktree. Claude→Codex uses bounded `codex exec --cd <dir>` through its tracked wrapper (raw output
  teed to a file, resumable session id captured where offered, per the staffing external-worker
  contract); Codex→Claude uses bounded `claude -p --model <model> '<self-contained prompt>'
  </dev/null` from the prepared directory and **never `--bare`**. Each command receives the coordinator
  assignment and upward successor; completion is accepted only after its durable return/effect is
  verified.
- Wrapper staffing evidence: the native Agent tool reports the spawned agent's type and model in its return metadata — that report is the wrapper-model proof. For `codex exec` children there is no native report; floor/cost compliance for the external model is **unproven** beyond the observable wrapper invocation, recorded per the template.
- Directional reachability and fallback: a failed Codex→Claude invocation removes only that route and applies the successor in `environment.md` § Model staffing; Claude→Codex remains available. No Anthropic-policy or credit monitor gates dispatch. (Recorded machine facts: versioned model aliases are rejected by the installed Claude CLI. Claude→`codex exec` **is** available in unattended children — the earlier "unavailable" record was stale; verified live 2026-07-25 (asher-skills#98) when a native unattended Agent child ran `codex exec -s read-only` for its verification and review passes, and the `backlog build` preflight probe succeeded.)
- Route trust: a routine dispatch trusts the recorded effect-verified verb — verification happens at setup, at re-verification, and when a route misbehaves, so dispatch needs no fresh probe session. A route that fails or hangs in use is drift: record the failure class, take the successor, re-verify that direction. Verification probe artifacts are cleaned up as part of the check.
- Can a spawned thread read a skill's bundled references from disk? Yes — under `.claude/skills/<name>/` and `docs/agents/` in the checkout.
- Durable monitor / wakeup for review round-trips: `ScheduleWakeup` / `Monitor` for polling; review is tracker-native, so a verdict wait polls the change request thread through the verified `--json` read verbs (§ Change review) — the retired tailnet surface's `review-await.py` block is no longer a wait path (asher-skills#116). Longer watches run per the `watch-until` skill's ladder — a watcher subagent, never the orchestrator inline (applies to both the approval gate and the PR-merge watch).

## The local binding — tracker contract

> Applies only when the tracker binding is `local`. This is the full contract; the verbs above summarize it.

- **Shape** — one file per issue: `.backlog/issues/<id>-<slug>.md`. Frontmatter: `state`, `work-type`, `surface`, `coordination`, `coordination-reason`, `deps`, and, while in flight, `branch`, `dispatched`, `coordinator-route`, and `upward-successor`. Body first, then comments as appended `## <date> — <author>` sections. Roles are the frontmatter values themselves — the role→label mapping in `backlog-policy.md` is the identity.
- **No index, no moves** — state changes flip frontmatter; closed issues stay in place. Agents and humans find issues by reading frontmatter, not a derived index. File moves on branches invite rename conflicts.
- **Three write classes** — every tracker write falls in exactly one:
  1. *Grooming writes* (labels, clarifications, dependencies, dedup) — on the main branch, in the primary checkout, committed before `backlog build` dispatches. Groom never edits a `building` issue's file — changes for one go through the build dispatcher or wait — with one exception: the human-confirmed orphan reset (`backlog-policy.md` § Building hygiene), safe because the claim is dead.
  2. *PR-bound lifecycle writes* (state → `in-review` at PR-open, → `closed` once review converges; plan and review links) — committed on the issue's own work branch, landing with the merge. A branch edits only its own issue file, so parallel worktrees cannot conflict.
  3. *Abort writes* (`needs-info` plus its open question, `needs-shaping` plus its open strategic decisions, blockers, clearing `building`) — never written from a worktree: the issue thread reports to the build dispatcher, the sole serialized writer to main.
- **ID allocation** — new issues are created only by the serialized main-branch writers (groom, or the build dispatcher on behalf of an issue thread), so sequential ids never collide.
- **Commit-before-fork** — `backlog build` commits the groomed tracker state, marks its queue `building`, commits again, and creates every worktree from that commit; each work branch is born carrying its own issue marked `building`.

## Custom bindings

For a platform this skill has no shipped default for, `backlog setup` derives the binding interactively: name the tool or API, exercise every verb above live, and record only commands that worked. A verb the platform cannot express is recorded as a gap with its fallback (e.g. no close-on-merge → the build dispatcher closes issues after merge), so downstream steps inherit the degradation explicitly rather than discovering it. Discover a **native dependency relation** before choosing a fallback; bind and exercise its read/write verbs so `backlog build` can form dependency waves. If it cannot be exercised, record the explicit fallback `backlog build` will use and why—never an intended or fabricated command presented as verified.
