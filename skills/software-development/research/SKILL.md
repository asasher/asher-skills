---
name: research
description: Research decision-relevant questions from primary sources and produce a cited, auditable dossier. Use when the user asks to investigate a topic, establish current facts, or fact-check a claim. Not for deciding what to do, proving a change works, or taste-judged prose.
argument-hint: "<the question to research>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [writing-for-humans, to-subagent, to-web]
---

# Research

Three rules.

1. **Work from primary sources.** Prefer the source that owns each claim — official documentation, source code, specifications, first-party APIs, the observed system or original record. A search snippet, aggregator, or uncited paraphrase is a discovery aid, never support.

2. **One HTML dossier.** The deliverable is a single self-contained HTML file: the question, the concise answer, then the findings — **every claim cited**, unknowns and contradictions visible, with an **as-of boundary** stated up front. The dossier lands on an artifact branch — `artifact/<ticket>-<slug>`, or `artifact/<slug>` when no ticket raised the question — and its `to-web` render link goes to the record that raised it: the ticket, or the raising conversation. Absent `to-web`, post the artifact-branch path instead of a render link.

3. **The claim audit.** Before returning, run [the claim audit checklist](reference/research-contract.md).

Independent subquestions may run in parallel via the `to-subagent` skill; absent it, work them sequentially in-session.

User-facing text follows the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.
