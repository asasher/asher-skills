
# backlog — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — Groom sweep and gate**

Tickets #10, #11, #12, and #13 enter the sweep. #10 and #11 form one subject because their decisions interlock; #12 forms another subject. Both subjects form one batch because they share a subsystem. #13 is routed directly to the ready role because its decisions are settled, so it is not shaping work.

Before the user responds, only the batch plan is presented. No thread exists, and #10–#12 have not yet been marked shaping.

Citations:

- “Sweep the tracker for unlabeled tickets and tickets carrying the needs-shaping role, or take the ids given.”
- “Route first: a ticket whose decisions are already settled gets the ready role…”
- “Tickets whose decisions interlock form one **subject**; subjects that belong together (same subsystem, same domain area) form one **batch**…”
- “**Confirm before anything spawns.** Present the batch plan…; no thread exists until they approve it.”

— `SKILL.md`, § `groom`

2. **P1b — Single batch**

No separate thread spawns. This session becomes the shaping thread and runs `shape` on #10–#12. After approval, all three tickets are marked with the shaping role; the one-thread-per-ticket rule still applies.

Citations:

- “Then, per approved batch: mark its tickets shaping per the label roles — a ticket never gets two threads…”
- “A single batch spawns nothing: this session becomes the shaping thread and runs the `shape` skill itself.”

— `SKILL.md`, § `groom`

3. **P2 — Two dispatch shapes**

For shaping, answer status from the tracker and the harness thread listing, and report how to attach to each thread. Shaping does not automatically send a result back to this dispatcher. In this scenario, the single approved batch ran in the current session, but the stated status sources remain the tracker and thread listing.

For builds, this session supervises the subagents and relays each review-ready change request or failure; a build that dies silently must also be reported.

Citations:

- “Grooming is interactive — human-in-the-loop work fans out as threads the user attends, and no result flows back.”
- “Report each thread and how to attach; status on request comes from the tracker and the harness's thread listing.”
- “Building is autonomous — it fans out as subagents this session supervises to completion.”
- “This session babysits the fleet: each build's completion wakes it, and it relays the outcome — the review-ready change request, or the failure, with a died-silent build reported, never dropped.”

— `SKILL.md`, introduction and § `groom`/`build`

4. **P3 — Double dispatch**

#21 is not dispatched again because it is already marked building.

Before #20’s subagent spawns, #20 is marked building. Its `build` execution is dispatched through the `to-subagent` skill in its own worktree, subject to the environment playbook’s isolation verdict.

Citations:

- “For each: mark it building per the label roles — a dispatched ticket must never dispatch twice…”
- “…then dispatch the `build` skill on it via the `to-subagent` skill, in its own worktree.”

— `SKILL.md`, § `build`

5. **P4 — Isolation verdict**

#20 and #22 run sequentially, one ticket at a time, in the main checkout. They do not run concurrently in separate worktrees.

Citation:

- “Isolation and concurrency follow the environment playbook's verdicts…: a repo that can't isolate builds one ticket at a time in the main checkout.”

— `SKILL.md`, § `build`

6. **P5 — Missing playbook**

`backlog build` stops rather than improvising tracker or platform behavior. The next action is to run `backlog setup` first so the missing playbook can be installed or reconciled.

Citation:

- “Missing playbooks: run `backlog setup` first — don't improvise them.”

— `SKILL.md`, introduction

7. **P6 — Merge boundary**

No. LGTM and completed change requests are insufficient authorization. The change requests wait until the user explicitly authorizes merging.

Citation:

- “Merging the resulting change requests waits for explicit authorization.”

— `SKILL.md`, § `build`

