# Playbook: Platform Bindings

> Project playbook for this repo. Shared — read by every stage that touches the tracker (`backlog groom`, `backlog build`, `backlog status`, the `build-change` sibling's pipeline), proposes or edits a PR (the `build-change` skill's create-PR step, `adversarial-review`, `prove-your-work`), publishes artifacts (`to-web`, `to-spec`, `prove-your-work`), or creates and publishes working copies (`backlog build` dispatch, `implement`, the `adversarial-review` fixer). The skill's references speak in **role nouns** — ticket (this file's issue), label, change request (PR), branch, worktree, push — and this file binds each role to this repo's real platform. Bindings are prose contracts, not adapter code: each verb records the working command (or harness tool call) verified by `backlog setup` — live at binding time, end-to-end when the smoke test runs. Bindings are repo data, never machine state: a verb that fails at use is drift — warn and suggest re-running `backlog setup`.

## Tracker — where issues live

- Binding: _<github | local | gitlab | custom>_.
- Verbs — record the verified command for each:
  - List open issues with their labels: _<e.g. `gh issue list --state open --json number,title,labels`; local: read the frontmatter of `.backlog/issues/*.md`>_.
  - Read one issue — title, body, comments, labels: _<e.g. `gh issue view <n> --json title,body,comments,labels`; local: read the issue file>_.
  - Comment: _<e.g. `gh issue comment <n> --body ...`; local: append a `## <date> — <author>` section>_.
  - Set / clear a role label: _<e.g. `gh issue edit <n> --add-label/--remove-label`; local: edit the `state:`/`work-type:` frontmatter>_.
  - Create an issue: _<e.g. `gh issue create`; local: new file per the shape below — created only by a serialized main-branch writer>_.
  - Close an issue: _<e.g. `gh issue close <n>`, or via the close linkage below; local: flip `state: closed` — on the work branch when a PR carries it, on the main branch otherwise>_.
  - Read an issue's unresolved blockers (so `backlog build` skips blocked work): _<GitHub: `gh api repos/<owner>/<repo>/issues/<n> --jq '.issue_dependencies_summary'` and treat `.blocked_by > 0` as blocked; local: read `deps` frontmatter; another native tracker: its verified list/count verb; fallback: the explicitly recorded convention>_.
  - Write a blocker link between two issues: _<GitHub: resolve the blocker's numeric database id with `gh api repos/<owner>/<repo>/issues/<blocker> --jq '.id'`, then `gh api -X POST repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by -F issue_id=<numeric-id>`; local: add the blocker id to `deps`; another tracker: its verified native write verb; fallback: the explicitly recorded convention>_.
  - Read an issue's children with their states and labels (so the build sweep can apply the closed-or-`delivered` rule, per `backlog-policy.md` § Dependencies): _<GitHub: `gh api repos/<owner>/<repo>/issues/<n>/sub_issues --jq '.[] | {number, state, labels: [.labels[].name]}'` — the native `sub_issues_summary` counter counts closures only, so it undercounts mid-flight; local: the open issues whose `parent` frontmatter names `<n>`, with their `state`; another native tracker: its verified list verb; fallback: the explicitly recorded convention>_.
  - Attach a child issue to a parent: _<GitHub: resolve the child's numeric database id with `gh api repos/<owner>/<repo>/issues/<child> --jq '.id'`, then `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<numeric-id>`; local: set the child's `parent` frontmatter to the parent id; another tracker: its verified native write verb; fallback: the explicitly recorded convention>_.
- Close-on-merge linkage: _<github: `Closes #<n>` in the PR body closes the issue at merge to the default branch — which is why stacked slices close at promotion, not at their feature-branch merge; local: the issue file's `state: closed` flip is committed on the work branch and lands with the merge — closure is atomic with the change by construction; custom: state how closure follows a merged change, or that it is manual>_.

## Change review — where a change is proposed and reviewed

