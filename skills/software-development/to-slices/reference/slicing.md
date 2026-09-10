# Slicing — the method

## Read the direction — one treatment for every input

To-slices splits a direction someone already decided. The input comes in one of these forms; all are read the same way: mine the decided direction, the actors, and the full surface.

- **A spec'd issue** (the primary input): an issue whose projection comment carries the spec's summary, render URL, and approved commit hash, given by id. Read the spec from the `artifact/<issue>` branch **at the approved hash**, the canonical direction, plus the issue's comment trail for refinements the user made after the projection.
- **A spec document**: a spec file given by path. Read it exactly as the branch file.
- **A plan document**: a per-issue design doc. Read it as direction for a single slice's worth of work, or a small cluster.
- **The raw current conversation**: when no spec or plan was written, mine the conversation and the codebase understanding built up in it.

Preserve the source spec verbatim. Publish the split as child issues and parent relations.

## Draft vertical slices — the default shape

The default output is **tracer-bullet issues.** A **slice** is a narrow-but-complete path through every layer the change spans (data, logic, interface, whatever the stack is): it does one real thing end to end and is **demoable on its own**. **Tracer bullet** is the sizing bar on top: one fresh context window, small enough that an agent picking it up cold can finish it without running out of room.

Prefer the thinnest slice that demonstrates a real capability through the whole path.

The draft is complete when every requirement in the direction maps to a slice: walk the direction's acceptance criteria and account for each; anything unassigned is a missing slice or a named exclusion the user approves.

**Every slice carries its rationale**, one or two sentences: why this boundary, and why the slice is demoable alone.

## The wide-refactor exception

One kind of work resists a vertical slice: a **mechanical, high-blast-radius change**, such as renaming a symbol used in a hundred places or swapping a dependency threaded through the codebase. Sequence it as three phases:

1. **Expand**: introduce the new form alongside the old, so both work at once. One issue.
2. **Migrate in batches**: move call sites over in reviewable batches, each its own issue, each demoable. Batches can run in parallel once expand lands.
3. **Contract**: remove the old form once nothing uses it. One issue, blocked on all the migrate batches.

The trigger is both conditions: the change is mechanical (little per-site judgement) and high blast radius (touches many sites). A change that is wide but not mechanical, or mechanical but small, is a normal vertical slice.

## How slices land

Slices of a spec'd issue land **stacked**: the spec issue's work branch is the spec branch, already carrying the shaping commits (`CONTEXT.md` terms, ADRs). Each slice's build branches from the spec branch and opens its PR into it, inheriting the language from birth. When a child's PR merges, the `merge` skill closes the child issue, which clears one of the spec issue's blockers. When the last child closes, the spec issue unblocks, `deliver` runs the coverage check on the spec branch, and the promotion PR carries the whole direction to the base branch at once. Include the landing sequence in the draft.

## Present the recommendation — the confirmation gate

**To-slices recommends; the user edits.** Present the split draft (template-guide § The split draft). The user reacts to reasons, moving a boundary or cutting an edge, and the draft is revised and re-presented until they approve.

**Approval gates publication.** That approval is also the readiness decision: the approved slices become `ready-for-agent` after the complete graph passes readback.

## Order and wire the edges

Once the split is approved, sort the issues into **dependency order, blockers first.** GitHub assigns an id at creation, so an issue can only reference its blocker once that id exists: every blocker must be created before its dependents. Topologically sort the graph; publish in that order.

Wire each prerequisite as a native GitHub issue blocking relationship. `backlog build` reads these edges and skips blocked work.

## Audit each issue before publication

Before publishing, audit every approved issue. Each must carry:

- **Observable acceptance**: criteria a verifier can exercise.
- **Inherited context links**: the spec (its issue and approved hash) and the decisions the slice relies on; a fresh context window must reach everything it needs from the issue alone.
- **An authority boundary**: settled decisions and the choices delegated to the executor.
- **UX context, for UI surfaces**: the register, the key states (empty, loading, error, disabled, responsive), and links to `PRODUCT.md` and `DESIGN.md` where they exist.
- **True blocking edges**: each identifies a prerequisite the dependent slice needs.

Fix or drop issues that fail the audit before publication.

## Publish

Before creating children, place an existing split parent in `shaping` and push its work branch so children will inherit the settled context. Create issues, blockers first, each with its title, body per template-guide § A single issue, work-type (`enhancement` or `bug`), and `shaping`. Link each issue to the spec's issue when one exists. Inherit its milestone; replacing an existing assignment requires the user's approval in the split plan.

Persist the approved draft and draft-to-issue mapping on the parent, or on the first created issue for a split without a parent. Update that mapping as each issue is created. On an interrupted create, inspect GitHub before retrying; adopt any matching issue. Wire each native blocker after its issue exists. Keep every new issue unreleased until the entire graph and parent relations pass readback.

## Parent the slices

When the input was a spec'd issue, the slices carry the installments but the parent keeps the whole. Finish by parenting it over them:

- **Attach every slice as a native sub-issue** of the parent.
- **Wire the parent `blocked_by` every slice** with the same dependency verb as § Order and wire. This is the gate: the parent stays out of `backlog build`'s sweep until every child closes, and a child attached later (a capture against the parent, a gap the coverage check files) re-blocks it the same way.
- **Relabel the parent `spec`**, replacing its previous work-type. The parent's remaining work is the coverage check `deliver` runs when the blockers clear.
- **Post a pointer comment** on the parent linking every child, so anyone landing on it sees the split. Each child links back to the parent (§ Audit, inherited context links).

Parenting applies when the source is an existing issue.

## Release after readback

Read back every created issue, work-type, milestone assignment, dependency, and parent relation against the approved draft. Verify that the spec branch exists remotely before releasing children that target it. Once the whole graph matches, replace `shaping` with `ready-for-agent` on the children and then the parent. Read the labels back and record completion on the mapping's issue. A release interrupted halfway is safe to resume because all dependencies already exist; preserve labels and claims a builder has since advanced.

An incomplete graph stays `shaping`, with its missing edges and next action recorded. Recovery finishes the existing graph before releasing any remaining issue.

## Durable content

Describe intent, modules, contracts, and shapes in prose that stays useful as files move. Keep implementation paths and snippets in the implementation work.

An issue may include a **prototype-validated snippet** that encodes a decision more precisely than prose can, such as a state machine, a reducer, a schema, or a type shape. Inline only that decision-rich fragment and note it came from a prototype.
