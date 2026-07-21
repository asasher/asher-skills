# Backlog — `draft` and `research` work-type routing probes

Situated dry-run probes for the `draft` and `research` work-types, per `docs/agents/probe-evals.md`.

Method: run the same scenario against the actual deployment targets — an **Opus subagent** (via the Agent
tool) and **`codex exec --sandbox read-only`** (gpt-5.6-sol) — each given `docs/agents/backlog-policy.md` and
`skills/delivery/backlog/reference/build-loop.md` in context (the routing surfaces a groomer / issue thread
reads). Require the executor to **cite the file and the exact sentence** that decided each answer, and to
**flag ambiguity as a valid answer**. Grade pass/fail against the key below, which is written before any runs
and keys on `plans/33-draft-work-type.html` acceptance criteria **ac-7..ac-9** — the plan is the source of
truth.

## Scenario

A backlog issue, groomed `ready-for-agent`, reads:

> **Write the v2 launch announcement memo for the blog** — 3–4 paragraphs, in our voice, covering what
> shipped and why it matters.

It carries no code changes and names no test.

## Probes

**P1 (ac-7/ac-8 — classification).** Which work-type does this issue take, and why? Name the role and cite the
sentence in `backlog-policy.md` that decides it.

**P2 (ac-7/ac-8 — definition of done).** You are the issue thread working this issue. What event tells you it
is complete — what is its definition of done? Does a mechanical `verify` pass/fail gate it? Cite the routing
in `build-loop.md` (steps 3 and 4).

**P3 (ac-7/ac-8 — artifact fate).** After the review verdict is `approve`, what happens to the memo you wrote
— is it kept or deleted? Cite the sentence.

**P4 (ac-9 — non-conflation).** A teammate says: "this is basically a prototype — produce it, get feedback,
then delete it once we've captured the gist." Per the policy, are they right? State the exact difference
between `draft` and `prototype`.

**P5 (reachability — grooming surface).** *Run with `docs/agents/backlog-policy.md` and
`skills/delivery/backlog/reference/groom.md` in context (the grooming surface — not `build-loop.md`).* You are
grooming this issue (it is not yet labelled). Which work-type role do you propose, and cite the sentence in
`groom.md` that lets you propose it. This probe fails if `groom.md` only offers bug/enhancement/refactor.

## Answer key

- **P1 (ac-7/ac-8):** Work-type **`draft`** — the deliverable is a novel artifact judged by taste/fit (a
  memo) with no testable spec. Cite the `draft` work-type bullet or the "Recognizing `draft`" note in
  `backlog-policy.md` ("groom to `draft`, not `enhancement`"). Answering `enhancement` / `bug` / `refactor` =
  **fail**.
- **P2 (ac-7/ac-8):** Done is the **human review verdict** at the review gate — the `review-loop` `approve`
  from step 3 (**"the human review verdict is the definition of done"**). **No** mechanical `verify`
  pass/fail: step 4's draft exception says the step is skipped and "degenerates to 'the review gate passed'."
  Claiming acceptance criteria are run through `verify` = **fail**.
- **P3 (ac-7/ac-8):** The memo is **kept** — committed to the work branch (and merged). Cite the "**Keep** the
  artifact … unlike `prototype`, which deletes its throwaway" line in build-loop step 3, or the "artifact is
  **kept** … that is the line against `prototype`" line in `backlog-policy.md`. Saying the memo is deleted =
  **fail**.
- **P4 (ac-9):** They are **wrong**. `draft` **keeps** the artifact — the memo *is* the deliverable;
  `prototype` is **throwaway** — the answer/decision is the deliverable and the artifact is deleted. A `draft`
  produces the real thing, not scaffolding to answer a question. Agreeing the memo should be deleted, or
  equating the two = **fail** (this is the ac-9 conflation check).

- **P5 (reachability):** Work-type **`draft`** — `groom.md` step 2 offers it: **"propose one work-type role —
  the full set is in `backlog-policy.md` § Label roles → Work-type (bug, enhancement, refactor, research, draft) …
  Propose `draft` for judgment-terminal work whose correctness is taste/fit."** An executor that can only
  reach bug/enhancement/refactor, or proposes `enhancement`, = **fail** (the route is unreachable from
  grooming).

Pass bar: **P1–P4 4/4 per executor on both executors** (ac-7 = Claude pass, ac-8 = codex pass, ac-9 = neither
conflates `draft` with `prototype`), **and P5 proposes `draft` on both executors** (the grooming entry point
is reachable).

