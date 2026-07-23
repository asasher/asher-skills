---
name: research
description: Research decision-relevant questions from primary sources and produce a cited, auditable dossier. Use when the user asks to investigate a topic, establish current facts, or audit a claim. Not for planning what to do, proving completed implementation behavior, or writing prose judged mainly by taste.
argument-hint: "<the question to research>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [to-subagent]
  setup: reference/setup.md
---

# Research

Own the epistemic stage: source question → primary-source observations → traceable inferences. The research
dossier is the deliverable.

## Commands

- **`<question>`** (default) — load [research-contract](reference/research-contract.md), then run every gate.
  Read `docs/agents/researching.md` when present for project source, storage, and concurrency bindings.
- **`setup`** — load [setup](reference/setup.md) and reconcile only the project research playbook.

## Gates

1. **Frame.** Write a brief that fixes the research question, intended use, scope and exclusions, definitions,
   time/version boundary, and what would count as a sufficient answer. Infer these from the request;
   ask only for a missing choice that would materially change the investigation.
   **Complete when:** every material claim can be judged in or out of scope and against an as-of boundary.
2. **Decompose.** Build a source map and split only genuinely independent subquestions. For multiple shards,
   dispatch workers via the `to-subagent` skill per the contract's parallel rules.
   **Complete when:** each shard has a distinct question/source family and the synthesis owner is named.
3. **Observe.** Work from primary sources per the contract's source hierarchy. Record each material finding
   as a cited claim packet.
   **Complete when:** every in-scope subquestion has primary-source observations or an explicit source gap.
4. **Reconcile.** Normalize duplicate claims; check version, date, jurisdiction, and definitions; surface
   contradictions. Separate facts/observations from inferences, and link every inference to the claim IDs
   that support it.
   **Complete when:** no material conclusion hides a conflict, unsupported leap, or stale boundary.
5. **Synthesize.** Write the dossier in the project-bound research location. Follow the contract's dossier
   order.
   **Complete when:** a cold reader can trace every material statement to a source or supporting claim IDs.
6. **Audit.** Run the contract's claim audit. Repair failures; never downgrade an unsupported assertion into
   prose that merely sounds cautious.
   **Complete when:** every audit item passes or the dossier names the exact unresolved gap and consequence.

## Return

Return the dossier path, the concise answer, material unknowns/contradictions, the as-of boundary, and the
audit result. Open the canonical artifact for the user. Creating a change request, moving tracker state, and
making the downstream decision are out of scope.

## Dependency surface

- **Bundled references** — `reference/research-contract.md` owns source, claim, fan-out, artifact, and audit
  rules; `reference/setup.md` owns playbook reconciliation; `templates/researching.md` is the delta seed.
- **Project playbook** — optional `docs/agents/researching.md`, owned by the repo after setup.
- **Sibling (optional, by name)** — `to-subagent`, for shard and challenger dispatch; absent it,
  shards run sequentially in-session.
