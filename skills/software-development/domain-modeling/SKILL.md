---
name: domain-modeling
description: Sharpen the project's domain model as decisions land. Use when pinning down domain terminology, recording an architectural decision, or maintaining the model during a live design conversation. Not for merely reading CONTEXT.md.
argument-hint: "[term, decision, or nothing — runs alongside a conversation]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [writing-for-humans]
---

# Domain Modeling

Build and sharpen the project's domain model alongside a design conversation — the discipline for when the model is changing.

User-facing text follows the `writing-for-humans` sibling; absent it, write plainly and say the standard was not loaded.

## Where the model lives

Most repos have a single context: `CONTEXT.md` at the root and ADRs under `docs/adr/`. A `CONTEXT-MAP.md` at the root means multiple contexts, each with its own `CONTEXT.md` and `docs/adr/`; infer which context the current topic belongs to, and ask when unclear. Formats: [context-format](reference/context-format.md), [adr-format](reference/adr-format.md).

Create files lazily: `CONTEXT.md` when the first term resolves, `docs/adr/` when the first ADR is needed.

**Register on create.** The first time `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` comes into existence, add its line to the project instruction file's `## Context documents` index — the instruction file the repo's harnesses actually load (`AGENTS.md` where the harness reads it or another file imports it; otherwise `CLAUDE.md` itself); create the section if absent: path, what it is, when to read it, one line each. The index is how a session running no skill still finds the model.

## Two destinations — is vs will-be

Main's context files describe the code that **is**. Route every write by that test:

- **During shaping** — a term or numbered ADR draft describes code that _will be_: it goes into the spec's **context delta** (in the format the references define), carried on the spec's artifact branch, and lands on main by the build that makes it true.
- **Direct writes to `CONTEXT.md`/`docs/adr/`** remain only for facts already true of the code — a term the code already embodies, a decision a build just made real, renaming or sharpening what exists.

## During the conversation

- **Challenge against the glossary.** A term that conflicts with `CONTEXT.md` gets called out immediately: "the glossary defines _cancellation_ as X, but you seem to mean Y — which is it?"
- **Sharpen fuzzy language.** Vague or overloaded terms get a proposed canonical: "you say _account_ — the Customer or the User? They're different things."
- **Stress-test with concrete scenarios.** Invent edge cases that force precision about the boundaries between concepts.
- **Cross-reference the code.** When the user states how something works, check whether the code agrees, and surface contradictions: "the code cancels whole Orders, but you just said partial cancellation exists — which is right?"
- **Write inline.** Terms and drafts land in `CONTEXT.md` or the context delta the moment they crystallise.

## ADRs — offer sparingly

Offer an ADR only when **all three** hold:

1. **Hard to reverse** — changing the decision later costs something real.
2. **Surprising without context** — a future reader would wonder "why on earth did they do it this way?"
3. **A real trade-off** — genuine alternatives existed and one was picked for specific reasons.

Any gate failing → no ADR.
