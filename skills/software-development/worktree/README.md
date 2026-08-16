# Worktree

Primitive for project-owned Git worktree mechanics. It prepares a branch and working copy without switching the primary checkout, inspects Git registration and dirty state, and removes only a clean, registered secondary worktree after project environment teardown. Workflows decide when isolation and cleanup occur; this skill makes those operations deterministic and auditable.

## Dependency surface

No sibling skills; reads the platform and environment bindings under `docs/agents/`, with the deterministic mechanics bundled in `scripts/worktree.py`.

## Provenance

No external sources.
