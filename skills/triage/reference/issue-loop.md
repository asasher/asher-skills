# Issue Loop — One Issue to a Reviewed PR

You are the issue thread for `<issue-url>`. The issue arrived `ready-for-agent` and classified by grooming, so do not re-triage it here. Work only on this issue until it is blocked for missing information or represented by a ready-for-review PR.

Each branch below hands off to a bundled reference (`reference/<name>.md`) for the workflow and a project playbook (`docs/agents/<name>.md`) for this repo's conventions. If a playbook is missing, report a setup gap and stop — do not improvise.

## Steps

1. Orient.
   - Read the issue title, body, comments, labels, and linked artifacts, including the findings and clarifications grooming recorded. Read the relevant code and tests when the text alone is ambiguous.
   - Completion criterion: you can state the issue's expected outcome and its work-type.

2. Confirm the work-type and route. Read `docs/agents/triage-policy.md` for this repo's label roles.
   - Grooming set the work-type, so read it and route in step 3. If no work-type role is present, report a grooming gap and stop — do not classify from scratch here.
   - If orienting reveals the issue actually lacks the information to proceed, set `needs-info`, comment the gap, drop `ready-for-agent`, tell the run thread, and open no PR.
   - Completion criterion: the work-type is known and ready to route, or the issue is handed back as `needs-info`.

3. Execute the branch.
   - **bug** → follow `reference/diagnose.md`.
   - **refactor** → follow `reference/refactor.md`.
   - **enhancement** → follow `reference/plan.md`; it decides whether a plan is needed, may hand a blocking design question to `reference/prototype.md`, and holds the approval gate. Once it returns an approved, committed plan or a skip decision, follow `reference/implement.md`.
   - Any branch — not just enhancement — may hand a blocking design question to `reference/prototype.md`; the branch's own reference states when.
   - Completion criterion: the branch's own completion criterion is met, or the thread is paused at the enhancement approval gate.

4. Verify behavior → follow `reference/verify.md`.
   - This is a loop: verify runs the checks and exercises the change against its acceptance criteria, handing failures back to the branch that built the change (`implement.md`, `diagnose.md`, or `refactor.md`) until every criterion passes or it hits its cap.
   - Delegate the whole loop to a subagent filling the delegate role per `verify.md`'s staffing rule; this thread stays coordinator and takes back any failure the subagent escalates as non-mechanical or twice-failed.
   - Completion criterion: every acceptance criterion passes, or the verify loop ends at its cap or an explicit blocker (reported, no PR opened).

5. Create the PR.
   - Open a ready-for-review PR, not a draft, once implementation and verification are complete. Target the base branch named in `docs/agents/environment.md`.
   - Body outline, in order — the body is the index for this change's evidence:
     - `Closes #<issue-number>` and the work-type.
     - **Summary** — what changed and why, in the issue's terms, including any scope discovery that shaped the change (e.g. "the backend already supported this end to end, so this is frontend-only").
     - **Changes** — the significant files/modules with the design reasoning a reviewer needs (why a save lands on this action, why a component was extracted), not a raw file list.
     - **Plan** (enhancements) — SHA-pinned link to the committed plan, noting where it was approved.
     - **Checks run** — each command and its result.
     - **Verification** — what stack the criteria were exercised against and the per-criterion outcome, including the verify step's recorded caveats: any criterion verified through a workaround names the gap and the substitute observation, framed as environment gaps vs product issues. Disclosed limitations, never silent claims.
     - **Evidence** — a placeholder: "Captured after review converges." Evidence is deliberately deferred to step 7 so it is captured once, against the reviewed HEAD.
   - Completion criterion: a ready-for-review PR exists whose body can close the issue.

6. Adversarial review → follow `reference/adversarial-review.md` against the new PR.
   - The verify loop (step 4) checks behavior against criteria; this loop reviews the diff for correctness and quality. If a fixer commit changes user-facing behavior, re-verify the affected criteria (evidence has not been captured yet, so nothing goes stale).
   - Completion criterion: review reaches `LGTM`, hits its iteration cap, or reports an explicit blocker.

7. Capture evidence → follow `reference/evidence.md`.
   - Runs once, after the review loop ends, against the branch's final HEAD — so the captured proof matches what merges. Skip if the playbook requires no evidence beyond green checks. Delegate per `evidence.md`'s staffing rule (the delegate role).
   - Commits after the Reviewer's `LGTM` may touch only `evidence/` — never product code — so the approval stays valid.
   - Replace the PR body's evidence placeholder with the verified ready-to-paste block (`gh pr edit` or equivalent) — do not rebuild or reformat the block. If a browser driver in `environment.md` can reach GitHub, eyeball the rendered body after the edit.
   - Completion criterion: the evidence is committed and pushed, and the PR body carries the verified block in place of the placeholder — or none is required.

8. Report back.
   - Send the run thread the issue number, work-type, branch, PR URL, checks, evidence, and review outcome.
   - Completion criterion: the run thread can update its handoff table without reading this whole thread.
