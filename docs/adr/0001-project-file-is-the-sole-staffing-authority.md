---
status: accepted
---

# The project file is the sole staffing authority; skills ship seeds, not runtime config

Staffing resolution used to span two surfaces: a per-harness module in the home directory carrying the roster, plus sparse project deltas. That module could not be versioned, reviewed in a change request, or read from a fresh clone, and base-plus-delta resolution is itself the drift generator — it is the shape that produces the "override silently re-copied the base" failure. We decided that a project's staffing playbook carries the **complete** roster and is the only thing read at resolution time, and that the roster the `staffing` skill ships is a **seed** consulted once at setup and never at runtime.

## Considered options

**Bundled roster as base, project file as overrides** — what asher-skills#107 first proposed. Rejected because it is still two-layer resolution: it relocates the drift generator rather than removing it, and a project diff still does not show the effective roster.

**Bundled roster only, no project layer** — rejected because reachability is genuinely per-checkout, and this repo already carries two real deltas.

## Consequences

Propagation stops being automatic. A roster change at source now requires an install _and_ a setup re-run per project, where previously editing one home-directory file served every project on the machine. That cost is deliberate, and it is why the installer is to report which skills changed and which setups are consequently stale — that reporting does not exist yet and is tracked separately. Until it does, the staleness is carried in an operator's head, which is the failure mode this decision otherwise accepts knowingly.

Because the roster is committed, it travels to machines that never ran its probes. The playbook therefore records the machine, probe date, and CLI versions at its head, and a session whose machine does not match re-runs setup rather than trusting the rows. A stale row is worse than a missing one: it resolves cleanly and fails at the moment of use.

The apparent duplication is intentional. Every project carrying its own roster looks redundant next to a skill that also ships one — but the shipped copy is a seed with unverified defaults, and the project copy is what an audit verified on a specific machine. Collapsing them by making the seed runtime-read would restore exactly the property this decision removes.
