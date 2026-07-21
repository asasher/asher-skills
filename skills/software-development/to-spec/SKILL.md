---
name: to-spec
description: Turn the current conversation into a spec — the direction document a design discussion earned but never wrote down. Pure synthesis, no interview; writes a self-contained HTML deliverable at docs/specs/<name>.html.
argument-hint: "[<name for the spec>]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: []
  optional: [serve-via-tailnet]
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

- **`to-spec [<name>]`** — synthesize the current conversation into a spec and write it to
  `docs/specs/<name>.html`. With no name, derive a short kebab-case one from the decided direction.

Load [synthesis](reference/synthesis.md) for the method (what to mine, the no-interview rule, dev-vs-non-dev
gating, the no-stale-content rule, sign-off) and [template-guide](reference/template-guide.md) for what goes
in each section. The fillable scaffold is [templates/spec-skeleton.html](templates/spec-skeleton.html).

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
4. **Write the spec** from the skeleton into `docs/specs/<name>.html`, in generic vocabulary — a
   self-contained HTML deliverable with stable element ids, same house style as a plan.
5. **Audit fidelity, then classify the Notes.** Before sign-off: every material decision from the
   conversation appears in the spec, and every Notes line is classified **blocking** (must be settled
   upstream before tickets), **delegated** (the executor may choose; boundary named), or **deferred**
   (parked, with a home). A spec with an unclassified material Note is not done; an open
   blocking Note means the direction isn't ready to build on — say so in the report.
6. **Sign-off — the direction's approval gate.** User present: approve inline. AFK: serve annotated via
   the optional `serve-via-tailnet` sibling. On approval: commit and project the thin tracking ticket
   (synthesis § Sign-off).

## What a spec is (and isn't)

- **Generic vocabulary.** A spec describes direction that later splits into **tickets**. Say "spec" and
  "ticket" — never GitHub-specific "issue." The unit of downstream work is a ticket.
- **The artifact is a repo doc** at `docs/specs/<name>.html` — a self-contained HTML deliverable (stable
  element ids, no external fetches), servable for review as-is.
- **No file paths or code snippets** — sole exception the prototype-validated snippet (synthesis § No stale
  content).
- **Adaptable to non-dev work.** The dev-only sections are optional; a spec for a process, a piece of content,
  or a decision uses the core sections alone.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [synthesis](reference/synthesis.md)
  and [template-guide](reference/template-guide.md), plus the fillable scaffold
  [templates/spec-skeleton.html](templates/spec-skeleton.html). These are the authority; they import no
  other skill's files.
- **Project playbooks** — the repo's **spec conventions**: where specs live and the spec→ticket vocabulary.
  Defaults to `docs/specs/`; a repo may record a different location or naming rule in its `docs/agents/`.
- **Sibling skills** — **optional `serve-via-tailnet` only**, for AFK sign-off from another device.
  Not a hard dependency: skipping it still produces a valid, committed spec.
