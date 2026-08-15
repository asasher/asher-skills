---
name: research
description: Research decision-relevant questions from primary sources and produce a cited, auditable dossier. Use when the user asks to investigate a topic, establish current facts, or audit a claim. Not for planning what to do, proving completed implementation behavior, or writing prose judged mainly by taste.
argument-hint: "<the question to research>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [plain-language, to-subagent, to-web]
---

# Research

Three rules.

1. **Work from primary sources.** Prefer the source that owns each claim — official documentation, source code, specifications, first-party APIs, the observed system or original record — and trace every claim to it. A search snippet, aggregator, or uncited paraphrase is a discovery aid, never support.

2. **One HTML dossier.** The deliverable is a single self-contained HTML file: the question, the concise answer, then the findings — **every claim cited** to the source that owns it, unknowns and contradictions visible, with an **as-of boundary** stated up front (facts are dated; say when they were true). The dossier lands on an artifact branch — `artifact/<ticket>-<slug>`, or `artifact/<slug>` when no ticket raised the question — and its `to-web` render link goes to the record that raised it: the ticket, or the raising conversation.

3. **The claim audit.** Before returning, run the checklist in [research-contract](reference/research-contract.md). Never downgrade an unsupported assertion into prose that merely sounds cautious — repair it or name the exact gap and its consequence.

Independent subquestions may run in parallel via the `to-subagent` skill; absent it, read sequentially in-session.

User-facing text follows the `plain-language` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers.
