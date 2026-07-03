# Plan

Target: an enhancement issue or feature request. Runs standalone or as the planning step of the `enhancement` branch.

What a plan covers, its HTML format and location, the plan-size threshold, review conduct, and who approves live in `docs/agents/planning.md`. If it is missing, report a setup gap and stop.

## Gates

1. **Decided** — a stated plan-or-skip decision grounded in the playbook's threshold. Small, low-risk changes skip planning and go straight to `reference/implement.md`.
2. **Design questions answered** — any question the plan cannot settle on paper (a state model that only feels right or wrong under real cases, a UI that needs to be seen) goes through `reference/prototype.md`; its answer — and for UI, the variant screenshots — is folded into the plan before review.
3. **Written** — the plan exists as an HTML document in the playbook's location, meets its checklist, and states the definition of done as explicit, testable acceptance criteria — each checkable pass/fail against a running app. These are the contract `reference/verify.md` and `reference/evidence.md` consume downstream.
4. **Approved** — the rendered plan was opened for the human, and a human approved it as-is or a revised resubmission before any implementation begins. If approval changes scope, update the plan first.
5. **Committed** — the approved plan is committed to the work branch before implementation is dispatched, so implementing agents read it from disk, and the playbook's posterity step (if any) has run.
