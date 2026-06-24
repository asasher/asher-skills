# Playbook: PR Reviewer Criteria

> Project playbook for this repo. The triage `adversarial-review` Reviewer subagent reads this file. Tune the criteria to what matters in this codebase.

## Scrutinize

- Structure, abstractions, modularity, and legibility.
- Duplication and naming.
- Testability and test coverage of the change.
- Behavior risk beyond the issue's scope.
- Repo-specific concerns (performance budgets, security surfaces, accessibility, API compatibility): _<add yours>_.

## How to comment

- Leave only actionable comments. Each names the expected improvement and why it matters.
- Review only the diff since the last seen SHA on re-review.
- Comment exactly `LGTM` when no actionable improvement remains.
