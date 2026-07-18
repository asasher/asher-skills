# Issue Loop — One Issue to a Reviewed PR

You are the staffed issue coordinator for `<issue-reference>`. Dispatch selected this route before creating the
worktree/child and supplied the coordination reason plus upward successor; do not re-triage or silently
re-staff yourself. Coordinate this issue until it is blocked or represented by a ready-for-review PR. Escalate
new product judgment, design, hard diagnosis, or an invalidated plan to the named successor; routine worker
handoffs still resolve through `staffing` at their own boundaries.

Each branch below hands off to a bundled reference (`reference/<name>.md`) for the workflow and a project playbook (`docs/agents/<name>.md`) for this repo's conventions. Tracker and PR mechanics come from `docs/agents/platform.md`. If a playbook is missing, report a setup gap and stop — do not improvise.

Liveness: this thread is bound by `reference/run.md` § Liveness contract — five-state reporting, no turn ends with live children/gates and no verified wake path (native harness notifications first; bounded foreground waits only where the harness cannot wake you), every wait recorded with owner/deadline/wake path. Terminal CI waits are the run thread's, not yours: report the PR and hand the CI watch up rather than parking here.

Tracker write discipline: on the local binding, this thread writes only its own issue file, only on its own branch — lifecycle updates that should merge with the change (state flips, plan and review links). Writes that must reach the main branch without a merge — `needs-info`, blockers, clearing `in-flight` — are reported to the run thread, the serialized main writer, never committed here (`platform.md` § The local binding). On bindings with a live tracker (GitHub), write directly via the tracker verbs.

## Steps

1. Orient.
   - Read the issue title, body, comments, labels, and linked artifacts, including the findings and clarifications grooming recorded. Read the relevant code and tests when the text alone is ambiguous.
   - Completion criterion: you can state the issue's expected outcome, work-type, surface, coordination reason, and upward successor.

2. Confirm the work-type and route. Read `docs/agents/backlog-policy.md` for this repo's label roles.
   - Grooming set the work-type, so read it and route in step 3. If no work-type role is present, report a grooming gap and stop — do not classify from scratch here.
   - If orienting reveals the issue actually lacks the information to proceed, hand it back: set `needs-info`, comment the gap, and drop the in-flight claim — directly via the tracker verbs where the binding allows, through the run thread's report otherwise — tell the run thread either way, and open no PR.
   - If orienting instead reveals unsettled *strategic* decisions — product judgment, scope, or design direction the groomed context neither settles nor explicitly delegates — hand it back the same way as **`needs-spec`**: comment the specific open decisions, apply the role, drop the claim, and open no PR. `needs-info` means the reporter owes facts; `needs-spec` means the issue needs the upstream shaping flow (interview → spec → tickets) before any thread can own it.
   - Completion criterion: the work-type is known and ready to route, or the issue is handed back as `needs-info` or `needs-spec`.

3. Execute the branch.
   - **bug** → follow `reference/diagnose.md`.
   - **refactor** → follow `reference/refactor.md`.
   - **enhancement** → the strategic decisions arrived settled: admission guarantees every product, design, and scope question is either resolved in the issue's groomed context (linked spec, recorded decisions, acceptance criteria) or **explicitly delegated** to this thread with its boundary named. Draft a **just-in-time tactical plan** — scoped to this ticket, inside the delegated authority, recorded in the thread and reflected in the PR body; never a human gate — then follow `reference/implement.md`. If a strategic question turns out to be open, or implementation **invalidates** an approved decision, do not settle it here: record the finding on the issue and hand it back as `needs-spec` per step 2 — the work returns through the upstream shaping flow. There is no in-run planning approval gate.
   - **research** → invoke the **`research` skill** by name with the issue's question, intended downstream use, scope, known time/version boundary, and `docs/agents/researching.md`. Research owns framing, source work, any nested fan-out, claim reconciliation, the dossier, and its source audit. **Backlog retains the lifecycle**: branch, issue state, commit, PR, review, and closure stay in this thread. Accept the handoff only with the canonical dossier path, concise answer, material unknowns/contradictions, as-of boundary, and passing audit or explicit unresolved gap.
   - **draft** → produce-and-review, for judgment-terminal work whose correctness is taste/fit (a memo, copy, narrative synthesis, code docs). Produce the artifact — authoring staffed by the **`staffing`** skill (by name) — then present it for sign-off through the **`review-loop`** skill (by name); the human review verdict **is** the definition of done. **Keep** the artifact: commit it to the work branch (unlike `prototype`, which deletes its throwaway — draft keeps the thing it made). There is no plan/implement spine and no mechanical acceptance-criteria run — see step 4.
   - Any branch — not just enhancement — may hand a blocking design question to the `prototype` skill (by name); the branch's own reference states when — and only for questions **within the issue's delegated authority**. A strategic question is a `needs-spec` handback, never a prototype session.
   - Staffing: build-out — `implement.md`, `refactor.md`, and fix commits — runs on the **builder** role for its surface, resolved by the `staffing` skill (by name), dispatched out of this thread. Diagnosis is coordinator-owned and stays here; new judgment or hard-diagnosis uncertainty escalates through the recorded upward successor.
   - Completion criterion: the branch's own completion criterion is met, or the issue is handed back (`needs-info` / `needs-spec`).

