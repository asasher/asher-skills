---
name: shape
description: Shape one GitHub ticket into an approved spec, or resume shaping from its tracker record.
metadata:
  requires: [bare-minimum-design, capture, domain-modeling, interview, principle-codebase-design, principle-experience-first, principle-type-system-discipline, prototype, research, to-branch, to-slices, to-spec, to-subagent, to-thread, to-web]
  optional: [technical-writing, typescript-best-practices, writing-for-humans]
---

# Shape

Shape **one ticket**. If none is identified, establish the ticket through `capture` before shaping; combine work that must be decided together into that ticket with the user's approval.

Read the ticket, comments, artifact links, claims, and environment playbook. If this session is on the primary checkout or wrong branch, dispatch `shape <ticket>` through `to-thread` in a worktree on `<ticket>-<slug>`, then hand off before editing. Reuse an owned worktree and pushed branch when they exist. Keep the primary checkout's branch unchanged.

Before reopening decisions, re-read ownership and establish this session's shaping claim on the ticket, replacing its readiness label with `shaping`. Accept a dispatch claim assigned to this session. Another live or uncertain owner holds the work until a confirmed stop and handoff. Read back ownership and state before proceeding. For an existing split, first follow [revision recovery](reference/revisions.md).

## Settle the decisions

Read the project instruction file, `CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, and relevant ADRs. Reconstruct open decisions from the ticket and carry settled answers forward. Run `interview` here, with `domain-modeling` recording resolved terminology. Use the writing standards when available.

Work in order, using `principle-experience-first` to question requirements and remove unnecessary behavior:

1. **Users and experience.** Select affected user types and their changed journey. Create or update `PRODUCT.md` using [its format](PRODUCT-FORMAT.md) when needed. At creation, register one link under `## Context documents` in the project instruction file, stating its purpose and when to read it.
2. **System behavior.** Settle observable rules, states, and failure paths. For UI work, invoke `bare-minimum-design` to record durable visual decisions in `DESIGN.md`; if unavailable, retain the unresolved design work in shaping.
3. **Implementation.** Apply the codebase and type-system principles to ownership, interfaces, and test seams; use TypeScript guidance when relevant. Record scope, migration constraints, verification risk, and each criterion's durable-test or temporary-check choice.

Research precise fact questions through `research`, or resolve uncertain mechanisms and alternatives through `prototype`, via `to-subagent` when useful. Independent questions may run together; decisions wait only on their prerequisites.

## Record and approve

Record decisions as they settle. Commit and push coherent context changes before publishing their ticket record and before every handoff or pause. The remote and ticket record must support continuation on another machine.

Publish specs and research as HTML. Keep runtime prototypes in their useful format, with a published HTML explanation of the result and launch recipe. When alternatives need human judgment, include an inspectable comparison: a reachable preview, published artifact, or captured relevant states. Commit and push artifact sources to `artifact/<ticket>` via `to-branch --push`, then publish through `to-web`. The ticket records the question, result, URL, and revision. Evidence media goes only to the bucket.

When decisions are settled, run `to-spec` from the complete record; delegate synthesis only when useful. Resolve blocking Notes before requesting approval. For a revision, present `to-spec`'s delta from the last approved spec alongside the published result. Record the user's approval against the published spec's commit hash. A later spec revision requires new approval.

If the approved spec recommends splitting, run `to-slices`, which owns approval of the concrete split. Carry any prior approval that already covers that exact revision and plan. Otherwise mark the ticket `ready-for-agent`. Push the work branch before releasing any ticket. Leave partial publication in `shaping`; before pausing, record open decisions and the next action. Capture unrelated work separately.