- Binding: _<github | local | gitlab | custom>_.
- Verbs:
  - Open a PR (ready for review, with a body per `change-description.md`): _<e.g. `gh pr create --title ... --body-file ...`; local: commit `.backlog/reviews/<issue-id>-<slug>.md` on the work branch, body per `change-description.md`, and set the issue's `state: in-review`>_.
  - Edit the PR body: _<e.g. `gh pr edit --body-file ...`; local: edit the review file and commit>_.
  - Read review comments since a SHA: _<e.g. `gh pr view --comments` / `gh api .../comments`; local: read the review file's appended review sections>_.
  - Post a review comment / reply: _<e.g. `gh pr comment`; local: append to the review file — Reviewer and Fixer each sign their sections>_.
  - Signal approval: _<an exact `LGTM` comment via the comment verb>_.
  - Merge: _<who merges and how — e.g. human merges on GitHub or explicitly authorizes the `merge-change` skill; local: human merges the branch; the automated loop itself never merges>_.
  - **`delivered` mechanics (stacked slices)** — applied by the `merge-change` skill in the same act as a slice's feature-branch merge: set the `delivered` label _<e.g. `gh issue edit <n> --add-label delivered`; local: set `state: delivered` frontmatter>_ and leave the ticket open; the parent spec ticket's promotion PR targets the base branch and carries one `Closes #<n>` line per slice, so closure fires natively at promotion.
- Where the review conversation persists: _<github: the PR thread; local: the review file, which merges with the change as its durable record>_.

## Version control — working copies and publication

- Binding: _<git; jj/custom are unsupported by the bundled Git `worktree` primitive until this project binds an equivalent project-owned prepare/inspect/remove implementation — absent one, record the isolation gap and do not dispatch>_.
- Verbs:
  - Prepare an isolated working copy off the base branch: the project-owned `worktree` skill — record its repo, base ref, and worktree root bindings here. The primitive creates the branch and working copy in one step, inspects ownership before reuse, and never switches the primary checkout.
  - Name a line of work: _<git: branch, per `environment.md` § Branching; jj: bookmark>_.
  - Sync the base before forking: _<e.g. `git fetch && git update-ref` / pull; local-only repo: none — the tracker commit below is the fork point>_.
  - Publish a line of work: _<e.g. `git push -u origin <branch>`; local-only repo: none — the branch is already visible; jj: `jj git push` or none>_.
  - **Push discipline**: commits on work, feature, and artifact branches reach the remote as they land — the remote is the backup, and pushing is not publication (the change request is). Waiting until a change request exists to push is drift from this binding.
  - Tear down a working copy: the `worktree` skill after environment teardown; it refuses dirty, unregistered, or primary-checkout paths.
- **Feature branches (stacked landing)** — a split spec ticket's work branch becomes its feature branch: _<naming, e.g. `<ticket>-<slug>`>_. Its shaping commits carry the `CONTEXT.md` terms and ADRs; slices branch off it and PR into it; the spec ticket's own PR is the feature→base merge.
- **Artifact branches** — specs, prototypes, and dossiers live on `artifact/<ticket>-<slug>` branches (`artifact/<slug>` when ticketless), plain shared history, **permanently unmerged by intent**: version-controlled while useful, deleted when spent. Every sweep skips the `artifact/` prefix on purpose; the branch ref is also the retention mechanism against GC.
- Pinned-SHA semantics: _<how a commit is referenced durably for plans, evidence, and blessed spec hashes — git/jj: the commit SHA/change-id; note any history-rewrite policy that can orphan pins>_.

## Artifact store — where media and renders live

> Read by the `to-web` sibling, and through it by `prove-your-work` (evidence media), `to-spec`, `prototype`, and `research` (preview-deployed renders). Media is never committed to the repo; the bucket is its permanent home, and callers embed by URL. Visibility is fixed: **public with unguessable keys** — content-addressed or random keys, immutable URLs, no listing.

