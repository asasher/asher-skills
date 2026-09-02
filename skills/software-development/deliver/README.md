# Deliver

Takes one unit of work to one review-ready PR in one worktree. The unit is a ready issue (unshaped, shaped, a child of a spec issue, or the spec issue itself once its children are closed), or a spec'd piece of work with no issue, in which case the PR is the record. `backlog build` fans one deliver thread per ready issue; the skill also runs on its own in a prepared worktree. Merging stays a human authorization.

## Dependency surface

Composes with the `implement`, `verify-your-work`, `adversarial-review`, `prove-your-work`, and `to-subagent` siblings (optionally `capture`, `diagnosing-bugs`, `technical-writing`), and reads the `docs/agents/environment.md` playbook.

## Provenance

Formerly `build-change`. No external sources.
