# Evidence

Target: a branch whose behavior `reference/verify.md` has confirmed against its acceptance criteria. Terminal capture step — runs once. In the build loop it runs **after adversarial review converges**, against the branch's final HEAD, so the captured proof matches what merges and is never invalidated by fixer commits; standalone it follows verify directly. Never run it on a change that has not passed verification; the point is to prove to a human that the criteria are met, so capturing a half-working state defeats it.

Staffing: capture is mechanical — a subagent filling the **checker** role runs it; the role and its fallback ladder are resolved by the `staffing` skill (by name).

What to capture, the format/storage contract, and the presentation contract (how artifacts render inline on the bound review surface) live in `docs/agents/evidence.md`; the review-surface and publication bindings in `docs/agents/platform.md`; how to ready, seed, and authenticate against the verification surface in `docs/agents/environment.md`. If any is missing, report a setup gap and stop.

**Styling-only reuse.** A verification capture may be reused only when it was taken at the final reviewed
HEAD and the Reviewer records **“no product-code change; no recapture.”** Any product-code,
fixture, environment, or HEAD change invalidates it. Ordinary changes still capture here after review.

## Gates

1. **Captured to criteria** — each artifact the playbook requires for the touched surface exists, captured against the now-confirmed-working verification surface, and names the acceptance criterion it demonstrates. Capture nothing for a change whose playbook requires no evidence beyond green checks.
2. **Stored and published** — every artifact is committed on the work branch per the playbook's format and storage contract, and the branch is published per the version-control binding. Publication happens here, not at PR creation: where the presentation contract pins embed URLs to this commit's SHA (the GitHub binding), they only resolve once that SHA is on the remote; a binding with no remote (local) satisfies this gate at the commit.
3. **Presentation prepared and verified** — the deliverable of this gate is a **ready-to-paste markdown block**, built against the published evidence commit per the playbook's presentation contract, grouped by the criterion each artifact proves, and passing the playbook's mechanical checks. Report the block back to the invoking thread; in the loop, the thread swaps it in for the PR body's evidence placeholder. The bar: every artifact renders inline; click-through links fail this gate.
