---
name: interview-with-docs
description: A relentless interview that also writes the useful shape down as it goes — glossary terms into CONTEXT.md, decisions into ADRs — so nothing settled evaporates with the conversation. Use when the elicited decisions should outlive the session and feed to-spec, tickets, or future sessions; use bare `interview` when nothing durable is wanted.
argument-hint: "<idea, problem, or reference to intake material>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [interview, domain-modeling]
  optional: []
---

# Interview With Docs

Run the `interview` skill, with the `domain-modeling` skill active throughout.

The interview asks; domain-modeling extracts **inline, the moment things crystallise** — terms into
`CONTEXT.md`, decisions passing the three-gate test into ADRs, never batched to the end. Everything else
deliberately evaporates with the conversation: the extraction *is* the record, not a transcript.

At exit, the interview's open-thread classification (settled / delegated / deferred / blocking) is written
where the caller directs — an issue comment, a spec's Notes — so downstream synthesis (`to-spec`,
`to-tickets`) reads crystallised artifacts plus classified threads, not memory.

Both siblings are composed **by name**. Absent either, state the requirement and offer the degraded form —
bare `interview` with the classification recorded in the conversation only — rather than failing silently.