# shape — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — Intake.** I read #142 and #147’s ticket threads and linked artifacts together because their decisions interlock; I read #150 separately. I also read `CONTEXT.md`, any matching documents identified by the `## Context documents` index, and the tracker binding in `docs/agents/platform.md`. If `PRODUCT.md` or `DESIGN.md` exists, I read those too.

   Citation — `SKILL.md`, “Intake”: “Read each subject: the ticket thread and linked artifacts when it's a ticket (tickets whose decisions interlock are one subject, read together), the handed material when it's an idea, plus the **repo context files** — `CONTEXT.md`, and `PRODUCT.md`/`DESIGN.md` where they exist — and the project instruction file's `## Context documents` index for the documents whose clauses match.”

   Citation — `SKILL.md`, “Dependency surface”: “**Project surface:** the repo context files (`CONTEXT.md`, plus `PRODUCT.md`/`DESIGN.md` where they exist); the instruction file's `## Context documents` index; the tracker binding in `docs/agents/platform.md` when the subject is a ticket.”

2. **P2 — Dispatch.** The vendor settlement API question goes to `research`; the wizard-versus-form question goes to `prototype`. Both are dispatched through `to-subagent`. Only frontier decisions dependent on those answers pause; independent frontier work continues, and the findings later return as evidence.

   Citation — `SKILL.md`, “The loop”: “A question that needs source-backed investigation goes to the `research` skill; a question paper can't settle goes to the `prototype` skill — each dispatched via the `to-subagent` skill.”

   Citation — same section: “A dispatched question blocks only what depends on it; results re-enter the frontier as evidence.”

3. **P3 — Labels.** No. I do not mark the tickets ready based on my own judgment. Readiness requires the user’s explicit signal.

   Citation — `SKILL.md`, “Done”: “Lifecycle labels are never shape's judgment: shape stamps nothing on its own — it only executes the user's explicit calls: the readiness signal (below) and an approved split.”

   Citation — `SKILL.md`, “Crystallise”: “Posting a spec is a proposal, not a state change — readiness still waits for the user's blessing.”

4. **P4 — Record.** Because these are tickets, I record the cadence decision on the relevant ticket thread immediately as it settles. If it crystallises a domain term or ADR-worthy decision, `domain-modeling` also writes it immediately according to that skill’s contract. The supplied file does not say whether cadence is inherently ADR-worthy, so that part is conditional.

   Citation — `SKILL.md`, “The loop”: “When the subject is a ticket, record settled decisions on its thread as they land — the thread is the resume state.”

   Citation — same section: “Run the `domain-modeling` skill alongside: terms and ADR-worthy decisions are written the moment they crystallise, per its own contract.”

5. **P5 — Crystallise.** I automatically run `to-spec` for the payouts subject. Its spec is posted on the subject’s ticket and opens with a diagram. The user must still bless readiness; any recommended ticket split also waits for explicit user approval before `to-tickets` executes it.

   Citation — `SKILL.md`, “Crystallise”: “When a subject's frontier is empty, run the `to-spec` skill on it — automatically, not on request: the spec lands on the subject's ticket, opening with a diagram (to-spec creates the ticket when the subject was only an idea).”

   Citation — same section: “Posting a spec is a proposal, not a state change — readiness still waits for the user's blessing.”

   Citation — same section: “A spec may end by recommending a split; executing one — the `to-tickets` skill superseding the ticket with born-shaped children — happens only on the user's explicit approval, in a comment or here in the thread.”

6. **P6 — Resume.** The fresh session reads the ticket thread, repo context files, and ADRs, then recomputes the frontier from unresolved decisions. It must not re-ask anything already answered by that durable record.

   Citation — `SKILL.md`, “Resume”: “A fresh session on the same subject reads the record — ticket thread, the repo context files, ADRs — recomputes the frontier from what is still open, and re-asks nothing the record answers.”

7. **P7 — Degrade.** I leave the wizard-versus-form question explicitly open and report that `prototype` is absent. I do not silently skip or guess the decision.

   Citation — `SKILL.md`, “Dependency surface”: “Absent one, park the affected work as open and say so; never silently skip.”

