# Adversarial Review

Target: a PR. Runs standalone (`triage adversarial-review <PR>`) or as the final step of the loop.

Spawn two subagents, Reviewer and Fixer, both working only on this PR. Reviewer reads `docs/agents/pr-reviewer.md` for what to scrutinize in this repo; Fixer reads `docs/agents/pr-fixer.md` for how this repo fixes and replies, and `docs/agents/environment.md` to run and test the app. If a required playbook is missing, report a setup gap and stop.

## Shared rules

- Before any work, identify the PR URL, issue number, branch, current head SHA, and the latest reviewer state.
- Set up a durable monitor or wakeup for PR pushes and comments when the tools allow. If none is possible, keep the active run polling while work remains. If neither works, comment `BLOCKED_MONITOR_SETUP` and report the blocker to the parent thread.
- After each iteration, persist state on the PR: agent name, iteration count, last seen SHA, status, next expected actor.
- Stop when Reviewer comments `LGTM`, five review/fix iterations are reached, or monitor setup is blocked.

## Reviewer

- Never edit code.
- Audit the PR against the criteria in `docs/agents/pr-reviewer.md`.
- Leave only actionable comments: each names the expected improvement and why it matters.
- After each Fixer commit, review only the diff since the last seen SHA before commenting again.
- When no actionable improvement remains, comment exactly `LGTM`.
- Completion criterion: the PR has `LGTM`, actionable comments for the current iteration, or a max-iteration summary.

## Fixer

- Watch for Reviewer comments.
- Fix every actionable comment from the current iteration per `docs/agents/pr-fixer.md`, unless a fix would change product behavior beyond the issue scope.
- Run the repo's checks (per `verifying.md`, accessing the app per `environment.md`) after changes, then commit and push.
- Reply to each addressed comment with what changed and the commit SHA. For an intentional non-fix, reply with the reason and the risk.
- Completion criterion: every actionable comment has a fix commit or an explicit non-fix reply, and Reviewer has been prompted to re-review.
