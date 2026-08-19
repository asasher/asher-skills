---
name: shape
description: Shape one ticket, until it carries a spec. Use when work needs shaping before anything builds on it, or to resume a shaping thread on its subject's record.
argument-hint: "<ticket id>"
metadata:
  requires: [domain-modeling, interview, to-spec, worktree]
  optional: [experience-first, writing-for-humans, prototype, research, to-backlog, to-branch, to-slices, to-subagent, watch-until]
---

# Shape

Settle **one ticket's** strategic decisions — one subject per thread — ending in a spec blessed at a commit hash. A **stateful orchestrator**: everything it settles lands in the **record** — the ticket thread, the spec on its artifact branch, and the context files committed on the ticket's work branch.

A shaping thread **opens no change request.** Its worktree sits on the **ticket's work branch**: context-file edits (`CONTEXT.md`, `PRODUCT.md`, `DESIGN.md`, ADRs) are committed there and pushed as they land — `build-change` later continues on the same branch, so they reach main inside the build's change request. Throwaway artifacts (spec, prototypes, dossiers) live on `artifact/*` branches (`artifact/<ticket>-<slug>`; `artifact/<slug>` when ticketless), published via the `to-branch` sibling.

User-facing text follows the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

## Intake

Read the subject: the ticket thread and linked artifacts when it's a ticket, the handed material when it's an idea, plus the **repo context files** — `CONTEXT.md`, and `PRODUCT.md`/`DESIGN.md` where they exist — and the project instruction file's `## Context documents` index for the documents whose clauses match. Seed the frontier: every open decision listed, every settled one recorded with its source.

When the dispatcher supplied a worktree, inspect it through the `worktree` skill and record the directory and branch. Every repository artifact produced during shaping stays in that worktree, on the subject's artifact branches.

## The loop

- Build the decision tree per the `experience-first` sibling — users, then experience, then system behavior, then implementation; implementation questions enter the frontier only when the behavior governing them is settled — then run the `interview` skill on the subject, inline in this thread. When the experience register's frontier empties, announce the seam: the user continues, or blesses that register and parks the subject for its next shaper. Absent `experience-first`, order the tree by dependency alone and say the standard was not loaded.
- Run the `domain-modeling` skill alongside, per its own contract: terms and ADR-worthy decisions are written into the context files the moment they crystallise — committed on the ticket's work branch and pushed. They reach main when the build's change request merges.
- A question that needs source-backed investigation goes to the `research` skill; a question paper can't settle goes to the `prototype` skill — each dispatched via the `to-subagent` skill (absent it, run them inline). Absent `research` or `prototype`, park the question as open and say so. A dispatched question blocks only what depends on it; results re-enter the frontier as evidence, their artifacts landing on artifact branches with links in the record.
- When the subject is a ticket, record settled decisions on its thread as they land.
- An item surfacing mid-thread that is real work but not this subject — a bug mentioned in passing, an adjacent idea — is offered to the `to-backlog` skill for capture. Absent that sibling, park the item as open and say so.

## Crystallise — the spec is the exit

When the subject's frontier is empty, run the `to-spec` skill on it automatically. It writes the spec to the artifact branch, stamps the ticket's **projection** with the commit hash it was rendered from, and creates the ticket when the subject was only an idea; the spec declares the **test split**. Posting a spec is a proposal, not a state change — readiness still waits for the user's blessing. A spec may end by recommending a split; executing one via the `to-slices` skill happens only on the user's explicit approval, in a comment or here in the thread. Absent that sibling, park the split as open and say so.

## The comment watch

Once the spec is published and no blessing has arrived in this thread, run the `watch-until` skill on the spec'd ticket — condition: a new comment from the user on the ticket. Absent that sibling, say comments need an explicit ping. On wake, classify: a tweak comment — apply the requested tweak as a new commit on the artifact branch, refresh the ticket's projection, reply with what changed, resume watching. A readiness signal ("LGTM", "ready for agent"), in that comment or arriving here in the thread — record the hash it blesses and exit to § Done. The watch carries a timeout; when it reports timed out, surface the open state and stop.

## Blessed at a hash

The blessing binds to the **artifact-branch commit hash** of the spec the user read, and may be **per register** (the `experience-first` sibling's seam): an experience blessing at one hash, an implementation blessing later at another — the subject stays in shaping until every register it needs is blessed. A later commit invalidates a blessing only when it **changes the text that blessing covers** — the whole spec for a whole-spec blessing, the register's sections for a register blessing; the mechanical check is a diff between the blessed hash and the head. Changed covered text needs a fresh blessing at its new hash; unchanged text keeps its blessing while other sections move. Shape executes only the user's explicit calls — the blessing and an approved split — and stamps no lifecycle label of its own.

## Done

The subject carries a spec blessed at a hash, and the work branch — context commits included — is pushed and recorded on the ticket: that branch is the handoff to `build-change`, which materializes its own worktree from it. Remove this thread's worktree through the `worktree` skill. Artifact branches stay as the record until spent. Report what settled and what remains open.

## Resume

A fresh session on the same subject reads the record at its head plus the repo context files, recomputes the frontier from what is still open, and re-asks nothing the record answers. A re-entered subject — a blessed spec the code later contradicts — seeds its frontier from the contradiction.

## Dependency surface

- **Siblings:** declared in frontmatter. Absent a required one, state the requirement and stop.
- **Project surface:** the repo context files and the `## Context documents` index (§ Intake); the tracker and branch bindings in `docs/agents/platform.md` when the subject is a ticket. Absent a tracker, idea shaping still works — the record lives on the artifact branch and in the raising conversation.
