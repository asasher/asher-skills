---
name: shape
description: Shape one ticket into a spec. Use before implementation or to resume shaping from the ticket record.
argument-hint: "<ticket id>"
metadata:
  requires: [domain-modeling, interview, principle-experience-first, prototype, research, to-backlog, to-branch, to-spec, to-subagent, to-web, worktree, writing-for-humans]
---

# Shape

Use the `worktree` skill to prepare or inspect a worktree on the ticket's work branch. The branch carries continuity across sessions and machines; the worktree may be reused or recreated. Commit and push project context changes on this branch as they land. The later build continues on it and opens the ticket's single change request.

Read the ticket, its linked artifacts, the project instruction file, and the project context files (`CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, ADRs). Reconstruct the design frontier from the ticket record. Re-ask nothing the record settles.

Use `writing-for-humans` for questions and ticket prose. Run `interview` inline, with `principle-experience-first` setting the target and `domain-modeling` tightening the language and recording terms as they settle.

Work the design tree in order:

1. **Users**: select the affected user types from `PRODUCT.md`. Add a new type there when the work introduces one. If the file does not exist, create it from [PRODUCT-FORMAT](./PRODUCT-FORMAT.md).
2. **Experience**: settle what changes in what each affected user sees, touches, and does.
3. **System behavior**: settle observable behavior shared across users or experienced indirectly.
4. **Implementation**: settle seams, schema, modules, and interfaces.

Settle every decision at one level before opening the next. When users, experience, and system behavior are settled, say: "Experience is settled. Implementation is next. This is a handoff point." The user may continue or park the ticket.

For a question that needs source-backed investigation, dispatch the `research` skill via `to-subagent`. For a question that needs an artifact to settle it, dispatch the `prototype` skill via `to-subagent`. Give each fresh subagent one question and only the context it needs. A dispatched question blocks only the decisions that depend on it.

For every returned dossier or prototype, publish the artifact to its own `artifact/<ticket>-<slug>` branch via `to-branch` with `--push`, publish that committed revision via `to-web`, then add a ticket projection with the question, concise result, durable URL, and commit hash. Present prototypes to the user and record the resulting decision on the ticket. Artifact branches retain the historical snapshots and never merge into main.

Record settled decisions on the ticket as they land. Offer work outside this ticket to `to-backlog`.

When the design frontier is empty, run `to-spec` inline so it can synthesize the ticket record and current conversation. Publish the returned HTML spec through the same `to-branch` then `to-web` sequence and write its projection to the ticket. After the user approves that published revision, record the approved commit hash and mark the ticket `ready-for-agent`.

Before pausing or completing, push the ticket branch and record every open frontier item on the ticket.
