# Diagnosing Bugs — answer key

- **P1:** Stop theory-building. Build and already run one unattended command that drives the actual path and
  asserts the exact symptom; it must be red-capable, deterministic enough, fast, and agent-runnable. No loop,
  no hypotheses.
- **P2:** Remove inputs, callers, config, data, and steps one at a time, rerunning after each cut. Done only
  when the smallest repro stays red and every remaining element is load-bearing.
- **P3:** Produce 3–5 ranked hypotheses before testing; each states a prediction that changing one variable
  will remove or worsen the symptom. Persist/show the list without blocking unattended work. A predictionless
  “vibe” fails.
- **P4:** Probe one prediction and variable at a time; prefer debugger/REPL, then boundary-targeted logs, each
  temporary log carrying a unique grep-able tag. Performance work needs a measured baseline/profiler/query plan
  and bisection, not logging.
- **P5:** A shallow seam that cannot reproduce the two-caller pattern is false confidence. Either write and
  watch a correct-seam test fail/pass, or explicitly record the no-seam architectural gap. Both require the
  original unminimised loop red before and green after.
- **P6:** Not complete. Rerun the original loop and project checks, pass the regression/no-seam gate, remove
  tagged logs and throwaway harnesses, and record the confirmed root cause.
- **P7:** Yes: the description covers slow/performance defects independently. `metadata` says model-invoked,
  execution `thread`, with no required or optional siblings.
- **P8:** Create only `docs/agents/diagnosing-bugs.md` from the delta template with verified facts. On rerun,
  preserve project edits/house substitutions and offer only factual reconciliation; do not recopy the method.
  An unchanged-facts rerun produces no diff.
- **P9:** Backlog invokes `diagnosing-bugs` by name; it accepts the handoff only with loop/output, minimal repro,
  named cause, fix, regression/no-seam proof, original green, cleanup, and checks. Backlog retains issue/worktree
  lifecycle, rulings/escalation, commits, PR, verify, evidence, review, and merge.
- **P10:** Stop. Return what loop attempts failed and request the concrete reproducing access, captured artifact,
  or permission for temporary instrumentation. Continuing with a theory fails.

Pass bar: 10/10 on both executors with supporting citations.