- Provider: _<S3-generic; reference example: Cloudflare R2>_.
- Bucket: _<name>_.
- Base URL: _<e.g. `https://<bucket>.<account>.r2.dev/` or the custom domain>_.
- Credential env-var names: _<e.g. R2: `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ACCOUNT_ID`; S3-generic: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` + endpoint>_ — names only, never values.
- Upload command: _<e.g. `aws s3 cp <file> s3://<bucket>/<key> --endpoint-url https://<account>.r2.cloudflarestorage.com`>_.

## Harness — how threads are spawned

- Binding: _<e.g. Claude Code | Codex | other — usually the harness the loop runs from; the model roster is owned by the `staffing` skill>_.
- Spawn a thread or subagent with a prompt and working directory: the `to-thread` and `to-subagent` siblings own the route mechanics; record here only what this repo's binding adds — _<e.g. a required wrapper, a working-directory constraint, or "nothing — sibling defaults">_. Pass the already-prepared directory exactly; do not request harness-native isolation.
- Route health is a runtime check, never a recorded state: try the route; on failure warn, fall back to the successor, and note the failure — a route that fails repeatedly across sessions is retro fodder, not a state machine's job.
- Can a spawned thread read this skill's bundled references from disk? _<yes at <path>; if no, the dispatcher pastes the reference into the prompt>_.
- Durable monitor / wakeup for review round-trips: _<the harness mechanism `adversarial-review` may use, or "polling only">_.

## The local binding — tracker contract

> Applies only when the tracker binding is `local`. This is the full contract; the verbs above summarize it.

- **Shape** — one file per issue: `.backlog/issues/<id>-<slug>.md`. Frontmatter: `state` (readiness role verbatim), `work-type`, `surface`, `coordination`, `coordination-reason`, `deps` (issue ids), `parent` (the parent issue id, when this issue is a child), and, while in flight, `branch`, `dispatched`, `deadline`, and `thread`. Body first, then comments as appended `## <date> — <author>` sections. Roles are the frontmatter values themselves — the role→label mapping in `backlog-policy.md` is the identity.
- **No index, no moves** — state changes flip frontmatter; closed issues stay in place. Agents and humans find issues by reading frontmatter, not a derived index. File moves on branches invite rename conflicts.
- **Three write classes** — every tracker write falls in exactly one:
  1. _Grooming writes_ (labels, clarifications, dependencies, dedup, merges) — on the main branch, in the primary checkout, committed before `backlog build` dispatches. Groom never edits a `building` issue's file — changes for one go through a comment or wait — with one exception: the human-confirmed orphan reset (`backlog-policy.md` § Building hygiene), safe because the claim is dead.
  2. _PR-bound lifecycle writes_ (state → `in-review` at PR-open, → `closed` once review converges — the one post-LGTM commit besides evidence; plan and review links) — committed on the issue's own work branch, landing with the merge. A branch edits only its own issue file, so parallel worktrees cannot conflict.
  3. _Abort writes_ (`needs-info` plus its open question, `needs-shaping` plus its open strategic decisions, blockers, clearing `building`) — never written from a worktree: the build thread posts the outcome comment, and a serialized main-branch writer (the next groom or status session) lands the frontmatter flip.
- **ID allocation** — new issues are created only by serialized main-branch writers, so sequential ids never collide.
- **Commit-before-fork** — `backlog build` commits the groomed tracker state, marks its claims `building`, commits again, and creates every worktree from that commit; each work branch is born carrying its own issue marked `building`.

## Custom bindings

For a platform this skill has no shipped default for, `backlog setup` derives the binding interactively: name the tool or API, exercise every verb above live, and record only commands that worked. A verb the platform cannot express is recorded as a gap with its fallback (e.g. no close-on-merge → closure is manual after merge), so downstream steps inherit the degradation explicitly rather than discovering it. Discover a **native dependency relation** before choosing a fallback; bind and exercise its read/write verbs so `backlog build` can skip blocked work. If it cannot be exercised, record the explicit fallback `backlog build` will use and why — never an intended or fabricated command presented as verified.
