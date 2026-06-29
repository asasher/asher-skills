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
   - **enhancement** → follow `reference/plan.md`; it decides whether a plan is needed and holds the approval gate. Once it returns an approved plan or a skip decision, follow `reference/implement.md`.
   - Completion criterion: the branch's own completion criterion is met, or the thread is paused at the enhancement approval gate.

4. Verify behavior → follow `reference/verify.md`.
   - This is a loop: verify runs the checks and exercises the change against its acceptance criteria, handing failures back to `implement.md`/`diagnose.md` until every criterion passes or it hits its cap.
   - Completion criterion: every acceptance criterion passes, or the verify loop ends at its cap or an explicit blocker (reported, no PR opened).

5. Capture evidence → follow `reference/evidence.md`.
   - Runs once, only after verify converges. Skip if the playbook requires no evidence beyond green checks.
   - Completion criterion: the required evidence exists under `evidence/<slug>/` ready to embed, or none is required.

6. Create the PR.
   - Open a ready-for-review PR, not a draft, once implementation and verification are complete. Target the base branch named in `docs/agents/environment.md`.
   - The body must include `Closes #<issue-number>`, the work-type, a summary, the checks run, evidence links, and the plan link for enhancements. The body is the index for this change's evidence.
   - For committed evidence, prefer repo-backed raw links pinned to a commit SHA:

```markdown
![alt](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png?raw=1)
```

   - Completion criterion: a ready-for-review PR exists whose body can close the issue.

7. Adversarial review → follow `reference/adversarial-review.md` against the new PR.
   - The verify loop (step 4) checks behavior against criteria; this loop reviews the diff for correctness and quality. If a fixer commit changes user-facing behavior, the evidence from step 5 goes stale — re-verify and re-capture the affected criteria.
   - Completion criterion: review reaches `LGTM`, hits its iteration cap, or reports an explicit blocker.

8. Report back.
   - Send the run thread the issue number, work-type, branch, PR URL, checks, evidence, and review outcome.
   - Completion criterion: the run thread can update its handoff table without reading this whole thread.
