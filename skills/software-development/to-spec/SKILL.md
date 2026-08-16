---
name: to-spec
description: Turn a settled conversation or shaping record into a spec — an HTML document on the subject's artifact branch, opening with a diagram; the ticket gets a summary, render link, and commit hash. Creates the ticket when none exists. Pure synthesis, no interview.
argument-hint: "[<ticket id, or a name for the spec>]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [writing-for-humans, to-web]
---

# To-Spec

To-spec owns one move: **take a conversation that already reached a decision and write the spec it earned.** It reads the current conversation and the codebase/project understanding built up in it, captures what was **decided**, and writes a **spec**: the high-level direction document downstream work builds on.

The defining constraint is **pure synthesis, no interview.** To-spec does not re-elicit requirements, does not re-ask what the conversation already settled, and does not stall waiting on the user. It captures what's decided and **flags what isn't in the spec's Notes** — an open question recorded is worth more here than a question asked.

User-facing text follows the `writing-for-humans` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers. Absent it, write plainly and say the standard was not loaded.

## Command surface

- **`to-spec [<ticket id, or name>]`** — synthesize the current conversation into a spec on the subject's artifact branch and project it onto the subject's ticket: given a ticket id, that ticket; given none, create the ticket to carry the projection (deriving a short kebab-case name from the decided direction). With no tracker bound, the projection lands in the raising conversation instead.

Load [synthesis](reference/synthesis.md) for the method (what to mine, the artifact sweep, the no-interview rule, dev-vs-non-dev gating, the no-stale-content rule, where the spec lives, sign-off) and [template-guide](reference/template-guide.md) for what goes in each section.

## How a spec gets written

The full method is in [synthesis](reference/synthesis.md); the shape:

1. **Mine, don't ask.** Read the conversation and the codebase/project understanding it built. Start from the shaping record when one exists (synthesis § What to mine). Extract the problem, the decided solution, the decisions taken and the constraints that forced them. Sweep every generated artifact that informed a decision into a **Supporting artifacts** entry (synthesis § Sweep the artifacts). Anything left undecided becomes a line in **Notes**, never a question back to the user.
2. **Classify the work — dev or non-dev.** Our work isn't all software. A **dev spec** keeps the dev-only sections (Testing decisions, Test split, Test seams) and runs the seams step below; a **non-dev spec** skips them and uses only the core sections.
3. **For dev specs only — sketch the test seams, declare the test split, sweep the contract surface.** Name the public seams the work would be tested at, **prefer the highest existing seam**, declare per acceptance criterion whether it lands as a durable suite test or a throwaway verification script (synthesis § The two declarations), and enumerate the contract decisions hiding as defaults (synthesis § Sweep the contract surface).
4. **Write the spec to the artifact branch** — one HTML document on `artifact/<ticket>-<slug>` (`artifact/<slug>` when ticketless), **opening with a diagram** of the moving parts (flow, sequence, or state — whichever fits) before any prose, then the template's sections in generic vocabulary. The branch file is **canonical**. Then write the ticket's **projection**: a writing-for-humans summary, the `to-web` render URL (absent that sibling, link the branch file and say the render was not deployed), and the commit hash it was rendered from; post a short comment noting what changed. Ticket reads, comments, creation, and the `artifact/` branch convention follow the tracker and branch bindings in `docs/agents/platform.md`. No ticket yet: create it. No tracker bound: land the projection in the raising conversation (synthesis § Where the spec lives).
5. **Audit fidelity, then classify the Notes.** Before sign-off, audit in both directions: every material decision from the conversation appears in the spec, and the spec covers the subject ticket's own stated requirements — delivered or explicitly excluded (synthesis § Sign-off). Every Notes line is classified **blocking** (must be settled upstream before tickets), **delegated** (the executor may choose; boundary named), or **deferred** (parked, with a home). A spec with an unclassified material Note is not done; an open blocking Note means the direction isn't ready to build on — say so in the report. A direction too big for one build ends the spec with a **recommended split** — a proposal only; splitting is the user's call.
6. **Sign-off — the direction's approval gate.** User present: approve inline. AFK: the projection sits on the ticket where comments reach it — the user's LGTM is the approval, and it binds to the **commit hash** the projection carries (synthesis § Sign-off). Any later commit past the blessed hash invalidates the blessing. Readiness labels are not to-spec's to apply.

## What a spec is (and isn't)

- **Generic vocabulary.** A spec describes direction that may later split into **tickets**. Say "spec" and "ticket" — never GitHub-specific "issue." The unit of downstream work is a ticket.
- **The branch file is canonical; the ticket holds a projection** — summary, render URL, and the commit hash it was rendered from. A stale projection is visible by its hash. Revisions are commits on the artifact branch; ticket comments are the notification trail.
- **Two declarations ride in the spec:** the **context delta** — new glossary terms and ADR drafts, landed on main by the build that makes them true — and the **test split** — per acceptance criterion, durable suite test or throwaway verification script.
- **No file paths or code snippets** — the only exceptions the prototype-validated snippet and the **Supporting artifacts** section's durable pointers (synthesis § No stale content).
- **Adaptable to non-dev work.** The dev-only sections are optional; a spec for a process, a piece of content, or a decision uses the core sections alone.