4. Verify behavior → follow `reference/verify.md`.
   - This is a loop: verify runs the checks and exercises the change against its acceptance criteria, handing failures back to the branch that built the change (`implement.md`, `diagnose.md`, or `refactor.md`) until every criterion passes or it hits its cap.
   - Delegate the whole loop to a subagent filling the **checker** role, resolved by the `staffing` skill (by name); this thread stays coordinator and takes back any failure the subagent escalates per `verify.md`'s triggers.
   - **draft exception.** A `draft` has no testable spec, so this step is skipped — it degenerates to "the review gate passed": the `review-loop` verdict from step 3 stands in for verify. Correspondingly, step 6 adversarial review degenerates for a pure-prose artifact (the human verdict was the review); a code-docs draft keeps a light correctness pass over the docs it touches.
   - **research exception.** Research correctness is checked by the `research` skill's claim audit, not by product behavior checks. Accept that audit as this gate only when it accounts for every material claim and unresolved gap. If the issue also changes product behavior, it was misclassified: return it to grooming instead of quietly adding implementation to the research branch.
   - Completion criterion: every acceptance criterion passes, the research claim audit passes with every gap accounted for, or the verify-equivalent ends at its cap or an explicit blocker (reported, no PR opened).

5. Create the PR.
   - Open a ready-for-review PR, not a draft, via the change-review binding's open verb, once the branch's deliverable and verification-equivalent are complete. Target the base branch named in `docs/agents/environment.md`.
   - Build the body per `docs/agents/change-description.md`: it carries the close linkage from `platform.md` (GitHub: `Closes #<n>`; local: the issue file's `state` flips on this branch and closure rides the merge), the checks and per-criterion verification with the verify step's caveats, and an evidence placeholder — evidence is deferred to step 7. For research, link the dossier and record its claim-audit result instead of inserting that placeholder; the research exception in step 7 applies.
   - Completion criterion: a ready-for-review PR exists whose merge will close the issue per the binding's linkage.

6. Adversarial review → follow `reference/adversarial-review.md` against the new PR.
   - The verify loop (step 4) checks behavior against criteria; this loop reviews the diff for correctness and quality. If a fixer commit changes user-facing behavior, re-verify the affected criteria.
   - Completion criterion: review reaches `LGTM`, hits its iteration cap, or reports an explicit blocker.

7. Capture evidence → follow `reference/evidence.md`.
   - Runs once, after the review loop ends, against the branch's final HEAD; `reference/evidence.md` carries the timing rationale. Skip if the playbook requires no evidence beyond green checks. Delegate the capture to the **checker** role, resolved by the `staffing` skill (by name).
   - **Research exception.** The dossier's claim ledger, citations, and audit are intrinsic provenance, not a second evidence package. Keep the deliverable under the project research root and skip this step unless a separate acceptance criterion explicitly requires proof beyond the dossier; never copy research into `evidence/` merely because it is reviewed.
   - Commits after the Reviewer's `LGTM` may touch only `evidence/`, the review file, and — on the local binding — the issue file's closing flip: set `state: closed` on this branch now, so the merge carries closure to main per `platform.md`'s close linkage. Never product code, so the approval stays valid.
   - When evidence was required, replace the PR body's evidence placeholder with the verified ready-to-paste block via the binding's edit-body verb — do not rebuild or reformat the block. If a browser driver in `environment.md` can reach the review surface, eyeball the rendered body after the edit.
   - Completion criterion: the evidence is committed and published, and the PR body carries the verified block in place of the placeholder — or none is required.

8. Report back.
   - Send the run thread the issue id, work-type, branch, PR reference, checks, evidence, and review outcome — plus any tracker writes it must apply as the serialized main writer. Quote each acceptance criterion's verification grade verbatim (`live | static-substitute | not-run | blocked` per `reference/verify.md`); never flatten grades into an unqualified PASS.
   - Completion criterion: the run thread can update its handoff table without reading this whole thread.
