# Worktree

Primitive for project-owned Git worktree mechanics. It prepares a branch and working copy without switching the primary checkout, inspects Git registration and dirty state, and removes only a clean, registered secondary worktree after project environment teardown. Workflows decide when isolation and cleanup occur; this skill makes those operations deterministic and auditable.

## Dependency surface

- **Bundled:** `scripts/worktree.py`; script and situated evals under `evals/`.
- **Project playbooks:** platform bindings for base/branch/root and environment bindings for bootstrap and teardown.
- **Siblings:** none.

## Provenance

No external sources.
