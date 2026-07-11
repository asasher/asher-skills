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

- **P1 (ac-3):** Ask the work-domain question **before any scaffolding**, with **exactly five options —
  software / writing / research / ops / general** — and propose **`writing`** as the default: the repo's
  evidence (prose manuscript, no code) is unambiguous, and the posture is confirm-not-interrogate.
  Not asking; a different option set; or proposing `software` despite the prose evidence = **fail**.
  (`software` is the default only when evidence is ambiguous.)
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
- **P5 (ac-8):** Every template in the **scaffold set — `templates/common/` plus the recorded work domain's
  pack** — must have its `docs/agents/` counterpart (for `writing`, whose pack is unshipped, the software
  stand-ins are those counterparts, so the full eleven still resolve). Citing only a flat `templates/*.md`
  rule = **fail**.

Pass bar: **P1–P5 5/5 on both executors**, with citations; a flagged genuine ambiguity counts as a pass for
that probe if the flagged wording is real (and is itself a finding to fix).
