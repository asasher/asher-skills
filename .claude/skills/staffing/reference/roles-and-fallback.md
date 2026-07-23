# Roles and the fallback ladder

Roles are defined by **workflow stage** and, within build-out, by **work surface**. The roster itself is
compiled by [machine-audit](machine-audit.md) and installed per
[install-and-reconcile](install-and-reconcile.md); this file defines the roles and succession,
machine-generically.

One model may fill several roles. **Separation is by thread, not by model:** delegating a role into its own
thread is what keeps the orchestrator's context coordinative, even when the same model would nominally do
both jobs.

## Roles

- **Orchestrator** — the most capable reachable model. Owns judgment, not production: grooming, dispatch,
  planning, prototype decisions, hard diagnosis, and every escalation. Do not spend it on routine build-out.
- **Issue coordinator** — owns one groomed issue's lifecycle and worker handoffs, resolved at dispatch per
  [rankings-and-routing](rankings-and-routing.md) § Resolution order.
  The roster's **coordinator-eligible set** contains reachable models at or above the Floor that can own a
  durable child and dispatch/escalate its worker stages. Record the
  chosen route and upward successor before creating the worktree or child. Routine work points up to the
  session orchestrator for new judgment/design/hard diagnosis/an invalidated plan; if the coordinator already
  is the orchestrator, record the roster's next orchestrator successor and any required human authority.
- **Builder** — owns production: implement, refactor, and the fix commits the loop surfaces. Routed by the
  **surface** the change touches:
  - **backend** — logic, data, APIs, tests. May be an external CLI when the harness can invoke one.
  - **ui** — components, styling, layout, client-only rendering. Takes a model with strong frontend judgment
    that clears the routing rules' taste gate. The backend
    builder never takes ui work unless the roster clears it for it.
  - **mixed** — split by file where practical (backend files to the backend builder, ui files to the ui
    builder); when it cannot be split cleanly, the builder owning the larger or riskier surface takes the
    whole change.
- **Checker** — owns the capped loops: verify ⇆ fix, evidence capture, and adversarial-review subagents.
  Checking anything that touches ui must stay on a ui-capable model, because the reviewer must satisfy the
  full review criteria, frontend included; a backend-only model may check only backend-only work.
- **Floor** — the minimum capability class the roster names. **Nothing staffs below it, in any role.** The
  floor is a hard constraint, not a preference; a project override may raise it but never staff beneath it.

Fix work surfaced by verify or adversarial review is re-delegated to the builder for its surface — **never
patched in the orchestrator's thread.** The orchestrator takes back only escalations flagged non-mechanical.

## Fallback ladder

Reachability degrades gracefully; it never silently drops a step.

- **A role's model is unreachable** → the **next most capable reachable model steps into the role**, per the
  roster's succession line. An orchestrator succession may leave one model both orchestrating and building
  its surface — acceptable; it is still preferable to stopping.
- **One sibling harness direction fails** → mark only that route unavailable and re-run the same pins, gates,
  and ranking over the remaining reachable candidates. Symmetry is a property of two working directions,
  not an assumption.
- **No other model is reachable at all** → run the delegated work **on the current model, in a subagent**
  when the harness allows one, inline only when no subagent is possible. Never skip the step.
- **A missing roster section degrades, it does not hard-stop.** If the install is incomplete (no staffing
  section found), staff the fallback above and **report a staffing gap** rather than stopping.

Succession changes *who* fills a role; it never merges the roles back into one thread.

## Worked example — the ui builder is unreachable

A ui change needs the ui builder, but that model cannot be reached from the current harness. Do **not** hand
it to the backend builder by default and do **not** stop. Walk the succession line: the next most capable
**reachable** model with sufficient taste for ui work (taste ≥ 7, per the routing rules) steps into the ui
builder role. If the only reachable model with adequate taste is the orchestrator, it takes the ui build
itself (an orchestrator/builder overlap the ladder explicitly allows). If no reachable model clears the ui
bar at all, run the ui work on the current model in a subagent and **report the staffing gap** — never ship
ui work through a model the roster would not clear for it, and never skip the change.
