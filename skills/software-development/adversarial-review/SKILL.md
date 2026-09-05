---
name: adversarial-review
description: Converge a PR through bounded review and fix passes, optionally checking behavioral claims in the same loop. Resume from the PR's persisted state.
metadata:
  requires: [code-review, to-subagent]
  optional: [diagnosing-bugs, verify-your-work]
---

# Adversarial review

Drive one PR to a current-head LGTM or an explicit stop. The PR's comments and commits carry the run state. Dispatch bounded passes via `to-subagent`; keep this session alive until every dispatched pass returns or is confirmed stopped.

Read [conduct](reference/conduct.md) for reviewer and fixer briefs. With supplied behavioral claims, also dispatch `verify-your-work`. If that sibling is absent, return verification incomplete; a review cannot substitute for behavioral proof. An explicit light-work omission or a standalone review without behavioral claims runs review only and reports that scope.

## Resume and bounds

Read the latest run state before dispatch: reviewed head and base, pass count, total budget, absolute deadline, findings, verification reports, and next actor. Initialize missing state with three review passes and a deadline one hour from now, shortened to any supplied earlier deadline. A supplied total budget overrides the default only for a new run; an existing run changes its bound through the extension ruling below. Persist these before starting.

A pass consumes budget when dispatched, including one interrupted before returning. Resume preserves the original deadline and consumed passes. Each dispatch receives the remaining deadline; on timeout, stop the worker and confirm it has stopped before another actor may write.

Cap exhaustion returns **stopped at a bound**. The driver may grant a bounded extension with a recorded ruling naming additional passes and a new deadline if needed, within any outer workflow deadline. Extend only when prior findings are resolving and the remainder is narrower. Widening or recurring findings stop. A product question requires a human ruling before resumption; an extension cannot answer it. Never reset the count by starting another invocation.

## The loop

1. **Pin inputs.** Push intended commits and require a clean tracked tree with local and remote heads equal. Resolve the target branch's current base SHA. Persist both SHAs and the next pass number.
2. **Check together.** Dispatch one read-only reviewer pass and, when required, one behavioral verifier in the same turn. Give both the pinned head, base, claims, and deadline. The reviewer reads code and checks CI status; it leaves runtime tests to the verifier. The verifier alone owns its temporary scripts, fixtures, and runtime checks. Serialize checks if the environment cannot isolate their mutable state.
3. **Join and classify.** Wait for both returns before allowing any writer. Compare their input SHAs with the branch and target again. A moved input invalidates the affected verdict; another pass uses the remaining budget. Persist the reports, unresolved findings, and any optional suggestions. A product question returns **product question**. Honor supplied scope limits: a coverage-check gap requiring a new independently deliverable slice is a product question, not a review-scale fix. Missing checks or an inaccessible environment return **verification incomplete** with the affected claims unless a human waiver already names those claims at this head; a proven pre-existing failure is reported separately with its issue, not silently passed.
4. **Converge or fix.** Add any supplied evidence or late-CI findings to the persisted reports before deciding convergence. With no blocking findings and all required claims verified or explicitly waived at this head, return **converged**, naming head, base, reports, and CI status. Pending CI is disclosed and remains a completion gate for the workflow using this result. With findings open, dispatch one fixer only when the budget and deadline permit a subsequent check pass; otherwise return stopped at a bound. Prefer resuming the implementer with its report; otherwise dispatch a fresh fixer with that report and the persisted findings. Address failures of required CI in the same fix pass. Re-enter step 1 after it returns.

When resuming, honor the recorded next actor: a returned checking pass with unresolved findings resumes at step 4; an interrupted fix is inspected before re-dispatch. A defect found after convergence enters step 4 with its evidence, then invalidates the old convergence. A completed final check pass may still converge when resuming at the cap; exhaustion forbids another pass, not accepting an already persisted valid result.

A fix invalidates both verification and review even when it addresses only one report. An accepted pushback can clear a finding only through a subsequent checking pass. The driver never edits code or accepts its own explanation as a passing verdict.

## Return

Persist and return one outcome: **converged**, **stopped at a bound**, **product question**, or **verification incomplete**. Include the head and base, passes consumed and remaining, deadline, report pointers, open findings or unverified claims, and next action. A state comment records progress; the blocking dispatch's return is what wakes this driver.
