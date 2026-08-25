---
name: research
description: Research one decision-relevant question from primary sources and produce a cited, auditable HTML dossier. Use to establish current facts or fact-check a claim, not to decide what to do.
argument-hint: "<the question to research>"
metadata:
  optional: [writing-for-humans]
---

# Research

1. **Work from primary sources.** Prefer the source that owns each claim: official documentation, source code, specifications, first-party APIs, the observed system, or the original record. Treat search snippets, aggregators, and uncited paraphrases as discovery aids.

2. **Write one HTML dossier.** Make it self-contained. State the question, concise answer, findings, unknowns, contradictions, and as-of boundary. Cite every claim.

3. **Audit every claim.** Run [the claim audit checklist](reference/research-contract.md) before returning.

Return the dossier path, concise answer, material unknowns and contradictions, as-of boundary, and audit result. Leave the downstream decision open.

Use `writing-for-humans` for the dossier and returned prose.
