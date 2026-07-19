# Raw auditor reports (verbatim)

Five independent auditors, 2026-07-20, each briefed with the `writing-great-skills` yardstick and the
no-behavior-change constraint. Apply edits from these quotes; the synthesis is in `findings.md`.

---
---

# Report 1 — backlog

# Backlog skill verbosity audit

Yardstick: `writing-great-skills` SKILL.md + GLOSSARY.md. Lens: no-ops, duplication, sediment, sprawl, restatement→leading-word collapse. All proposals behavior-preserving unless marked RISKY. Word counts from `wc -w`.

A structural note that frames most findings: the references are loaded per-subcommand (progressive disclosure is already right), but the same rules were re-inlined at every site that *touches* them instead of at the one site that *owns* them. The five worst offenders — the resolved-scaffold-set algorithm, the parallelism asymmetry, the local-binding write discipline, the check-discovery contract, and the needs-info/needs-spec boundary — each exist at 3–5 sites.

## SKILL.md — 903 words

1. `[dedupe]` § References "`reference/` and `templates/` are bundled with this skill; `docs/agents/` is the target repo's playbook, created by `backlog setup`…" duplicates § Dependency surface items 1–2 ("Bundled references — … ship with the skill and are not looked for in the target repo" / "Project playbooks — `docs/agents/*.md`, installed into the target repo by `setup`"). → Keep § Dependency surface as SSOT; § References keeps only the unique sentences ("A subcommand's bundled reference is the **orchestration contract**…", the missing-playbook stop rule). Same three definitions survive once.
2. `[dedupe]` § Commands closing paragraph "Five capabilities are **composed by plain name**, never imported: `diagnosing-bugs` owns the bug method; `research` …; `staffing` …; `review-loop` …; `prototype` …" — the same five siblings with the same one-line ownerships reappear in § Dependency surface item 3 and in frontmatter `requires`. → Keep the Commands-paragraph version (it carries the ownership glosses the table needs); item 3 becomes "**Sibling skills** — the five named above, composed by plain name; `setup` ensures presence; absent one, state the requirement rather than failing silently." Every rule (ensured-by-setup, degrade-by-stating) survives.
3. `[dedupe]` § Seams "**A queue of one is a first-class invocation**: `backlog run <issue>` is the interactive chat-and-build shape — the same build loop, no waves." duplicates run.md's "A **queue of one** is a normal run: … interactive chat-and-build is this shape, not a separate mechanism." → run.md is SSOT (it executes the rule); Seams keeps only "a queue of one is first-class (`backlog run <issue>`)". Invocation shape still discoverable at the surface; contract lives where it runs.
4. `[dedupe]` § Seams "Its *inputs* vary by entryway — criteria from the ticket, the spec, or written at loop start; evidence obligation scaling with absence — the gates never do." The entryway list and the evidence-scaling rule are stated operationally in `templates/software/verifying.md` § Acceptance criteria. → Cut the em-dash parenthetical; keep "Its inputs vary by entryway; the gates never do." The operative enumeration lives in the playbook verify actually reads.
5. `[collapse]` § Seams groom bullet "The tracker as truth: admission audit, route judgment, serialized writes, the verify-first triage discipline. The only stage that stamps readiness." — "The only stage that stamps readiness" restates groom.md/policy's confirm-gate and run.md's never-stamps rule. → Keep it *here* as the one-line seam and treat the Seams line as the summary it is — no cut — but drop "the verify-first triage discipline" (names nothing any reference defines; sediment from an earlier design).
6. `[cut]` description, sentence 2: "Works against GitHub, a local on-disk tracker, or any bound platform." This is identity, and the skill is user-invoked (`disable-model-invocation: true`) — per the yardstick, a user-invoked description is a one-line human summary; platform-agnosticism is § References' "Nouns are roles" content. → DELETE sentence. No trigger branch depends on it. (No synonym-trigger problems otherwise: "groom" / "run" / "subcommands standalone" are distinct branches, one trigger each.)

Estimated after: ~770.

## reference/run.md — 1,815 words

1. `[dedupe]` Step 1 completion criterion, "Resolve the backlog set by overlaying `templates/common/` with the recorded work domain's pack … with same-name pack files shadowing common, then adding each same-name `templates/software/` baseline as a flagged stand-in … The required backlog-owned step names are `implementing`, `verifying`, `evidence`, `refactoring`, `change-reviewer`, and `change-fixer`; for `skill-authoring`, preflight therefore requires ten backlog-owned counterparts (three unshadowed common files, three native pack files, and four flagged software stand-ins)…" — the full scaffold-set algorithm + the ten-counterpart enumeration, restated verbatim from setup.md (where it appears twice more). → Replace with: "every playbook in the **resolved scaffold set** (`reference/setup.md` § step 2's definition, from the recorded work domain) has its `docs/agents/` counterpart, plus `docs/agents/diagnosing-bugs.md` and `docs/agents/researching.md`." Preflight still checks the identical set; the set is computed by one definition instead of three.
2. `[collapse]` Step 2 "`ready-for-agent` is the human's confirmation from grooming, so no further confirmation is needed before dispatch." + "Issues without `ready-for-agent` are not run — they have not been groomed and released". Rationales duplicate `backlog-policy.md`'s role definitions. → "Dispatch needs no further confirmation (`ready-for-agent` *is* the human's confirmation). Issues without it are not run." Both operative rules (don't re-ask; don't run unstamped) survive; the policy gloss goes.
3. `[collapse]` Step 2 "lacking work-type, surface, coordination class, or coordination reason — or, for an enhancement, the recorded route judgment —" → "lacking any dispatch-metadata field (`backlog-policy.md` § Dispatch metadata, incl. the enhancement route judgment)". The field list already lives in the policy section named; skip-don't-infer behavior unchanged.
4. `[dedupe]` Step 4 local bullet "commit any uncommitted groomed tracker state first, then commit the `in-flight` marks — worktrees fork from a commit, so this claim commit is the fork point and every work branch is born carrying its own issue marked `in-flight` (`platform.md` § The local binding)." Near-verbatim with platform.md § "Commit-before-fork". → "Local tracker binding: follow `platform.md` § Commit-before-fork; the claim commit is the fork point." platform.md (installed in every target repo) keeps the full mechanics.
5. `[dedupe]` Step 5 "apply pin → provider/fallback → eligible executor → taste gate → `intelligence > taste > cost`; never choose cheapest-first." This is the `staffing` skill's own ladder (verified present in `skills/system/staffing/SKILL.md` and its references), invoked by name in the same sentence. → "…invoke the `staffing` skill by name with … ; it applies its selection ladder — never cheapest-first." One guard word retained; algorithm has one home.
6. `[collapse]` Step 6 "clear `in-flight`, set the reported role (`needs-info` for missing information, `needs-spec` for unsettled or invalidated strategic decisions, `ready-for-human` for verify caps and blockers per `backlog-policy.md`)" — the three glosses duplicate the policy's role definitions. → "clear `in-flight`, set the reported role per `backlog-policy.md`, and commit the comment on main." Which role applies is decided by the reporting thread anyway; run just applies what's reported.
7. `[cut]` Liveness contract, "Status is a lookup, never an investigation." Nice line, but the preceding sentence already mandates heartbeats with phase/effect/next-event — this adds no new obligation. Borderline leading-sentence; if kept anywhere, keep here only. Weak-cut: DELETE.

Estimated after: ~1,540.

## reference/build-loop.md — 1,632 words

1. `[dedupe]` Liveness paragraph: "…bound by `reference/run.md` § Liveness contract — five-state reporting, no turn ends with live children/gates and no verified wake path (native harness notifications first; bounded foreground waits only where the harness cannot wake you), every wait recorded with owner/deadline/wake path." Everything after the em-dash restates the section it just cited. → "…bound by `reference/run.md` § Liveness contract. Terminal CI waits are the run thread's, not yours: report the PR and hand the CI watch up rather than parking here." The one thread-specific delta (CI handoff) survives; the contract has one home.
2. `[dedupe]` Tracker-write paragraph: "on the local binding, this thread writes only its own issue file, only on its own branch — lifecycle updates that should merge with the change (state flips, plan and review links). Writes that must reach the main branch without a merge — `needs-info`, blockers, clearing `in-flight` — are reported to the run thread, the serialized main writer, never committed here…" — near-verbatim restatement of platform.md § The local binding's write classes 2 and 3. → "Tracker write discipline: on the local binding, follow `platform.md` § The local binding's write classes — this thread commits only class-2 writes (its own issue file, own branch); class-3 abort writes go through the run thread. On live trackers (GitHub) write directly via the tracker verbs." Same partition, one definition.
3. `[dedupe]` Step 2: "`needs-info` means the reporter owes facts; `needs-spec` means the issue needs the upstream shaping flow (interview → spec → tickets) before any thread can own it." Duplicates `backlog-policy.md` § Label roles (`needs-spec`: "Boundary with `needs-info`: there the reporter owes facts; here the product owner owes shaping … cleared when the upstream shaping flow (interview → spec → tickets) delivers…"). Step 2 already tells the thread to read that playbook. → DELETE the boundary sentence; keep the two handback procedures (they are the step's actions). Routing decisions unchanged — the definitions still load with the policy playbook.
4. `[dedupe]` Step 3 enhancement: "the strategic decisions arrived settled: admission guarantees every product, design, and scope question is either resolved in the issue's groomed context (linked spec, recorded decisions, acceptance criteria) or **explicitly delegated** to this thread with its boundary named." This is groom.md step 3's `route: direct` definition restated. → "the strategic decisions arrived settled or delegated (groom's recorded `route: direct` judgment)." The thread's obligations (JIT plan, no human gate, needs-spec on open/invalidated questions) all remain verbatim.
5. `[collapse]` Step 3, four occurrences of "resolved by/staffed by the `staffing` skill (by name)" plus two more in steps 4 and 7. → State once at first use "roles resolve through the `staffing` skill (by name) throughout"; thereafter "fills the **builder** role", "the **checker** role". Same resolutions, one convention declaration.
6. `[collapse]` Step 3 draft: "(unlike `prototype`, which deletes its throwaway — draft keeps the thing it made)" — the keep-vs-throwaway contrast also lives in the policy's `draft` label and prototype's own description. → Keep "**Keep** the artifact: commit it to the work branch." and cut the parenthetical. The behavioral rule (commit it) is untouched.
7. `[RISKY]` Step 8 "Quote each acceptance criterion's verification grade verbatim (`live | static-substitute | not-run | blocked` per `reference/verify.md`); never flatten grades into an unqualified PASS." verify.md step 5 already says every report up the chain quotes grades verbatim — but the coordinator executing step 8 may never have loaded verify.md (the checker subagent did). Cutting could lose the rule exactly where it bites. Leave as-is.

Estimated after: ~1,440.

## reference/groom.md — 1,066 words

1. `[dedupe]` Step 1 orphan sweep: "an `in-flight` issue whose recorded branch no longer exists, or is quiet past the policy playbook's horizon, is surfaced to the human as a candidate reset per `backlog-policy.md` § In-flight hygiene — never reset silently." Near-verbatim with that policy section ("…is a corpse: `groom` surfaces it to the human as a candidate reset… Never silently reset — the branch may hold unmerged work."). → "Sweep for orphans while listing per `backlog-policy.md` § In-flight hygiene — never reset silently; a human-confirmed reset is applied here as a grooming write." Detection conditions live once, in the policy the step already cites.
2. `[dedupe]` Header "…it never edits an issue that is `in-flight` — a change for one goes through the run thread or waits (`platform.md` § The local binding) — with one exception: the human-confirmed orphan reset in step 1, safe because the claim is dead." AND step 1 "A reset the human confirms is applied here as a grooming write (on main, on the local binding) — the dead claim cannot race it." AND platform.md write class 1 carries the identical exception with the identical rationale. → platform.md § The local binding is SSOT for the write rule + exception; groom's header keeps the pointer, step 1 keeps the action (finding 1's wording), and both "safe because the claim is dead" rationales collapse to the platform.md one.
3. `[dedupe]` Header "Runs standalone (`backlog groom`) or as the first half of bare `backlog`, which grooms and then offers to run." The offer-to-run behavior is stated in SKILL.md routing rule 1 and again in step 6 ("As bare `backlog`, offer to run them; standalone, stop here"). → Header: "Runs standalone (`backlog groom`) or as the first half of bare `backlog`." Step 6 keeps the operative offer/stop split.
4. `[cut]` Header "The interactive pre-flight phase — the actual triage." — "the actual triage" adds nothing to "The interactive pre-flight phase"; and the next sentence already states outputs. → "The interactive pre-flight phase."
5. `[cut]` Step 3 "This judgment was formerly made mid-run by the plan gate; it happens only here now, so a dispatched run never pauses for planning approval." History is sediment; the load-bearing half ("a dispatched run never pauses for planning approval") already exists in build-loop step 3 ("There is no in-run planning approval gate") — which is the thread that would wrongly pause. → DELETE sentence.
6. `[collapse]` Step 2 "Propose `research` when the terminal deliverable is a source-backed account of what is known, inferred, contradicted, and unknown. Propose `draft` when correctness is instead judgment/taste — a memo, copy, or narrative synthesis." Duplicates the policy's fuller `research`/`draft` definitions and its "Recognizing the boundary" blockquote, which the step's first sentence already directs the groomer to read. → Cut both sentences; the policy blockquote is the routing rule and is written for exactly this decision.

Estimated after: ~940.

## reference/setup.md — 3,581 words (the sprawl center)

