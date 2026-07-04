# Model Staffing

The skill defines three roles; the Model staffing section of `docs/agents/environment.md` (written by `triage setup`) records who fills them, because the roster depends on the harness the loop runs in — a harness that cannot reach another vendor's models fills every role from its own lineup.

- **Lead** — the most capable model reachable. Runs the issue thread and its thinking-heavy steps: groom, run, orient, diagnose, plan, prototype, implement, refactor.
- **Delegate** — the next most capable tier below the lead, never below the floor. Runs the capped loops: verify ⇆ fix, evidence capture, and the adversarial-review subagents. May be an external CLI for backend-only work when the playbook allows it; the Reviewer must satisfy the full criteria in `docs/agents/pr-reviewer.md`, frontend included, so it takes only delegates the playbook clears for review.
- **Floor** — the minimum capability class the playbook names. Nothing staffs below it.

## Fallback ladder

A missing playbook hard-stops a subcommand; a missing Model staffing *section* only degrades — setup ran incompletely, so staff the fallback below and report a staffing gap rather than stopping. When that section is missing, the harness offers no model override, or no tier fits between the current thread's model and the floor, run the delegated work on the current model — in a subagent when the harness allows one, inline only when none is possible — never skipping the step. Delegation into a separate thread still keeps the capped loops out of the lead context.