## Research work-type scenario

A backlog issue reads:

> **Establish how Wayfinder works before we decide whether to adopt it.** Inspect its upstream skill source,
> tracker adapters, and related skills at a pinned commit. Produce a cited dossier that separates direct
> observations from inferences and unresolved questions. Do not implement or recommend adoption.

The repo's `docs/agents/researching.md` binds durable dossiers to `research/<slug>/`.

**R1 — classification.** Which work-type does grooming propose, and why is this not `draft` or `enhancement`?

**R2 — ownership.** In the build loop, which skill owns framing, source work, fan-out, reconciliation, dossier,
and audit? Which lifecycle responsibilities remain with backlog?

**R3 — verification.** Does the product-behavior verify loop run? What gate replaces it, and what condition
would reveal that the issue was misclassified?

**R4 — evidence boundary.** After review, where does the dossier remain? Should the thread copy the report or
its citations into `evidence/` because a human reviewed it?

**R5 — substage boundary.** Change the issue to “adopt Wayfinder in this repo, researching its tracker model
first.” Which work-type owns the issue, and how is research used?

### Research answer key

- **R1:** `research`: the terminal question is what primary sources establish, with traceability and a claim
  audit. It is not `draft` because taste/voice is not the definition of done, and not `enhancement` because no
  behavior changes. Cite `backlog-policy.md` and `groom.md`.
- **R2:** The `research` sibling owns the epistemic work and returns the canonical path, answer, gaps,
  boundary, and audit. Backlog retains branch, tracker state, commit, PR, review, and closure. Cite build-loop
  step 3.
- **R3:** Product verification does not run; the research claim audit accounts for every material claim and
  gap. If product behavior also changes, return to grooming because the issue is misclassified. Cite step 4.
- **R4:** Keep the dossier under `research/<slug>/`. Its citations/audit are intrinsic provenance; do not copy
  it into `evidence/` merely because it was reviewed. Cite step 7 and the project playbooks.
- **R5:** `enhancement` owns the behavior change and invokes `research` as a substage before planning/decision.
  A research subproblem does not replace the issue's terminal work type. Cite the policy boundary note.

Pass bar: R1–R5 5/5 on both executors with citations.

---

# Backlog — setup work-domain probes (issue #32)

Situated dry-run probes for the work-domain question and domain baseline packs in `backlog setup`, per
`docs/agents/probe-evals.md`. Written before the change landed (test-first): against the pre-change
`setup.md` — which never asks a domain and scaffolds a flat `templates/` — P1, P2, and P4 have no
satisfiable citation, which is the recorded red baseline.

Method: run the same probes against both deployment executors — a **Claude subagent** (Agent tool) and
**`codex exec --sandbox read-only`** (gpt-5.6-sol) — each given the post-change
`skills/delivery/backlog/reference/setup.md`, a file listing of `skills/delivery/backlog/templates/`,
`skills/delivery/backlog/templates/common/backlog-policy.md`, and the `diagnosing-bugs` setup surface in context (P5 additionally gets
`skills/delivery/backlog/reference/run.md`). Require the executor to **cite the file and the exact sentence** that
decided each answer, and to **flag ambiguity as a valid answer**. Grade pass/fail against the key below,
written before any runs; it keys on `plans/32-setup-domain-packs.html` acceptance criteria ac-3..ac-6 and
ac-8 — the plan is the source of truth.

## Probes

**P1 (ac-3 — the question).** You are running `backlog setup` step 2 on a fresh repo: a novel manuscript —
prose chapters under `manuscript/`, no `package.json`, no `src/`, no test runner; `docs/agents/` is empty.
What do you ask the user before scaffolding any playbook, what options do you offer, and what default do
you propose for this repo? Cite the sentence that decides each part.

**P2 (ac-4/ac-5 — what installs).** Continuing P1, the user confirms `writing`. Exactly which backlog-owned
templates install into `docs/agents/`, which sibling-owned diagnosis and research playbooks are reconciled separately, and
what do you flag or report? Where is the chosen domain recorded? Cite the sentences.

**P3 (ac-6 — legacy re-run).** You re-run `backlog setup` on a repo whose `docs/agents/` already holds all
eleven playbooks, installed by an older backlog version; its `backlog-policy.md` has no Work-domain
section. Which work domain do you reconcile against, which template set does that give you, and what do you
write into the installed `backlog-policy.md`? Cite the sentence.

