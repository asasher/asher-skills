# To Branch

Commits files to a branch without checking it out and prints the commit hash; the bundled `scripts/to-branch.py` does the work through a temporary index and never force-moves a ref. `shape` uses it to publish every dossier, prototype, and spec revision to the issue's `artifact/<issue>` branch while its worktree stays on the work branch.

## Provenance

No external sources.
