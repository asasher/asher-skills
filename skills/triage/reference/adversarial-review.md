# Adversarial Review

Target: a PR. Runs standalone (`triage adversarial-review <PR>`) or as the final step of the loop.

Staffing: both subagents fill the **delegate** role — one capability tier below this thread, never below the floor. Read the Model staffing section of `docs/agents/environment.md` for who fills the role in the running harness. The Fixer may go to an external CLI delegate when the playbook allows it and the PR touches only backend code; the Reviewer must satisfy the full criteria in `pr-reviewer.md`, frontend included, so it takes only delegates the playbook clears for review. If the staffing section is missing, the harness offers no model override, or no tier fits between this thread's model and the floor, spawn both on the current model rather than skipping review.

Spawn two subagents, Reviewer and Fixer, both working only on this PR. The Reviewer's criteria, comment conduct, and approval bar live in `docs/agents/pr-reviewer.md`; the Fixer's fix-and-reply conduct in `docs/agents/pr-fixer.md`, with `docs/agents/environment.md` to run and test the app. If a required playbook is missing, report a setup gap and stop.

## Shared rules

- Before any work, identify the PR URL, issue number, branch, current head SHA, and the latest reviewer state.
- Set up a durable monitor or wakeup for PR pushes and comments when the tools allow. If none is possible, keep the active run polling while work remains. If neither works, comment `BLOCKED_MONITOR_SETUP` and report the blocker to the parent thread.
- After each iteration, persist state on the PR: agent name, iteration count, last seen SHA, status, next expected actor.
- Stop when Reviewer comments `LGTM`, five review/fix iterations are reached, or monitor setup is blocked.

## Roles

- **Reviewer** — never edits code. Audits the PR per its playbook and leaves comments; signals approval with an exact `LGTM` comment. Iteration complete when the PR has `LGTM`, actionable comments for the current iteration, or a max-iteration summary.
- **Fixer** — watches for Reviewer comments and addresses the current iteration's per its playbook, pushes, and replies. Iteration complete when every actionable comment has a fix commit or an explicit non-fix reply, and the Reviewer has been prompted to re-review.
