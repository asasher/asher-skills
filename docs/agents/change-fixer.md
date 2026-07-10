<!-- backlog-templates: v2026-07-10.2 -->

# Playbook: Change Fixer Conventions

> Project playbook for this repo. The backlog `adversarial-review` Fixer subagent reads this file for how this team fixes and responds to review; the loop mechanics are in the skill's `reference/adversarial-review.md`.

## Fix

- Address every actionable comment from the current iteration, unless a fix would change product behavior beyond the issue scope. The Reviewer's structural pushes are in scope by default — behavior-preserving restructuring is what this loop is for.
- Follow `implementing.md` for branch and commit conventions, and its test standards for any tests the fix touches.
- Run the checks in `verifying.md` after changes (accessing the app per `environment.md`), then commit and push.

## Reply

- Reply to each addressed comment with what changed and the commit SHA.
- For an intentional non-fix, reply with the reason and the risk.
- Re-prompt the Reviewer once the iteration's comments are handled.