8. **P8 — Comment watch.** After #150’s spec is published and the user goes AFK, I run `watch-until` on that ticket. On “add the retry cadence to the spec,” I update the ticket or spec, reply with what changed, and resume watching. On “LGTM — ready for agent,” I apply the tracker’s readiness role because that is the user’s explicit decision.

   Citation — `SKILL.md`, “After the spec”: “Run the `watch-until` skill on the spec'd tickets — condition: a new comment from the user, or an explicit readiness signal ("LGTM", "ready for agent"), in a comment or here in the thread.”

   Citation — same section: “On a comment: apply the requested tweak to the ticket or spec, reply with what changed, resume watching.”

   Citation — same section: “On the readiness signal: apply the readiness role per the tracker's label roles — the user's decision, executed.”

9. **P9 — Engines.** Two engines run, not three: one engine handles the interlocked #142/#147 payouts subject, and one handles unrelated #150. Each is dispatched through `to-subagent`. Each engine returns its question frontier; this session combines both into one user-facing round, tags questions by subject, then routes the answers back to the appropriate engine and re-dispatches it.

   Citation — `SKILL.md`, “One engine per subject”: “A batch of several runs one engine per subject — merely-related subjects never share one, interlocked tickets always do — each dispatched via the `to-subagent` skill.”

   Citation — same section: “Engines are non-interactive, so an interview round is a dispatch cycle: each engine reads its subject's record, computes its question frontier, and returns it; this session combines the frontiers into **one round for the user**, questions tagged by subject, then routes the answers back and re-dispatches each engine with its own.”

# to-spec — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — No interview:** Do not ask the user. Record retry policy as an open question in **Notes** and continue.

   Citation — `reference/synthesis.md`, “The one rule”: “When something was genuinely left undecided, **record it as a line in the spec's Notes** — an open question, named plainly — and move on.”

2. **P2 — Classification:** Mark every Notes line as **blocking**, **delegated**, or **deferred**. An open blocking Note means the direction is not ready to build on and must be settled upstream first.

   Citation — `SKILL.md`, step 5: “every Notes line is classified **blocking** (must be settled upstream before tickets), **delegated** (the executor may choose; boundary named), or **deferred** (parked, with a home).”

   Citation — same step: “an open blocking Note means the direction isn't ready to build on — say so in the report.”

3. **P3 — Stale content:** Do not include `src/payments/worker.ts`. The prototype-validated reducer snippet may appear if it captures a decision more precisely than prose; include only that decision-rich fragment and identify it as prototype-derived.

   Citation — `reference/synthesis.md`, “No stale content”: “The spec carries **no file paths and no code snippets.**”

   Citation — same section: “The single exception: a **prototype-validated snippet** that encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape.”

   Citation — same section: “Inline only that decision-rich fragment and note it came from a prototype.”

4. **P4 — AFK sign-off:** Leave the spec on its newly created ticket, where the user can approve it with an LGTM on the ticket or later in the conversation. To-spec does **not** apply a readiness label after that LGTM.

   Citation — `reference/synthesis.md`, “Sign-off”: “**User AFK, spec on a ticket** — the spec already sits where the user's comments reach it; their LGTM on the ticket (or in the conversation) is the approval.”

   Citation — same sentence: “To-spec applies no readiness label — that decision travels by the tracker's label roles and belongs to whoever executes the user's call.”

5. **P5 — Home and revision:** Create a live-tracker ticket titled from the command argument `payouts` and put the spec in its body, which is canonical. A later revision rewrites that body in place and posts a short comment describing what changed.

   Citation — `reference/synthesis.md`, “Where the spec lives”: “Given no ticket but a bound tracker (`docs/agents/platform.md`), **create the ticket** — titled from a short kebab-case slug for the decided direction (the command argument, or derived from the solution when omitted) — and write the spec as its body.”

   Citation — same section: “Every revision rewrites the body in place and posts a **short comment noting what changed** — the body stays the one current spec; the comments are the revision trail and the notification.”

6. **P6 — Vocabulary:** Change it to: **“Split this into tickets.”**

   Citation — `reference/synthesis.md`, “Vocabulary”: “A **spec** is the direction document, split downstream into **tickets**.”

   Citation — same section: “Never call the downstream unit an ‘issue’ — that's one tracker's word, and the pair is deliberately tracker-agnostic.”

