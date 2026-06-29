# Plan

Target: an enhancement issue or feature request. Runs standalone or as the planning step of the `enhancement` branch.

Read `docs/agents/planning.md` for this repo's plan format, location, plan-size threshold, and approval conventions. If it is missing, report a setup gap and stop.

## Steps

1. Decide whether the change needs a plan.
   - Apply the playbook's plan-size threshold. Small, low-risk changes skip planning and go straight to `reference/implement.md`.
   - Completion criterion: a stated decision — plan or skip — grounded in the playbook's threshold.

2. Write the plan.
   - Produce the plan in the format and location the playbook specifies. Cover what the playbook requires (typically: user stories, definition of done, evidence required, implementation outline, risks, test plan).
   - State the definition of done as explicit, testable acceptance criteria — each something the verify loop can check pass/fail against a running app. These are the contract `reference/verify.md` and `reference/evidence.md` consume downstream.
   - Completion criterion: the plan exists in the specified location, meets the playbook's checklist, and its acceptance criteria are individually checkable.

3. Stop at the approval gate.
   - Wait for human approval before implementation. If approval changes scope, update the plan before coding.
   - Completion criterion: the plan is approved as-is, or revised and re-submitted; no implementation begins until approval.
