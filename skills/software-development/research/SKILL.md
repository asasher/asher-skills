---
name: research
description: Research one decision-relevant question from primary sources and produce a cited, auditable HTML dossier. Use to establish source-backed facts or fact-check a claim, not to decide what to do.
metadata:
  optional: [diagram-design, writing-for-humans]
---

# Research

1. **Work from primary sources.** Prefer the source that owns each claim: official documentation, source code, specifications, first-party APIs, the observed system, or the original record. Treat search snippets, aggregators, and uncited paraphrases as discovery aids.

2. **Write one HTML dossier.** Make it self-contained. State the question, concise answer, findings, unknowns, contradictions, and as-of boundary. Cite every claim. When structure, sequence, flow, or relationships are material to the answer and a visual teaches more than prose or a table, use the `diagram-design` sibling in embedded mode for the smallest useful figure. Every claim in the figure must trace to the dossier's cited findings. When that sibling is absent, use prose or a table and report the missing diagram support if it materially reduced clarity.

3. **Audit every claim.** Run [the claim audit checklist](reference/research-contract.md) before returning.

Return the dossier path, concise answer, material unknowns and contradictions, as-of boundary, and audit result. Leave the downstream decision open.

Use `writing-for-humans` for the dossier and returned prose.
