# Adversarial Review Instructions

Create two subagents: Reviewer and Fixer. Both work only on the current PR.

## Shared Rules

- Before review or fix work, identify the PR URL, issue number, branch, current head SHA, and latest reviewer state.
- Set up and verify a durable monitor or wakeup for relevant PR pushes and comments when the available tools support it.
- If no durable monitor exists, keep the active run in a polling loop while work remains.
- If neither monitoring nor polling is possible, comment `BLOCKED_MONITOR_SETUP` on the PR and report the blocker to the parent thread.
- Persist state on the PR after each iteration: agent name, iteration count, last seen SHA, status, and next expected actor.
- Stop when Reviewer comments `LGTM`, five review/fix iterations are reached, or monitor setup is blocked.

## Reviewer

- Do not edit code.
- Audit the PR for structure, abstractions, modularity, legibility, duplication, naming, testability, and unnecessary behavior risk.
- Leave only actionable PR comments. Each comment must name the expected improvement and why it matters.
- After each Fixer commit, review the diff since the last seen SHA before commenting again.
- If no actionable improvements remain, comment exactly `LGTM`.
- Completion criterion: the PR has `LGTM`, actionable comments for the current iteration, or a max-iteration summary.

## Fixer

- Watch for Reviewer comments.
- Fix every actionable comment from the current iteration unless the fix would change product behavior beyond the issue scope.
- Run appropriate checks after changes.
- Commit and push fixes, then reply to each addressed comment with what changed and the commit SHA.
- If a comment is intentionally not fixed, reply with the reason and the risk.
- Completion criterion: every actionable Reviewer comment has a fix commit or explicit non-fix reply, and the Reviewer has been prompted to re-review.
