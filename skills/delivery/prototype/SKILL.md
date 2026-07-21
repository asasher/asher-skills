---
name: prototype
description: Answer one design question with a throwaway artifact — keep the answer, delete the scaffolding. Usable anywhere, not only dev. Use to settle a state model, UI, or document direction with real alternatives — directly, or when a workflow skill hits a question paper can't settle. Not for building the real thing.
argument-hint: "<design question>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [review-loop, staffing]
  optional: []
---

# Prototype

Build the smallest throwaway artifact that answers one design question. The answer is durable; the artifact
is not. Load [prototyping](reference/prototyping.md) for the behavior, variants, and falsification shapes, capture, and cleanup.
Use optional `docs/agents/prototyping.md` only for repo-specific placement.

## Entry

Run directly on an explicit question or accept a handoff from any workflow. If the question is vague, narrow
it before building. The invoking thread keeps framing and interpretation; dispatch build-out through
`staffing route <prototype-builder task>`.

## Gates

1. **Question stated.** Record one question and its shape (behavior, form, or falsification per the
   reference): for behavior/falsification, the claim the artifact can falsify; for variants, the alternatives
   presented and the decision they settle.
2. **Built and exposed.** Provide one command or URL and visible state. Serve rendered answer sheets through
   `review-loop`; drive live interactive artifacts directly. Iterate only to settle the named question.
3. **Answer captured.** Write the decision, why, and relevant variant captures into the caller's durable
   record.
4. **Cleaned.** Delete the artifact or deliberately absorb only its validated core into real work.

An interface's non-obvious presentation choices — the visual hierarchy, which actions are overt, what
each journey step shows — are decisions, not taste calls: a variants prototype settles them;
implementation never invents them.

Failure to expose a falsifiable observation — or, for variants, real alternatives a human can react to —
returns to gate 1. Missing `review-loop` degrades to local open;
missing `staffing` is reported.

## Dependency surface

- **Bundled:** `reference/prototyping.md`, the caller-neutral technique.
- **Project:** optional placement delta `docs/agents/prototyping.md`.
- **Siblings:** required `review-loop` and `staffing`, invoked by name.
