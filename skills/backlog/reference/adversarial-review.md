# Adversarial Review

Target: a PR. Runs standalone (`backlog adversarial-review <PR>`) or as the final step of the loop.

Staffing: the Reviewer fills the **checker** role and the Fixer the **builder** role for the PR's surface — both roles, the Reviewer constraint, and the fallback ladder are resolved by the `staffing` skill (by name).

Spawn two subagents, Reviewer and Fixer, both working only on this PR. The Reviewer's criteria, comment conduct, and approval bar live in `docs/agents/pr-reviewer.md`; the Fixer's fix-and-reply conduct in `docs/agents/pr-fixer.md`, with `docs/agents/environment.md` to run and test the app. Comments, replies, and approval travel through the change-review binding's verbs in `docs/agents/platform.md` — a PR thread on GitHub, appended sections of the committed review file on the local binding. If a required playbook is missing, report a setup gap and stop.

## Shared rules

- Before any work, identify the PR reference, issue id, branch, current head SHA, and the latest reviewer state.
- Set up a durable monitor or wakeup for pushes and comments when the harness binding in `platform.md` names one. If none is possible, keep the active run polling while work remains. If neither works, comment `BLOCKED_MONITOR_SETUP` and report the blocker to the parent thread.
- After each iteration, persist state on the PR via the comment verb: agent name, iteration count, last seen SHA, status, next expected actor.
- Stop when Reviewer comments `LGTM`, five review/fix iterations are reached, or monitor setup is blocked.

## Roles

- **Reviewer** — never edits code. Audits the PR per its playbook and leaves comments; signals approval with an exact `LGTM` comment. Iteration complete when the PR has `LGTM`, actionable comments for the current iteration, or a max-iteration summary.
- **Fixer** — watches for Reviewer comments and addresses the current iteration's per its playbook, pushes, and replies. Iteration complete when every actionable comment has a fix commit or an explicit non-fix reply, and the Reviewer has been prompted to re-review.
