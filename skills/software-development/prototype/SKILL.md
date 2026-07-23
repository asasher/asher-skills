---
name: prototype
description: Answer one design question with a throwaway artifact — keep the answer, delete the scaffolding. Usable anywhere, not only dev. Use to settle a state model, UI, or document direction with real alternatives — any question paper can't settle. Not for building the real thing.
argument-hint: "<design question>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [to-subagent]
---

# Prototype

Build the smallest throwaway artifact that answers one design question. The answer is durable; the artifact
is not. Load [prototyping](reference/prototyping.md) for the behavior, variants, and falsification shapes, capture, and cleanup.
Use optional `docs/agents/prototyping.md` only for repo-specific placement.

## Entry

Run on an explicit question; if it is vague, narrow it before building. Framing and interpretation stay
here; build-out may be dispatched via the `to-subagent` skill.

## Gates

1. **Question stated.** Record one question and its shape (behavior, form, or falsification per the
   reference): for behavior/falsification, the claim the artifact can falsify; for variants, the alternatives
   presented and the decision they settle.
2. **Built and exposed.** Provide one command or URL and visible state. Open rendered answer sheets
   locally; drive live interactive artifacts directly. Iterate only to settle the named question.
3. **Answer captured.** Write the decision, why, and relevant variant captures into the record of the work
   that raised the question — the ticket thread or the conversation playback.
4. **Cleaned.** Delete the artifact or deliberately absorb only its validated core into real work.

An interface's non-obvious presentation choices — the visual hierarchy, which actions are overt, what
each journey step shows — are decisions, not taste calls: a variants prototype settles them;
implementation never invents them.

Failure to expose a falsifiable observation — or, for variants, real alternatives a human can react to —
returns to gate 1. Missing `to-subagent` builds in-session.

## Dependency surface

- **Bundled:** `reference/prototyping.md`, the technique.
- **Project:** optional placement delta `docs/agents/prototyping.md`.
- **Siblings (optional, by name):** `to-subagent` (build-out dispatch).
