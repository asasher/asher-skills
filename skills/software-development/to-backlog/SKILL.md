---
name: to-backlog
description: Capture the loose items a conversation has surfaced — bugs, enhancement ideas, follow-ups — as minimal work-typed tickets in the bound tracker. Optionally attaches the captured tickets as children of a named parent ticket. Not for decomposing a decided direction — that's to-slices.
argument-hint: "[<parent ticket id to attach captured tickets under>]"
metadata:
  optional: [to-slices]
---

# To-Backlog

To-backlog owns one move: **get what the conversation surfaced into the tracker before it evaporates.** A working conversation — a user interview, a shaping thread, a build session — throws off loose items. It is capture, not decomposition: N unrelated undecided things into the intake queue, not one decided thing into ordered parts. For the latter, the `to-slices` sibling — absent it, say the decomposition move is unavailable and capture the direction as a single ticket instead.

The defining discipline is **context fidelity**: each ticket must survive a cold read at grooming, because this conversation evaporates. Each ticket carries what the chat knew — that fidelity is what lets grooming send a clear item straight to ready instead of defaulting everything to shaping.

## Command surface

- **`to-backlog`** — sweep the current conversation for capture-worthy items and publish the confirmed list as tickets.
- **`to-backlog <parent ticket id>`** — same, but attach each published ticket as a **child** of the given parent. Use when the captured tickets are installments of a parent's direction — e.g. gaps discovered while building one of its slices; under the backlog policy's open-children rule, attaching them re-blocks a spec-typed parent by itself.

## How a capture happens

1. **Sweep the whole conversation, first message to last.** Collect every **loose item** — real work that is not this conversation's deliverable: reported defects, requested or implied enhancements, follow-ups, questions that became work. Skip what is already tracked, already in scope here, or idle musing no one committed to. The step is done when every turn has been checked and each loose item is collected or deliberately skipped.
2. **Confirm the list — the human gate.** Present one compact list: per item a one-line title, the proposed work-type per the label roles (`docs/agents/backlog-policy.md` § Label roles) — a fact the conversation knows — and a one-phrase note of what context the ticket will carry. The user edits, drops, adds; **nothing publishes before they approve.** This is a confirm, not a quiz.
3. **Publish minimal tickets.** Create each through the tracker binding recorded in `docs/agents/platform.md` — absent a recorded binding, state the gap and ask the user before publishing anything. Each ticket gets a title, the work-type label, and a context-fidelity body — the symptom and repro as reported for a bug, the motivating exchange and intent for an enhancement, links to any artifact the conversation named — and nothing else. **Apply no readiness role**: an un-routed ticket is grooming's intake by design — readiness is grooming's judgment, and capture applying a readiness role would make it a second grooming.
4. **Attach to the parent, when one was given.** Wire each created ticket as the parent's child per the platform playbook's recorded relation.
5. **Readback.** Verify against the live tracker: every confirmed item maps to exactly one created ticket with its work-type, no readiness role, and — when a parent was given — its child relation resolving to the parent. Fix any miss before reporting the capture done.

## What a captured ticket is (and isn't)

- A **ticket** is the unit of claimable work — the tracker's "issue" role in a tracker-agnostic word.
- **Minimal but self-sufficient.** A captured ticket is context fidelity at the altitude of a report — not acceptance criteria, not a slice, not a plan.
- **As reported, not as investigated.** Verbatim reporter material — an error message, a stack trace, a quoted behavior — goes in as evidence; the conversation's own digging — file paths, code snippets — stays out.
