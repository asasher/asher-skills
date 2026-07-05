# Model Staffing

The skill defines roles by **workflow stage** and, within build-out, by **work surface**; the Model staffing section of `docs/agents/environment.md` (written by `triage setup`) records which model fills each role, because the roster depends on the harness the loop runs in — a harness that cannot reach another vendor's models fills every role from its own lineup. One model may fill several roles: separation is by thread, not by model — delegating into separate threads is what keeps the orchestrator's context coordinative.

## Roles

- **Orchestrator** — the most capable model reachable. Owns judgment, not production: groom, `run` dispatch, orient, plan, prototype decisions, hard diagnosis, and every escalation. Do not spend it on routine build-out.
- **Builder** — owns production: implement, refactor, and the fix commits the loops surface. Routed by the surface the change touches:
  - **backend** — logic, data, APIs, tests. May be an external CLI when the harness can invoke one.
  - **ui** — components, styling, layout, client-only rendering. Takes a model with strong frontend judgment; the backend builder never takes ui work unless the roster clears it for it.
  - **mixed** — split by file where practical (backend files to the backend builder, ui files to the ui builder); when it can't be split cleanly, the builder owning the larger or riskier surface takes the whole change.
- **Checker** — owns the capped loops: verify ⇆ fix, evidence capture, and the adversarial-review subagents. The Reviewer must satisfy the full criteria in `docs/agents/pr-reviewer.md`, frontend included, so checking anything that touches ui stays on a ui-capable model; a backend-only model may check only backend-only work.
- **Floor** — the minimum capability class the playbook names. Nothing staffs below it, in any role.

Fix work surfaced by verify or adversarial review is re-delegated to the builder for its surface — never patched in the orchestrator's thread. The orchestrator takes back only escalations flagged non-mechanical.

## Fallback ladder

A missing playbook hard-stops a subcommand; a missing Model staffing *section* only degrades — setup ran incompletely, so staff the fallback below and report a staffing gap rather than stopping. When a role's model is unreachable, the next most capable reachable model steps into the role, per the roster's succession line — an orchestrator succession may leave one model both orchestrating and building its surface. When no other model is reachable at all, run the delegated work on the current model — in a subagent when the harness allows one, inline only when none is possible — never skipping the step. Delegation into a separate thread still keeps build-out and the capped loops out of the orchestrator context.
