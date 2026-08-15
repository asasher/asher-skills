# Agent-ready codebase

Reference skill holding the repo-readiness standard for parallel agent builds: the four-item checklist (worktrees, stack per worktree, auth per worktree, maintained seed), the certify-and-punch-list method, and the use-vs-change rule for genuinely shared resources. It defines, it never runs as a workflow — `backlog setup` certifies against it and writes the repo's answers into `docs/agents/environment.md`; punch-list gaps become groomable tickets.

## Dependency surface

- **Bundled:** none — `SKILL.md` is the whole standard.
- **Project playbooks:** `docs/agents/environment.md` holds the repo's certification results.
- **Siblings:** `worktree` (exercised by checklist item 1), `backlog` (runs the certification).

## Provenance

No external sources.
