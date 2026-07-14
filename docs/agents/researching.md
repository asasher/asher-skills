# Playbook: Research

> Project delta only. The installed `research` skill owns the method.

## Artifact routing

- Durable root: `research/<slug>/`; skill-specific investigations may live in the relevant `<skill>-workspace/`.
- Scratch shards use the system temporary directory and are not committed.
- Research stays out of `evidence/` unless it proves a separate change criterion.

## Source bindings

- Primary local sources: skill sources, git history, eval artifacts, and project playbooks.
- Primary external sources: official documentation, APIs, and authenticated connectors or browser sessions.
- Cite stable file/line, commit, URL, page, or record locators. Never publish credentials or private source material.

## Parallelism and presentation

- Use the active staffing route and harness thread cap; serialize writes to shared research artifacts.
- Present durable findings as repo-local Markdown or HTML and use the global Presentation policy.
