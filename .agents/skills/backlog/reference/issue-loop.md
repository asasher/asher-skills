# Issue Loop — One Issue to a Reviewed PR

You are the issue thread for `<issue-reference>`. The issue arrived `ready-for-agent` and classified by grooming, so do not re-triage it here. Work only on this issue until it is blocked for missing information or represented by a ready-for-review PR.

Each branch below hands off to a bundled reference (`reference/<name>.md`) for the workflow and a project playbook (`docs/agents/<name>.md`) for this repo's conventions. Tracker and PR mechanics come from `docs/agents/platform.md`. If a playbook is missing, report a setup gap and stop — do not improvise.

Tracker write discipline: on the local binding, this thread writes only its own issue file, only on its own branch — lifecycle updates that should merge with the change (state flips, plan and review links). Writes that must reach the main branch without a merge — `needs-info`, blockers, clearing `in-flight` — are reported to the run thread, the serialized main writer, never committed here (`platform.md` § The local binding). On bindings with a live tracker (GitHub), write directly via the tracker verbs.

## Steps

1. Orient.
   - Read the issue title, body, comments, labels, and linked artifacts, including the findings and clarifications grooming recorded. Read the relevant code and tests when the text alone is ambiguous.
   - Completion criterion: you can state the issue's expected outcome and its work-type.

2. Confirm the work-type and route. Read `docs/agents/backlog-policy.md` for this repo's label roles.
   - Grooming set the work-type, so read it and route in step 3. If no work-type role is present, report a grooming gap and stop — do not classify from scratch here.
   - If orienting reveals the issue actually lacks the information to proceed, hand it back: set `needs-info`, comment the gap, and drop the in-flight claim — directly via the tracker verbs where the binding allows, through the run thread's report otherwise — tell the run thread either way, and open no PR.
   - Completion criterion: the work-type is known and ready to route, or the issue is handed back as `needs-info`.

3. Execute the branch.
   - **bug** → follow `reference/diagnose.md`.
   - **refactor** → follow `reference/refactor.md`.
   - **enhancement** → invoke the **`plan` skill** by name: it decides plan-or-skip, settles blocking design questions (itself composing the `prototype` skill by name), writes the HTML plan, and holds the approval gate. The `plan` skill stops at approval — **backlog owns the dev-tail**: on an approved plan, commit it to the work branch before dispatching build, and write the tracker posterity digest per `docs/agents/planning.md`/`platform.md` conventions (this dev-tail was formerly the plan step's gate 5 + posterity — it stays here now). Then follow `reference/implement.md`. On a skip decision, go straight to `reference/implement.md`.
   - **draft** → produce-and-review, for judgment-terminal work whose correctness is taste/fit (a memo, copy, a research synthesis, code docs). Produce the artifact — authoring staffed by the **`staffing`** skill (by name) — then present it for sign-off through the **`review-loop`** skill (by name); the human review verdict **is** the definition of done. **Keep** the artifact: commit it to the work branch (unlike `prototype`, which deletes its throwaway — draft keeps the thing it made). There is no plan/implement spine and no mechanical acceptance-criteria run — see step 4.
   - Any branch — not just enhancement — may hand a blocking design question to the `prototype` skill (by name); the branch's own reference states when.
   - Staffing: build-out — `implement.md`, `refactor.md`, and fix commits — runs on the **builder** role for its surface, resolved by the `staffing` skill (by name), dispatched out of this thread; diagnosis is orchestrator work and stays here.
   - Completion criterion: the branch's own completion criterion is met, or the thread is paused at the enhancement approval gate.

4. Verify behavior → follow `reference/verify.md`.
   - This is a loop: verify runs the checks and exercises the change against its acceptance criteria, handing failures back to the branch that built the change (`implement.md`, `diagnose.md`, or `refactor.md`) until every criterion passes or it hits its cap.
   - Delegate the whole loop to a subagent filling the **checker** role, resolved by the `staffing` skill (by name); this thread stays coordinator and takes back any failure the subagent escalates per `verify.md`'s triggers.
   - **draft exception.** A `draft` has no testable spec, so this step is skipped — it degenerates to "the review gate passed": the `review-loop` verdict from step 3 stands in for verify. Correspondingly, step 6 adversarial review degenerates for a pure-prose artifact (the human verdict was the review); a code-docs draft keeps a light correctness pass over the docs it touches.
   - Completion criterion: every acceptance criterion passes, or the verify loop ends at its cap or an explicit blocker (reported, no PR opened).

5. Create the PR.
   - Open a ready-for-review PR, not a draft, via the change-review binding's open verb, once implementation and verification are complete. Target the base branch named in `docs/agents/environment.md`.
   - Build the body per `docs/agents/pr.md`: it carries the close linkage from `platform.md` (GitHub: `Closes #<n>`; local: the issue file's `state` flips on this branch and closure rides the merge), the checks and per-criterion verification with the verify step's caveats, and an evidence placeholder — evidence is deferred to step 7.
   - Completion criterion: a ready-for-review PR exists whose merge will close the issue per the binding's linkage.

6. Adversarial review → follow `reference/adversarial-review.md` against the new PR.
   - The verify loop (step 4) checks behavior against criteria; this loop reviews the diff for correctness and quality. If a fixer commit changes user-facing behavior, re-verify the affected criteria.
   - Completion criterion: review reaches `LGTM`, hits its iteration cap, or reports an explicit blocker.

7. Capture evidence → follow `reference/evidence.md`.
   - Runs once, after the review loop ends, against the branch's final HEAD; `reference/evidence.md` carries the timing rationale. Skip if the playbook requires no evidence beyond green checks. Delegate the capture to the **checker** role, resolved by the `staffing` skill (by name).
   - Commits after the Reviewer's `LGTM` may touch only `evidence/`, the review file, and — on the local binding — the issue file's closing flip: set `state: closed` on this branch now, so the merge carries closure to main per `platform.md`'s close linkage. Never product code, so the approval stays valid.
   - Replace the PR body's evidence placeholder with the verified ready-to-paste block via the binding's edit-body verb — do not rebuild or reformat the block. If a browser driver in `environment.md` can reach the review surface, eyeball the rendered body after the edit.
   - Completion criterion: the evidence is committed and published, and the PR body carries the verified block in place of the placeholder — or none is required.

8. Report back.
   - Send the run thread the issue id, work-type, branch, PR reference, checks, evidence, and review outcome — plus any tracker writes it must apply as the serialized main writer.
   - Completion criterion: the run thread can update its handoff table without reading this whole thread.
