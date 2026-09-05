# Deliver

Takes one unit of work to one review-ready PR in one worktree. The unit is a ready issue (unshaped, shaped, a child of a spec issue, or the spec issue itself once its children are closed), or a spec'd piece of work with no issue, in which case the PR is the record. `backlog build` fans one deliver thread per ready issue; the skill also runs on its own in a prepared worktree. Merging stays a human authorization. Delivery opens the PR after implementation, runs one combined verification/review loop, and records revision-specific checkpoints for resumption.

## Dependency surface

Composes with the `implement`, `verify-your-work`, `adversarial-review`, `prove-your-work`, and `to-subagent` siblings (optionally `capture`, `technical-writing`), and reads the `docs/agents/environment.md` playbook.

## Provenance

Formerly `build-change`.

The September 2026 revision uses the local orchestration audit's recommendations on overlapping checks, early PRs, risk-scaled verification, and persisted progress. Those recommendations draw on [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack), as reviewed in the September 3 audit, and Anthropic's [long-running agent harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). The workflow is rewritten here; it has no runtime dependency on either source.
