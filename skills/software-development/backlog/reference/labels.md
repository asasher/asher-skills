# Labels, claims, deadlines, branches

The fixed conventions every backlog verb and verb skill shares. They are not configured per repo: `backlog setup` creates the labels, and the branch names follow from the issue number.

## Readiness labels

One per open issue once groomed; none means "not yet groomed".

- `needs-shaping`: parked for shaping. Product, design, or scope decisions are neither settled nor delegated, or a build found the blessed spec contradicted by the code. Never selected by `backlog build`.
- `shaping`: a shaping thread is attending it. Set by `backlog groom` at dispatch, so a subject never gets two threads. Cleared when the spec is blessed; abandonment returns it to `needs-shaping`.
- `ready-for-agent`: released. Groom sets it for an issue whose decisions are settled; `shape` sets it when the spec is approved; `to-slices` sets it on the children of an approved split. Requires a work-type.
- `building`: claimed. A build thread owns it; the claim comment is the dispatch declaration. Set by `backlog build`, replacing `ready-for-agent`. Superseded by closure, by a reclaim comment, or by the human-confirmed orphan reset.
- `ready-for-human`: only a human may work it. Also the handback target for a build that hits an environment blocker or a verification cap: the comment names why only a human can act on what remains. A blocker a repo change could clear is work, not a handback.
- `needs-info`: parked, waiting on the reporter.

## Work-type labels

Required on `ready-for-agent`; decides how `deliver` routes the work.

- `bug`: something that should work and does not. Routed to diagnosis.
- `enhancement`: new or changed behavior. The default for anything that is not a bug.
- `spec`: a split parent. Set by `to-slices` when an approved spec's split creates children; replaces the previous work-type. The issue holds the spec its children deliver in installments; when the last child closes it unblocks, and `deliver` runs the coverage check and opens the promotion PR. Every shaped issue has a spec; only a split parent carries the `spec` label.

Closure reasons use GitHub's own defaults (`duplicate`, `wontfix`, `invalid`) and are applied at close, never swept.

## Label colors

Applied by `scripts/reconcile-labels.py --repo <owner/name>`, dry-run first, `--create` only with the user's consent. Readiness roles are saturated and temperature-coded from parked to flying; work-types are pastel, `bug` and `spec` the deliberate exceptions.

| Label | Color | Description |
| --- | --- | --- |
| `needs-shaping` | `#D93F0B` | Parked for shaping: unsettled product or scope decisions; never selected by backlog build |
| `shaping` | `#FBCA04` | A shaping thread is attending this issue; set by backlog groom at dispatch |
| `needs-info` | `#D876E3` | Parked, waiting on the reporter |
| `ready-for-agent` | `#0E8A16` | Released: an agent may work it; requires a work-type |
| `ready-for-human` | `#5319E7` | Human-only; agents skip. Also the handback target for blockers |
| `building` | `#1D76DB` | Claimed: a build thread owns it; the claim comment is the dispatch declaration with its deadline |
| `bug` | `#D73A4A` | Something isn't working |
| `enhancement` | `#A2EEEF` | New feature or request |
| `spec` | `#8250DF` | Parent of a split: coverage check and promotion PR once every child is closed |

## Dependencies

- **Blocking** uses GitHub's native issue dependency. Read: `gh api repos/<owner>/<repo>/issues/<n> --jq '.issue_dependencies_summary'`, and treat `.blocked_by > 0` as blocked. Write: resolve the blocker's database id with `gh api repos/<owner>/<repo>/issues/<blocker> --jq '.id'`, then `gh api -X POST repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by -F issue_id=<id>`. A blocker clears when the blocking issue closes.
- **Children** use GitHub sub-issues for navigation: `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<id>`; read with `gh api repos/<owner>/<repo>/issues/<n>/sub_issues`. The sub-issue relation carries no gate by itself: a spec issue is gated because `to-slices` also wires it `blocked_by` each child. A child attached later (a capture against the parent, a gap the coverage check files) is wired the same way and re-blocks the parent.
- `backlog build` skips any issue with an open blocker.

## Claims

The claim comment is the dispatch declaration, one event with two readers: the human reads a statement, the next runner reads the claim. It carries the issue digest, the work branch, the worktree path, the model, effort, and harness, the thread name, the dispatcher's identity, and the deadline as an absolute timestamp.

- Claims are attributed: posted by the runner's own GitHub account, naming the branch. Another actor's claim, even expired, is not yours to clear; a takeover note may still land on the issue.
- Concurrent runners are possible. `building` is applied optimistically; the rare duplicate pickup in the window between sweep and claim is accepted rather than carrying a lock.
- A reclaim of your own expired claim is a new claim comment superseding the old, resuming from the branch so nothing is discarded. The ledger stays event-shaped: claim, outcome, reclaim.
- **Orphan sweep**: a `building` issue whose branch no longer exists, or whose claim has gone quiet past the quiet horizon of seven days, is surfaced by `backlog status` as a candidate reset to `ready-for-agent`. Never silently reset: the branch may hold unmerged work.

## Deadlines

Every claim carries a deadline as an absolute timestamp. Size it to the expected build in hours, not days: four hours for a routine issue, eight for a spec issue's coverage check or a wide change. `backlog status` rules on it; the dispatching thread passes it to `deliver` and through it to every subagent it dispatches.

## Readiness decision

- Groom proposes a route for every swept issue and applies `ready-for-agent` only to issues the human confirms in the plan. Parking and closure roles ride the plan's blanket approval.
- In a shaping thread the blessing records the commit hash of the spec on the artifact branch; the blessing authorizes exactly that revision. A commit past the blessed hash invalidates readiness: the issue returns to shaping until re-blessed.
- An approved split blesses its children: they publish `ready-for-agent`.

## Branches

- **Base branch**: recorded in `docs/agents/environment.md` § Branching (usually `main`). Worktrees and work branches fork from it; PRs target it, except a child's PR.
- **Work branch**: `<issue>-<slug>`, born inside its worktree, never checked out in the primary checkout. Shaping commits context changes on it; the later build continues on it and opens the issue's single PR. Pushed as commits land: the remote is the backup, and pushing is not publication.
- **Spec branch**: a spec issue's work branch. Children branch from it and PR into it; the spec issue's own PR is the promotion from the spec branch to the base branch, carrying `Closes #<spec issue>`.
- **Artifact branch**: `artifact/<issue>`, one per issue, holding every research dossier, prototype, and spec revision as commits. Permanently unmerged by intent; the blessed hash pins the spec revision; deleted when the issue closes. Every sweep skips the `artifact/` prefix.