**P4 (ac-4 — the shadow rule).** Suppose a future `templates/writing/` pack ships and includes its own
`change-description.md`; `templates/common/` also ships one. Installing for domain `writing`, which of the
two files lands in `docs/agents/change-description.md`, and why? Cite the rule.

**P5 (ac-8 — run preflight).** *Also given `skills/delivery/backlog/reference/run.md`.* `backlog run` starts on a
repo whose recorded work domain is `writing`. Per run's step-1 preflight, which templates must have
`docs/agents/` counterparts for the loop to proceed? Cite the completion criterion.

## Answer key

- **P1 (ac-3):** Ask the work-domain question **before any scaffolding**, with the current **six options —
  software / skill-authoring / writing / research / ops / general** — and propose **`writing`** as the default: the repo's
  evidence (prose manuscript, no code) is unambiguous, and the posture is confirm-not-interrogate.
  Not asking; a different option set; or proposing `software` despite the prose evidence = **fail**.
  (`software` is the default only when evidence is ambiguous; the skill-authoring option does not change
  this manuscript's default.)
- **P2 (ac-4/ac-5):** Install the **four `templates/common/` playbooks** plus — because no `writing` pack
  ships yet — the **six `templates/software/` step playbooks as stand-ins**, each **flagged in its installed
  header as a code-flavored stand-in to tailor**, then invoke `diagnosing-bugs setup` and `research setup` to
  reconcile their separate `docs/agents/diagnosing-bugs.md` and `docs/agents/researching.md` deltas. Name the
  missing-pack gap and record **`writing`** in the installed `backlog-policy.md` § Work domain. Copying either
  sibling method from backlog, omitting an owner, or not
  recording the domain = **fail**.
- **P3 (ac-6):** **`software`** — an install with no recorded domain reconciles its ten backlog-owned files
  against `templates/common/` + `templates/software/`; the existing diagnosis playbook and newly required
  research playbook are reconciled by their sibling owners. Add the missing § Work domain section recording
  `software`. Reconciling against another pack, treating the repo as fresh, or absorbing a sibling method back
  into backlog = **fail**.
- **P4 (ac-4):** The **pack's** file — the install set is `common/` overlaid by `templates/<domain>/`, and a
  same-name pack file **shadows** the common file. Answering common's file, or "conflict/ask the user" =
  **fail**.
- **P5 (ac-8):** Every playbook in the **resolved scaffold set** must have its `docs/agents/` counterpart:
  common overlaid by the recorded work domain's pack, then same-name software stand-ins for absent required
  backlog steps. For `writing`, all ten backlog-owned counterparts resolve and diagnosis/research are sibling-owned.
  Citing only a flat `templates/*.md` rule = **fail**.

Pass bar: **P1–P5 5/5 on both executors**, with citations; a flagged genuine ambiguity counts as a pass for
that probe if the flagged wording is real (and is itself a finding to fix).

---

# Backlog — skill-authoring baseline-pack probes (issue #35)

Run the same three situated probes through an in-session executor and an independent read-only CLI executor.
Give each the categorized backlog references and templates plus the `diagnosing-bugs` and `research` setup surfaces. Require
exact citations, preserve both transcripts, and grade against this prewritten key.

**S1 — fresh registration and install.** A fresh repo has `SKILL.md` files below `skills/`, but no app stack
or test runner. Which domain is proposed, and which project playbooks resolve after confirmation? Separate
backlog-owned files from the sibling-owned diagnosis and research playbooks and identify every stand-in.

**S2 — re-run, shadow, and partial resolution.** The recorded domain is `skill-authoring`; both common and
pack environment templates exist, while `implementing`, `refactoring`, `change-reviewer`, and
`change-fixer` are absent. What wins, what is repaired, and may `run` pass preflight before repair?

**S3 — mid-verify discipline.** Situated scenarios exist, but no answer key or executor run does. There is no
app. What happens next, through which executor roles, what is retained, and why is an app screenshot not the
behavioral verification seam?

## Answer key

- **S1:** Offer six domains and propose `skill-authoring`. Backlog resolves ten counterparts: three
  unshadowed common files, native skill-authoring `environment`, `verifying`, and `evidence`, plus four
  flagged same-name software stand-ins. Invoke `diagnosing-bugs setup` and `research setup` for the eleventh
  and twelfth project playbooks; diagnosis selects its skill-authoring delta and research binds the repo's
  research root/sources. Record the domain and report every stand-in.
- **S2:** The pack environment shadows common. Preserve the three native pack files, add only the four
  missing software stand-ins, and keep preflight red until all ten backlog files plus the diagnosis and research playbooks
  exist. Silent fallback, replacing pack files, or letting backlog write diagnosis fails.
- **S3:** Write the answer key first; run the same scenario through an in-session executor and an independent
  read-only CLI executor; require citations; preserve both transcripts; and grade every prewritten criterion
  in a verdict table. Executor-harness probes are the skill-behavior surface. Scripts are driven directly and
  rendered artifacts are added only when the skill produces a visual surface.

Pass bar: **S1–S3 3/3 on both executors**, with exact citations and the per-probe verdict table retained.

---

## Issue #48 — issue-coordinator dispatch probes

Run these situated probes with `reference/groom.md`, `reference/run.md`, and the staffing routing references.
The key below is fixed before execution.

**D1 — routine issue.** A ready bug is groomed with surface `backend`, coordination class `routine`, and the
reason “reproduction and acceptance seam are already named.” When is its coordinator selected relative to
worktree/thread creation, what inputs are passed, and how is the model chosen?

**D2 — orchestrator required.** An enhancement is marked `orchestrator-required` because one expensive,
unsettled product decision remains. Who coordinates it, and what successor is recorded?

**D3 — missing dispatch metadata.** A ready refactor has a work type but no surface or coordination class.
Does `run` infer them or create an orchestrator child as a safe default?

### Answer key

- **D1:** Before creating either worktree or child, `run` calls `staffing` with work type, surface,
  coordination class/reason, known uncertainty, and required capabilities. `routine` filters to
  coordinator-eligible reachable models, then uses **pin → provider/fallback → eligible executor → taste
  gate → intelligence > taste > cost**; cheapest-first and automatic orchestrator both fail. The dispatch
  record names the chosen coordinator and session orchestrator as upward successor.
- **D2:** `orchestrator-required` routes to the session orchestrator, with the next reachable orchestrator
  succession named for route failure. It does not first start a cheaper coordinator and hope it escalates.
- **D3:** Skip and report a grooming gap. No worktree, child, or in-flight claim is created; neither inference
  nor default-orchestrator dispatch passes.

Pass bar: 3/3 per executor with citations. Structural confirmation checks that `run.md` calls staffing before
either creation verb, no longer says every issue dispatches on the orchestrator role, and the policy template
plus dogfood playbook define all dispatch metadata fields.

---

## Issue #55 — loop-refinement probes

Run these with `reference/diagnose.md`, `reference/verify.md`, `reference/evidence.md`,
`reference/adversarial-review.md`, `reference/run.md`, `reference/run-state.md`, `reference/setup.md`, and both
the source and installed platform/reviewer/evidence playbooks. The key is fixed before the remaining behavior
edits.

**R1 — guarded direct fix.** A human reports an observable dark-theme styling defect and names the wrong
token. A second fixture looks equally obvious, but the first fix leaves the symptom unchanged. Route both.

**R2 — styling evidence reuse.** Verification captured the styling result. Review changes no product code;
compare that case with HEAD, fixture, or environment drift before merge.

**R3 — native dependencies.** Setup binds GitHub, then `run` sees an issue whose native blocked-by count is
one. What verbs are recorded, what happens now, and what happens after the edge clears? Contrast a tracker
whose native relation cannot be exercised.

**R4 — terminal handoff.** A run completes normally; another exhausts its harness limit. What durable outputs
must each leave, where, and what must a fresh Claude or Codex session do before dispatch?

**R5 — behavior ruling.** Reviewer finds a genuine product-semantics question outside the approved plan.
Who may rule, who edits, what is reverified, and who reviews the new HEAD?

### Answer key

- **R1:** The first case may take direct fix only with the human report, observable visual/copy symptom, and
  named styling/copy cause; it gets appropriate visual verification (both themes for theme-sensitive work).
  The unchanged symptom is the first contradictory observation: preserve it and invoke `diagnosing-bugs`
  rather than making another direct guess.
- **R2:** Reuse passes only when the capture HEAD is the final reviewed HEAD and Reviewer records
  “no product-code change; no recapture.” Any product-code, fixture, environment, or HEAD drift requires fresh
  final-HEAD evidence.
- **R3:** GitHub records the issue read exposing `.issue_dependencies_summary` and the native `blocked_by`
  write using the blocker's numeric issue id. A positive unresolved count keeps the issue out of the wave;
  zero after edge removal releases it. An unavailable native relation records and uses an explicit fallback,
  never an invented command.
- **R4:** Both terminal paths write the tracker handoff table and atomic `handoff.md` under the shared run
  root with state pointers, learned protocols, environment/resources, cleanup debts, blockers, and
  `not_before`. A fresh session audits tracker/refs/worktrees/events/processes against the checkpoint and
  handoff without relying on chat memory.
- **R5:** Reviewer makes no edit and sends evidence to the issue coordinator. The coordinator rules only
  inside the approved plan; otherwise it escalates to the session orchestrator/human. Fixer receives the
  explicit ruling, edits, runs targeted reverification, and returns the new HEAD to the same Reviewer.

Pass bar: 5/5 per executor with citations. Structural checks require synchronized source/dogfood dependency,
reviewer, and evidence contracts and no direct-fix loop that omits the contradictory-observation fallback.

---

## Issue #54 — setup verification-data probe

**V1.** Setup finds one admin account, no second tenant, a real-fixture ceiling of 100 records, and an
approved synthetic scale fixture. What must it record before declaring verification ready, including fixture
ownership and lifetime?

### Answer key

PASS only if setup records standing accounts/tenants and permissions, real scale affordances/limits, the
approved synthetic substitute and where it is not valid, collision-safe per-issue fixture names, retention
through final evidence, named cleanup ownership, and any unmet criterion class as a blocker. Inventing a
second account or deferring the inventory to verify fails.

---

## Issue #60 — cross-harness wrapper probe

Run with `reference/setup.md` and `templates/common/platform.md`.

**W1.** Backlog setup binds a Claude→Codex route and a Codex→Claude route. For each, what owns the native
agent-tree node, how is it named and staffed, what work may it do, who verifies the requested effect, and what
finding remains if the native spawn API cannot select or report the wrapper model?

### Answer key

PASS only if every sibling CLI is nested in a watched native wrapper named with external model/task and
staffed by the cheapest native model allowed by the current floor. The wrapper only supervises the bounded
non-interactive process and relays raw output plus lifecycle status; the parent owns prompt, judgment, and
effect verification. Missing wrapper-model selection/report keeps floor/cost compliance unproven even when
observability and relay pass. Direct CLI dispatch, wrapper synthesis, or claiming cheapest-model proof from
exit zero fails.

## Enhancement degating probes (issue #80)

Situated dry-run probes for the decoupled enhancement route: no in-run planning gate, groom's route judgment,
and the `needs-spec` handback. Same method as above — run each probe against both executors (Claude subagent
via the Agent tool, and `codex exec --sandbox read-only` on gpt-5.6-sol), with only the named surfaces in
context, requiring file + exact-sentence citations. Key written before any runs; keys on issue #80's
acceptance criteria.

### Scenario D — dispatched enhancement (surfaces: `reference/build-loop.md` + `docs/agents/backlog-policy.md`)

You are the issue thread for a `ready-for-agent` → `in-flight` **enhancement**. Its grooming comment carries a
complete Dispatch block including `route: direct — decisions settled in linked spec #91; UI copy delegated to
the thread`. The linked spec records the schema and UX decisions and the acceptance criteria.

**P-D1 (no gate).** You reach step 3 and route on `enhancement`. Is there any point before implementation
where you invoke a planning skill or pause for a human planning approval? What do you produce before
following `reference/implement.md`, and where is it recorded? Cite the enhancement bullet.

**P-D2 (invalidation handback).** Mid-implement you discover the spec's recorded schema decision cannot work
(the platform API it assumed does not exist). Name the exact state you apply, the other actions you take, and
what you do **not** do. Cite the sentences.

**P-D3 (delegated vs strategic).** Two questions arise: (a) which of two equivalent list-virtualization
libraries to use; (b) whether the feature should also be shown to anonymous users. For each: settle it
yourself, prototype it, or hand back? Cite the authority language.

### Scenario E — grooming surface (surfaces: `reference/groom.md` + `docs/agents/backlog-policy.md`)

An open issue reads: "**Add gamification to the driver app** — make deliveries feel rewarding. Streaks?
Badges? Leaderboard?" It has no spec link, no recorded decisions, and the human, asked, says "good question —
I need to think about what we actually want."

**P-E1 (route stamp).** Which readiness role does this issue get, and why is it not `needs-info` and not
`ready-for-agent`? Cite the route-judgment sentence.

**P-E2 (admission contract).** What must an `enhancement`'s dispatch record contain before `ready-for-agent`
may be applied? Cite § Dispatch metadata.

### Scenario F — run surface (surfaces: `reference/run.md` + `docs/agents/backlog-policy.md`)

**P-F1 (run never pauses).** During an AFK run on the local tracker binding, an issue thread reports back:
"strategic decision invalidated — handing back." What does the run thread write, and does any planning
approval gate open mid-run? Cite step 6.

### Answer key (issue #80)

- **P-D1:** **No** planning skill, **no** human planning gate — "There is no in-run planning approval gate."
  Before `implement.md` the thread drafts a **just-in-time tactical plan**, "scoped to this ticket, inside
  the delegated authority, recorded in the thread and reflected in the PR body; never a human gate."
  Invoking a `plan` skill, or pausing for approval = **fail**.
- **P-D2:** Apply **`needs-spec`** (not `needs-info`, not `ready-for-human`): record the finding on the
  issue, drop the in-flight claim, tell the run thread, open **no PR** (step 2 handback + "implementation
  **invalidates** an approved decision … hand it back as `needs-spec`"). Not done: settling the product
  question in-thread ("do not settle it here"), or a planning session. Choosing `needs-info`, deciding the
  new schema alone, or opening a PR anyway = **fail**.
- **P-D3:** (a) is **within delegated authority** → settle it in the tactical plan (a prototype is allowed:
  "only for questions **within the issue's delegated authority**"). (b) is **strategic** (product scope) →
  `needs-spec` handback: "A strategic question is a `needs-spec` handback, never a prototype session."
  Prototyping (b), or handing back (a) = **fail**.
- **P-E1:** **`needs-spec`** — the route judgment: the enhancement is not **direct-executable** (product
  decisions neither settled nor delegated), and the human cannot settle them in this conversation. Not
  `needs-info` (the reporter owes no facts; the *product owner* owes shaping), not `ready-for-agent` (no
  route judgment possible). `ready-for-agent`, `needs-info`, or inventing the gamification design = **fail**.
- **P-E2:** Surface (+capabilities), coordination class, coordination reason, **and** the
  `route: direct — <why settled/delegated>` line; "A `ready-for-agent` enhancement without it is a grooming
  gap." Omitting route = **fail**.
- **P-F1:** The run thread, as serialized writer, clears `in-flight` and sets **`needs-spec`** with the
  reported comment ("`needs-spec` for unsettled or invalidated strategic decisions"), and the run
  **continues** — no planning gate exists to open. Pausing the run for approval, or setting `needs-info` =
  **fail**.

Pass bar: **P-D1–P-F1 6/6 on both executors.** Ambiguity flagged with a citation is a valid answer only where
the surfaces genuinely conflict; the surfaces above are expected to decide every probe.

## Seam probes (issues #87/#85)

Surfaces: `SKILL.md` (§ Seams) + `docs/agents/verifying.md`. Key written before any runs.

**P-S1 (queue of one).** The user says "just build #42 with me now — skip the whole backlog machinery." Is a
separate mechanism needed? What is this invocation, exactly? Cite.

**P-S2 (criteria without a ticket).** In an interactive chat-and-build with no ticket, where does verify get
its pass/fail criteria? Cite.

**P-S3 (UI gate).** A UI ticket's build is done; the project's `external-dependencies.lock.json` records
impeccable. What runs before the PR is review-ready, and what happens to P0/P1 findings? Cite.

### Answer key

- **P-S1:** No new mechanism — "A queue of one is a first-class invocation: `backlog run <issue>` is the
  interactive chat-and-build shape — the same build loop, no waves." Inventing a lighter path that skips the
  dev tail = **fail**.
- **P-S2:** From "the criteria the build loop wrote into the PR body at its start — verify always has a
  target, even without a ticket." Claiming verify is skipped without a ticket = **fail**.
- **P-S3:** The UI-state sweep (happy/empty/loading/error/disabled/responsive + accessibility basics) and
  impeccable's `critique`/`audit` as scored gates, with "P0/P1 findings … routed back into the fix loop
  before the PR is called review-ready." Calling it review-ready with open P0s = **fail**.

Pass bar: 3/3 on both executors.