1. `[dedupe]` The **resolved scaffold set** algorithm appears in full twice — step 1 ("Resolve the **scaffold set** for that domain in two passes: overlay `templates/common/` with `templates/<domain>/` … The required backlog-owned step names are `implementing`, `verifying`, `evidence`, `refactoring`, `change-reviewer`, and `change-fixer`…") and step 2 ("Scaffolding and reconciliation draw from the **resolved scaffold set**: first overlay … The required backlog-owned step names are …") — plus a third partial restatement in step 2's "Missing-baseline degrade" bullet, plus run.md, plus `backlog-policy.md` § Work domain. → Define once (a short "Resolved scaffold set" definition block above step 1, or in step 1); step 2 says "draw from the resolved scaffold set (step 1)"; the degrade bullet keeps only its genuinely new content (the flag-line requirement, the never-leave-uninstalled rule, report gaps). Identical set computed everywhere; ~150 words gone and a four-site maintenance hazard closed.
2. `[dedupe]` The skill-authoring counterpart count — "ten counterparts: three unshadowed common files, three native pack files, and four flagged software stand-ins" — appears in step 1's completion criterion, step 2's completion criterion, and run.md step 1. → State once, in the same scaffold-set definition ("for `skill-authoring` the set resolves to ten backlog-owned files: …"); both completion criteria say "all counterparts of the resolved set". Same check, one enumeration.
3. `[dedupe]` Step 3 wrapper contract: "a watched native wrapper named for the external model/task, staffed by the cheapest native model allowed by the floor, supervising a bounded non-interactive command and returning raw output plus lifecycle status without synthesis. The parent verifies the effect. Record the spawn request or child metadata that proves wrapper staffing; if the harness cannot select or report it, … mark floor/cost compliance unproven." Near-verbatim with `templates/common/platform.md` § Harness (the create-verb slot text + "Wrapper staffing evidence" slot). → Setup keeps the action: "For each sibling-harness dispatch, bind and smoke-test the wrapper contract per `platform.md` § Harness, and record the wrapper-staffing evidence its slot names." The contract text lives in the artifact setup writes.
4. `[dedupe]` Step 3 dependency relation: "GitHub reads `.issue_dependencies_summary` and writes `dependencies/blocked_by` using the blocker's numeric issue id; local uses `deps` frontmatter." — the exact commands are already the shipped defaults in platform.md's tracker-verb slots; and the surrounding discover-before-fallback rule is restated in platform.md § Custom bindings ("Discover a **native dependency relation** before choosing a fallback; bind and exercise its read/write verbs … record the explicit fallback … never an intended or fabricated command presented as verified"). → Setup keeps "Discover the tracker's native dependency relation, exercise read and write, record per `platform.md` (shipped defaults for GitHub/local; § Custom bindings otherwise)." All verbs, probes-with-throwaways, and the no-fabrication rule survive — the command text once.
5. `[dedupe]` Step 4 vs `reference/worktree-isolation.md`: (a) the asymmetry rule ("a preference to serialize is always honored … `parallel-safe` is *never* granted by preference alone … Preference can only tighten toward serialize; only the list can license parallel") restates worktree-isolation § Parallelism verdict + § shared-singleton list; (b) "A greenfield repo with no stack yields an empty list honestly; a real app never does" ≈ the list section's "An empty list is a real result for a greenfield repo…; a real application never produces one"; (c) the row schema and example enumeration ("the database, host ports, `node_modules`/install dirs, build caches, test databases, a cloud deployment or auth tenant — each with its collision mode and whether local namespacing can isolate it") restates the probes + list sections; (d) "this is a **hard constraint, not a preference**: with the list's singletons shared, a parallel fan-out would corrupt shared state" restates the verdict section's hard-constraint paragraph; (e) the serialized-exception-lane example list ("destructive operations on a shared tenant, real third-party endpoints without per-worktree credentials, features needing deliberately distinct users") appears verbatim in worktree-isolation *and* the environment template. → worktree-isolation.md is SSOT for all five. Step 4 becomes: ask the intent; run the probes and record the list per `worktree-isolation.md` § shared-singleton list; derive the verdict per its § Parallelism verdict (asymmetric — the list licenses parallel, preference only serializes); the three parallel-intent sub-outcomes stay (already-isolated / offer scaffold with approval / cloud-singleton explain-and-note-manual-path) since those are setup *actions*; agree and record the exception lane per its definition. Every gate and outcome survives; ~200 words gone.
6. `[dedupe]` Step 5 check discovery vs `templates/software/verifying.md` § Checks — near-verbatim twins ("Judge the invocation, not the exit code… a command that runs but reports failures is still recorded… record it with its baseline status… Omit only a command that does not exist…", both with the same source-enumeration list). → Setup.md is SSOT (setup performs the discovery); the template's blockquote compresses to: "Discovered and invocation-verified by `backlog setup` (its step 5 contract): verified verbatim commands only; a currently-red command is still recorded with its baseline status." `verify` at runtime needs only the recorded commands + the red-is-still-the-gate posture, which survives.
7. `[dedupe]` Step 5 CI gate "Record it as a distinct gate: `verify`'s local checks prove the change, but the PR cannot merge until this CI gate is green" duplicates verifying.md § CI merge gate's "Local checks prove the change; CI-green is the merge condition — neither substitutes for the other." → Keep the template's (runtime-read) version; setup says "Discover the CI merge-gate from the CI config and record it in `verifying.md` § CI merge gate."
8. `[dedupe]` Step 6 driver bullets duplicate `templates/common/environment.md` § Driving the app's driver-per-surface defaults (isolated `agent-browser`, user-session carve-out with per-use consent, Computer-Use gate, driver-failure-is-a-blocker-never-a-downgrade). → The installed playbook is the runtime SSOT (verify/evidence read it); setup step 6 keeps the setup-time actions — confirm a working driver per surface, obtain the Computer-Use approval *at setup*, help set up what's missing, record blockers — and points at the template's defaults instead of re-listing them. All gates survive in the file that binds at runtime.
9. `[dedupe]` Step 6 verification-data inventory list ("standing accounts/tenants and permissions; largest feasible real scale; any plan-approved synthetic substitute …; collision-safe per-issue fixture names; fixture retention through final evidence; and the named owner/command for cleanup") mirrors environment.md § Verification data's rows. → "Inventory verification data now, not during verify — fill every row of `environment.md` § Verification data; record absent affordances as blockers rather than inventing them." Same exhaustiveness bar (every row), one schema.
10. `[dedupe]` Step 9: (a) the long re-enumeration of environment.md contents duplicates the template's own section headings → "Record steps 4–6's results into the named sections of `environment.md`"; (b) "`environment.md` § Presenting is a pointer the `review-loop` skill fills…; § Model staffing is the `staffing` skill's roster… — backlog does not write either here" triplicates steps 7–8 and the template's own ownership blockquotes → DELETE from step 9 (steps 7–8 keep it); (c) "Record the **verified check commands and the CI merge-gate** from step 5 in `verifying.md`" — keep (it's the write instruction).
11. `[cut]` Step 3 label provisioning: "creation is an upsert, not an approval gate — cheap and reversible" — the sentence before already says create-what's-missing and the sentence after says report; "cheap and reversible" argues rather than instructs. Weak-cut: keep "creation is an upsert, not an approval gate", drop "— cheap and reversible".

Estimated after: ~2,850.

## reference/worktree-isolation.md — 1,296 words

1. `[dedupe]` § shared-singleton list: "The list *gates* the parallelism verdict below asymmetrically: a `parallel-safe` verdict must be backed by a list with no un-isolated collision (a parallel verdict without a clear list behind it is unverified), while `serialize-verification` may equally be a plain user preference to serialize — the list is what licenses parallel, not what forbids serialize." — restated ~40 lines later by § Parallelism verdict's own bullets ("Never granted by preference alone" / "or the user simply chose to serialize") plus its hard-constraint paragraph. → List section keeps one clause: "The list gates the verdict (§ Parallelism verdict)." The asymmetry lives once, in the verdict section that defines the verdict.
2. `[collapse]` § Parallelism verdict hard-constraint paragraph: "…so a parallel fan-out that ignores it corrupts shared state (interleaved DB writes, clobbered build artifacts, a mid-run install pulled out from under a running check). A user preference for parallel does not override a shared datastore or a shared build cache —" The example triple restates three probe rows from § Audit probes. → "…so a parallel fan-out that ignores it corrupts shared state (see the probes' collision modes). Preference does not override the list —". Constraint, asymmetry, and the two routes to parallel-safe all survive.
3. `[cut]` Intro "Do not impose a scheme blindly. First classify the regime, then detect whether the repo already solves it, then — only with approval — scaffold." — the second sentence is the file's own section order restated; the approval gate is stated again at § Scaffold pattern ("write only with explicit approval"). → Keep "Do not impose a scheme blindly." Delete the itinerary sentence.

Estimated after: ~1,200.

## reference/run-state.md — 476 words

Tight; the densest file in the skill. One finding:

1. `[cut]` "A stale or missing board is never canonical." — the preceding sentence already defines the board as a projection rebuilt from streams; "never canonical" is entailed. Weak-cut; defensible to keep as the operative warning. Verdict: keep (a projection being non-canonical when stale is exactly the mistake a resuming agent makes; this line changes behavior). No cuts proposed.

## reference/verify.md — 558 words

1. `[collapse]` § Staffing "the role and its fallback ladder are resolved by the `staffing` skill (by name)" — the "(by name)"/"fallback ladder" boilerplate recurs across implement/refactor/evidence/adversarial-review; within this file it is fine once. Cross-file: see the global note below; no in-file cut.
2. `[dedupe]` Step 2 "Create missing fixtures with the playbook's unique per-issue names before the loop and retain them through final evidence." — retention duplicates environment.md § Verification data's lifetime row, but this is the executing instruction and the playbook is repo-tuned data; keep. No cut.
3. `[cut]` § Loop step 5 "— and every report up the chain quotes the grade verbatim" vs build-loop step 8: intentional two-actor coverage (see build-loop RISKY item). Keep.

This file is near its floor. Estimated after: ~550.

## reference/evidence.md — 394 words

1. `[cut]` "Never run it on a change that has not passed verification; the point is to prove to a human that the criteria are met, so capturing a half-working state defeats it." First clause is already entailed by the Target line ("a branch whose behavior `reference/verify.md` has confirmed"); the rationale clause is exposition. → Keep "Never run it on a change that has not passed verification." Delete the rationale. (Half-sentence cut, ~20 words.)
2. `[dedupe]` § Styling-only reuse vs `templates/software/evidence.md` and `change-reviewer.md` — see the templates below; this reference is the SSOT and keeps its paragraph unchanged.

Estimated after: ~375.

## reference/adversarial-review.md — 386 words

1. `[RISKY]` § Behavior ruling vs `templates/software/change-reviewer.md` § How to comment (final bullet): near-verbatim overlap on the Reviewer's half ("stops without editing… sends the question plus evidence to the issue coordinator… review that new HEAD yourself; do not invent behavior"). But the two files load into different contexts — this reference into the orchestrating thread (and it alone carries the coordinator's and Fixer's halves), the playbook into the Reviewer subagent, which may never see this file. Cutting either side risks the rule vanishing from one actor's context. Leave both; if one must go, trim the Reviewer-playbook bullet to its actor-local imperative and keep the full protocol here.
2. `[cut]` § Roles Reviewer "Audits the PR per its playbook and leaves comments" — "and leaves comments" is entailed by everything around it; trivial. Not worth an edit on its own. No standalone cuts proposed.

Estimated after: ~385.

## reference/implement.md — 251 · reference/refactor.md — 184 · reference/diagnose.md — 307

1. `[dedupe]` implement.md and refactor.md open with the identical sentence: "Staffing: build-out fills the **builder** role for its surface, resolved by the `staffing` skill (by name); in the loop, the issue thread dispatches it rather than building in its own context." — also stated in build-loop step 3's staffing bullet. Each file runs standalone, so per-file presence is licensed; but build-loop step 3's version ("Staffing: build-out — `implement.md`, `refactor.md`, and fix commits — runs on the **builder** role…") is the duplicate *in the loop context*, where both files are loaded. → Keep the per-file lines (standalone contract); trim build-loop's bullet to the parts the branch files don't carry: "Diagnosis is coordinator-owned and stays here; new judgment or hard-diagnosis uncertainty escalates through the recorded upward successor." Builder-role dispatch survives in the two files that execute it.
2. `[cut]` diagnose.md "Do not restate or edit its six-phase method here." — this instructs the *file's* reader not to do something the file already doesn't do; as a runtime guard against re-deriving the method inline it has some bite, but the preceding sentence ("invoke the **`diagnosing-bugs`** sibling by name") already assigns the method wholesale. Weak-cut: DELETE.
3. diagnose.md's guarded-direct-fix lane is dense and all load-bearing (entry facts, one-guess cap, contradictory-observation exit) — no cuts.

Estimated after: ~245 / 184 / 295.

## templates/common/backlog-policy.md — 1,289 words

1. `[dedupe]` § Work domain "Playbooks resolve from `templates/common/` overlaid by `templates/<domain>/`, then same-name `templates/software/` stand-ins for any required step the domain pack omits." — fourth statement of the scaffold-set algorithm. The installed repo never resolves templates; only `setup` and `run`'s preflight do, and both hold the skill's references. → Replace with "Playbooks resolve per the skill's `reference/setup.md` (the resolved scaffold set)." The next bullet's stand-in explanation ("those step playbooks are `software` baselines standing in, each flagged…") is repo-facing context for a human reading a flagged file — keep.
2. `[dedupe]` § Label roles `research`: "The dossier is kept under the project's research root; its citations are intrinsic provenance, not an `evidence/` copy." — loop-step behavior (build-loop step 7's research exception owns it), not routing information; a groomer never acts on it. → DELETE the sentence from the label definition; keep the epistemic-terminal definition and the claim-audit clause (those route).
3. `[dedupe]` § Label roles `draft`: "…no mechanical `verify` pass/fail. The artifact is **kept** (committed and merged), unlike `prototype`, which is throwaway — keep the answer, delete the artifact." — same status: build-loop step 3/4 owns the kept-artifact and skipped-verify mechanics. → Keep "the definition of done is the **human review verdict** at the review gate" (that *is* routing-relevant — it defines judgment-terminal); cut the kept-vs-prototype tail. RISKY-lite: a groomer distinguishing `draft` from `prototype`-worthy work might lean on that contrast — but `prototype` is not a work-type in this taxonomy, so no routing branch uses it. Proceed.
4. `[collapse]` § In-flight hygiene "applied optimistically — the loop accepts the rare duplicate pickup in the window between queue build and marking rather than carrying a lock. `run` re-reads each issue immediately before marking it and skips any that changed." Second sentence duplicates run.md step 4's claim procedure (which cites this section for the accept-the-residue posture). → Policy keeps the posture ("optimistic claim; no lock; rare duplicate accepted"); run.md keeps the procedure (re-read before marking). Cut the policy's procedural sentence.

Estimated after: ~1,200.

## templates/common/platform.md — 1,447 words

1. `[cut]` § The local binding note "> Applies only when the tracker binding is `local`. This is the full contract; the verbs above summarize it." — declared summary/contract split; this is deliberate architecture, and both layers are read by different passes (verb slots by executing steps, the contract by setup/groom/run). Keep as-is — this file is the SSOT several other files should defer to (see run.md 4, build-loop 2, groom 2), so it *gains* status in this audit rather than losing words.
2. `[dedupe]` § Custom bindings final sentences ("Discover a **native dependency relation** before choosing a fallback; bind and exercise its read/write verbs so `run` can form dependency waves…") — twin of setup step 3 (resolved there in setup's favor of *this* file: setup points here). Keep here.
3. `[cut]` Tracker verb "Duplicate links: recorded per `backlog-policy.md` § Dependencies." — pure pointer to a pointer; the policy's § Dependencies already names the convention slot. Weak-cut: DELETE the row (setup fills slots from the policy anyway). ~8 words.

Estimated after: ~1,435. (Net: this file mostly absorbs SSOT status.)

## templates/common/environment.md — 1,017 words

1. `[dedupe]` § Parallelism verdict "— gated by the shared-singleton list above, asymmetrically: `parallel-safe` requires a list with no un-isolated collision; `serialize-verification` may come from that list (a hard constraint) or from a plain preference to serialize." and the "If serialized, why" gloss "(…a hard constraint, since a parallel fan-out would corrupt that shared state)". The asymmetry governs *setup's derivation*, and setup holds worktree-isolation.md; `run` only reads the verdict value. → Verdict row: "Verdict: _<parallel-safe | serialize-verification>_ — derived by `setup` from the shared-singleton list (`reference/worktree-isolation.md` § Parallelism verdict)." "If serialized, why" keeps its two fill options minus the argumentative parenthetical. Behavior identical: the deriving agent still has the full rule loaded.
2. `[dedupe]` § Driving the app driver row — the long default gloss ("**agent-browser with an isolated profile** … user-session carve-out, with per-use consent … Computer Use gate … A driver failure surfaces as a blocker; it never falls back to a less-isolated surface") — counterpart of setup step 6. Per the setup finding, this installed file is the *runtime* SSOT (verify/evidence read it), so it keeps the gates; setup defers here. No cut in this file; the pair is resolved in its favor.
3. `[dedupe]` § Serialized exception lane example list "destructive shared-tenant operations, real third-party endpoints, deliberately distinct users" — third occurrence (worktree-isolation, setup, here). Here it's fill-guidance inside a placeholder; harmless but third. → Trim to "_<issue classes that must serialize even when parallel-safe (see `worktree-isolation.md`); or "none">_".

Estimated after: ~960.

## templates/common/change-description.md — 349 words

1. `[collapse]` CI-status row "The PR is a merge candidate only once CI passes; a red or pending gate is disclosed here, not omitted." First clause duplicates verifying.md § CI merge gate's merge precondition; the disclosure rule is this file's own. → "the host CI merge-gate (`verifying.md` § CI merge gate) and whether it is green — a red or pending gate is disclosed, not omitted. Where there is no CI, say so." ~10 words; precondition survives at its SSOT.

Estimated after: ~340.

## templates/software/implementing.md — 771 words

Dense, high-quality shipped default; the TDD content is all behavioral. Two small items:

1. `[dedupe]` "A skipped test is a stated decision, recorded in the seam agreement below — not an omission." vs § Build test-first "…and the surfaces deliberately left untested, with why — and record both against the plan." Same recording rule twice in one file. → Keep the § Build test-first version (it's the procedure); the § What deserves a test sentence becomes "A skipped test is a stated decision, not an omission." (drops the duplicate recording clause).
2. `[cut]` "Defer to `CLAUDE.md` / linters / formatters in this repo for style." — arguably a no-op (agents defer to repo tooling by default), but it anchors the adjacent fill-slot ("Anything not captured by tooling…"). Keep.

Estimated after: ~760.

## templates/software/verifying.md — 550 words

1. `[dedupe]` § Checks blockquote-style intro — near-verbatim twin of setup step 5 (see setup finding 6; resolved in setup's favor). → Compress to: "Run narrowest-first, then broaden by touched surface. Discovered and invocation-verified by `backlog setup` (verbatim, seen-to-run commands only; a currently-red command is still the real gate — recorded with its baseline status, never blanked; a stack-dependent check is confirmed with the stack up). Do not record a guessed command." All runtime-relevant posture survives; the discovery-source enumeration lives in setup. ~45 words saved.
2. § Acceptance criteria — SSOT for the entryway/evidence-scaling rule (SKILL.md § Seams defers here per that file's finding 4). Keep unchanged.

Estimated after: ~505.

## templates/software/evidence.md — 1,028 words

1. `[dedupe]` "Captured once, after adversarial review converges, each artifact mapped to the acceptance criterion it proves. Styling-only verification captures may be reused only when their HEAD is the final reviewed HEAD and the Reviewer records **"no product-code change; no recapture"**; product-code, fixture, environment, or HEAD drift forces fresh final-HEAD evidence." — both sentences restate `reference/evidence.md` (timing + the § Styling-only reuse paragraph), and the evidence step always loads both files together. → Replace the paragraph with: "Timing and styling-only reuse follow `reference/evidence.md` (capture after review converges; reuse only under its Reviewer-confirmed exception)." The reviewer-side wording stays in change-reviewer.md (different actor/context — see below). ~40 words.
2. The GitHub-binding mechanics (camo/raw/SHA rules, mechanical checks) are unique, empirically earned content — no cuts. The § Presentation intro sentence "a click-through link defeats the evidence" duplicates reference/evidence.md gate 3's "click-through links fail this gate" — `[collapse]`: keep one per file is defensible (different altitude); weak-keep.

Estimated after: ~985.

## templates/software/change-reviewer.md — 987 words

1. `[collapse]` § Be ambitious remedies: "Preferred remedies point the same direction: delete a layer of indirection rather than polishing it; reframe the state model so conditionals disappear; extract the helper or split the file; move logic behind the abstraction that owns it; reuse the canonical utility." — last two clauses restate blockers 3–4's own remedies ("the logic wants a dedicated abstraction…", "push code to the layer that already owns the concept"). → Trim to the first three clauses. Direction preserved; per-blocker remedies keep their homes.
2. `[RISKY]` § Also scrutinize bullet 1 ("Open every test, fixture, document, or probe cited as criterion coverage; confirm it exists and exercises the claimed runtime seam") duplicates verify.md § Loop step 1 — but as deliberate defense-in-depth across two different actors (checker, then Reviewer). Cutting removes the Reviewer's independent re-check: behavior change. Keep.
3. `[RISKY]` § How to comment final bullet (product-semantics ruling) vs adversarial-review.md § Behavior ruling — see that file's finding 1. Keep.
4. `[RISKY]` § Approval bar's styling-reuse verdict sentence — third statement of the reuse rule, but the Reviewer subagent plausibly loads only this playbook, and the Reviewer is the actor who must *utter* the exact verdict string. Keep.

Estimated after: ~970.

## templates/software/change-fixer.md — 148 · refactoring.md — 300

Both tight. refactoring.md: no cuts — every line binds (unmodified-tests rule, no-behavior+structure commits, no-seam and no-logic branches). change-fixer.md: no cuts.

## templates/skill-authoring/ — environment.md 524 · evidence.md 409 · verifying.md 326

1. `[collapse]` environment.md § Worktree isolation regime "**local-isolatable** — checked-in skill files and stdlib-only scripts are isolated by the worktree unless the repository records an external shared resource below." — fine; no cut.
2. `[dedupe]` evidence.md "An uncited executor summary or a screenshot without the keyed behavioral verdict is not sufficient proof of a skill decision." partially restates verifying.md's citation requirement ("Require citations to the file and exact sentence deciding every answer… grade every probe against every prewritten criterion") — but verify and evidence are different steps with different loaders; the evidence-side bar is its own gate. Keep.
3. `[cut]` verifying.md § Checks "not quiz questions or instructions to drive an app" — the negative examples earn their place against the known failure mode (inventing an app for a skills repo). Keep. No cuts proposed in this pack beyond: evidence.md "If review changed behavior, reverify the affected criteria first." duplicates build-loop step 6's re-verify rule — but this pack installs into repos where the evidence step runs standalone too. Keep.

Estimated after: unchanged (~1,259 total).

## Global cross-file duplication ledger (single sources of truth)

| Rule | SSOT | Sites to reduce to pointers |
|---|---|---|
| Resolved scaffold set + required-step names + skill-authoring counts | `reference/setup.md` (define once, step 1) | setup step 2, setup degrade bullet (partial), `reference/run.md` step 1, `templates/common/backlog-policy.md` § Work domain |
| Parallelism asymmetry, empty-list-is-honest, exception-lane examples | `reference/worktree-isolation.md` § Parallelism verdict / § list | setup step 4 (×4 restatements), worktree-isolation § list (in-file), `templates/common/environment.md` § Parallelism verdict |
| Local-binding write classes, orphan-reset exception, commit-before-fork | `templates/common/platform.md` § The local binding | `reference/build-loop.md` write paragraph, `reference/run.md` steps 4 & 6, `reference/groom.md` header + step 1 |
| Check discovery ("judge the invocation", red-suite rule, source list) | `reference/setup.md` step 5 | `templates/software/verifying.md` § Checks intro |
| needs-info / needs-spec boundary + role glosses | `templates/common/backlog-policy.md` § Label roles | `reference/build-loop.md` step 2, `reference/run.md` step 6 |
| Liveness contract | `reference/run.md` § Liveness contract | `reference/build-loop.md` liveness paragraph (keep only the CI-handoff delta) |
| Styling-only evidence reuse | `reference/evidence.md` | `templates/software/evidence.md` (reviewer playbook keeps its actor-local verdict string — RISKY to cut) |
| Wrapper/sibling-harness dispatch contract | `templates/common/platform.md` § Harness | `reference/setup.md` step 3 |
| Staffing selection ladder | `staffing` sibling skill | `reference/run.md` step 5 |
| Route-judgment / "settled or delegated" definition | `reference/groom.md` step 3 (+ policy § Dispatch metadata) | `reference/build-loop.md` step 3 enhancement preamble |

Deliberate duplication to **keep** (different actors, disjoint contexts): per-reference "playbook missing → report setup gap and stop"; per-branch "Standalone with a PR intended: continue to…"; verify-vs-reviewer artifact-opening check; behavior-ruling protocol in both adversarial-review.md and change-reviewer.md; grade-quoting in both verify.md and build-loop step 8.

## Totals

- **Now:** 21,994 words across SKILL.md + 13 reference + 13 template files.
- **Estimated after:** ~20,000 words (≈ 1,900–2,000 cut, ~9%). The cut concentrates in `setup.md` (−~730), `run.md` (−~275), `build-loop.md` (−~190), with the rest spread thin — most leaf files (run-state, refactor, change-fixer, the skill-authoring pack) are already near their floor.

## Five highest-value edits

1. **Define "resolved scaffold set" once in `reference/setup.md`** and point to it from setup step 2, run.md step 1's preflight criterion, and backlog-policy § Work domain. Largest single dedupe (~350 words across four sites) and it closes a live maintenance hazard: the required-step list and the skill-authoring "ten counterparts" arithmetic currently must be edited in lockstep at four places.
2. **Make `worktree-isolation.md` § Parallelism verdict the sole home of the preference/list asymmetry** (and the exception-lane examples, and empty-list-is-honest), collapsing setup step 4's four restatements and the environment template's gloss (~250 words). The rule is subtle enough that five slightly-different phrasings *invite* drift in exactly the place a wrong verdict corrupts shared state.
3. **Make `platform.md` § The local binding the SSOT for tracker-write discipline** — build-loop's write paragraph, run.md's claim-commit bullet and step-6 role glosses, and groom's doubled orphan-exception all become one-clause pointers (~170 words). Every writer already loads platform.md, so nothing leaves any actor's context.
4. **Collapse the setup↔template twins**: check discovery (setup step 5 keeps it; verifying.md § Checks compresses), driver gates (environment.md keeps it; setup step 6 compresses), wrapper contract and dependency relation (platform.md keeps both; setup step 3 compresses), verification-data inventory (environment.md rows; setup points) (~300 words across setup + two templates).
5. **Strip build-loop's re-inlined definitions** — the liveness parenthetical, the needs-info/needs-spec boundary, the "strategic decisions arrived settled" definition, the draft/prototype contrast (~130 words). Build-loop is the file pasted into every issue-thread prompt, so these tokens are paid on every dispatched issue — the highest per-word runtime cost in the skill.

---
---

# Report 2 — shaping trio (interview, domain-modeling, interview-with-docs)

# Skill-prose verbosity audit — interview / domain-modeling / interview-with-docs

Yardstick: `writing-great-skills` (no-ops, duplication, sediment, sprawl, single source of truth, leading-word collapse, description = triggers only, one trigger per branch). All proposals behavior-preserving unless tagged RISKY.

## 1. `skills/thinking/interview/SKILL.md` — 766 words

1. **[collapse]** description: `"about an idea, problem, or direction until shared understanding is real"` → `"about an idea or problem until shared understanding is real"` — "direction" is a third synonym for the same single branch (the argument-hint already names the intake shapes); one trigger per branch.
2. **[cut]** description: `"— batch frontier rounds, facts looked up not asked, recommendations offered as hypotheses"` → DELETE — pure identity/mechanics already authoritative in the body (§ Rounds, § Facts); the yardstick says descriptions keep triggers, not method summaries, and no user prompt will contain "batch frontier rounds".
3. **[dedupe]** intro: `"The session is done when the frontier is empty, coverage holds, and the user confirms — not when the conversation feels aligned."` → DELETE — § Stopping states both tests, the confirmation, and `"'We feel aligned' is the sign-off, never the test"` verbatim-in-meaning; § Stopping stays the single source, so every gate survives.
4. **[collapse]** § Intake: `"**Provided artifacts are read, not asked about**: a question whose answer is in the material is never put to the user."` → `"**Provided artifacts are read, not asked about.**"` — the clause after the colon restates the bolded rule, and § Facts already carries `"Never ask the user for anything you could find"`.
5. **[cut]** § Rounds: `"Early frontiers are naturally small; if one balloons past comfortable answering, split it"` → `"If a round balloons past comfortable answering, split it"` — "early frontiers are naturally small" is exposition, changes no behavior.
6. **[RISKY]** § Rounds: `"— a cap is manners, not a rule."` — reads as restating the split rule, but it actively forbids the model from inventing a fixed question cap; cutting could change behavior. Keep unless an eval shows otherwise.
7. **[collapse]** § Rounds: `"labelled as provisional, never presented as a default the user is nudged to accept"` → `"labelled provisional, never a nudged default"` — same two obligations (provisional label; no default-nudging), telegraphic.
8. **[RISKY]** § Rounds: `"Questions whose answers depend on another question still open in this round belong to a later round."` — formally implied by the frontier definition (prerequisite unsettled ⇒ not frontier), but it guards the specific intra-round failure of asking both at once; deleting risks that failure returning.
9. **[collapse]** § Exit: `"This skill records nothing durable: settled terms and decisions live in the conversation and the playback."` → `"This skill records nothing durable."` — the second clause restates the first from the other side.
10. **[dedupe]** § Exit: `"run `interview-with-docs`, which composes this skill with `domain-modeling` so the useful shape is written the moment it crystallises."` → `"run `interview-with-docs`."` — the composer's identity lives in the composer's own description and body; the sibling pointer alone preserves the routing behavior.

Estimated after: ~685.

## 2. `skills/thinking/domain-modeling/`

### SKILL.md — 516 words

1. **[cut]** description: `"— challenge terms against the glossary, stress-test with concrete scenarios, and write CONTEXT.md entries and ADRs the moment they crystallise"` → DELETE — verbatim identity of § During the session; description keeps its three genuine triggers ("pinning down domain terminology", "recording an architectural decision", "another skill needs the model maintained") plus the negative trigger, so invocation is unchanged. (Also `"Build and sharpen"` → `"Sharpen"` — synonym pair, one verb suffices.)
2. **[dedupe]** intro: `"This is the *active* discipline — challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. Consuming `CONTEXT.md` for vocabulary is not this skill; this skill is for when the model is *changing*."` → `"This is the *active* discipline: for when the model is *changing*, not merely consumed."` — the gerund list previews § During the session word-for-word, and the anti-scope already lives in the description's "Not for merely reading CONTEXT.md"; § During the session remains the single source of every rule.
3. **[dedupe]** intro: `"…owning one: `interview-with-docs` composes it with `interview`; a groom session, spec session, or triage thread may invoke it directly when terms or decisions are moving."` → end the sentence at `"owning one."` — the caller roster is the description's reach clause `"(interview-with-docs, groom, a spec session)"`; "when terms or decisions are moving" restates "model is changing".
4. **[dedupe]** § Where the model lives: `"(`0001-slug.md`, `0002-slug.md`, …)"` → DELETE — numbering is `adr-format.md`'s content (stated there twice: header line and § Numbering), and the pointer to that file sits two lines below.
5. **[collapse]** § During the session: `"**Write inline, never batch.** A resolved term goes into `CONTEXT.md` right then."` → `"**Write inline, never batch** — a resolved term goes into `CONTEXT.md` before the conversation moves on."` or simply drop the second sentence — it restates the bolded rule.
6. **[dedupe]** § ADRs: `"An ADR can be a single paragraph; the value is recording *that* and *why*, not filling out sections."` → DELETE — stated verbatim in `adr-format.md` ("That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why* — not in filling out sections."), which is the format file's job; keep `"Any gate failing → no ADR."`
7. **[RISKY]** § During the session: `"— no implementation details, no spec content, no scratch notes"` elaborates `"a glossary and nothing else"`; the enumeration guards three distinct temptations, so I would keep it.

Estimated after: ~415.

### reference/context-format.md — 338 words

1. **[collapse]** § Rules: `"Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs."` → DELETE — the preceding sentence (`"General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively."`) already is the rule; this is the same test rephrased as self-talk.
2. **[dedupe]** § Single vs multi-context: `"The skill infers which structure applies: - If `CONTEXT-MAP.md` exists… - If only a root `CONTEXT.md` exists… - If neither exists, create a root `CONTEXT.md` lazily… When multiple contexts exist, infer which one the current topic relates to. If unclear, ask."` → DELETE all of it — every rule (structure inference, context inference, ask-when-unclear, lazy creation) is stated in SKILL.md § Where the model lives, which is the right home since it's needed every run before this file is even opened; this file keeps only the two structure examples, its actual format content.
3. (Aside, not verbosity: the `**Order**` entry in the Structure example holds a placeholder while its siblings hold concrete definitions — inconsistent template, flagged for the author, no proposal.)

Estimated after: ~260.

### reference/adr-format.md — 443 words

1. **[dedupe]** `"Create the `docs/adr/` directory lazily — only when the first ADR is needed."` → DELETE — SKILL.md's `"No `docs/adr/`? Create it when the first ADR is needed."` is the live, every-run copy of this rule.
2. **[dedupe]** § When to offer an ADR: the entire three-gate block — `"All three of these must be true: 1. **Hard to reverse** … 2. **Surprising without context** … 3. **The result of a real trade-off** …"` → DELETE — duplicated (with drifted wording: "costs something real" vs "is meaningful" — classic two-sources drift) in SKILL.md § ADRs — offer sparingly, which must hold the gates since they decide *whether* to offer before this file is ever opened. Replace the section header's body with one pointer line ("The three gates are in SKILL.md; below, what typically passes them.") and promote `### What qualifies` to carry the section.
3. **[collapse]** same section: `"If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond 'we did the obvious thing.'"` → DELETE — three sentences that each re-argue one gate; pure restatement, no rule or edge case lost.
4. Keep: Template, "That's it…" (single source after SKILL.md edit 6), Optional sections, Numbering, What qualifies — all live, unduplicated format reference.

Estimated after: ~335.

## 3. `skills/thinking/interview-with-docs/SKILL.md` — 205 words

1. **[cut]** description: `"— so nothing settled evaporates with the conversation"` → DELETE — rationale restating "writes the useful shape down as it goes" and the trigger "should outlive the session"; both triggers ("outlive the session…", "use bare `interview` when…") survive intact.
2. **[dedupe]** body: `"The interview asks; domain-modeling extracts **inline, the moment things crystallise** — terms into `CONTEXT.md`, decisions passing the three-gate test into ADRs, never batched to the end."` → `"The interview asks; `domain-modeling` extracts as it crystallises."` — inline/never-batch, terms→CONTEXT.md, and the three-gate test are all the sibling's own authoritative rules (§ During the session, § ADRs); the composer should point, not restate, and `requires: [domain-modeling]` guarantees the sibling is present. This is the file's clearest composer-restates-sibling violation.
3. **[dedupe]** `"the interview's open-thread classification (settled / delegated / deferred / blocking)"` → `"the interview's open-thread classification"` — the taxonomy is defined in `interview` § Exit, a required sibling; the parenthetical is a second source that will drift.
4. **[cut]** `"— so downstream synthesis (`to-spec`, `to-tickets`) reads crystallised artifacts plus classified threads, not memory"` → DELETE — rationale for the preceding rule ("written where the caller directs — an issue comment, a spec's Notes"), which alone carries the behavior.
5. **[cut]** `"Both siblings are composed **by name**."` → DELETE — frontmatter `requires:` plus the degrade sentence that follows already encode this; the sentence adds no instruction either sibling-present or sibling-absent.

Estimated after: ~155.

## Totals

- Now: **2,268 words** across the five audited files (766 + 516 + 338 + 443 + 205; evals/README/licenses excluded per scope).
- Estimated after all non-RISKY proposals: **~1,850 words** (roughly −18%).

## Five highest-value edits

1. **adr-format.md — delete the duplicated three-gate section** (dedupe #2 + #3): ~90 words, removes the trio's largest duplication, and the two copies have already drifted in wording — living proof of the maintenance cost.
2. **context-format.md — delete the inference/lazy-creation rules** (dedupe #2): ~55 words; SKILL.md § Where the model lives is the every-run single source, leaving the reference file purely format.
3. **Both mechanics-summary description cuts** (interview #2, domain-modeling #1): ~30 words, but these sit in the always-loaded context window — highest value per word in the whole audit.
4. **domain-modeling intro collapse** (SKILL.md #2 + #3): ~48 words of the § During the session bullets and the description's caller roster previewed before the reader reaches either single source.
5. **interview-with-docs composer restatement** (#2): only ~16 words, but it fixes the exact cross-skill failure the audit was asked to catch — the composer restating a required sibling's rules, creating a third copy of the three-gate test.

---
---

# Report 3 — formation (to-spec, to-tickets, merge-changes)

# Skill-prose audit — to-spec, to-tickets, merge-changes

Yardstick: `.agents/skills/writing-great-skills/` (SKILL.md + GLOSSARY.md). All targets are user-invoked (`disable-model-invocation: true`), which matters twice: per the yardstick their descriptions should be "a one-line summary, trigger lists stripped," and description edits are guaranteed behavior-neutral (the agent never sees them). The dominant pattern across all three skills is **SKILL.md restating its own reference files nearly verbatim** — the "the shape" summaries have sedimented into full second copies of the method. Since each SKILL.md *orders* the reference loaded ("Load [synthesis]…", "Load [slicing]…"), the reference file is the single source of truth and the summary steps can collapse to headline + pointer.

## 1. skills/delivery/to-spec/

### SKILL.md — 1,018 words

1. `[collapse]` Description: "…Use when closing out a conversation that reached a decision. Not for eliciting requirements." → DELETE both sentences. User-invoked: description is human-facing, triggers stripped per yardstick; "Not for eliciting requirements" is a synonym of "Pure synthesis, no interview" already in the same description. Zero behavior impact — the model never loads this description.
2. `[cut]` "A long back-and-forth with the agent ends with a direction settled but nothing durable to hand off; the next step — splitting that direction into pickup-able work — has nothing to read. To-spec closes that gap." → DELETE. Motivational exposition; the preceding bolded sentence already states the move, no rule lives here.
3. `[dedupe]` "It is a synthesis primitive, not an interviewer." → DELETE. Restates "pure synthesis, no interview" that opens the very next paragraph.
4. `[dedupe]` "Shipped as our own — no external skill is installed for this." → DELETE. Machine truth already in frontmatter (`requires: []`, no `metadata.external`); provenance belongs in README per repo convention. (Same sentence appears in to-tickets SKILL.md — cross-skill boilerplate.)
5. `[cut]` "This is the only command; invoked bare, it runs the synthesis." → DELETE. One bullet in the surface = only command; "with no name, derive…" already covers bare invocation. No-op.
6. `[dedupe]` Step 1: "When the conversation ran through the `interview` / `interview-with-docs` siblings, their crystallised artifacts — `CONTEXT.md` terms, ADRs, the exit classification of open threads — are the primary inputs: synthesis reads the record, not memory alone." → "Start from the interview record when one exists (synthesis § What to mine)." Full text lives verbatim in synthesis.md § What to mine, which is force-loaded.
7. `[dedupe]` Step 3: "Skip this entirely for non-dev specs." → DELETE. Step 2 already says a non-dev spec "skips both"; synthesis.md says it a third time ("For a non-dev spec this step does not run at all").
8. `[collapse]` Step 6, from "There is no separate plan stage…" through "…`to-tickets` wires the slice tickets to it." → "Sign-off — the direction's approval gate. User present: approve inline. AFK: serve via the optional `review-loop` sibling. On approval: commit and project the thin tracking ticket (synthesis § Sign-off)." Every clause (no plan stage, just-in-time tactics, review-ready-as-is, tracker-bound thin ticket, links-and-state-never-content) survives verbatim in synthesis.md § Sign-off.
9. `[dedupe]` Bullet "The artifact is a repo doc…": "It is coarser than a plan: a plan is per-ticket and gated for approval before implementation; a spec is the pre-ticket direction the tickets are cut from." → DELETE clause. Same comparison lives in template-guide § Order and altitude (SSOT for altitude).
10. `[collapse]` Bullet "No file paths or code snippets." full text ("They rot as the codebase moves… Everything else is prose.") → "**No file paths or code snippets** — sole exception the prototype-validated snippet (synthesis § No stale content)." The complete rule, including the exception's scope and the "note it came from a prototype" requirement, lives in synthesis.md § No stale content.
11. `[collapse]` Dependency surface, bundled-refs parentheticals "(the no-interview synthesis method, dev-vs-non-dev gating, the seams step, the no-stale-content rule, and sign-off)" and "(what each section holds and which are dev-only)" → DELETE. The "Load [synthesis]…" line under § Command surface already carries these same enumerations — keep that copy, since it's the one that fires the load.
12. `[dedupe]` Sibling-skills bullet: "the spec is already a self-contained review-ready HTML with stable element ids, so it serves as-is. When the user is present, approval is inline." → DELETE clauses. Third statement of both facts (step 6 and synthesis § Sign-off carry them); keep only "optional `review-loop`; not a hard dependency — skipping it still produces a valid, committed spec."

### reference/synthesis.md — 1,052 words

13. `[cut]` "To-spec's job is to write the spec a conversation already earned, not to run a fresh requirements pass. This file is the method." → "The method." First sentence restates SKILL.md's opening move; § The one rule immediately below carries the content.
14. `[dedupe]` "Notes are not free-floating: at publish time each one is classified **blocking / delegated / deferred** (§ Sign-off), because a spec whose material Notes are unclassified cannot feed execution-ready tickets." → DELETE. The classification requirement and the feed-gate both live in § Sign-off (and the classification *definitions* live only in SKILL.md step 5 — keep those). Forward-stated gate = duplication.
15. `[cut]` "The one thing to-spec never produces is an interview." → DELETE. Third restatement of the section's own heading rule within the same section.
16. `[cut]` "(Adapted from Matt Pocock's `to-spec`, shipped as our own.)" → DELETE. Repo convention: credits live in README, never in skill content. Pure convention fix, no behavior.
17. `[dedupe]` "For a non-dev spec this step does not run at all." → DELETE. § Classify already commands the skip (see item 7).
18. `[dedupe]` "use only the core sections (Problem, Solution, User stories, Implementation decisions, Out of scope, Notes)" → "use only the core sections (template-guide)". Template-guide is the section SSOT; two enumerations will drift.
19. `[dedupe]` "Don't invent testing prose to fill a heading that doesn't apply." → DELETE here. Template-guide § Dev-only says the same ("Don't manufacture prose to fill a heading that doesn't apply") at the point where sections are defined — keep that copy.
20. `[RISKY]` "Capture the decision, not a survey of options that were discussed and dropped." duplicates template-guide's "Decisions, not a survey of discarded options." One could go — but one guards *mining*, the other guards *writing the section*, and both files load; flagging rather than proposing, since attention at both moments may be intended.

### reference/template-guide.md — 413 words

21. `[dedupe]` Intro: "— a self-contained HTML deliverable with stable element ids, same house style as a plan;" → DELETE clause. Stated in SKILL.md step 4 and synthesis § Naming (the SSOT for the artifact contract); this file's job is section contents only.
22. `[dedupe]` § Order and altitude: "a spec is coarser than a plan (which is per-ticket and gated for approval before implementation)" — keep here as the SSOT, but note the parenthetical describes the **retired** plan stage as if live. `[RISKY]` to reword (legacy plans are still an accepted to-tickets input), but "gated for approval before implementation" contradicts synthesis's "the lifecycle has no separate plan stage" — sediment; suggest "(the retired per-ticket stage)" if touched at all.

## 2. skills/delivery/to-tickets/

### SKILL.md — 1,104 words

23. `[collapse]` Description: "Use to turn direction into pickup-able tickets." → DELETE. Synonym trigger — restates the opening clause "Split a decided direction … into backlog-ready … tickets" (one trigger per branch); and the skill is user-invoked, so triggers do no work anyway. Keep "Not for writing the direction itself — that's to-spec" (genuine disambiguation) or drop it too — either is behavior-neutral.
24. `[cut]` "A spec captures direction but nothing pickup-able; someone still has to cut it into tracer-bullet tickets, order them, and wire the dependencies by hand. To-tickets automates that split — the consumer half of the discussion → work bridge that `to-spec` opens." → DELETE. Exposition; the bolded move sentence and the numbered steps carry every rule.
25. `[dedupe]` "Shipped as our own — no external skill is installed for this." → DELETE (same as item 4).
26. `[dedupe]` "And unlike `to-spec` (pure synthesis, no interview), to-tickets **does** interview: the quiz on granularity and blocking edges is the human-confirmation step, and nothing publishes before it is approved." → DELETE. slicing.md § Quiz opens with the identical contrast and carries the publish gate; step 3 states the gate a third time.
27. `[cut]` "This is the only command; invoked bare, it runs the split." → DELETE (same as item 5).
28. `[collapse]` Load-line parenthetical "(what to read, the vertical-slice default, the wide-refactor exception, the quiz, dependency ordering and backlog's edge convention, the readiness default, the no-stale-content and never-modify-parent rules)" — keep this copy; DELETE the dependency-surface bullet's mirror "(the split method)" plus scaffold re-listing (item 35). One enumeration home.
29. `[dedupe]` Step 3: "Iterate until approved. Nothing publishes before approval." → DELETE. Stated in ¶2 (now cut per item 26) and, authoritatively, in slicing § Quiz ("**nothing publishes before it is approved**"); the step heading "the human-confirmation step" preserves the gate's presence in the step list.
30. `[collapse]` Step 3b, from "Before publishing, every ticket carries…" through "…never published thin." → "3b. **Audit each ticket for readiness** (slicing § Audit) — a ticket failing the audit is fixed or dropped, never published thin." All five criteria (observable acceptance, inherited context links, authority boundary, UX context, true edges) are duplicated bullet-for-bullet in slicing § Audit each ticket for readiness. Highest-drift duplication in the three skills.
31. `[collapse]` Step 4, from "Wire each edge **exactly as the repo's recorded convention**…" through "…skips blocked work." → "Wire each edge exactly as the repo's recorded convention (slicing § Order and wire)." Native-relation-vs-body-marker, playbook citation, platform verbs, and the `backlog run` consumer all live verbatim in slicing.
32. `[collapse]` Step 5, from "blockers first, in generic 'ticket' vocabulary — **never as local files while a live tracker is bound**…" through "…(Matt's posture)." → "blockers first, per slicing § Publish; readiness stays with `backlog groom` (slicing § Readiness alignment)." Every clause (local-files ban, local-binding exception, tracking-ticket link, groom default, apply-on-approval option) is duplicated in slicing §§ Publish / Readiness. Also strips "(Matt's posture)" — attribution banned from skill content by repo convention.
33. `[dedupe]` Bullet "A tracer bullet, not a task list": "— sequenced expand→migrate-in-batches→contract instead of forced into a slice" → DELETE clause; step 2 already names the sequence and slicing § wide-refactor holds the full rule with its two-condition trigger.
34. `[collapse]` Bullet "No file paths or code snippets." full text → "**No file paths or code snippets** — sole exception the prototype-validated snippet (slicing § No stale content)." (Mirror of item 10.)
35. `[collapse]` Bullet "The parent is never touched.": "To-tickets reads the spec or parent issue; it never edits it. The source of truth is preserved." → DELETE sentences, keep the bolded header + pointer. slicing § Read carries the identical sentences.
36. `[dedupe]` Dependency surface: "These come from the repo, not from the `backlog` skill's files: to-tickets emits **into** backlog's convention, it does not import backlog." → DELETE. slicing § Order and wire states it ("The convention is a **project playbook**, not a `backlog` import: to-tickets emits *into* it, so the playbook's wording is the authority") — keep that copy, it sits where the edge gets written.

### reference/slicing.md — 1,324 words

37. `[cut]` Header: "This file is the method. It imports no other skill's files; the tracker and dependency conventions it names are read from the repo's project playbooks, not from another skill." → DELETE second sentence. The dependency surface in SKILL.md is the declared home for import/playbook provenance; restated again in § Order and wire.
38. `[dedupe]` § Publish: "— but the skill's own text stays generic: a **ticket** is the tracker's issue role in a tracker-agnostic word." → DELETE. Verbatim duplicate of § Vocabulary two sections down (and of SKILL.md bullet 2).
39. `[cut]` § Vocabulary: "(\"Ticket\" == \"issue,\" same role — worth standardizing the repo on eventually, not required here.)" → DELETE. Authoring-time aside to a future maintainer — sediment, no runtime rule.
40. `[cut]` § Readiness: "Matt Pocock's posture is that" → DELETE attribution; keep the rule: "…**Note the option** to apply readiness on approval — the quiz *is* the human confirmation, so a user who wants it may bless the tickets on the spot —". Credits-in-README convention; rule text unchanged.
41. `[dedupe]` § Read, spec bullet: "This is the contract path; a repo may record a different specs location in its `docs/agents/`, honor it when present." — keep here as SSOT; nothing to cut in this file, but note SKILL.md's dependency-surface "A repo may record a different specs location or dependency convention; honor it when present" is the duplicate → DELETE that SKILL.md sentence (the playbook bullets above it already say the playbooks govern).

### reference/template-guide.md — 527 words

42. `[dedupe]` § Order and altitude: "Publish order is the topological sort of the edge list — blockers first — so each `depends on #N` resolves to a real, earlier id." → DELETE. Verbatim content of slicing § Order and wire and SKILL.md step 6's readback criterion; this file's remit is field contents.
43. `[dedupe]` Depends-on field: "These are what `backlog run` reads to skip blocked work." → DELETE. Fifth statement of this fact (SKILL step 4, dep surface, slicing § Order and wire, ticket.md comment); keep slicing's.
44. `[dedupe]` Source field: "; never edited by to-tickets" → DELETE. Fourth home of never-modify-parent; slicing § Read is SSOT and tickets.md's inline "never modified by to-tickets" already guards the fill-in moment.
45. `[RISKY]` "coarser than a plan (which is per-ticket and gated before implementation)" — same retired-stage sediment as item 22; flag, don't cut.

### templates/ticket.md — 205 words

46. `[dedupe]` Header comment: "One ticket = one tracer bullet: a narrow-but-complete path through every layer, demoable on its own, sized to one fresh context window. Not a horizontal layer. No file paths or code (prototype-validated snippet excepted)." → "One tracer bullet — see reference/template-guide.md for each field." The definition lives in slicing (method) and template-guide (fields) — a third full copy in the scaffold is drift surface. Keep the operational comments (VERBATIM edge copying, omit-for-root, work-type) — those fire at fill-in time and aren't restated at that grain elsewhere. `[RISKY]` only if the template is ever filled without the guide loaded; SKILL.md's Load line makes the guide mandatory, so behavior holds.

### templates/tickets.md — 275 words

47. `[dedupe]` Header comment, "Revise it against their feedback on granularity and blocking edges; re-present until approved. Only then publish, blockers first, turning local Tn labels into tracker ids and the edge list into `- [ ] depends on #N` lines copied verbatim from the repo's dependency playbook." → "Revise through the quiz; publish only after approval (slicing § Quiz, § Order and wire)." The Tn→id and verbatim-form mechanics are restated in this same file's Edge-list comment (line 32) — keep that copy, it sits beside the edges.

## 3. skills/delivery/merge-changes/ — SKILL.md, 482 words

Already close to the yardstick's shape (flat reference + steps, single home for most rules). Three findings:

48. `[collapse]` Description: "Merge reviewed, review-ready changes on the user's explicit request — verify readiness, order dependent PRs, merge, reconcile, and report. Invoking this skill is the merge approval gate; backlog and every implementation loop stop at review-ready PRs and never merge. Not for reviewing changes or building them." → "Merge review-ready changes on the user's explicit request — the merge approval gate that backlog and every implementation loop stop short of." "reviewed, review-ready" is a synonym pair; the verb chain restates the Steps; the gate sentence survives (it's the description's one real job); user-invoked, so no invocation behavior at stake.
49. `[dedupe]` Boundaries: "; never interpret lifecycle labels, green checks, or reviewer approval as a merge request." → DELETE clause, keep "Never merge outside the request's scope." Paragraph 1 states the identical rule with a wider enumeration ("Automated review approval, green checks, `ready-for-agent`, or a reviewer's `LGTM` … are never authorization to merge") — keep that copy, it's the more complete one.
50. `[cut]` Boundaries, staffing bullet: "the whole flow is judgment-light coordination —" → optional micro-trim; the operative rules ("stays with the invoking session; delegate nothing but mechanical check-watching") stand alone. Marginal — skip if in doubt.

## Totals

| File | Now | Est. after |
|---|---|---|
| to-spec/SKILL.md | 1,018 | ~700 |
| to-spec/reference/synthesis.md | 1,052 | ~950 |
| to-spec/reference/template-guide.md | 413 | ~385 |
| to-tickets/SKILL.md | 1,104 | ~700 |
| to-tickets/reference/slicing.md | 1,324 | ~1,245 |
| to-tickets/reference/template-guide.md | 527 | ~475 |
| to-tickets/templates/ticket.md | 205 | ~175 |
| to-tickets/templates/tickets.md | 275 | ~250 |
| merge-changes/SKILL.md | 482 | ~445 |
| **Total** | **6,400** | **~5,325 (−17%)** |

## Five highest-value edits

1. **Item 30** — collapse to-tickets step 3b's full readiness-audit restatement to a pointer. Two parallel five-bullet lists of publish-gate criteria is the worst drift risk in the set; slicing § Audit becomes the sole gate text.
2. **Item 8** — collapse to-spec step 6's sign-off/on-approval block. The approval gate, the no-plan-stage rule, and the thin-tracking-ticket projection each currently have two full homes; synthesis § Sign-off becomes the only one.
3. **Items 10 + 34** — the no-stale-content rule (paths/snippets ban + prototype exception) currently has four near-verbatim homes across the two skills; reduce to one per skill (the reference file), leaving a bolded one-line pointer in each SKILL.md.
4. **Items 31 + 32** — collapse to-tickets steps 4–5's edge-wiring and publish mechanics, which duplicate slicing §§ Order-and-wire/Publish/Readiness clause for clause (~90 words) — and the playbook-citation text is exactly where a future convention change would otherwise have to be edited twice.
5. **Items 16, 32, 40** — strip the three external attributions ("Adapted from Matt Pocock's `to-spec`…", "(Matt's posture)", "Matt Pocock's posture is that") from skill content. Smallest word count but the only findings that are outright convention violations (credits live in README), and each is a clean delete with the rule text untouched.

One cross-skill note: the two `reference/template-guide.md` files do **not** duplicate each other's content (one covers spec sections, the other ticket fields) — but they share a structurally identical "Order and altitude" closer whose "plan (per-ticket and gated…)" parenthetical is retired-stage sediment in both (items 22, 45); since skills are self-contained by convention, this can't be deduped across skills, only fixed in parallel.

---
---

# Report 4 — probes (prototype, research, diagnosing-bugs)

# Skill-Prose Verbosity Audit

Yardstick: `.agents/skills/writing-great-skills/SKILL.md` + `GLOSSARY.md`. Read-only; no files touched. Word counts via `wc -w`. All proposals preserve every rule, gate, criterion, ordering, and edge case; cross-file dedupes rely on the fact that each reference file is loaded unconditionally on the default command (prototype's SKILL.md says "Load prototyping…" for every run; research loads the contract before "every gate"; diagnosing-bugs loads diagnosis.md for the default command), so a rule moved to its single source of truth is still in context on every run.

## 1. prototype (1,548 words: SKILL.md 294, reference/prototyping.md 1,254)

### skills/delivery/prototype/SKILL.md — 294 words

1. `[collapse]` Description: "Answer one design question with a throwaway artifact, then throw it away — keep the answer, delete the scaffolding." → "Answer one design question with a throwaway artifact — keep the answer, delete the scaffolding." The discard is stated three times ("throwaway", "throw it away", "delete the scaffolding"); two survive, so the trigger and rule are intact.
2. `[collapse]` Description: "settle a state model, layout, UI, or document direction with real alternatives rather than argument" → "settle a state model, UI, or document direction with real alternatives". "layout"/"UI" are synonym triggers for the single form-shape branch, and "rather than argument" restates what "real alternatives" already means; one trigger per branch survives.
3. `[RISKY]` Description: "Usable anywhere, not only dev." Candidate cut — identity already carried by the reference's intro and by the "document direction" trigger — but it may be doing invocation work on non-dev prompts. Flagging rather than proposing.
4. `[dedupe]` Gate 3: "The prototype itself is never the record." → DELETE. Verbatim duplicate of reference/prototyping.md § Capture and cleanup; the gate already requires writing "into the caller's durable record", and the reference (always loaded) keeps the rule.
5. `[dedupe]` "Missing project placement uses a self-contained scratch/workspace artifact." → DELETE. Duplicate of the reference's fuller rule ("Absent a playbook: a self-contained file in a scratch/workspace directory, outside any shipped artifact"), which is the stronger single source. (Keep the adjacent `review-loop`/`staffing` degrade clauses — those are the composer-declares-and-degrades surface and are *not* the same condition as the reference's no-surface fallback.)
6. `[collapse]` Dependency surface: "invoked by name with no file imports" → "invoked by name". "No file imports" is a design fact with no runtime effect — there are no imports to refrain from.

### skills/delivery/prototype/reference/prototyping.md — 1,254 words

1. `[dedupe]` Intro: "The bundled, authoritative technique for the `prototype` skill. This is what makes the skill usable anywhere — a codebase, a document, a design surface, with or without a project playbook." → DELETE. Pure identity, already established by SKILL.md which loaded this file; the paragraph's live content (playbook = "where", this file = "how", fallback rule) survives in the remaining sentences.
2. `[dedupe]` Para 2: "A prototype is a **throwaway artifact that answers one design question.** The answer is the only deliverable." and "Throwaway from day one: keep the answer, delete the artifact." → DELETE both; keep only the medium sentence ("The medium is usually code, but it need not be — …"). The definition duplicates SKILL.md's opener and the description; "Throwaway from day one" is restated as the first Rules bullet, which survives.
3. `[cut]` "— getting this wrong wastes the whole prototype" → DELETE. Motivational no-op; the rule "The question decides the shape" stands.
4. `[cut]` Rules: "No one should have to remember a path." → DELETE. Rationale for a rule already stated exactly ("One command to run, or one URL to open").
5. `[cut]` Rules: "Learn fast, then delete." → DELETE. Restates throwaway; "Skip the polish. No tests, no error handling beyond runnable, no abstractions." carries all the behavior.
6. `[cut]` Behavior shape: "The point is identical: drive the idea through cases until it either holds or breaks." → DELETE. Restates the shape's italic purpose line; the non-code mechanics (state table, scenario run) stand alone.
7. `[cut]` Form shape: "either way the human flips between real alternatives, not descriptions of them" → DELETE. Restates the form-shape definition from § Pick the shape ("flipped between so a human can react to real alternatives").
8. `[collapse]` Review-loop: "serve the rendered artifact / variant sheet so the answer arrives as annotated feedback rather than prose in chat, and end the pause with…" → "serve the rendered artifact / variant sheet, and end the pause with…". The "so…" clause is rationale; serving via review-loop and the URL requirement are unchanged.
9. `[dedupe]` Staffing: "Framing the question and reading the answer is orchestrator work and stays with the invoking thread." → DELETE. Duplicate of SKILL.md § Entry ("The invoking thread keeps framing and interpretation; dispatch build-out through `staffing route`…").
10. `[cut]` Staffing: "Don't hand-wave the routing; ask staffing." → DELETE. Restates the immediately preceding dispatch rule ("dispatched to the builder the **`staffing`** skill resolves").
11. `[cut]` Capture: "so the decision record outlives the prototype" → DELETE. Rationale; the capture mechanics (screenshot/sheet per variant, winner marked) are unchanged.
12. `[cut]` Cleanup: "Nothing throwaway stays." → DELETE. Restates "Then delete." plus the enumerated dispositions, which cover every case (losing variants, switcher, winner, module).

## 2. research (1,809 words: SKILL.md 580, reference/research-contract.md 883, reference/setup.md 162, templates/researching.md 184)

### skills/thinking/research/SKILL.md — 580 words

1. `[collapse]` Description: "produce a cited, auditable dossier that separates facts and observations from supported inferences" → "produce a cited, auditable dossier". The separation rule is identity already bound by gate 4 and the contract's claim ledger; triggers unchanged.
2. `[collapse]` Description: "investigate a topic, compare authoritative sources, establish current facts, audit a claim" → "investigate a topic, establish current facts, or audit a claim". "Compare authoritative sources" is a synonym of the investigate branch (comparison is the method, not a distinct entry); "establish current facts" (recency) and "audit a claim" stay as genuinely distinct triggers.
3. `[dedupe]` Gate 2: "…use `staffing route` for workers, preserve capacity for synthesis, and assign one coordinator as the only dossier writer. A caller that already runs issues in parallel does not forbid nested fan-out; it reduces the available worker budget." → "…use `staffing route` for workers per the contract's parallel rules." All three rules live verbatim-strength in the contract § Parallel research ("Reserve at least one execution slot for the coordinator/synthesizer"; coordinator owns the "final file" and workers "never concurrently edit the canonical dossier"; "When the caller is already parallel, choose the inner fan-out from the remaining capacity"). Completion criterion unchanged.
4. `[dedupe]` Gate 3: "Work from primary sources: official specifications and documentation, source code and commit history, first-party APIs and records, or raw datasets. Use secondary sources and search results to discover primary material, never as silent substitutes." → "Work from primary sources per the contract's source hierarchy." The source list is contract § Source hierarchy item 1; the discovery-aids rule is its "discovery aids, not support" sentence. "Record each material finding as a cited claim packet" and the completion criterion stay.
5. `[dedupe]` Gate 4: "surface contradictions instead of voting them away" → "surface contradictions". The no-majority-vote rule is the contract's "Do not resolve conflicting sources by majority vote."
6. `[dedupe]` Gate 5: "Lead with the answer, then facts and observations, inferences, contradictions, unknowns, method, and source index. Keep recommendations separate and include them only when requested." → "Follow the contract's dossier order." The eight-item order is contract § Dossier order; the recommendations rule is the ledger's "Recommendations are downstream judgments: keep them outside the ledger unless the user explicitly asks…". Completion criterion unchanged.
7. `[dedupe]` Gate 6: "Run the contract's claim audit, using an independent challenger when the work was parallelized or the decision is consequential." → "Run the contract's claim audit." The contract's challenger condition is strictly broader ("consequential conclusions, weak-source claims, or multi-shard work"), so deferring cannot weaken the gate. "Repair failures; never downgrade an unsupported assertion…" stays — it is unique.

### skills/thinking/research/reference/research-contract.md — 883 words

No cuts proposed. The file is the single source of truth the SKILL.md dedupes lean on; its audit checklist intentionally restates rules (that is the checklist mechanism, not duplication). The scope sentence ("Apply this contract to local code/document research…") is behavior-bearing — it stops citation rigor from being read as web-only.

### skills/thinking/research/reference/setup.md — 162 words

1. `[dedupe]` Step 2: "Default durable general research to `research/<slug>/`; record any project override explicitly." → "Record any project override of the default root explicitly." The default root is already stated in the pre-filled template bullet *and* the contract's fallback ("Without one, create a durable dossier under `research/<lowercase-hyphenated-slug>/`") — three statements of one default; contract + template suffice.
2. `[dedupe]` Step 4: "Re-running setup with unchanged facts must produce no diff." → DELETE. Same meaning as the completion criterion's "an immediate rerun is idempotent" in the same file.
3. `[cut]` "…or place a research deliverable in `evidence/`." → DELETE clause. Setup only writes the playbook, so this cannot fire during setup; the evidence boundary is owned by the contract's Artifact section, loaded on every research run.

### skills/thinking/research/templates/researching.md — 184 words

1. `[dedupe]` "Evidence boundary: research deliverables remain under the research root even when reviewed; `evidence/` is reserved for criterion-linked proof of a separate completed change." → DELETE bullet. Near-verbatim duplicate of the contract's Artifact section, which is loaded alongside the playbook on every run; the bullet is method, and the template's own header says to keep "only this repo's … bindings here."

## 3. diagnosing-bugs (1,181 words: SKILL.md 269, reference/diagnosis.md 565, reference/setup.md 143, templates/ 83 + 121)

### skills/delivery/diagnosing-bugs/SKILL.md — 269 words

1. `[collapse]` Description: "Use when a defect is broken, failing, throwing, flaky, slow, or assigned for diagnosis…" → "Use when a defect is failing, flaky, slow, or assigned for diagnosis…". "Broken / failing / throwing" are three synonym triggers for the one failing-defect branch; "flaky" (nondeterminism) and "slow" (perf) are the genuinely distinct branches and stay.
2. `[dedupe]` Contract: "If no red-capable loop can be built, stop with what was tried and the concrete access, artifact, or temporary instrumentation needed. Do not replace a missing signal with a theory." → DELETE. Near-verbatim duplicate of diagnosis.md phase 1 ("If no such loop is possible, stop. List what was tried and request the missing reproducing environment, captured artifact, or permission for temporary instrumentation. Do not hypothesize without a loop."), which is loaded on every default run and fires at the exact moment the rule applies; the caller still receives the stop-report because phase 1 mandates producing it.
3. `[RISKY]` Contract item 3 ("the fix, regression proof at the correct seam or an explicit no-seam finding, and the original loop green") is near-verbatim with phase 5's gate. Flagged, not proposed: the Contract list is the caller-facing interface visible without loading diagnosis.md, so cutting either side could change what a composing workflow reads as the return spec.

### skills/delivery/diagnosing-bugs/reference/diagnosis.md — 565 words

No cuts proposed. Every phase is instruction + gate with no restatement between phases; the phase-6 "Done" line is the required gate form, not duplication. This file is what the yardstick's telegraphic ideal looks like.

### skills/delivery/diagnosing-bugs/reference/setup.md — 143 words

1. `[dedupe]` Step 4: "Re-running setup with unchanged facts must produce no diff." → DELETE. Same meaning as the completion criterion's "an immediate rerun is idempotent" in the same file (identical pattern to research setup).

### skills/delivery/diagnosing-bugs/templates/diagnosing-bugs.md — 83 words

No findings; all placeholders plus a live ownership header.

### skills/delivery/diagnosing-bugs/templates/skill-authoring/diagnosing-bugs.md — 121 words

1. `[dedupe]` "Known model-dependent surfaces: preserve cited transcripts, repeat the same scenario, and report reproduction rate when one run is nondeterministic." → "Known model-dependent surfaces: preserve cited transcripts; nondeterministic runs follow the bundled flaky-bug rule." Repetition and reproduction-rate reporting are phase 1's flaky rule ("raise and record the reproduction rate with repetition…"), loaded on every run; the domain delta (transcripts) survives, and the template's own header says to keep only deltas.

## Totals

- **Now:** 4,538 words across the nine audited markdown files (prototype 1,548; research 1,809; diagnosing-bugs 1,181).
- **Estimated after:** ~4,120 words (prototype ~1,350; research ~1,645; diagnosing-bugs ~1,125) — roughly a 9% reduction, concentrated where duplication crosses the SKILL.md/reference boundary. The dominant pattern across all three skills: gates/contracts in SKILL.md re-inlining rules their always-loaded reference already owns.

## Five highest-value edits

1. **research/SKILL.md gate 3** — replace the inlined source list + discovery-aids rule with a pointer to the contract's source hierarchy. Kills the largest exact cross-file duplication in the set.
2. **research/SKILL.md gate 2** — defer coordinator/capacity/nested-fan-out mechanics to the contract's parallel rules. Three rules currently maintained in two places each.
3. **prototype/reference/prototyping.md intro** — delete the two identity paragraphs' restatements (~75 words) that duplicate the SKILL.md that just loaded the file.
4. **diagnosing-bugs/SKILL.md stop paragraph** — delete; phase 1 owns the near-verbatim rule at the moment it fires.
5. **diagnosing-bugs description trigger collapse** — "broken, failing, throwing" → "failing". Smallest edit, but descriptions pay context load on every turn of every session, so synonym triggers there are the most expensive duplication per word.

---
---

# Report 5 — services + UX (review-loop, staffing, setup-asher-skills, bare-minimum-ux)

# Skill-prose verbosity audit

Yardstick loaded (`writing-great-skills` SKILL + GLOSSARY). All findings are behavior-preserving unless tagged RISKY. In-scope total: **15,619 words**.

## 1. `skills/system/review-loop/` — 4,546 words

### SKILL.md — 342 words

1. `[collapse]` Description: "Present a rendered HTML artifact — a plan, prototype, maquette, or doc — to a human for sign-off, and block until a verdict. Use to serve an artifact for review, await the verdict, or sweep dead hub entries — directly or from a sibling skill that needs a sign-off gate. Not for writing the artifact." → "Present a rendered HTML artifact for human sign-off and block until the verdict; also sweeps dead hub entries. Not for writing the artifact." — Skill is `disable-model-invocation: true`, so per yardstick the description is human-facing: trigger lists are dead weight, and "present…for sign-off"/"serve…for review" and "block until a verdict"/"await the verdict" are synonym pairs naming one branch twice. Invisible to the agent, so zero behavior change.
2. `[dedupe]` "It never authors the artifact." duplicates the description's "Not for writing the artifact." SSOT: the body line (agent-facing). DELETE from description or body — keep one.
3. `[dedupe]` serve command: "Return only after the detached worker passes its authenticated identity check; its lifetime is independent of this turn and any watcher." — third statement of the serve lifecycle (also `review-loop.md` § Durable serve and `scripts.md` § review-server.py). SSOT: `scripts.md`, which the command already points at. → "run `scripts/review-server.py` with the flags in [scripts](reference/scripts.md)." Behavior held by the mandated reference.
4. `[RISKY]` await command: "…watcher selected with `staffing route <watcher task>`" **contradicts** `watch.md`: "**Do not resolve the watcher with a generic `staffing route` of the watch task** … Read the Floor value the roster publishes instead." Not a verbosity cut — a fork in the single source of truth. One of the two must be corrected to match the other; I cannot dedupe without picking the intended behavior. Flagging, not proposing.
5. `[dedupe]` Loop contract: "Missing surface config degrades to local open—never a public tunnel." — verbatim meaning of `surface-and-hub.md` § Local fallback, which the same paragraph mandates loading. DELETE; the loaded reference carries the rule.

### reference/review-loop.md — 951 words

1. `[dedupe]` § Durable serve, "Its OS session, closed inherited descriptors, state-scoped log, and atomic PID/port/instance record make the endpoint independent of the issuing exec session, PTY, agent turn, and watcher. Teardown is explicit and idempotent: `--stop --state <dir>` verifies the live instance before signaling and removes its hub row." — mechanics restated in `scripts.md` (worker-startup paragraph and **Stop** paragraph) nearly verbatim. SSOT: `scripts.md`. Replace section body with: "The serve command returns only after a detached worker answers its authenticated health check; mechanics and teardown in [scripts](scripts.md). The watcher only delivers an event after submission; it never owns the server that must receive that event." Every mechanic survives in the CLI doc.
2. `[dedupe]` § Verdict-coded await gate, "Its **exit code is the verdict**: `0` approve, `3` approve_with_nits, `10` request_changes, `124` timeout" — exit-code table appears four times (SKILL.md, here, `scripts.md`, `watch.md`). SSOT: `scripts.md`. Here keep "Its **exit code is the verdict** — branch on it without parsing ([scripts](scripts.md))"; codes preserved at the SSOT.
3. `[collapse]` "The scripts implement this contract; this doc *is* the contract." → "This doc is the contract the scripts implement." Same assertion once.
4. `[cut]` "from the #46 self-approval incident" — provenance sediment inside shipped content; the heuristics themselves are the rule. DELETE the phrase; every heuristic stays.
5. `[cut]` "Custody hardening (the awaiting thread never holding what can mint a verdict) remains open follow-up; until then" — issue-tracker sediment; keep only "these checks are the guard." The guard rule is unchanged.
6. `[collapse]` § Hash-bound approval: "Editing the artifact after a page load invalidates any prior-hash approval, so the human can never sign off on a version they did not see." → keep only "so the human can never sign off on a version they did not see" attached to the 409 sentence — the first clause restates the rejection mechanism just stated.

### reference/scripts.md — 891 words

1. `[collapse]` Intro paragraph vs. the post-JSON paragraph both state launcher-verifies-worker ("The public invocation starts one detached worker, verifies its authenticated `/version`…" / "Serve returns only after `/version` answers with the same `pid` and random `instance_id`."). Keep the detailed second; trim the intro to "Starts one detached worker and exits with the review metadata as JSON." Identity check preserved below.
2. `[dedupe]` Case-statement comments in Typical invocation ("changes requested — revise + write ledger, then re-serve/re-await", "timeout — end the turn with the two links; re-await next turn") restate `review-loop.md` §§ ledger/timeout. Low value; acceptable as example glue — cut only if squeezing.

### reference/surface-and-hub.md — 1,186 words

1. `[dedupe]` § Publish, don't fork: "The review server serves the file on disk and injects the chrome at serve time, so the committed file stays byte-pure while the human still gets the review UI." — verbatim meaning of `review-loop.md` § Serve-time chrome (both files load together per SKILL.md). SSOT: `review-loop.md`. Keep only the principle sentence "A presented artifact is the committed file, served in place — never a diverging copy."
2. `[collapse]` § Bringing the tailnet up intro: "So the **serve step owns a connectivity precondition**: before it publishes an artifact or starts the review server, it confirms the node is up and brings it up only when it is not." — restates bullets 1–2 that immediately follow ("Detect, don't assume", "Bring it up only as a publish precondition… all three hold"). Keep the bolded clause, delete the trailing "before it publishes… is not" — the bullets carry the exact conditions.
3. `[dedupe]` Bullet 4: "fall back to the local-only review — open the rendered file on the machine and say remote review is unavailable, the same degradation as an unrecorded surface. **Never enable Funnel or improvise a public tunnel** to route around a down tailnet." → "fall back to the local-only review (§ Local fallback)." — the fallback wording and no-tunnel rule are verbatim in § Local fallback above in the same file.
4. `[cut]` Closing paragraph "This is the connectivity companion to *The surface is only as awake as the machine* above: that bullet covers a sleeping machine, this covers a disconnected node. Both keep the surface honest — a review only publishes to a URL the human can actually reach." — summary restating both sections; no rule lives only here. DELETE.
5. `[dedupe]` § Path-prefix mounts, "The server matches its endpoints (`/`, `/version`, `/event`, `/hub`) **suffix-tolerantly**, so it works whether the proxy strips the prefix before forwarding (the backend sees `/event`) or preserves it (…)." — restates `scripts.md`'s Endpoints preamble. SSOT: `scripts.md`. Keep the chrome's mount-relative half (unique here) plus "the server side is suffix-tolerant ([scripts](scripts.md))."
6. `[dedupe]` § Swept, not trusted: "…runs `review-server.py --sweep --surface <dir>`, which probes each entry's URL, drops the dead, regenerates the index, and prints `{"swept":[…]}`." — verbatim from `scripts.md` § Sweep mode. → "…runs the sweep ([scripts](scripts.md) § Sweep mode)."
7. `[dedupe]` "An optional `--surface-label` adds a suffix to the hub heading (e.g. a repo name); default none." — duplicate of the `scripts.md` flag-table row. DELETE; CLI table is SSOT.

### reference/watch.md — 1,019 words (highest duplication density in the skill)

1. `[cut]` "**No change to `review-await.py` is needed** — the existing cursor already makes cross-turn re-arming safe; the loop lives in the watcher's contract, not the script." — authoring-time design note (sediment); the runtime rule (loop-until-verdict, cursor losslessness) is fully stated above it. DELETE sentence.
2. `[cut]` "This is the property the approval-delivery hardening turns on: … and it holds through a path-prefixed mount (the real deployment shape — see [surface-and-hub] § Path-prefix mounts), where the verdict POST reaches the server and fires the verdict-coded await regardless of whether the proxy strips or preserves the prefix." — hardening-issue sediment plus a third restatement of prefix tolerance (SSOT `scripts.md`/`surface-and-hub.md`). DELETE from "This is the property…" to end of paragraph; the wake rule preceding it is intact.
3. `[cut]` § Both gates closing paragraph: "In both cases the rule is identical: don't park the orchestrator, delegate the hold to a cheap staffing-resolved watcher, loop-until-signal, and wake the parent on completion." — whole-doc summary; every clause already stated. DELETE.
4. `[dedupe]` Staffing bullet: "an unpinned, no-capability task is ranked by `intelligence > taste > cost`, so `route` returns the **most capable** reachable model (cost is only a tie-break)" — restates staffing's `rankings-and-routing.md` inside review-loop. Keep the instruction ("do not use a generic route; read the published Floor") and cite staffing for why; the rule survives at its owner. (Interacts with SKILL.md finding 4.)
5. `[dedupe]` Same bullet: "Walk staffing's succession ladder if the Floor route is unavailable; if none remains, run the watch on the current model in a subagent—never skip it." — third statement (also review-loop SKILL.md "Missing staffing runs the watcher on the current model…" and staffing's `roles-and-fallback.md`). SSOT inside review-loop: SKILL.md's degradation line; here → "on route loss follow staffing's fallback ladder; absent staffing, per SKILL.md's degradation." No step lost.
6. `[collapse]` "This defangs **both** ceilings at once: the `--timeout` exit and the harness Bash-tool ceiling are just re-arm boundaries, not the end of the watch, so an arbitrarily long AFK review survives." → "Both ceilings become re-arm boundaries, so an arbitrarily long AFK review survives." — same claim, half the words.
7. `[RISKY]` § Why the orchestrator must not hold it inline — ~170 words of rationale ("both observed in practice", the strand-scenario paragraph). Rationale sections can be load-bearing for compliance with a counter-intuitive rule; cutting may weaken adherence. Flag only; if trimmed, keep the two bullet headlines and cut the "The verdict then strands…" paragraph (its content reappears in "durable backstop").

### reference/setup.md — 157 words

1. `[dedupe]` Step 3: "The server owns receipt of browser events; a watcher only delivers a recorded verdict." — contract restatement (SSOT: `review-loop.md` § Durable serve). Setup's job is recording commands; DELETE the sentence, rule survives at the contract.

**Review-loop estimate: 4,546 → ~3,900.**

## 2. `skills/system/staffing/` — scoped files 3,709 words

### SKILL.md — 378 words

1. `[collapse]` Description: "Own the model roster for a machine and its projects — who staffs which task. Use to install or reconcile the roster, add a project override, or resolve any "which model should do this?" question…" — "who staffs which task" and "which model should do this?" are one branch named twice (synonym trigger). DELETE "— who staffs which task"; the question-form trigger remains.
2. `[RISKY-dedupe]` § Resolution (the pre-gate sentence + numbered steps 1–4) is a compressed duplicate of `rankings-and-routing.md` § Resolution order, which the `route` command mandates loading. Proposed: collapse to "Load [rankings-and-routing] and follow its resolution order; on route loss, [roles-and-fallback]." plus keep only "If no model is reachable, use the current model in a subagent and report the gap; never skip the stage." RISKY because sibling skills may read only SKILL.md without running `route`; if that read-path matters, keep the summary and instead dedupe the reference (worse trade). Every gate/order survives at the SSOT either way.
3. `[dedupe]` § Layers: "Reachability is directional and effect-verified; one failed direction produces an asymmetric graph." — fourth statement of the directionality rule (also `machine-audit.md` step 1 and step 4, `install-and-reconcile.md` § External-worker, `roles-and-fallback.md` ladder). SSOT: `install-and-reconcile.md` ("Reachability state is per direction… One failed direction never disables the healthy direction."). Trim here to "Reachability is directional and effect-verified."

### reference/roles-and-fallback.md — 826 words

1. `[collapse]` Intro: "The roster — which model fills each role — is not written here; it is compiled from the machine audit into the global base and specialized by any project override (see [machine-audit] and [install-and-reconcile]). This file defines the *roles themselves* and how succession works when a role's model is unreachable, generically — no single machine's model names appear." → "The roster itself is compiled by [machine-audit](machine-audit.md) and installed per [install-and-reconcile](install-and-reconcile.md); this file defines the roles and succession, machine-generically." Same scoping, one sentence.
2. `[dedupe]` Issue coordinator role: "Resolve it at dispatch from the issue's work type, surface, coordination class/reason, known uncertainty, and required capabilities. … A `routine` issue resolves over that set by the normal pins, gates, and ranking—never cheapest-first. `orchestrator-required` work uses the orchestrator." — third statement of the coordinator pre-gate (also SKILL.md § Resolution, `rankings-and-routing.md` § Resolution order pre-gate). SSOT: `rankings-and-routing.md`. Keep the role definition (owns lifecycle, coordinator-eligible set, record-successor rule — unique here); replace the resolution mechanics with "resolved at dispatch per [rankings-and-routing] § Resolution order."
3. `[collapse]` Builder-ui and Worked example both spell "taste ≥ 7, per the routing rules". Keep the number only at its SSOT (`rankings-and-routing.md` step 3); here say "clears the routing rules' taste gate." The threshold survives in one place.
4. `[dedupe]` "Delegation into a separate thread still keeps build-out and the capped loops out of the orchestrator context, even mid-fallback." — restates the intro's "Separation is by thread, not by model" within the same file. Keep only "Succession changes *who* fills a role; it never merges the roles back into one thread."
5. `[RISKY]` § Worked example (~120 words) contains no rule not already stated (ladder + taste gate + subagent fallback + report-gap). Worked examples raise predictability on edge paths; full deletion may change fallback behavior in the ugly case it dramatizes. Flag as candidate; safest trim is its final sentence "never ship ui work through a model the roster would not clear for it, and never skip the change" → already stated as ladder rules.

### reference/rankings-and-routing.md — 748 words

1. `[dedupe]` § Defaults, not quality waivers: "Taste ≥ 7 remains a hard gate for user-facing work." — verbatim duplicate of step 3 in the same file ("This is a hard gate, not a preference."). DELETE bullet.
2. `[dedupe]` Same section: "Cost is the final tie-break only." — duplicate of step 4's ordering. Merge into the escalation bullet: "Escalate to a more capable reachable route without asking when cheaper output misses the bar." (unique, keep).
3. `[dedupe]` Same section: "Orchestration, design, and hard diagnosis go to the most capable reachable model." — duplicates `roles-and-fallback.md` § Orchestrator. SSOT: roles file. DELETE.
4. `[dedupe]` Same section: "Never staff below the floor and never attribute a provider's effect to its current model operator." — first half duplicates `roles-and-fallback.md` § Floor ("Nothing staffs below it, in any role"); second half is the file-intro rule ("Never infer a provider from a model name") plus the registry paragraph ("must not claim the effect as native Claude capability") — a third in-file statement. DELETE bullet; both rules survive at their first statements. Net: the whole § Defaults collapses to the two unique bullets (escalation; independent second reviewer).

### reference/machine-audit.md — 848 words

1. `[collapse]` The "it's only an example, not the roster" caveat is stated five times: intro ("never shipped fixed"), the § header "(illustrative only — NOT the shipped roster)", the pre-example paragraph ("It is an *example of output*, never the authoritative table — a different machine produces a different set of rows. Reproduce the *shape*, not these values"), the code comment "SEED VALUES, tune to your machine", and the post-example paragraph ("Everything above is **audit output for one environment**. On a machine with, say, no Codex CLI… Never present the five-model rows as the canonical staffing roster; they are a labeled example…"). Keep the header parenthetical + "Reproduce the shape, not these values" + the code comment; DELETE the post-example paragraph entirely and the pre-example paragraph's first sentence. The rule ("never treat as canonical") survives thrice-stated-once. ~80 words.
2. `[dedupe]` "so seed them, then let the user tune" (§ audit procedure) / "the user edits these to fit their own machine and pricing" (§ default seed) / "Then hand the seeded numbers to the user to tune" (§ writing) — same instruction three times in one file. SSOT: § The default seed. DELETE the other two clauses.
3. `[cut]` "— the deliberately-untested part of this skill is the subjective quality of those seed numbers." — author-side eval commentary (sediment); no runtime rule. DELETE.
4. `[collapse]` § audit procedure closing paragraph "From (1) you have the **rows**… From (2) you have the **sibling harness mechanics**…" pre-states § Writing the roster steps 1–2. Keep only the unique caveat ("judgment numbers are human assessments, not machine-detectable") — and even that reappears as § default seed's first sentence, so the paragraph can reduce to one pointer: "Steps (1)–(2) feed § Writing the roster; the judgment numbers cannot be probed — see § The default seed."
5. `[dedupe]` "Presence alone is not reachability." (step 2) vs. "Installation or model documentation alone is insufficient." (§ writing, step 2) — same rule twice in-file. Keep the first; the § writing line → "(presence alone is insufficient — step 2)".

### reference/install-and-reconcile.md — 581 words

1. `[dedupe]` § Module-first owner reconciliation is the staffing-side SSOT for the four-module barrier — keep it, and dedupe callers toward it (see setup.md below and setup-asher-skills findings). No cut here.
2. `[dedupe]` "Do not poll vendor policy or credits as a dispatch precondition." vs. `machine-audit.md` step 1 "Do not poll vendor policy or credit notices; real invocation behavior is the operational signal." — same rule, two phases (audit vs dispatch). Low severity; if deduping, SSOT here (dispatch-time), audit points.

### reference/setup.md — 269 words

1. `[dedupe]` Step 3 ("If a global base exists, leave it intact and offer only a project delta. If none exists, ask whether to create a consented global base or a project-only roster.") is a near-verbatim restatement of `install-and-reconcile.md` § Scope decision — which step 2 already mandates following ("then follow the scope decision in [install and reconcile]"). DELETE step 3 entirely; the rule survives at the mandated SSOT.
2. `[dedupe]` Step 4's barrier choreography ("Apply no global pointer until… staged and read back all four deferred modules… preflights and applies both Presentation sections… verifies all four final sections and finalizes…") restates `install-and-reconcile.md` § Module-first owner reconciliation. Keep step 4's unique mechanics (`{{COMMON}}` marker, `render-global.py render/check/stage/apply`) and replace the choreography prose with "per [install-and-reconcile] § Module-first owner reconciliation." ~60 words; ordering and gates survive at the SSOT.

### templates/global/staffing.common.md — 17 words
Clean; no findings.

**Staffing estimate: 3,709 → ~3,250.**

## 3. `skills/system/setup-asher-skills/` — 6,782 words

### SKILL.md — 565 words

1. `[collapse]` Description (user-invoked, `disable-model-invocation: true`): "…or audit an existing install for drift — one decision at a time, project-local by default. Not for authoring skills or arbitrary undeclared installs." — "one decision at a time, project-local by default" is body identity, not a trigger, and the description is human-facing anyway. → "The prompt-driven installer for this skills repo: set a project up, add a skill with its closure, or audit an install for drift. Not for authoring skills or undeclared installs." Invisible to the agent; three command-branches kept.
2. `[dedupe]` § Setup sequence steps 1–4 (~170 words) compress-duplicate `interview.md` Phases 1–4, which the `setup` command mandates loading (and `add` loads "interview confirm/write"). Collapse to the four phase names plus pointers; every gate survives in interview.md. Keep only rules a bare read needs before loading — arguably none, since every command loads its reference.
3. `[dedupe]` Trailing paragraph: "Repeated single-skill add commands can replace earlier selections from the same source, so batching is a correctness rule. A missing setup pointer is a no-op; a failed owner stops dependants and retry resumes there." — all three clauses restate interview Phase 4 ("Run **one command per scope**: repeated single-skill calls can replace earlier selections…"; "A skill without a declared setup branch is a valid no-op."; "A failure stops every dependent… A retry recompiles the same graph and re-invokes idempotently from the failed owner."). DELETE; SSOT interview.
4. `[dedupe]` Dependency surface: "(`scripts/catalog.py` — the catalog is compiled fresh from skill frontmatter every run, never stored)" — third statement of no-stored-snapshot (also catalog.md intro, audit-mode step 1). SSOT: `catalog.md`. Trim to "(`scripts/catalog.py`)".
5. `[dedupe]` Dependency surface: "Owner playbooks are guaranteed by invoking their public setup commands, never copied or interpreted here." + § What this skill does not do: "**Write a `docs/agents/` playbook itself.** It guarantees them via each skill's setup (phase 4 step 3)." + interview step 3: "**setup-asher-skills never reads, copies, or interprets another skill's setup reference.**" — triple. SSOT: interview step 3. Keep one line in SKILL.md at most.
6. `[dedupe]` § What this skill does not do: "**Ship an `ask-asher` router.** The `## Agent skills` block is the per-project map." — third statement (also interview step 4 "**There is no separate `ask-asher` router skill** — this block is the map." and the template comment "It is a map, not a router: there is no `ask-asher` dispatcher skill."). Retired-design guard sediment. SSOT: the template comment (lives where the block is written). DELETE the other two.

### reference/interview.md — 2,922 words

1. `[cut]` "Adapted from `setup-matt-pocock-skills`: explore first, present decisions one at a time…, confirm the whole thing, then write." — external attribution in skill content violates the repo's own "credits live in the README" convention, and the sequence it describes is restated two sentences later ("The sequence is **audit → interview → confirm → write.**"). DELETE the attribution clause; move credit to README (out of scope for this audit's edits).
2. `[cut]` "This file stands alone — it imports no other skill's files and names the siblings it composes only by plain name." — no-op for the executing agent (there are no imports to refuse); authoring-convention note. DELETE. (Same for `audit-mode.md`'s "This file stands alone.")
3. `[dedupe]` Intro: "Nothing touches disk until the user approves the whole plan at confirm." duplicates Phase 3's "Nothing touches disk until the user approves this. This is the single write gate." SSOT: Phase 3. DELETE the intro instance.
4. `[dedupe]` Phase 1: "prior-install evidence, not the block alone, decides routing: greenfield (no block and no installed asher-skills) runs `setup`, while a block or installed asher-skills routes to `audit`" — third statement of the routing rule (SKILL.md "No argument routes to setup only when…"; audit-mode intro). SSOT: SKILL.md (it is the dispatch rule). Here → "routing per SKILL.md; see [audit-mode](audit-mode.md)."
5. `[dedupe]` Phase 2 scope bullet ("Everything is **project-local by default**; the only skill offered a **global** install is `staffing`… Never offer any other skill global.") near-verbatim duplicates `catalog.md` § Scope — project-first — and both files load together on every setup run. SSOT: catalog § Scope. Bullet → "**Scope is surfaced only where it matters** — apply [catalog](catalog.md) § Scope; route staffing's global write through its own consent gate."
6. `[dedupe]` Phase 2 external bullet's last sentence "An undeclared external request is not added to this setup run." — one of six statements of the no-undeclared-externals rule across the skill (SKILL.md description; SKILL.md § not-do; catalog § Canonical source ¶3 "never auto-installed"; this bullet; repo-pointer template). SSOT: catalog § Canonical source; keep the template copy (ships to consumers). DELETE here and trim SKILL.md § not-do to its first sentence.
7. `[cut]` Phase 2: "Never pull a sibling silently and invisibly." — "silently and invisibly" is one adverb twice, and the bullet's bolded lead already commands the disclosure. → "Never pull a sibling silently."
8. `[dedupe]` Phase 4 step 1: "This is one shared notion consumed by the READ path (audit's catalog choice) and this WRITE path (Phase 4's install guard), so the two cannot diverge." — mirror-duplicate of audit-mode step 1's closing sentence; the preceding clause already points at audit-mode step 1 as canonical. DELETE this sentence (and, below, keep audit-mode's — one direction of the pointer suffices).
9. `[dedupe]` Phase 4 step 1: "(the same repo-is-the-source reasoning as audit's self-catalog choice)" — restates finding 8's pointer within the same step. DELETE.
10. `[dedupe]` Mount shape is specified twice within Phase 4 step 1 — the "source directory is never an install destination" bullet (primary real dir + `.claude/skills` symlink + lock entry) and the later verification paragraph ("The unvaried primary mount must be a real `.agents/skills/<name>` directory, and every expected harness alias must be a symlink to that primary. A primary symlink, independent alias directory, regular-file mount, dangling alias, or wrong-target alias is not a valid install.") — plus `catalog.md` § variants ("The default remains one real `.agents/skills/<name>` primary plus any harness alias symlinks."). SSOT: the verification paragraph (it is the checkable criterion). Trim the earlier bullet to the tool-specific facts it uniquely holds (lock fields, v1.5.15 symlink-only-if-dir-exists quirk).
11. `[cut]` "(it reported "Installed 3 skills" when 4 were requested)" — anecdote; the rule "`-y` mode can under-report the count" stands alone. DELETE parenthetical.
12. `[collapse]` "(`-g` is scope, `-y` still skips the prompt — they are orthogonal)" — the sentence already said `-y` skips the prompt; flag orthogonality is default model knowledge (no-op). DELETE parenthetical.
13. `[dedupe]` "Every install command targets `asasher/asher-skills` and nothing else — see [catalog](catalog.md) § Canonical source and declared externals." — pointer plus restatement; the rule is the SSOT's first bolded sentence. → keep pointer only.
14. `[dedupe]` fallbackOrigin paragraph, final clause: "`audit-mode` treats such an entry (marked `fallbackOrigin`, or missing `computedHash`) as expected, not drift." — forecasts audit-mode's own Drift bullet, which states it and back-points here. SSOT: audit-mode. DELETE clause; keep "Tell the user the entry is fallback-origin."
15. `[collapse]` Step 4 states create-minimal-CLAUDE.md twice: "when Claude Code will work in the project, also create a minimal `CLAUDE.md` beginning with `@AGENTS.md`" and, one paragraph later, "ensure its `CLAUDE.md` begins with an `@AGENTS.md` import (create a minimal `CLAUDE.md` holding just the import if none exists)". Merge into the bolded guarantee paragraph; one instruction, both conditions preserved.
16. `[dedupe]` Step 6 barrier choreography (~200 words) is the setup-asher-skills-side SSOT — keep, and point SKILL.md step 4's tail and audit-mode's Global-owner-drift bullet at it (see those findings).

### reference/catalog.md — 1,329 words

1. `[dedupe]` § Canonical source ¶3: "Before any external write, follow [interview](interview.md) Phase 4: verify provenance, inspect and disclose source/version/scope/hooks, get explicit consent, use the provider-specific installer, verify the declared capability, and record the result in the consumer's separate `external-dependencies.lock.json`." — full summary of interview Phase 4 step 2, co-loaded. → "Before any external write, follow [interview](interview.md) Phase 4 step 2." All gates survive at the SSOT.
2. `[dedupe]` Same ¶: "An arbitrary external request that is not in the selected closure is never auto-installed; offer an Asher-authored equivalent if one exists, or state that the request needs a separate deliberate install outside this setup run." — keep (this is the elected SSOT for the rule, per interview finding 6); the *other* five instances go.
3. `[dedupe]` § Install and setup closure, "The current notable edges are visible by compiling the catalog: backlog requires diagnosing-bugs, prototype, research, review-loop, and staffing; research requires staffing; …" (~95 words) — a prose snapshot of edges in the very file that declares "**No snapshot is stored:** the catalog is compiled fresh … so it can never go stale." This list *can* go stale (it is exactly the drift the skill audits for elsewhere). SSOT: the compiled catalog. → "Edges come from compiling the catalog (`closure`); never maintain a prose copy." Behavior preserved because the file already mandates compiling.
4. `[dedupe]` "When closure resolution adds a sibling, **tell the user which sibling came along and why** — the pull is never silent ([interview](interview.md) § Phase 2)." — restates the co-loaded interview Phase 2 bullet it cites. → pointer only, or DELETE (interview is the SSOT for interview conduct).
5. `[dedupe]` § Runtime composition: "A required install edge may support more than one runtime reach and is not itself proof that a dispatch occurs." — restates the section's own opening "Install edges only guarantee presence; they do not say how work moves at runtime." DELETE the trailing sentence.
6. `[dedupe]` "exact required/optional/setup closure comes from compiling the sources (`scripts/catalog.py compile` / `closure`)" — third in-file statement of compile-don't-store. DELETE.
7. `[dedupe]` "`fair-deal` installs inside a deal project and is **never** global." (single-purpose ¶) and "(and `fair-deal` is explicitly never global)" (§ Scope) — same rule twice in-file. Keep the § Scope instance (rules section); DELETE the other.

### reference/audit-mode.md — 1,277 words

1. `[dedupe]` § no-version-stamps: "**setup introduces no such stamp.**" — flat repeat of the section's first sentence two sentences later. DELETE.
2. `[cut]` "(backlog's earlier `vNN` stamps are retired; its setup reconciles the same way)" — historical cross-skill sediment; the posture statement stands without it. DELETE (low severity — mild resistance value if old stamps are still encountered in the wild).
3. `[dedupe]` Intro routing sentences ("Re-invoking setup on a project that already has a `## Agent skills` block runs `audit`. A project with installed asher-skills but no block also reaches `audit`…") — third statement of the dispatch rule; SSOT SKILL.md. Keep only the Missing-map framing sentence.
4. `[collapse]` Overlap bullet: "Also report A `.claude/skills/<name>` alias symlinked to the `.agents/skills/<name>` primary is the expected mount shape, not overlap and not a second installed package. An independent alias directory is a Mount-shape failure." — dangling "Also report" (editing sediment) and the last sentence duplicates the Mount-shape bullet above it. → "A `.claude/skills/<name>` alias symlinked to the primary is the expected mount shape, not overlap; an independent alias directory is a Mount-shape finding, not overlap."
5. `[dedupe]` Global owner drift bullet's barrier sequence ("both providers' Presentation and Staffing modules must be staged/read back before both globals preflight; apply Presentation to both, then Staffing to both, verify all four final sections, and remove the barrier") — restates interview Phase 4 step 6. → "Pointer migration is proposed through the shared four-module barrier ([interview](interview.md) Phase 4 step 6)." Ordering survives at the SSOT.
6. `[dedupe]` Drift bullet: "(read both and judge; don't diff a stamp)" — restates § no-version-stamps in the same file. DELETE parenthetical (low).

### templates — 689 words total

1. `[cut]` `agent-skills-block.md` example rows: "| plan | Turns a feature into a reviewed plan held at an approval gate | project |" — the `plan` skill is retired (catalog: "the spec's review gate replaced the retired plan stage"). Stale example = sediment that invites installing a dead skill. DELETE row. Similarly "| backlog | Runs admitted issues through groom → build → review to a merged PR |" is stale against the current contract ("review-ready PR; merging is the explicit merge-changes workflow") — fix or delete. Example-only, so behavior-safe.
2. `[dedupe]` `agent-skills-block.md` comment: "It is a map, not a router: there is no `ask-asher` dispatcher skill." — elected SSOT for the router guard (keep here; delete the interview/SKILL.md copies per earlier findings).
3. `[collapse]` `repo-pointer.md`: "Every Asher-authored skill comes from this repo." — restates the template's first sentence ("The agent skills in this project come from [asher-skills]…"). DELETE; the never-substitute rule lives in catalog § Canonical source.
4. `presentation.common.md`, both pointers: clean; no findings.

## 4. `skills/creative/bare-minimum-ux/` — 582 words

### SKILL.md — 303 words

1. `[collapse]` Description: "Use when building or reviewing application UX, web interfaces, or frontend flows." — "application UX / web interfaces / frontend flows" are three synonyms for one branch. → "Use when building or reviewing user-facing UI." Build vs review are the two genuine branches; both kept.
2. `[collapse]` Rule 1: "Do not surface internal instructions, prompts, implementation details, design constraints, or acceptance criteria in user-facing product copy. Only write copy that an actual end user should see. Treat build guidance as private context unless explicitly asked to expose it." → "Do not surface internal instructions, prompts, implementation details, design constraints, or acceptance criteria in user-facing copy unless explicitly asked to expose them." Full prohibition list and the exception survive.
3. `[collapse]` Rule 3 example: "e.g For a table add row button at the bottom is good cause you press and see the row added but add row button at the top is bad cause you have to scroll down to see the added row, it could be good if the row is added to the top." → "e.g. a table's add-row button belongs where the new row appears (bottom-insert → bottom button; top-insert → top button)." Same rule, both cases, half the words.
4. `[collapse]` § Deeper craft, "This overlay stays deliberately small; the deep design capability is **Impeccable**, declared above as a provenance-checked external requirement." → "The deep design capability is **Impeccable**, the external declared above." — "overlay stays deliberately small" is self-description (no-op); "provenance-checked external requirement" restates the frontmatter it points at.

### references/notifications.md — 182 words
Clean — flat peer-set of unique rules, telegraphic already. No findings.

### references/planning.md — 97 words

1. `[RISKY]` **Orphan reference file: nothing points at it.** `SKILL.md` links only `references/notifications.md`; `planning.md` has no context pointer anywhere in the skill, so it never loads — dead weight regardless of its prose. Fix is either a pointer in SKILL.md (a behavior *addition*, hence RISKY under this audit's constraint) or deletion (behavior-preserving only in the degenerate sense that it already never fires). Flagging for the owner to decide.
2. `[collapse]` Item 3: "list of the steps of users journey and what information they'll need at each step and how do we progressively present them just enough information they need at each point" → "list the user-journey steps and the minimum information each needs, presented progressively." — "just enough information they need at each point" restates "what information they'll need at each step."

## Totals

- **Now:** 15,619 words in scope.
- **Estimated after:** ~13,350–13,500 words (roughly a 14% reduction, all from duplication/sediment — no rule, gate, ordering, or edge case removed from its single source of truth).

## Five highest-value edits

1. **Resolve the `staffing route` watcher contradiction** (review-loop SKILL.md await vs. `watch.md`'s explicit prohibition) — not a word-count win but the audit's most important find: two sources of truth that currently disagree on behavior.
2. **Collapse the four-module barrier choreography to two SSOTs** — keep `staffing/reference/install-and-reconcile.md` § Module-first and `setup-asher-skills/reference/interview.md` Phase 4 step 6; convert the three other full restatements (staffing setup.md step 4, setup-asher-skills SKILL.md step 4 tail, audit-mode Global-owner-drift) into pointers. Largest cross-file dedupe (~150 words) on the most intricate, most drift-prone procedure in the repo.
3. **Deduplicate the coordinator pre-gate / resolution order to `rankings-and-routing.md`** — currently stated in full three times (staffing SKILL.md, rankings-and-routing, roles-and-fallback), with "never cheapest-first" and "current-model-in-a-subagent, never skip" each stated three times. One edit point instead of three for staffing's core algorithm.
4. **Cut `machine-audit.md`'s quintuple "it's only an example" caveat and triple "user tunes the seeds"** — the single biggest intra-file collapse (~100 words) with zero rules lost.
5. **Delete `catalog.md`'s prose sibling-edge list** — it is a stored snapshot inside the file whose thesis is "no snapshot is stored, so it can never go stale"; it duplicates the compiled catalog and is the one passage guaranteed to rot.

Also worth acting on even though it isn't top-5 by words: `bare-minimum-ux/references/planning.md` is an orphan — no pointer in SKILL.md ever loads it.