7. **P7 — Diagram first:** The ticket body must begin with a fenced `mermaid` diagram showing the moving parts—using a flow, sequence, or state-machine form as appropriate—before any prose.

   Citation — `reference/synthesis.md`, “The diagram comes first”: “Every spec **opens with a diagram** of the moving parts — before any prose.”

   Citation — same section: “Pick the form that fits the direction: a flow of the pieces, a sequence of the actors, a state machine of the lifecycle — written as a fenced `mermaid` block.”

8. **P8 — Too big:** Do not split it into tickets. End the spec with a **Recommended split** section proposing the three build slices and their blocking edges; the user decides whether to perform the split.

   Citation — `reference/synthesis.md`, “Recommend the split, never perform it”: “When the decided direction is clearly bigger than one build, end the spec with a **Recommended split** section: the proposed slices in a sentence each, and which edges would block which.”

   Citation — same section: “It is a proposal only — splitting is the user's call, and executing it belongs to a different move.”

# to-tickets — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — Recut.** “Add all the payout models” is a horizontal layer, not a complete, demoable slice. Recut it into narrow end-to-end tickets spanning the required data, logic, and UI layers.  
   Citation — `reference/slicing.md`, § Draft vertical slices: “A tracer bullet is a **narrow-but-complete path through every layer**” and “The anti-pattern is the **horizontal layer** — ‘all the models,’ then ‘all the logic,’ then ‘all the UI.’”

2. **P2 — Use the wide-refactor sequence.** Create:

   1. One **expand** ticket introducing the new symbol alongside the old.
   2. Several **migrate-in-batches** tickets covering the ~120 sites in reviewable batches; these may run in parallel after expand.
   3. One **contract** ticket removing the old symbol, blocked by every migration ticket.

   This treatment is justified only because the rename is both **mechanical** and **high blast radius**. The number and boundaries of migration batches are not specified and must be settled during drafting and the quiz.  
   Citation — `reference/slicing.md`, § The wide-refactor exception: “The trigger is **both** conditions: the change is *mechanical* (little per-site judgement) **and** *high blast radius* (touches many sites).” The same section requires: “**Expand** — introduce the new form alongside the old,” “**Migrate in batches**,” and “**Contract** — remove the old form once nothing uses it.”

3. **P3 — Do not publish yet.** Present the complete draft and quiz the user specifically about granularity and blocking edges. Their approval of the spec’s recommendation authorizes running `to-tickets`; it does not replace approval of the actual drafted split.  
   Citation — `reference/slicing.md`, § Quiz the user: “**Iterate until approved.** This quiz *is* the human confirmation for the whole operation — **nothing publishes before it is approved.**”

4. **P4 — Stop before publishing and ask the user how to proceed.** Do not create local ticket files merely as a fallback.  
   Citation — `reference/slicing.md`, § Publish in the bound tracker’s format: “No recorded binding at all: state the gap and ask the user how to proceed — a backlog needs a tracker, so publishing waits on that decision.”

5. **P5 — Leave readiness unset by default.** Approval of the split alone does not automatically apply readiness. Apply it only if the user also asks to bless the tickets for pickup.  
   Citation — `reference/slicing.md`, § Readiness: “Do **not** auto-apply the readiness role on a fresh split” and “absent that request, leave readiness unset.”

6. **P6 — Create blockers first in topological dependency order.** Each dependent is created only after its blockers have real IDs. Because this repo records GitHub’s native relation, write every edge as native `blocked_by`, using the verified mechanism in `platform.md`, rather than inventing a body marker.  
   Citation — `reference/slicing.md`, § Order and wire the edges: “Once the split is approved, sort the tickets into **dependency order — blockers first**” and “Where the playbook records the tracker's **native blocking relation** … write the native edge.”

7. **P7 — Supersede #42 without editing its spec.** Apply the tracker’s superseded/excluded label role to #42, post a comment linking every child, and make each child link back to #42. Leave the body’s spec text unchanged.  
   Citation — `reference/slicing.md`, § Supersede the parent: “mark it per the tracker's superseded/excluded label role … and post a comment linking every child” and “The parent's spec text is never edited.”

