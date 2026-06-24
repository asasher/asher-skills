# Playbook: PR Fixer Conventions

> Project playbook for this repo. The triage `adversarial-review` Fixer subagent reads this file. Tailor it to how this team fixes and responds to review.

## Fix

- Address every actionable comment from the current iteration, unless a fix would change product behavior beyond the issue scope.
- Follow `implementing.md` for branch and commit conventions.
- Run the checks in `verifying.md` after changes, then commit and push.

## Reply

- Reply to each addressed comment with what changed and the commit SHA.
- For an intentional non-fix, reply with the reason and the risk.
- Re-prompt the Reviewer once the iteration's comments are handled.
