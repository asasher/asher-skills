# Slicing — the method

## Read the direction — one treatment for every input

To-slices splits a direction someone already decided. The input comes in one of these forms; all are read the same way: mine the decided direction, the actors, and the full surface.

- **A spec'd issue** (the primary input): an issue whose projection comment carries the spec's summary, render URL, and blessed commit hash, given by id. Read the spec from the `artifact/<issue>` branch **at the blessed hash** (`git show <hash>:<path>`), the canonical direction, plus the issue's comment trail for refinements the user made after the projection.
- **A spec document**: a spec file given by path. Read it exactly as the branch file.
- **A plan document**: a per-issue design doc. Read it as direction for a single slice's worth of work, or a small cluster.
- **The raw current conversation**: when no spec or plan was written, mine the conversation and the codebase understanding built up in it.

**Never modify the spec text.** To-slices reads the direction; it never edits it. Parenting a split issue over its slices changes issue state, not spec content.

## Draft vertical slices — the default shape

The default output is **tracer-bullet issues.** A **slice** is a narrow-but-complete path through every layer the change spans (data, logic, interface, whatever the stack is): it does one real thing end to end and is **demoable on its own**. **Tracer bullet** is the sizing bar on top: one fresh context window, small enough that an agent picking it up cold can finish it without running out of room.

The anti-pattern is the **horizontal layer**: "all the models," then "all the logic," then "all the UI." A horizontal issue cannot be demoed alone and does not derisk the whole path; a vertical slice proves the path end to end early and often. Prefer the thinnest slice that still demonstrates a real capability.

The draft is complete when every requirement in the direction maps to a slice: walk the direction's acceptance criteria and account for each; anything unassigned is a missing slice or a named exclusion the user approves.

**Every slice carries its rationale**, one or two sentences: why this boundary, and why the slice is demoable alone.

## The wide-refactor exception

One kind of work resists a vertical slice: a **mechanical, high-blast-radius change**, such as renaming a symbol used in a hundred places or swapping a dependency threaded through the codebase. Forcing it into a vertical slice is a fiction. Sequence it instead as three phases:

1. **Expand**: introduce the new form alongside the old, so both work at once. One issue.
2. **Migrate in batches**: move call sites over in reviewable batches, each its own issue, each demoable. Batches can run in parallel once expand lands.
3. **Contract**: remove the old form once nothing uses it. One issue, blocked on all the migrate batches.

The trigger is both conditions: the change is mechanical (little per-site judgement) and high blast radius (touches many sites). A change that is wide but not mechanical, or mechanical but small, is a normal vertical slice.

## How slices land

Slices of a spec'd issue land **stacked**: the spec issue's work branch is the spec branch, already carrying the shaping commits (`CONTEXT.md` terms, ADRs). Each slice's build branches from the spec branch and opens its PR into it, inheriting the language from birth. When a child's PR merges, the `merge` skill closes the child issue, which clears one of the spec issue's blockers. When the last child closes, the spec issue unblocks, `deliver` runs the coverage check on the spec branch, and the promotion PR carries the whole direction to the base branch at once. Say this in the draft so the user sees the landing, not just the cuts.

## Present the recommendation — the confirmation gate

**To-slices recommends; the user edits.** Present the split draft (template-guide § The split draft). The user reacts to reasons, moving a boundary or cutting an edge, and the draft is revised and re-presented until they approve.

**Nothing publishes before approval.** One gate confirms the whole operation, and that approval is also the readiness decision: the approved slices become `ready-for-agent` after the complete graph passes readback.

## Order and wire the edges

Once the split is approved, sort the issues into **dependency order, blockers first.** GitHub assigns an id at creation, so an issue can only reference its blocker once that id exists: every blocker must be created before its dependents. Topologically sort the graph; publish in that order.

Wire each dependency as a native `blocked_by` edge: resolve the blocker's database id with `gh api repos/<owner>/<repo>/issues/<blocker> --jq '.id'`, then `gh api -X POST repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by -F issue_id=<id>`. `backlog build` reads these edges and skips blocked work.

## Audit each issue — ready, or not published

Before publishing, audit every approved issue. Each must carry:

- **Observable acceptance**: criteria a verifier can exercise, not vibes.
- **Inherited context links**: the spec (its issue and blessed hash) and the decisions the slice relies on; a fresh context window must reach everything it needs from the issue alone.
- **An authority boundary**: what the executor may decide versus what is settled and must not be re-decided.
- **UX context, for UI surfaces**: the register, the key states (empty, loading, error, disabled, responsive), and links to `PRODUCT.md` and `DESIGN.md` where they exist.
- **True blocking edges only**: an edge that merely sequences convenience is not a blocker.

An issue failing the audit is fixed or dropped, never published thin for grooming to repair later.

## Publish

Before creating children, place an existing split parent in `shaping` and push its work branch so children will inherit the settled context. Create issues with `gh issue create`, blockers first, each with its title, body per template-guide § A single issue, work-type (`enhancement` or `bug`), and `shaping`. Link each issue to the spec's issue when one exists.

Persist the approved draft and draft-to-issue mapping on the parent, or on the first created issue for a split without a parent. Update that mapping as each issue is created. On an interrupted create, inspect GitHub before retrying; adopt the matching issue instead of creating a duplicate. Wire each native blocker after its issue exists. Keep every new issue unreleased until the entire graph and parent relations pass readback.

## Parent the slices

When the input was a spec'd issue, the slices carry the installments but the parent keeps the whole. Finish by parenting it over them:

- **Attach every slice as a sub-issue** of the parent: `gh api -X POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<id>`.
- **Wire the parent `blocked_by` every slice** with the same dependency verb as § Order and wire. This is the gate: the parent stays out of `backlog build`'s sweep until every child closes, and a child attached later (a capture against the parent, a gap the coverage check files) re-blocks it the same way.
- **Relabel the parent `spec`**, replacing its previous work-type. The parent's remaining work is the coverage check `deliver` runs when the blockers clear.
- **Post a pointer comment** on the parent linking every child, so anyone landing on it sees the split. Each child links back to the parent (§ Audit, inherited context links).

A source that was not an issue (a spec document, a plan, the conversation) has nothing to parent; skip this step.

## Release after readback

Read back every created issue, work-type, dependency, and parent relation against the approved draft. Verify that the spec branch exists remotely before releasing children that target it. Once the whole graph matches, replace `shaping` with `ready-for-agent` on the children and then the parent. Read the labels back and record completion on the mapping's issue. A release interrupted halfway is safe to resume because all dependencies already exist; preserve labels and claims a builder has since advanced.

An incomplete graph stays `shaping`, with its missing edges and next action recorded. Recovery finishes the existing graph before releasing any remaining issue.

## No stale content

An issue carries **no file paths and no code snippets.** They rot the moment the codebase moves; an issue is intent and the slice, not implementation. Describe the module, the contract, or the shape in prose instead.

The single exception: a **prototype-validated snippet** that encodes a decision more precisely than prose can, such as a state machine, a reducer, a schema, or a type shape. Inline only that decision-rich fragment and note it came from a prototype.
