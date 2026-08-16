---
name: to-backlog
description: Capture the loose items a conversation has surfaced — bugs, enhancement ideas, follow-ups — as minimal tickets in the bound tracker, each carrying its chat context and a work-type but no readiness role, so the tracker's next routing pass finds and routes them. Optionally attaches captures as children of a named parent ticket. Not for decomposing a decided direction — that's to-slices.
argument-hint: "[<parent ticket id to attach captures under>]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# To-Backlog

To-backlog owns one move: **get what the conversation surfaced into the tracker before it evaporates.** A working conversation — a user interview, a shaping thread, a build session — throws off items that are not its subject: a bug someone describes in passing, an enhancement idea, a follow-up nobody should have to remember. To-backlog sweeps them up, confirms the list with the user, and publishes each as a minimal ticket into the bound tracker — **work-typed but carrying no readiness role**, so the tracker's routing sweep finds and routes them. It is capture, not decomposition: N unrelated undecided things into the intake queue, not one decided thing into ordered parts. For the latter, the `to-slices` sibling.

The defining discipline is **context fidelity**: this conversation evaporates, and whoever routes or builds the ticket later won't have it. Each ticket carries what the chat knew — that fidelity is what lets the routing pass send a clear item straight to ready instead of defaulting everything to shaping.

## Command surface

- **`to-backlog`** — sweep the current conversation for capture-worthy items and publish the confirmed list as tickets.
- **`to-backlog <parent ticket id>`** — same, but attach each published ticket as a **child** of the given parent through the parent/child relation the platform playbook records. Use when the captures are installments of a parent's direction — e.g. gaps discovered while building one of its slices; under the backlog policy's open-children rule, attaching them re-blocks a spec-typed parent by itself.

## How a capture happens

1. **Sweep the conversation.** Collect every item that is real work but not this conversation's deliverable: reported defects, requested or implied enhancements, follow-ups, questions that became work. Skip what is already tracked, already in scope here, or idle musing no one committed to.
2. **Confirm the list — the human gate.** Present one compact list: per item a one-line title, the proposed work-type per the label roles (`docs/agents/backlog-policy.md` § Label roles — the type is a fact best known now, while the context is live), and a one-phrase note of what context the ticket will carry. The user edits, drops, adds; **nothing publishes before they approve.** This is a confirm, not a quiz — no granularity or edge interrogation; captures are not a split.
3. **Publish minimal tickets.** Create each through the tracker binding recorded in `docs/agents/platform.md`: a title, the work-type label, and a body carrying the item's chat context — the symptom and repro as reported for a bug, the motivating exchange and intent for an enhancement, links to any artifact the conversation named. **Apply no readiness role**: an un-routed ticket is the routing sweep's intake by design. No dependency edges, no readiness audit, no slicing — a capture that needs those has outgrown capture and belongs to shaping or `to-slices`.
4. **Attach to the parent, when one was given.** Wire each created ticket as the parent's child per the platform playbook's recorded relation.
5. **Readback.** Verify against the live tracker: every confirmed item maps to exactly one created ticket with its work-type, no readiness role, and — when a parent was given — its child relation resolving to the parent. Fix any miss before reporting the capture done.

## What a capture is (and isn't)

- **Minimal but self-sufficient.** A capture ticket is the item plus its live context, at the altitude of a report — not acceptance criteria, not a slice, not a plan. It must survive being read cold by a groom session that never saw this chat.
- **Work-typed, never readiness-labeled.** The work-type (bug / enhancement / whatever the label roles name) is recorded at capture because it is a fact the conversation knows. Readiness is a routing judgment and belongs to the routing pass — capture applying a readiness role would make it a second routing pass.
- **Generic vocabulary.** A **ticket** is the unit of pickup-able work — the tracker's "issue" role in a tracker-agnostic word, same as every sibling.
- **No file paths or code snippets**, with one exception: a verbatim fragment the reporter themselves gave (an error message, a stack trace, a quoted behavior) is evidence, and evidence is context.

## Dependency surface

- **Project playbooks** — read from `docs/agents/`: the **label roles** (`backlog-policy.md` § Label roles — the work-type names, and the rule that no-readiness-role is routing intake), the **parent/child relation** (`platform.md` — how a child is attached), and the **tracker binding** (`platform.md` — how tickets are created). Absent a recorded binding, state the gap and ask the user before publishing anything.
- **Sibling skills** — `to-slices`, named only as the boundary: a "capture" that is really a decided direction to decompose is handed there, on the user's call. Absent the sibling, state that the decomposition move is unavailable and capture the direction as a single ticket instead.
