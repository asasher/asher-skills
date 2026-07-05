# Evidence

Target: a branch whose behavior `reference/verify.md` has confirmed against its acceptance criteria. Terminal capture step — runs once. In the issue loop it runs **after adversarial review converges**, against the branch's final HEAD, so the captured proof matches what merges and is never invalidated by fixer commits; standalone it follows verify directly. Never run it on a change that has not passed verification; the point is to prove to a human that the criteria are met, so capturing a half-working state defeats it.

Staffing: capture is mechanical — a subagent filling the **checker** role runs it; see `reference/staffing.md` for the role and its fallback ladder, and the Model staffing section of `docs/agents/environment.md` for the roster.

What to capture, the format/storage contract, and the presentation contract (how artifacts render inline on GitHub) live in `docs/agents/evidence.md`; how to stand up, seed, and authenticate against the app in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Gates

1. **Captured to criteria** — each artifact the playbook requires for the touched surface exists, captured against the now-confirmed-working stack, and names the acceptance criterion it demonstrates. Capture nothing for a change whose playbook requires no evidence beyond green checks.
2. **Stored and pushed** — every artifact is committed on the work branch per the playbook's format and storage contract, and the branch is pushed. The push happens here, not at PR creation: the embed URLs are pinned to this commit's SHA, and they only resolve once that SHA is on the remote.
3. **Presentation prepared and verified** — the deliverable of this gate is a **ready-to-paste markdown block**, built against the pushed evidence commit per the playbook's presentation contract, grouped by the criterion each artifact proves, and passing the playbook's mechanical checks. Report the block back to the invoking thread; in the loop, the thread swaps it in for the PR body's evidence placeholder. The bar: every artifact renders inline; click-through links fail this gate.
