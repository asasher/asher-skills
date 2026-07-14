---
name: research
description: Research decision-relevant questions from primary sources and produce a cited, auditable dossier that separates facts and observations from supported inferences. Use when the user asks to investigate a topic, compare authoritative sources, establish current facts, audit a claim, or when another skill needs source-backed findings before a decision. Not for planning what to do, proving completed implementation behavior, or writing prose judged mainly by taste.
metadata:
  invocation: model
  execution: orchestrator
  requires: [staffing]
  optional: []
  setup: reference/setup.md
---

# Research

Own the epistemic stage: source question → primary-source observations → traceable inferences. The research
dossier is the deliverable; a caller retains its issue, plan, implementation, or review lifecycle.

## Commands

- **`<question>`** (default) — load [research-contract](reference/research-contract.md), then run every gate.
  Read `docs/agents/researching.md` when present for project source, storage, and concurrency bindings.
- **`setup`** — load [setup](reference/setup.md) and reconcile only the project research playbook.

## Gates

1. **Frame.** Write a brief that fixes the research question, intended use, scope and exclusions, definitions,
   time/version boundary, and what would count as a sufficient answer. Infer these from the request and caller;
   ask only for a missing choice that would materially change the investigation.
   **Complete when:** every material claim can be judged in or out of scope and against an as-of boundary.
2. **Decompose.** Build a source map and split only genuinely independent subquestions. For multiple shards,
   use `staffing route` for workers, preserve capacity for synthesis, and assign one coordinator as the only
   dossier writer. A caller that already runs issues in parallel does not forbid nested fan-out; it reduces the
   available worker budget.
   **Complete when:** each shard has a distinct question/source family and the synthesis owner is named.
3. **Observe.** Work from primary sources: official specifications and documentation, source code and commit
   history, first-party APIs and records, or raw datasets. Use secondary sources and search results to discover
   primary material, never as silent substitutes. Record each material finding as a cited claim packet.
   **Complete when:** every in-scope subquestion has primary-source observations or an explicit source gap.
4. **Reconcile.** Normalize duplicate claims; check version, date, jurisdiction, and definitions; surface
   contradictions instead of voting them away. Separate facts/observations from inferences, and link every
   inference to the claim IDs that support it.
   **Complete when:** no material conclusion hides a conflict, unsupported leap, or stale boundary.
5. **Synthesize.** Write the dossier in the project-bound research location. Lead with the answer, then facts
   and observations, inferences, contradictions, unknowns, method, and source index. Keep recommendations
   separate and include them only when requested.
   **Complete when:** a cold reader can trace every material statement to a source or supporting claim IDs.
6. **Audit.** Run the contract's claim audit, using an independent challenger when the work was parallelized or
   the decision is consequential. Repair failures; never downgrade an unsupported assertion into prose that
   merely sounds cautious.
   **Complete when:** every audit item passes or the dossier names the exact unresolved gap and consequence.

## Return

Return the dossier path, the concise answer, material unknowns/contradictions, the as-of boundary, and the
audit result. Standalone, open the canonical artifact. Under a caller, return control without creating a PR,
moving tracker state, making the downstream decision, or copying the dossier into `evidence/`.

## Dependency surface

- **Bundled references** — `reference/research-contract.md` owns source, claim, fan-out, artifact, and audit
  rules; `reference/setup.md` owns playbook reconciliation; `templates/researching.md` is the delta seed.
- **Project playbook** — optional `docs/agents/researching.md`, owned by the repo after setup.
- **Sibling skill** — required `staffing`, invoked by name for coordinator, shard, and challenger routes.
