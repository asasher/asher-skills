---
name: domain-modeling
description: Build and sharpen the project's domain model as decisions land — challenge terms against the glossary, stress-test with concrete scenarios, and write CONTEXT.md entries and ADRs the moment they crystallise. Use when pinning down domain terminology, recording an architectural decision, or when another skill (interview-with-docs, groom, a spec session) needs the model maintained while it works. Not for merely reading CONTEXT.md — that is a one-line habit any skill can do.
argument-hint: "[term, decision, or nothing — runs alongside a conversation]"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: []
---

# Domain Modeling

Actively build and sharpen the project's domain model while designing. This is the *active* discipline —
challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment
they crystallise. Consuming `CONTEXT.md` for vocabulary is not this skill; this skill is for when the model
is *changing*.

It runs alongside a conversation rather than owning one: `interview-with-docs` composes it with `interview`;
a groom session, spec session, or triage thread may invoke it directly when terms or decisions are moving.

## Where the model lives

Most repos have a single context: `CONTEXT.md` at the root and ADRs under `docs/adr/`
(`0001-slug.md`, `0002-slug.md`, …). A `CONTEXT-MAP.md` at the root means multiple contexts, each with its
own `CONTEXT.md` and `docs/adr/`; infer which context the current topic belongs to, and ask when unclear.
Formats: [context-format](reference/context-format.md), [adr-format](reference/adr-format.md).

Create files lazily — only when there is something to write. No `CONTEXT.md`? Create it when the first term
resolves. No `docs/adr/`? Create it when the first ADR is needed.

## During the session

- **Challenge against the glossary.** A term that conflicts with `CONTEXT.md` gets called out immediately:
  "the glossary defines *cancellation* as X, but you seem to mean Y — which is it?"
- **Sharpen fuzzy language.** Vague or overloaded terms get a proposed canonical: "you say *account* — the
  Customer or the User? They're different things."
- **Stress-test with concrete scenarios.** Invent edge cases that force precision about the boundaries
  between concepts.
- **Cross-reference the code.** When the user states how something works, check whether the code agrees, and
  surface contradictions: "the code cancels whole Orders, but you just said partial cancellation exists —
  which is right?"
- **Write inline, never batch.** A resolved term goes into `CONTEXT.md` right then. `CONTEXT.md` is a
  glossary and nothing else — no implementation details, no spec content, no scratch notes.

## ADRs — offer sparingly

Offer an ADR only when **all three** hold:

1. **Hard to reverse** — changing the decision later costs something real.
2. **Surprising without context** — a future reader would wonder "why on earth did they do it this way?"
3. **A real trade-off** — genuine alternatives existed and one was picked for specific reasons.

Any gate failing → no ADR. An ADR can be a single paragraph; the value is recording *that* and *why*, not
filling out sections.

## Dependency surface

- **Bundled:** [context-format](reference/context-format.md), [adr-format](reference/adr-format.md).
- **Siblings:** none required. Callers compose this skill by name; absent it, they state the gap rather than
  writing glossary entries ad hoc.
