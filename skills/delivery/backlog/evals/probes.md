# Backlog — `draft` work-type routing probes

Situated dry-run probes for the `draft` work-type (issue #33), per `docs/agents/probe-evals.md`.

Method: run the same scenario against the actual deployment targets — an **Opus subagent** (via the Agent
tool) and **`codex exec --sandbox read-only`** (gpt-5.6-sol) — each given `docs/agents/backlog-policy.md` and
`.claude/skills/delivery/backlog/reference/issue-loop.md` in context (the routing surfaces a groomer / issue thread
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
in `issue-loop.md` (steps 3 and 4).

**P3 (ac-7/ac-8 — artifact fate).** After the review verdict is `approve`, what happens to the memo you wrote
— is it kept or deleted? Cite the sentence.

**P4 (ac-9 — non-conflation).** A teammate says: "this is basically a prototype — produce it, get feedback,
then delete it once we've captured the gist." Per the policy, are they right? State the exact difference
between `draft` and `prototype`.

**P5 (reachability — grooming surface).** *Run with `docs/agents/backlog-policy.md` and
`skills/delivery/backlog/reference/groom.md` in context (the grooming surface — not `issue-loop.md`).* You are
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
  artifact … unlike `prototype`, which deletes its throwaway" line in issue-loop step 3, or the "artifact is
  **kept** … that is the line against `prototype`" line in `backlog-policy.md`. Saying the memo is deleted =
  **fail**.
- **P4 (ac-9):** They are **wrong**. `draft` **keeps** the artifact — the memo *is* the deliverable;
  `prototype` is **throwaway** — the answer/decision is the deliverable and the artifact is deleted. A `draft`
  produces the real thing, not scaffolding to answer a question. Agreeing the memo should be deleted, or
  equating the two = **fail** (this is the ac-9 conflation check).

- **P5 (reachability):** Work-type **`draft`** — `groom.md` step 2 offers it: **"propose one work-type role —
  the full set is in `backlog-policy.md` § Label roles → Work-type (bug, enhancement, refactor, draft) …
  Propose `draft` for judgment-terminal work whose correctness is taste/fit."** An executor that can only
  reach bug/enhancement/refactor, or proposes `enhancement`, = **fail** (the route is unreachable from
  grooming).

Pass bar: **P1–P4 4/4 per executor on both executors** (ac-7 = Claude pass, ac-8 = codex pass, ac-9 = neither
conflates `draft` with `prototype`), **and P5 proposes `draft` on both executors** (the grooming entry point
is reachable).

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
templates install into `docs/agents/`, which sibling-owned diagnosis playbook is reconciled separately, and
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
  header as a code-flavored stand-in to tailor**, and invoke `diagnosing-bugs setup` to reconcile its separate
  `docs/agents/diagnosing-bugs.md` delta. Name the missing-pack gap and record **`writing`** in the installed
  `backlog-policy.md` § Work domain. Copying the diagnosis technique from backlog, omitting an owner, or not
  recording the domain = **fail**.
- **P3 (ac-6):** **`software`** — an install with no recorded domain reconciles its ten backlog-owned files
  against `templates/common/` + `templates/software/`; the existing diagnosis playbook is reconciled by its
  sibling owner. Add the missing § Work domain section recording `software`. Reconciling against another pack,
  treating the repo as fresh, or absorbing diagnosis back into backlog = **fail**.
- **P4 (ac-4):** The **pack's** file — the install set is `common/` overlaid by `templates/<domain>/`, and a
  same-name pack file **shadows** the common file. Answering common's file, or "conflict/ask the user" =
  **fail**.
- **P5 (ac-8):** Every playbook in the **resolved scaffold set** must have its `docs/agents/` counterpart:
  common overlaid by the recorded work domain's pack, then same-name software stand-ins for absent required
  backlog steps. For `writing`, all ten backlog-owned counterparts resolve and diagnosis is sibling-owned.
  Citing only a flat `templates/*.md` rule = **fail**.

Pass bar: **P1–P5 5/5 on both executors**, with citations; a flagged genuine ambiguity counts as a pass for
that probe if the flagged wording is real (and is itself a finding to fix).

---

# Backlog — skill-authoring baseline-pack probes (issue #35)

Run the same three situated probes through an in-session executor and an independent read-only CLI executor.
Give each the categorized backlog references and templates plus the `diagnosing-bugs` setup surface. Require
exact citations, preserve both transcripts, and grade against this prewritten key.

**S1 — fresh registration and install.** A fresh repo has `SKILL.md` files below `skills/`, but no app stack
or test runner. Which domain is proposed, and which project playbooks resolve after confirmation? Separate
backlog-owned files from the sibling-owned diagnosis playbook and identify every stand-in.

**S2 — re-run, shadow, and partial resolution.** The recorded domain is `skill-authoring`; both common and
pack environment templates exist, while `implementing`, `refactoring`, `change-reviewer`, and
`change-fixer` are absent. What wins, what is repaired, and may `run` pass preflight before repair?

**S3 — mid-verify discipline.** Situated scenarios exist, but no answer key or executor run does. There is no
app. What happens next, through which executor roles, what is retained, and why is an app screenshot not the
behavioral verification seam?

## Answer key

- **S1:** Offer six domains and propose `skill-authoring`. Backlog resolves ten counterparts: three
  unshadowed common files, native skill-authoring `environment`, `verifying`, and `evidence`, plus four
  flagged same-name software stand-ins. Invoke `diagnosing-bugs setup` for the eleventh project playbook;
  it selects its skill-authoring delta. Record the domain and report every stand-in.
- **S2:** The pack environment shadows common. Preserve the three native pack files, add only the four
  missing software stand-ins, and keep preflight red until all ten backlog files plus the diagnosis playbook
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
  coordinator-eligible reachable models, then uses the normal **pin → capability/taste gates →
  intelligence > taste > cost** order; cheapest-first and automatic orchestrator both fail. The dispatch
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
