# Slicing — the method

## Read the approved ticket

Require a ticket whose record links the published spec and approval of its exact commit hash. Read that spec from `artifact/<issue>` at the approved hash, plus the complete ticket history. A standalone document, plan, or conversation first needs a ticket and approved published spec.

The approved revision is the direction. Later comments may refine slice boundaries within it; changes to requirements, acceptance, or exclusions need a revised approved spec before slicing. Preserve the source spec verbatim and record the approved hash on the split and children.

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

Slices land **stacked**: the spec issue's work branch is the spec branch, already carrying the shaping commits (`CONTEXT.md` terms, ADRs). Each slice's build branches from the spec branch and opens its PR into it, inheriting the language from birth. When a child's PR merges, the `merge` skill closes the child issue, which clears one of the spec issue's blockers. When the last child closes, the spec issue unblocks, `deliver` runs the coverage check on the spec branch, and the promotion PR carries the whole direction to the base branch at once. Include the landing sequence in the draft.

## Present the recommendation — the confirmation gate

**To-slices recommends; the user edits.** Present the split draft (template-guide § The split draft). Carry existing approval when it covers the exact source revision, slices, graph, and landing plan. Present only changed or unapproved parts; resolve boundary edits within the approved direction.

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

Before publication, re-read the parent's and existing children's claims. Establish publication ownership for the parent and child records being changed, accepting this session's shaping claim. Changing another live or uncertain owner's records or authority requires a confirmed stop and handoff. Hold the parent and open children whose contracts change in `shaping`, then push the work branch so children inherit settled context. Reconcile existing children against the approved draft, including their source hashes and coverage of completed work. Create missing issues, blockers first, each with its title, body per template-guide § A single issue, work-type (`enhancement` or `bug`), and `shaping`. Link each child to the parent. Inherit its milestone; replacing an existing assignment requires the user's approval in the split plan.

Persist the approved draft, approval record, and draft-to-issue mapping on the parent. Update that mapping as each issue is created. On an interrupted create, inspect GitHub before retrying; adopt any matching issue. Wire each native blocker after its issue exists. Keep every new issue unreleased until the entire graph and parent relations pass readback.

## Parent the slices

The slices carry the installments and the parent keeps the whole. Finish by parenting it over them:

- **Attach every slice as a native sub-issue** of the parent.
- **Wire the parent `blocked_by` every slice** with the same dependency verb as § Order and wire. This is the gate: the parent stays out of `backlog build`'s sweep until every child closes, and a child attached later (a capture against the parent, a gap the coverage check files) re-blocks it the same way.
- **Relabel the parent `spec`**, replacing its previous work-type. The parent's remaining work is the coverage check `deliver` runs when the blockers clear.
- **Post a pointer comment** on the parent linking every child, so anyone landing on it sees the split. Each child links back to the parent (§ Audit, inherited context links).

## Release after readback

Read back every created issue, work-type, milestone assignment, dependency, and parent relation against the approved draft. Verify that the spec branch exists remotely before releasing children that target it. Once the whole graph matches, replace `shaping` with `ready-for-agent` on held open children and then the parent. Read the labels back and record completion on the mapping's issue. A release interrupted halfway resumes the existing graph; preserve labels and claims a builder has since advanced. Read back unchanged records without taking ownership of their live builders.

An incomplete graph stays `shaping`, with its missing edges and next action recorded. Recovery finishes the existing graph before releasing any remaining issue.

## Durable content

Describe intent, modules, contracts, and shapes in prose that stays useful as files move. Keep implementation paths and snippets in the implementation work.

An issue may include a **prototype-validated snippet** that encodes a decision more precisely than prose can, such as a state machine, a reducer, a schema, or a type shape. Inline only that decision-rich fragment and note it came from a prototype.
