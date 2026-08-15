# Roles and fallback

Roles are defined by **workflow stage** and, within build-out, by **work surface**. A role is a named preset of bars — it tells the caller what to state, and resolution proceeds per [rankings-and-routing](rankings-and-routing.md): filter below the bars, take the cheapest survivor.

One model may fill several roles. **Separation is by thread, not by model:** delegating a role into its own thread is what keeps the orchestrator's context coordinative, even when the same model would nominally do both jobs.

## Roles as bars

- **Orchestrator** — judgment, not production: grooming, dispatch, planning, prototype decisions, hard diagnosis, and every escalation. High intelligence bar. Do not spend it on routine build-out.
- **Builder** — production: implement, refactor, and the fix commits the loop surfaces. Bars follow the **surface** the change touches:
  - **backend** — logic, data, APIs, tests. Intelligence bar sized to the task's difficulty; no taste bar.
  - **ui** — components, styling, layout, client-only rendering. Carries the hard taste bar for user-facing work; a model below it never takes ui work.
  - **mixed** — split by file where practical (backend files to the backend route, ui files to the ui route); when it cannot be split cleanly, the whole change takes the stricter surface's bars.
- **Checker** — verify ⇆ fix loops, evidence capture, and review subagents. Checking anything user-facing carries the same taste bar as building it, because the reviewer must satisfy the full review criteria; a below-bar model may check only work with no user-facing surface.

Fix work surfaced by verify or review is re-delegated to a builder-bar route for its surface — **never patched in the orchestrator's thread.** The orchestrator takes back only escalations flagged non-mechanical.

## Fallback

There are no succession lists. Fallback is the resolution rule itself: **the next-cheapest survivor above the same bars steps in.**

- **A route fails at the point of use** → warn the user, take the next-cheapest survivor above the bars, continue. The warning is the record; a route failing repeatedly across sessions is retro fodder.
- **Output misses the bar** → escalate to a more capable survivor without asking.
- **No model above the bars is reachable** → run the work **on the current model, in a subagent** when the harness allows one, inline only when no subagent is possible, and **report the staffing gap**. Never skip the step, and never quietly ship user-facing work through a model below the taste bar — the gap report is the honesty mechanism.
- **A missing playbook degrades, it does not hard-stop.** Staff the fallback above, report the staffing gap, and suggest `staffing setup`.

## Worked example — the ui route fails

A ui change resolves to the cheapest survivor above the taste bar, but that route fails at dispatch. Do **not** hand the work to a below-bar model and do **not** stop. Warn the user, then take the next-cheapest survivor still above the taste bar — even if that is the most expensive model on the roster. If nothing above the bar is reachable, run the ui work on the current model in a subagent and report the staffing gap.
