# Backlog — `draft` work-type routing probes

Situated dry-run probes for the `draft` work-type (issue #33), per `docs/agents/probe-evals.md`.

Method: run the same scenario against the actual deployment targets — an **Opus subagent** (via the Agent
tool) and **`codex exec --sandbox read-only`** (gpt-5.6-sol) — each given `docs/agents/backlog-policy.md` and
`.claude/skills/backlog/reference/issue-loop.md` in context (the routing surfaces a groomer / issue thread
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
`skills/backlog/reference/groom.md` in context (the grooming surface — not `issue-loop.md`).* You are
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
`skills/backlog/reference/setup.md`, a file listing of `skills/backlog/templates/`, and
`skills/backlog/templates/common/backlog-policy.md` in context (P5 additionally gets
`skills/backlog/reference/run.md`). Require the executor to **cite the file and the exact sentence** that
decided each answer, and to **flag ambiguity as a valid answer**. Grade pass/fail against the key below,
written before any runs; it keys on `plans/32-setup-domain-packs.html` acceptance criteria ac-3..ac-6 and
ac-8 — the plan is the source of truth.

## Probes

**P1 (ac-3 — the question).** You are running `backlog setup` step 2 on a fresh repo: a novel manuscript —
prose chapters under `manuscript/`, no `package.json`, no `src/`, no test runner; `docs/agents/` is empty.
What do you ask the user before scaffolding any playbook, what options do you offer, and what default do
you propose for this repo? Cite the sentence that decides each part.

**P2 (ac-4/ac-5 — what installs).** Continuing P1, the user confirms `writing`. Exactly which template
files do you install into `docs/agents/`, from which directories, and what do you flag or report beyond the
install? Where is the chosen domain recorded? Cite the sentences.

**P3 (ac-6 — legacy re-run).** You re-run `backlog setup` on a repo whose `docs/agents/` already holds all
eleven playbooks, installed by an older backlog version; its `backlog-policy.md` has no Work-domain
section. Which work domain do you reconcile against, which template set does that give you, and what do you
write into the installed `backlog-policy.md`? Cite the sentence.

**P4 (ac-4 — the shadow rule).** Suppose a future `templates/writing/` pack ships and includes its own
`change-description.md`; `templates/common/` also ships one. Installing for domain `writing`, which of the
two files lands in `docs/agents/change-description.md`, and why? Cite the rule.

**P5 (ac-8 — run preflight).** *Also given `skills/backlog/reference/run.md`.* `backlog run` starts on a
repo whose recorded work domain is `writing`. Per run's step-1 preflight, which templates must have
`docs/agents/` counterparts for the loop to proceed? Cite the completion criterion.

## Answer key

- **P1 (ac-3):** Ask the work-domain question **before any scaffolding**, with the current **six options —
  software / skill-authoring / writing / research / ops / general** — and propose **`writing`** as the default: the repo's
  evidence (prose manuscript, no code) is unambiguous, and the posture is confirm-not-interrogate.
  Not asking; a different option set; or proposing `software` despite the prose evidence = **fail**.
  (`software` is the default only when evidence is ambiguous; `skill-authoring` was registered after issue
  #32 and does not change this manuscript's default.)
- **P2 (ac-4/ac-5):** Install the **four `templates/common/` playbooks** plus — because no `writing` pack
  ships yet — the **seven `templates/software/` step playbooks as stand-ins**, each **flagged in its
  installed header as a code-flavored stand-in to tailor**, with the **gap named in the setup report**;
  record **`writing`** in the installed `backlog-policy.md` § Work domain. Leaving the seven uninstalled;
  installing them unflagged/silently; or not recording the domain = **fail**.
- **P3 (ac-6):** **`software`** — an install with no recorded domain reconciles as software, so the template
  set is `templates/common/` + `templates/software/` and nothing changes behavior; reconciliation adds the
  missing § Work domain section recording `software`. Reconciling against another pack, treating the repo
  as a fresh install, or leaving the domain unrecorded = **fail**. (Confirming the default with the user is
  acceptable; blocking on it as if unknown is not.)
- **P4 (ac-4):** The **pack's** file — the install set is `common/` overlaid by `templates/<domain>/`, and a
  same-name pack file **shadows** the common file. Answering common's file, or "conflict/ask the user" =
  **fail**.
- **P5 (ac-8):** Every playbook in the **resolved scaffold set** must have its `docs/agents/` counterpart:
  common overlaid by the recorded work domain's pack, then same-name software stand-ins for absent required
  steps. For `writing`, whose pack is unshipped, the software stand-ins are those counterparts, so the full
  eleven still resolve. Citing only a flat `templates/*.md` rule = **fail**.

Pass bar: **P1–P5 5/5 on both executors**, with citations; a flagged genuine ambiguity counts as a pass for
that probe if the flagged wording is real (and is itself a finding to fix).

---

# Backlog — skill-authoring baseline-pack probes (issue #35)

Situated dry-run probes for the `skill-authoring` work domain, partial-pack resolution, and skill-behavior
verification in `backlog setup` and `backlog run`, per `docs/agents/probe-evals.md`.

Method: run the same three probes against both deployment executors — an **in-session Claude subagent** and
**`codex exec --sandbox read-only`** — each given the post-change `skills/backlog/reference/setup.md`,
`skills/backlog/reference/run.md`, `skills/backlog/reference/verify.md`,
`skills/backlog/templates/common/backlog-policy.md`, the relevant
`skills/backlog/templates/skill-authoring/` playbooks, and a file listing of `skills/backlog/templates/`.
Require each executor to **cite the file and exact sentence** that decides every answer, and to **flag
ambiguity as a valid answer**. Preserve both cited transcripts and grade each probe criterion pass/fail
against the key below, written before any executor run; it keys on
`plans/35-skill-authoring-pack.html` acceptance criteria **ac-3, ac-6, ac-8, and ac-10..ac-14** — the plan
is the source of truth.

## Probes

**P1 (ac-8/ac-10/ac-11 — fresh registration and install).** You are running `backlog setup` on a fresh
repo with `skills/formatter/SKILL.md` and `skills/linter/SKILL.md`, but no app stack, source tree, or test
runner. What exact work-domain choices do you offer, which default do you propose, and what files resolve
into `docs/agents/` after the user confirms it? Identify every native source and every stand-in, including
what is flagged, reported, and recorded. Cite the deciding sentences.

**P2 (ac-10/ac-12/ac-13 — re-run, shadow, and partial resolution).** You re-run setup on a repo whose
recorded domain is `skill-authoring`. Both `templates/common/environment.md` and
`templates/skill-authoring/environment.md` exist. The installed playbooks corresponding to
`implementing.md`, `refactoring.md`, `change-reviewer.md`, and `change-fixer.md` are absent; all other
resolved counterparts are present. Which environment baseline wins, which skill-authoring files remain
native, which missing files are reconciled from software, and what must setup report? May `backlog run`
pass preflight before those four files exist? State the full counterpart count after repair and cite the
rules.

**P3 (ac-3/ac-6/ac-14 — mid-verify discipline).** A skill's situated probe scenarios have been written,
but there is no answer key and no executor has run them. The repo has no app or stack. You are about to
verify a behavior change. What must happen next, in what order, through which executor roles, what must each
run produce, and how is the result graded and retained as evidence? Explain how the shared setup and verify
paths ready and exercise this no-app surface without blocking on app access. A teammate proposes replacing
this with "drive the app and take a screenshot"; decide whether that is the skill-behavior verification seam
and cite the relevant playbooks and shared references.

## Answer key

- **P1 (ac-8/ac-10/ac-11):** Offer **exactly six options — software / skill-authoring / writing / research /
  ops / general** — and propose **`skill-authoring`** because the repo has `SKILL.md` files under
  `skills/<name>/`. Resolve **eleven counterparts**: the three unshadowed common files
  (`backlog-policy.md`, `platform.md`, `change-description.md`); the four native skill-authoring files
  (`environment.md`, `verifying.md`, `evidence.md`, `diagnosing-bugs.md`), with the pack environment
  shadowing common; and the four same-name software stand-ins (`implementing.md`, `refactoring.md`,
  `change-reviewer.md`, `change-fixer.md`). Every stand-in is header-flagged as code-flavored and every gap
  is named in the setup report; record `skill-authoring` in installed `backlog-policy.md` § Work domain.
  A five-value list, a `software` default, installing common environment, treating all seven software
  files as stand-ins, omitting a required step file, or silent/unflagged fallback = **fail**.
- **P2 (ac-10/ac-12/ac-13):** The **skill-authoring `environment.md` wins** the same-name shadow. Keep
  native skill-authoring `verifying.md`, `evidence.md`, and `diagnosing-bugs.md`; fill only the absent
  `implementing.md`, `refactoring.md`, `change-reviewer.md`, and `change-fixer.md` from their same-name
  software baselines, flag every installed stand-in, and name every gap in the setup report. **`run`
  preflight fails** until all four exist; after repair the resolved skill-authoring scaffold has **eleven
  counterparts** (three unshadowed common + four native pack + four stand-ins). Choosing common
  environment, replacing native pack files with software, passing preflight with seven files, or failing
  to flag/report the four gaps = **fail**.
- **P3 (ac-3/ac-6/ac-14):** **Write the answer key before any run**, then run the **same situated probes**
  through an **in-session executor** and an **independent CLI executor**. Require both to cite the deciding
  text and preserve both transcripts; grade each answer **per prewritten criterion** in a pass/fail verdict
  table, retaining the transcripts and table as evidence (and showing the relevant before/after verdict
  shift for a behavioral rework). "Drive the app" is **not** the skill-behavior seam: executor-harness
  probes replace it; scripts are still invoked directly, real CI is still recorded, and rendered artifacts
  are added only when the skill produces a visual surface. Running before keying, using only one executor,
  accepting uncited output, grading only an aggregate result, discarding transcripts, or substituting an
  app screenshot = **fail**. Shared setup must record the checked-in `evals/` scenarios as seed state,
  executor roles as the drivers, cited transcripts plus the verdict table as the evidence path, and a
  load-skill/submit-scenario exercise path — it must not require a nonexistent app or stack. Shared verify
  must ready that executor-harness surface with the scenario, deployment context, and prewritten key, then
  exercise and re-run criteria against that same surface. Blocking on app access or claiming that verify's
  stack/app wording overrides the skill-authoring playbooks = **fail**.

Pass bar: **P1–P3 3/3 on both executors**, with exact citations; a flagged genuine ambiguity counts as a
pass for that probe if the cited wording is genuinely ambiguous (and becomes a finding to fix). Retain both
executor transcripts and the per-probe verdict table.