8. **P8 — Do not run a split.** The oversized ticket may warrant recommending a split through some other workflow, but `to-tickets` cannot initiate it without an explicit user call.  
   Citation — `SKILL.md`, opening section: “To-tickets runs only on the user's explicit call — recommending a split is someone else's move; performing one is never self-initiated.”

# prototype — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — Narrow the question before building.** Record: “Should the payout flow be a wizard or a single form?” and identify it as a variants-shape question comparing those alternatives.  
   **Citation:** `SKILL.md`, Entry: “Run on an explicit question; if it is vague, narrow it before building.”

2. **P2 — No. It is a prototype decision, not a later implementer taste call.** Which actions are overt must be settled through the variants.  
   **Citation:** `SKILL.md`, Gates: “An interface's non-obvious presentation choices — the visual hierarchy, which actions are overt, what each journey step shows — are decisions, not taste calls: a variants prototype settles them; implementation never invents them.”

3. **P3 — Expose and open the variants before iterating.** Provide one command or URL plus visible state, then open the rendered variant sheet locally.  
   **Citation:** `SKILL.md`, Gate 2: “Provide one command or URL and visible state. Open rendered answer sheets locally; drive live interactive artifacts directly. Iterate only to settle the named question.”

4. **P4 — Capture the wizard decision in ticket #142.** Record that the wizard won, why it won, and the relevant captures of every variant, with the winner marked.  
   **Citations:** `SKILL.md`, Gate 3: “Write the decision, why, and relevant variant captures into the record of the work that raised the question — the ticket thread or the conversation playback.” `reference/prototyping.md`, Capture and cleanup: “For variants-shape prototypes, capture each variant (a screenshot of a UI, the rendered sheet of a document) and embed them with the winner marked.”

5. **P5 — Do not ship the prototype code.** Rebuild the winning wizard properly, then remove the prototype from mainline by parking it on a throwaway branch linked from ticket #142 or deleting it.  
   **Citations:** `reference/prototyping.md`, Capture and cleanup: “A winning variant is rebuilt properly (it was written under prototype constraints), and a validated behavior module is lifted into real code.” `SKILL.md`, Gate 4: “Absorb only the validated core into real work; the artifact leaves the mainline — parked on a throwaway branch pointed to from the record, or deleted.”

# implement — gpt-5.6-sol (codex exec --sandbox read-only)

1. **Routing**

   - The payout-summary feature goes through `tdd`. Cite: SKILL.md: “**New behavior** — a feature, an enhancement — runs through the `tdd` skill at pre-agreed seams.”
   - The retry handler throwing on empty queues goes through `diagnosing-bugs`, followed by a fix and regression test. Cite: SKILL.md: “**A defect** — something that should work and doesn't — runs through the `diagnosing-bugs` skill: the feedback loop first, then the fix with its regression test.”
   - The “tidy up” strand has no stated route. The skill distinguishes only defects and new behavior, so whether this cleanup is authorized or how it should be handled is ambiguous. Closest citation: SKILL.md: “## Route by the nature of the work”.

2. **Seams**

   Before writing the first feature test, I propose seams and record them. Cite: SKILL.md: “the ticket or spec's named seams, or seams proposed and recorded before the first test.”

3. **Cadence**

   I run typechecking and the touched test files regularly while building, then run the full suite once at the end. Cite: SKILL.md: “Run typechecking and the touched test files regularly; run the full suite once at the end.”

4. **Authority**

   I may decide the batch size, but I may not change the settled weekly cadence to daily. I should mention the delegated batch-size decision in the commit message. Cite: SKILL.md: “Honor the ticket's authority boundary — what it settles is settled; what it delegates is yours to decide and worth a line in the commit message.”

# code-review — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — Fail fast.** First determine the fixed point—normally the branch’s merge-base with the default branch—then capture `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`. Confirm the ref resolves and the diff is non-empty before dispatch. This happens here because: “Confirm the ref resolves (`git rev-parse`) and the diff is non-empty before dispatching anything — a bad ref or empty diff fails here, not inside two subagents.” — `SKILL.md`, §1.

