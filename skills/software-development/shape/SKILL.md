---
name: shape
description: Shape one GitHub ticket into an approved spec, or resume shaping from its tracker record.
metadata:
  requires: [capture, domain-modeling, interview, principle-codebase-design, principle-experience-first, principle-type-system-discipline, prototype, research, to-branch, to-slices, to-spec, to-subagent, to-thread, to-web]
  optional: [technical-writing, typescript-best-practices, writing-for-humans]
---

# Shape

Shape **one ticket**. If none is identified, establish the ticket through `capture` before shaping; combine work that must be decided together into that ticket with the user's approval.

Read the ticket, comments, artifact links, and environment playbook. If this session is on the primary checkout or wrong branch, dispatch `shape <ticket>` through `to-thread` in a worktree on `<ticket>-<slug>`, then hand off before editing. Reuse an owned worktree and pushed branch when they exist. Keep the primary checkout's branch unchanged.

## Settle the decisions

Read the project instruction file, `CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, and relevant ADRs. Reconstruct open decisions from the ticket; re-ask nothing it settles. Run `interview` here, with `domain-modeling` recording resolved terminology. Use the writing standards when available.

Work in order, using `principle-experience-first` to question requirements and remove unnecessary behavior:

1. **Users and experience.** Select affected user types and their changed journey. Create or update `PRODUCT.md` using [its format](PRODUCT-FORMAT.md) when needed.
2. **System behavior.** Settle observable rules, states, and failure paths.
3. **Implementation.** Apply the codebase and type-system principles to ownership, interfaces, and test seams; use TypeScript guidance when relevant. Record scope, migration constraints, verification risk, and each criterion's durable-test or temporary-check choice.

Offer a pause before implementation design. Research precise fact questions through `research`, or resolve uncertain mechanisms and alternatives through `prototype`, via `to-subagent` when useful. Independent questions may run together; decisions wait only on their prerequisites.

## Record and approve

Record decisions as they settle. Commit and push coherent context changes before publishing their ticket record and before every handoff or pause. A later machine continues from the remote, not this session's memory.

Publish specs and research as HTML. Keep runtime prototypes in their useful format, with a published HTML explanation of the result and launch recipe. Commit and push artifact sources to `artifact/<ticket>` via `to-branch --push`, then publish through `to-web`. The ticket records the question, result, URL, and revision. Evidence media goes only to the bucket.

When decisions are settled, run `to-spec` from the complete record; delegate synthesis only when useful. Resolve blocking Notes before requesting approval. Record the user's approval against the published spec's commit hash. A later spec revision requires new approval.

If the approved spec recommends splitting, obtain approval for the split and run `to-slices`. Otherwise mark the ticket `ready-for-agent`. Push the work branch before releasing any ticket. Leave partial publication in `shaping`; before pausing, record open decisions and the next action. Capture unrelated work separately.
