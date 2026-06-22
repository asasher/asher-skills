# Issue Thread Instructions

You are the issue thread for `<issue-url>`. Work only on that issue until it is blocked by missing information or represented by a ready-for-review PR.

## Steps

1. Orient on the issue.
   - Read the issue title, body, comments, current labels, and linked artifacts.
   - Read the relevant code and tests before choosing a work branch when the issue text alone is ambiguous.
   - Completion criterion: you can state the issue's expected outcome and why it is a `bug`, `enhancement`, `refactor`, or `needs-info`.

2. Classify and label.
   - Use `needs-info` when the issue lacks enough information to identify the desired outcome, reproduction path, affected surface, or safe implementation scope.
   - Use `bug` when the reported behavior contradicts intended or documented behavior.
   - Use `enhancement` when the issue asks for new or changed user-facing capability.
   - Use `refactor` when the requested change should preserve behavior while improving structure, maintainability, or tests.
   - Apply exactly one primary label: `bug`, `enhancement`, `refactor`, or `needs-info`.
   - Completion criterion: the issue has the chosen primary label, or the thread has reported that labeling is blocked.

3. Stop early for `needs-info`.
   - Add a concise issue comment listing the missing facts or decisions.
   - Report the blocker to the triage thread.
   - Completion criterion: the issue is labeled `needs-info`, the missing information is stated on the issue, and no implementation PR is opened.

4. Execute the selected branch.
   - Bug: invoke the `diagnose` skill when available. Reproduce or explain the failure before changing code, then implement the fix and verify the failing path now passes.
   - Enhancement: create an HTML plan under `plans/<issue-number>-<slug>.html`, then wait for human approval before implementation. The plan must include user stories, definition of done, evidence required, implementation outline, risks, and test plan. Use Mermaid diagrams or syntax-highlighted code only when they make the plan clearer. After approval, implement the approved plan; if approval changes scope, update the plan before coding.
   - Refactor: invoke the `tdd` skill when available. Add or identify tests that lock the behavior that must remain unchanged before modifying implementation.
   - Completion criterion: a bug has a verified fix, a refactor has unchanged behavior tests passing, and an enhancement is either paused at the plan-review gate or implements the approved plan.

5. Verify and capture proof.
   - Run the narrowest meaningful checks first, then broader checks required by the touched surface.
   - When UI or workflow evidence is useful, use `agent-browser` if available.
   - When email delivery or inbox behavior is part of the issue, use `agentmail` if available.
   - Static visual evidence belongs under `evidence/<issue-or-feature-slug>/` as PNG or JPEG.
   - Short flow evidence should be recorded as MP4 for local inspection, converted to a small GIF, and committed under `evidence/<issue-or-feature-slug>/`.
   - Completion criterion: the PR can name the checks run and link or embed any evidence needed for review.

6. Create the PR.
   - Create a ready-for-review PR, not a draft, once implementation and verification are complete.
   - The PR body must include `Closes #<issue-number>`, classification, summary, tests, evidence links, and the plan link for enhancements.
   - Use repo-backed raw links with a commit SHA for committed evidence when possible:

```markdown
![Descriptive alt text](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.png?raw=1)
![Descriptive alt text](https://github.com/<owner>/<repo>/blob/<commit-sha>/evidence/<slug>/<file>.gif?raw=1)
```

   - Completion criterion: the PR exists, is ready for review, and its body can close the issue.

7. Run adversarial review.
   - After the PR exists, load and execute `ADVERSARIAL_REVIEW_INSTRUCTIONS.md`.
   - Completion criterion: adversarial review reaches `LGTM`, reaches its iteration limit, or reports an explicit blocker.

8. Report back.
   - Send the triage thread the issue number, label, branch, PR URL, checks, evidence, and adversarial review outcome.
   - Completion criterion: the parent triage thread has enough information to update its handoff table without reading this whole issue thread.
