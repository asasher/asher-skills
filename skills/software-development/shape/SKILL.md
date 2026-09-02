---
name: shape
description: Shape one GitHub issue into a blessed spec on its own branch, and split it into child issues when the approved spec recommends it. Use before implementation or to resume shaping from the issue record.
metadata:
  requires: [domain-modeling, interview, principle-codebase-design, principle-experience-first, principle-type-system-discipline, prototype, research, technical-writing, to-branch, to-slices, to-spec, to-subagent, to-web, worktree, writing-for-humans]
  optional: [capture, typescript-best-practices]
---

# Shape

Use the `worktree` skill to prepare or inspect a worktree on the issue's work branch (`<issue>-<slug>`, from the base branch recorded in `docs/agents/environment.md`). The branch carries continuity across sessions and machines; the worktree may be reused or recreated. Commit and push project context changes on this branch as they land. The later build continues on it and opens the issue's single PR.

Read the issue (`gh issue view <n> --comments`), its linked artifacts, the project instruction file, and the project context files (`CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, ADRs). Reconstruct the design frontier from the issue record. Re-ask nothing the record settles.

Separate the desired outcome from proposed solutions and claimed requirements. For each claimed requirement, identify its source and why it exists. Keep explicit decisions in the record settled unless new evidence creates a conflict. Treat inherited process, current structure, and solution language as open design material.

Use `writing-for-humans` for questions and `technical-writing` for issue prose. Run `interview` inline, with `principle-experience-first` setting the target and `domain-modeling` tightening the language and recording terms as they settle.

At each level, question, subtract, then simplify. A step, choice, state, rule, or interface earns its place when removing it would worsen an affected user's observable experience or violate a supported constraint.

Work the design tree in order:

1. **Users**: select the affected user types from `PRODUCT.md`. Add a new type there when the work introduces one. If the file does not exist, create it from [PRODUCT-FORMAT](./PRODUCT-FORMAT.md).
2. **Experience**: map the affected part of the current core loop. Remove or merge steps, choices, and states that have not earned their place. Then settle what changes in what each affected user sees, touches, and does.
3. **System behavior**: inspect the current process, states, and rules. Remove or merge behavior that has not earned its place. Then settle observable behavior shared across users or experienced indirectly.
4. **Implementation**: design the coherent target as if every retained requirement had existed from the first version. Record migration, compatibility, rollout, and temporary-coexistence constraints separately. Apply `principle-codebase-design` to settle module ownership, interfaces, seams, and tests at those seams. For a statically typed target, apply `principle-type-system-discipline` to settle domain states, semantic identifiers, authoritative schemas, and parsing at external and network boundaries. For a TypeScript target, also use `typescript-best-practices` when available. Settle, per acceptance criterion, which checks become durable guards in the suite and which are throwaway verification scripts.

Settle every decision at one level before opening the next. When users, experience, and system behavior are settled, say: "Experience is settled. Implementation is next. This is a handoff point." The user may continue or park the issue.

For a question that needs source-backed investigation, dispatch the `research` skill via `to-subagent`. For a question that needs an artifact to settle it, dispatch the `prototype` skill via `to-subagent`. Give each fresh subagent one question and only the context it needs. A dispatched question blocks only the decisions that depend on it.

Every artifact is HTML and lives in two places. For each returned dossier or prototype, commit it to the issue's artifact branch `artifact/<issue>` via `to-branch` with `--push`, publish that committed revision via `to-web`, then comment a projection on the issue: the question, the concise result, the durable URL, and the commit hash. Present prototypes to the user and record the resulting decision on the issue. The artifact branch never merges; it is deleted when the issue closes.

Record settled decisions on the issue as they land. Offer work outside this issue to the `capture` skill; absent it, list the items at the close.

When the design frontier is empty, run `to-spec` inline so it can synthesize the issue record and current conversation. For a revision, also pass the previous approved spec so its acceptance-criterion identifiers remain stable. If synthesis returns a blocking Note, record it on the issue and reopen that part of the design frontier. Otherwise publish the returned HTML spec through the same `to-branch` then `to-web` sequence and comment its projection on the issue.

After the user approves a published revision, close the session in this order:

1. Record the approved commit hash on the issue: that hash is the blessing, and a later commit on the artifact branch invalidates it.
2. When the spec recommends a split, present the recommendation and ask. On yes, run `to-slices` inline against this issue: it publishes the children as `ready-for-agent` sub-issues, wires this issue `blocked_by` each child, and relabels this issue `spec`.
3. Push the work branch. Swap `shaping` for `ready-for-agent` on this issue. A split issue is now ready and blocked, and unblocks when its last child closes.

Before pausing without approval, push the work branch and record every open frontier item on the issue.
