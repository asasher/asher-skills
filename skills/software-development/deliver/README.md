# Deliver

Builds one ready GitHub ticket in its worktree, resuming a local or pushed branch when needed. The owner implements, verifies routine work, fixes findings, and packages evidence inline. Independent code review always runs; high-risk work also gets an independent verifier. An ordinary PR opens after implementation checks and becomes review-ready only with current proof and required CI.

The ticket and PR preserve progress, revisions, remaining review bounds, and the next action across machines. Merging requires the human's named selection. Dependencies live in SKILL.md.

## Provenance

Formerly `build-change`.

The September 2026 revision uses the local orchestration audit's recommendations on overlapping checks, early PRs, risk-scaled verification, and persisted progress. Those recommendations draw on [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack), as reviewed in the September 3 audit, and Anthropic's [long-running agent harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). The workflow is rewritten here; it has no runtime dependency on either source.
