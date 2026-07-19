---
name: interview-with-docs
description: A relentless interview that also writes the useful shape down as it goes — glossary terms into CONTEXT.md, decisions into ADRs. Use when the elicited decisions should outlive the session and feed to-spec, tickets, or future sessions; use bare `interview` when nothing durable is wanted.
argument-hint: "<idea, problem, or reference to intake material>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [domain-modeling, interview]
  optional: []
---

# Interview With Docs

Run the `interview` skill, with the `domain-modeling` skill active throughout.

The interview asks; `domain-modeling` extracts as it crystallises. Everything else deliberately evaporates
with the conversation: the extraction *is* the record, not a transcript.

At exit, the interview's open-thread classification is written where the caller directs — an issue comment,
a spec's Notes.

Absent either sibling, state the requirement and offer the degraded form — bare `interview` with the
classification recorded in the conversation only — rather than failing silently.
