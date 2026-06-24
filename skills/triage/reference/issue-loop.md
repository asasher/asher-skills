# Issue Loop — One Issue to a Reviewed PR

You are the issue thread for `<issue-url>`. Work only on that issue until it is blocked for missing information or represented by a ready-for-review PR.

Each branch below hands off to a bundled reference (`reference/<name>.md`) for the workflow and a project playbook (`docs/agents/<name>.md`) for this repo's conventions. If a playbook is missing, report a setup gap and stop — do not improvise.

## Steps

1. Orient.
   - Read the issue title, body, comments, labels, and linked artifacts. Read the relevant code and tests when the text alone is ambiguous.
   - Completion criterion: you can state the issue's expected outcome and its type.

2. Classify and label.
   - `needs-info` — not enough to identify the desired outcome, reproduction, affected surface, or safe scope.
   - `bug` — reported behavior contradicts intended or documented behavior.
   - `enhancement` — asks for new or changed user-facing capability.
   - `refactor` — should preserve behavior while improving structure, maintainability, or tests.
   - Apply exactly one primary label.
   - Completion criterion: the issue carries its primary label, or labeling is reported as blocked.

3. Stop early for `needs-info`.
   - Comment the missing facts or decisions on the issue. Open no PR.
   - Completion criterion: the issue is labeled `needs-info`, the gap is stated on the issue, and the run thread is told.

4. Execute the branch.
   - **bug** → follow `reference/diagnose.md`.
   - **refactor** → follow `reference/refactor.md`.
   - **enhancement** → follow `reference/plan.md`; it decides whether a plan is needed and holds the approval gate. Once it returns an approved plan or a skip decision, follow `reference/implement.md`.
   - Completion criterion: the branch's own completion criterion is met, or the thread is paused at the enhancement approval gate.

5. Verify → follow `reference/verify.md`.
   - Completion criterion: the checks the PR will claim have been run, and any needed evidence is captured.

6. Create the PR.
   - Open a ready-for-review PR, not a draft, once implementation and verification are complete. Target the base branch named in `docs/agents/environment.md`.
   - The body must include `Closes #<issue-number>`, the classification, a summary, the checks run, evidence links, and the plan link for enhancements. The body is the index for this change's evidence.
   - For committed evidence, prefer repo-backed raw links pinned to a commit SHA:

```markdown
![alt](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png?raw=1)
```

   - Completion criterion: a ready-for-review PR exists whose body can close the issue.

7. Adversarial review → follow `reference/adversarial-review.md` against the new PR.
   - Completion criterion: review reaches `LGTM`, hits its iteration cap, or reports an explicit blocker.

8. Report back.
   - Send the run thread the issue number, label, branch, PR URL, checks, evidence, and review outcome.
   - Completion criterion: the run thread can update its handoff table without reading this whole thread.
