---
name: to-spec
description: Synthesize a settled conversation or shaping record into one self-contained HTML spec. Use after the decisions are made. Pure synthesis, no interview or publication.
argument-hint: "[<settled record or subject>]"
metadata:
  optional: [writing-for-humans]
---

# To spec

Take a conversation that already reached a decision and write the spec it earned. Undecided points become Notes lines, never questions.

Use `writing-for-humans` for the spec. Load [synthesis](reference/synthesis.md) for the method and [template guide](reference/template-guide.md) for the content contract.

1. **Mine the record.** Start from the shaping record when one exists, then use the current conversation to fill in around it. Sweep every decision-informing artifact into Supporting artifacts. Finish when every source category in synthesis is represented or recorded as a Notes line.
2. **Classify the work.** A dev spec includes the dev-only sections; a non-dev spec skips them.
3. **For a dev spec, settle the test contract.** Name the highest existing public test seams, declare the durable-test or throwaway-script split for each acceptance criterion, and expose contract choices that would otherwise become implementation defaults.
4. **Write one HTML spec.** Open with a diagram, then follow the template order. Put experience before implementation when both apply. State implementation as recommendations and leave only genuine forks open. A direction too large for one build ends with a recommended split, not created tickets.
5. **Audit fidelity.** Classify every Notes line as blocking, delegated, or deferred. Check that every material source decision appears in the spec and every spec statement traces back to the source material.

Write the spec as an untracked scratch file. Return its path, concise summary, classified Notes, and fidelity-audit result.
