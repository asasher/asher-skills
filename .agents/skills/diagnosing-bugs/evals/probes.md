# Diagnosing Bugs — situated probes

Run each probe through both deployment executors with `SKILL.md` and only the named reference/playbook in
context. Require file-and-sentence citations. Grade against `answer-key.md`, written before execution.

## Probes

**P1 — red before theory.** A checkout intermittently returns HTTP 500. You have a plausible stack-frame
theory but no command that catches the reported failure. What is your next move and what gate must exist before
hypotheses?

**P2 — reproduce and minimise.** Your browser script reliably shows the reported stale total. It currently
creates three accounts, twenty orders, and visits six pages. What do you do before hypothesising, and when are
you done?

**P3 — ranked falsifiable hypotheses.** Give the required shape and checkpoint for the hypotheses before
instrumentation. What makes a hypothesis invalid?

**P4 — targeted instrumentation.** Two hypotheses differ at a cache boundary. How do you instrument them,
and what cleanup affordance must temporary logging carry? Include the performance-regression branch.

**P5 — regression proof or no seam.** The bug requires two callers but the only testable unit exposes one.
May you add that shallow test and call the regression locked? State the valid outcomes and the original-loop
requirement.

**P6 — cleanup.** The minimal test is green after the fix, but a `[DEBUG-a4f2]` log remains and the original
unminimised command has not been rerun. Is diagnosis complete? List the terminal evidence.

**P7 — independent invocation.** A user directly reports a slow endpoint outside backlog. Does this skill
apply, which execution context owns it, and which siblings must be installed?

**P8 — setup reconciliation.** On first setup no diagnosis playbook exists; on the second run the repo has
customized its test command and logging notes. What may setup write, what must it preserve, and what proves the
second run is correct?

**P9 — backlog parity.** A backlog issue takes the bug branch. Which skill owns the diagnosis method, what
must return before backlog accepts the handoff, and which responsibilities remain with backlog?

**P10 — no loop.** Production alone reproduces the defect and the agent lacks access, traces, and permission
to instrument. May it continue with its leading theory? What exact return is required?
