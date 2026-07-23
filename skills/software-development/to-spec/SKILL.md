---
name: to-spec
description: Turn a settled conversation or shaping record into a spec on the subject's ticket — body canonical, opening with a diagram; creates the ticket when none exists. Pure synthesis, no interview. Falls back to a repo doc when no tracker is bound.
argument-hint: "[<ticket id, or a name for the spec>]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# To-Spec

To-spec owns one move: **take a conversation that already reached a decision and write the spec it earned.**
It reads the current conversation and the codebase/project understanding built up in it, captures what was
**decided**, and writes a **spec**: the high-level direction document downstream work builds on.

The defining constraint is **pure synthesis, no interview.** To-spec does not re-elicit requirements, does not
re-ask what the conversation already settled, and does not stall waiting on the user. It captures what's
decided and **flags what isn't in the spec's Notes** — an open question recorded is worth more here than a
question asked.

## Command surface

- **`to-spec [<ticket id, or name>]`** — synthesize the current conversation into a spec and land it on
  the subject's ticket: given a ticket id, that ticket's body; given none, create the ticket to carry it
  (deriving a short kebab-case name from the decided direction). With no tracker bound, fall back to a
  repo doc at `docs/specs/<name>.md`.

Load [synthesis](reference/synthesis.md) for the method (what to mine, the no-interview rule, dev-vs-non-dev
gating, the no-stale-content rule, sign-off) and [template-guide](reference/template-guide.md) for what goes
in each section.

## How a spec gets written

The full method is in [synthesis](reference/synthesis.md); the shape:

1. **Mine, don't ask.** Read the conversation and the codebase/project understanding it built. Start from
   the interview record when one exists (synthesis § What to mine). Extract the problem, the decided
   solution, the decisions taken and the constraints that forced them. Anything left undecided becomes a
   line in **Notes**, never a question back to the user.
2. **Classify the work — dev or non-dev.** Our work isn't all software. A **dev spec** keeps the dev-only
   sections (Testing decisions, Test seams) and runs the seams step below; a **non-dev spec** skips both and
   uses only the core sections.
3. **For dev specs only — sketch the test seams.** Name the public seams the work would be tested at and
   **prefer the highest existing seam**.
4. **Write the spec onto the ticket** — the ticket body is canonical, **opening with a diagram** of the
   moving parts (flow, sequence, or state — whichever fits) before any prose, then the template's
   sections in generic vocabulary. Rewrite the body in place and post a short comment noting what
   changed; the comments are the revision trail. No ticket yet: create it. No tracker bound: fall back
   to `docs/specs/<name>.md` (synthesis § Where the spec lives).
5. **Audit fidelity, then classify the Notes.** Before sign-off: every material decision from the
   conversation appears in the spec, and every Notes line is classified **blocking** (must be settled
   upstream before tickets), **delegated** (the executor may choose; boundary named), or **deferred**
   (parked, with a home). A spec with an unclassified material Note is not done; an open
   blocking Note means the direction isn't ready to build on — say so in the report. A direction too
   big for one build ends the spec with a **recommended split** — a proposal only; splitting is the
   user's call.
6. **Sign-off — the direction's approval gate.** User present: approve inline. AFK: the spec sits on the
   ticket where comments reach it — the user's LGTM is the approval (synthesis § Sign-off). Readiness
   labels are not to-spec's to apply.

## What a spec is (and isn't)

- **Generic vocabulary.** A spec describes direction that may later split into **tickets**. Say "spec"
  and "ticket" — never GitHub-specific "issue." The unit of downstream work is a ticket.
- **The artifact lives on the ticket** — body canonical, diagram first, comments as the revision trail.
  The repo doc at `docs/specs/<name>.md` — the same diagram-first body — is the fallback
  home when no tracker is bound.
- **No file paths or code snippets** — sole exception the prototype-validated snippet (synthesis § No stale
  content).
- **Adaptable to non-dev work.** The dev-only sections are optional; a spec for a process, a piece of content,
  or a decision uses the core sections alone.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [synthesis](reference/synthesis.md)
  and [template-guide](reference/template-guide.md). These are the authority; they import no
  other skill's files.
- **Project playbooks** — the **tracker binding** in `docs/agents/platform.md` (how a ticket body is
  read, rewritten, and commented), and the repo's spec conventions for the no-tracker fallback
  (defaults to `docs/specs/`; a repo may record a different location or naming rule in its
  `docs/agents/`).
