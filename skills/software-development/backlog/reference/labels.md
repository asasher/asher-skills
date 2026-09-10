# Labels, claims, deadlines, branches

The fixed conventions every backlog verb and verb skill shares. `backlog setup` creates this fixed label set; branch names follow from the issue number.

## Readiness labels

One per open issue once groomed; none means "not yet groomed".

- `needs-shaping`: parked for shaping. Product, design, or scope decisions need resolution or delegation, or a build found the approved spec contradicted by the code. Build eligibility starts at `ready-for-agent`.
- `shaping`: a shaping thread or an approved split publication owns it. Set at dispatch, or while a split is being wired, so grooming reads it as active context and building skips it. Cleared when the spec is approved and any split graph has passed readback; abandonment returns it to `needs-shaping` after recovery.
- `ready-for-agent`: released. Groom sets it for an issue whose decisions are settled; `shape` sets it when the spec is approved; `to-slices` sets it on the children of an approved split. Requires a work-type.
- `building`: reserved or claimed. The provisional claim reserves capacity until a build thread is verified alive; the claim comment is the dispatch declaration. Set by `backlog build`, replacing `ready-for-agent`. Superseded by closure, by a reclaim comment, or by the human-confirmed orphan reset.
- `ready-for-human`: only a human may work it. Also the handback target for a build that hits an environment blocker or a verification cap: the comment names why only a human can act on what remains. Route blockers a repo change can clear as work.
- `needs-info`: parked, waiting on the reporter.

## Work-type labels

Required on `ready-for-agent`; decides how `deliver` routes the work.

- `bug`: something that should work and does not. Routed to diagnosis.
- `enhancement`: new or changed behavior. The default for anything that is not a bug.
- `spec`: a split parent. Set by `to-slices` when an approved spec's split creates children; replaces the previous work-type. The issue holds the spec its children deliver in installments; when the last child closes it unblocks, and `deliver` runs the coverage check and opens the promotion PR. Every shaped issue has a spec; only a split parent carries the `spec` label.

Close consolidated or duplicate tickets as `not planned`, with a comment linking the surviving ticket and explaining the disposition. Include these closure decisions in the groom plan.

## Label appearance

The bundled [label reconciler](../scripts/reconcile-labels.py) owns colors and descriptions. [Setup](setup.md) previews and applies that scheme with the user's approval.

## Milestones

For batch capture, consolidation, splitting, or completion, use [milestone grouping](milestones.md). Milestones organize tickets; native dependencies and approved spec splits govern execution.

## Dependencies

- **Blocking** uses GitHub's native issue dependency. An issue stays blocked while any blocker is open; closing the blocker satisfies that dependency.
- **Children** use GitHub sub-issues for navigation. A spec issue's gate comes from `to-slices` wiring it `blocked_by` each child. A child attached later (a capture against the parent, a gap the coverage check files) is wired the same way and re-blocks the parent.
- `backlog build` skips any issue with an open blocker.

GitHub REST relationship writes take database IDs (`id`), rather than issue numbers: `sub_issue_id` for children and `issue_id` for blockers. Read back both relationships after writing.

## Claims

The claim comment is the provisional dispatch declaration, one event with two readers: the human reads a statement, the next runner reads the claim. It carries the issue digest, the work branch, the worktree path, the model, effort, and harness, the thread name, the dispatcher's identity, and the deadline as an absolute timestamp.

- Claims are attributed: posted by the runner's own GitHub account, naming the branch. Preserve other actors' claims, including expired ones; record takeovers as superseding notes.
- Serialize admission for concurrent dispatchers on the same machine through one dispatch owner or a shared lock covering capacity check, claim, and verified spawn. Count live builds and unresolved reservations against the configured limit. Re-read the issue before claiming; a duplicate claim stops before a second worker starts.
- Record the verified thread id on spawn success. On failure, post a failed-dispatch outcome and release the claim only after the worker is confirmed stopped or never started. Retain the reservation while worker liveness is uncertain.
- A reclaim of your own expired claim is a new claim comment superseding the old, resuming from the branch so nothing is discarded. The ledger stays event-shaped: claim, outcome, reclaim.
- **Orphan sweep**: a `building` issue whose branch no longer exists, or whose claim has gone quiet past the quiet horizon of seven days, is surfaced by `backlog status` as a candidate reset to `ready-for-agent`. Require human confirmation for a reset, preserving any unmerged work.

## Deadlines

Every claim carries a deadline as an absolute timestamp. Size it to the expected build in hours: four hours for a routine issue, eight for a spec issue's coverage check or a wide change. `backlog status` rules on it; the dispatching thread passes it to `deliver` and through it to every subagent it dispatches.

## Readiness decision

- Groom proposes a route for every swept issue and applies `ready-for-agent` only to issues the human confirms in the plan. Parking and closure roles ride the plan's blanket approval.
- In a shaping thread the approval records the commit hash of the spec on the artifact branch; the approval authorizes exactly that revision. A newer spec revision invalidates readiness; unrelated research or prototype commits do not: the issue returns to shaping until re-approved.
- An approved split approves its children, but they receive `ready-for-agent` only after all issues, parent relations, and blockers have been read back. Partially published splits remain `shaping` for recovery.

## Branches

- **Base branch**: recorded in `docs/agents/environment.md` § Branching (usually `main`). Worktrees and work branches fork from it; PRs target it, except an approved spec split child's PR.
- **Work branch**: `<issue>-<slug>`, created and used in its secondary worktree, preserving the primary checkout's branch. Shaping commits context changes on it; the later build continues on it and opens the issue's single PR. Pushed as commits land: the remote supports recovery; publication also requires a linked record.
- **Spec branch**: a spec issue's work branch. Children branch from it and PR into it; the spec issue's own PR is the promotion from the spec branch to the base branch, carrying `Closes #<spec issue>`.
- **Artifact branch**: `artifact/<issue>`, one per issue, holding every research dossier, prototype, and spec revision as commits. Permanently unmerged by intent; the approved hash pins the spec revision; deleted when the issue closes. Build selection ignores the `artifact/` prefix; status inspects it for recovery and cleanup.