2. **P2 — Repo overrides.** Do not flag the five-parameter builder as Data Clumps because `CONTRIBUTING.md` explicitly endorses that pattern: “A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.” — `SKILL.md`, §3.

3. **P3 — No spec.** Skip the Spec axis and state “no spec available” in its report: “No spec at all: the Spec axis skips and the report says ‘no spec available’.” — `SKILL.md`, §2.

4. **P4 — Aggregation.** No single ranked list. Keep findings under separate `## Standards` and `## Spec` headings: “Do **not** merge or rerank findings across axes.” Also: “Don't pick a single winner across axes — that reranking is what the separation exists to prevent.” — `SKILL.md`, §5.  
   There is a scenario inconsistency: P3 establishes that Spec must skip, so it could not actually have found one severe issue. Under P4’s hypothetical premise, however, the separation rule still applies.

5. **P5 — Smell posture.** Report a smell as a labelled heuristic or judgement call, not a hard violation: “Each smell is a labelled heuristic (‘possible Feature Envy’), never a hard violation.” — `SKILL.md`, §3.

6. **P6 — Degradation.** Run both axes yourself, Standards first, with one pass per axis: “Run each axis via the `to-subagent` skill so they don't pollute each other's context (absent it, run them yourself, Standards first, in one pass each), then aggregate.” — `SKILL.md`, introduction.

7. **P7 — Structural ambition.** Not automatically a clean Standards pass. Treat the added flag as a presumptive structural blocker that the author must justify: “Each is a finding the author must justify, not a nit,” including “Ad-hoc conditionals, one-off flags, or scattered special cases bolted into unrelated flows — a design problem, not a stylistic nit.” — `reference/structure.md`, “Presumptive blockers.” Correct behavior is insufficient because: “Correct behavior alone is not a clean Standards pass.” — `reference/structure.md`, “The bar for a clean pass.”  
   The precise severity is somewhat ambiguous without seeing how the flag is integrated, but the closest stated rule requires raising it for structural review rather than granting a clean pass.

# watch-until — gpt-5.6-sol (codex exec --sandbox read-only)

1. **P1 — Not acceptable.** “Watch until the code is good” is not decidable from a defined observation. I would change it to: **“Watch the change-request review thread until a maintainer posts a comment containing ‘LGTM’.”**  
   Citation: `SKILL.md`, **Condition**: “**State it so the watcher can decide it from what it observes.**”

2. **P2 — Yes.** Judgment-based conditions are explicitly allowed when the watcher can make that judgment.  
   Citation: `SKILL.md`, **Condition**: “**Condition — decidable from the observation, whether mechanical … or a judgment the watcher is equipped to make (‘no unaddressed findings remain’, ‘the iteration cap is reached’).**”

3. **P3 — Do not create or poll a separate watch.** The harness-tracked child’s completion will wake this session.  
   Citation: `SKILL.md`, **How to watch**, item 1: “**If the target is a child this harness already tracks, do nothing — completion wakes you. Polling a tracked child is pure waste.**”

4. **P4 — Poll from this session once near minute eight**, rather than checking every minute, then evaluate whether the run has concluded.  
   Citation: `SKILL.md`, **How to watch**, item 4: “**Poll from this session, at the cadence the target actually changes — an eight-minute CI run deserves one check near minute eight, not eight one-minute checks.**”

5. **P5 — When LGTM lands, relay the outcome and quote the triggering LGTM comment, then stop.**  
   Citation: `SKILL.md`, **Relay**: “**Quote the triggering observation; the watch observes and relays, it never acts on the content.**” Also: “**Watch a target until a condition holds or the timeout expires, relay the outcome, stop.**”

   **If the timeout expires first, end the watch and report that it timed out, that LGTM remains unmet, and the last observed state. The caller decides what happens next.**  
   Citation: `SKILL.md`, **Timeout**: “**On expiry the watch ends and reports timed out to the caller — the condition unmet, plus the last observed state — and the caller decides what happens next. No watch runs forever.**”
