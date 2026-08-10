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

- Executor routes: resolve from the staffing playbook and the machine-local overlay it declares (`docs/agents/staffing.md`) — never restate routes or aliases here. Worker cap: the harness's own thread cap; serialize writes to shared research artifacts.
- Present durable findings as repo-local Markdown or HTML per `environment.md` § Presenting to the human — on the change request or opened locally; `serve-via-tailnet` on demand when the human needs the artifact on another device, never as the default route.
