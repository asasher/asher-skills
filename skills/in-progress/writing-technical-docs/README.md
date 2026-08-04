# Writing Technical Docs

> **Status: in progress.** Tier 1 situated probes pass 6/6 on both executors (Codex gpt-5.6-sol child and Claude fable-5 CLI, 2026-08-04). The checker passes 13 deterministic tests. A human field test remains. Install knowingly.

Writes and rewrites technical documentation as a reader contract: verified facts, stable terminology, explicit conditions, direct actions, and observable results. The default branch uses controlled technical prose without pretending to enforce the full ASD-STE100 dictionary. A strict source-backed branch prevents unsupported compliance claims and requires the official standard, the applicable terminology source, and qualified human review.

The skill covers READMEs, API references, getting-started guides, procedures, runbooks, safety instructions, error messages, deprecation notices, pull-request descriptions, and release notes. Its bundled checker reports the mechanical subset with line-level findings while leaving meaning and judgment to the writer.

## Shape

- `SKILL.md` — the reader-contract workflow, core controlled-prose rules, truth pass, and completion criteria.
- `reference/artifact-patterns.md` — branch-specific information structures for common technical artifacts.
- `reference/asd-ste100.md` — the boundary between controlled prose, STE-inspired text, and a legitimate compliance claim.
- `scripts/check_prose.py` — a standard-library heuristic checker for sentence length, semicolons, passive voice, contractions, hedges, nominalizations, phrasal verbs, promotional terms, and dash review.
- `evals/` — situated probes, a prewritten answer key, and deterministic checker tests.

## Sources and credits

- **Relationship:** original technical-documentation workflow informed by ASD-STE100 and the linked anti-slop experiment.
- **Official source:** [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/), Issue 9 (January 15, 2025), including the [official standard](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf), [FAQ](https://www.asd-ste100.org/STE_faq.html), and [tool guidance](https://www.asd-ste100.org/STEsoftware.html).
- **Experiment source:** Ege Çelebi's [“The cure for AI slop is a 1986 aircraft manual” kit](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop). The skill uses its two-mode writing idea, anti-slop categories, experimental caveats, and machine-checkable subset.
- **Local changes:** adds source-first factual verification, a reader contract, artifact-specific structures, exact-literal protection, explicit compliance language, line-level diagnostics, and safety boundaries. It does not ship the copyrighted ASD-STE100 standard or transcript.

## Install

`npx github:asasher/asher-skills install --skill writing-technical-docs`
