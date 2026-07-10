# Plan — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `SKILL.md` in context, plus the one `reference/` file named by a probe
when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the
executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a
valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade
pass/fail against the key. **The answer key is written before any runs** and graded against the plan's
acceptance criteria (`plans/4-extract-plan.html`, ids ac-1..ac-10) — the plan is the source of truth; do not
grade against looser criteria.

The file-check criteria (ac-1, ac-3, ac-4, ac-5, ac-6, ac-7, ac-8, ac-10) are additionally confirmed by
grep/parse against the tree, as the staffing/review-loop evals do for their structural criteria. The probes
below exercise the *routing and understanding* of the contract where a reasoning probe adds value. Probes P1
through P5 are the **five core routing probes ac-9 names**; each must pass on **both** executors.

## Probes

**P1 (ac-9a, core).** You are asked to plan a **non-code effort** — a two-week competitor-research sprint.
Walk the gates: is `plan` willing to plan a non-code undertaking at all? When you reach the approval gate, how
do you present the plan for sign-off — do you build a review UI, or something else? Name the mechanism and
cite it.

**P2 (ac-9b, core).** A caller asks you to plan a **one-line copy fix** to a settings label — trivial,
reversible, a few minutes. What does gate 1 decide, and on what rule? Cite the threshold.

**P3 (ac-9c, core).** Mid-flow you need to decide **which model should author this plan**, and later who
should build what it describes. Does `plan` carry its own model ranking? What does it do instead? Name the
skill and cite the sentence.

**P4 (ac-9d, core).** `review-loop`'s await returned **request-changes** on your plan. What is the required
sequence before you re-present, and whose contract owns the ledger step? Be specific about what must be
written for each prior annotation. Cite it.

**P5 (ac-9e, core).** A human just **approved** your plan. What is the deliverable, and what must you **not**
do next? Is committing the plan or starting the implementation part of this skill? Cite the rule.

**P6 (ac-2).** A workflow skill wants to depend on `plan`. From `SKILL.md`, list the three kinds of
dependency pointer the skill declares, and state exactly which **sibling skills** it names and the role of
each.

**P7 (ac-3).** Does `plan` ship a review server or await script of its own? When it presents a plan, what
exactly does it invoke, and by what means — a file import or a name? Cite the convention.

**P8 (ac-4, ac-5).** Read `reference/plan-contract.md` **without** `SKILL.md`. Does the gate sequence include
a "commit the plan" or "start implementing" gate? Where do those steps live, and whose concern are they? Does
the contract assume the undertaking is code, or a running app? Cite the sentences.

**P9 (ac-6).** You are invoking `plan` in a repo that has **no `docs/agents/planning.md` and no review
surface**. Can the skill still run? What provides the threshold, format, and gates, and what happens at the
approval gate? Cite the two-layer / local-fallback rules.

**P10 (ac-7).** Read `templates/plan-skeleton.html`. Does it carry the stable-id contract (stable section
ids; `<li id="ac-N" data-criterion>` criteria)? Is it self-contained (inline styles/SVG, no external
fetches)? Does its header comment bake in any workflow-specific ("backlog") identity? Cite what you checked.

**P11 (ac-8).** Read `skills/plan/agents/openai.yaml`. Is it well-formed per `AGENTS.md` § Conventions (the `agents/openai.yaml` rule),
and is `allow_implicit_invocation` set correctly for a skill that runs a multi-gate flow and holds an
approval gate? State the value and why it is right.

**P12 (ac-10).** (Also read `skills/plan/README.md` for this probe — the non-breaking/deferral statement
lives there.) You just extracted `plan`. Does `backlog` still plan exactly as before, and did you touch its
`reference/plan.md` / `templates/planning.md` / `plan-skeleton.html`? What is explicitly deferred? Cite it.
(Note: the executor is not given `backlog`'s files; grade the *deferral claim and its citation*, and confirm
"backlog untouched" separately by the file-check below.)

## Answer key

- **P1 (ac-9a):** Yes — `plan` is **domain-neutral**; a research sprint is a valid undertaking (SKILL.md
  description / § domain-neutral). At the approval gate it does **not** build a review UI — it **presents the
  plan through the `review-loop` skill by name** (serve → annotate → verdict-coded await). Cite
  plan-contract.md § gate 4 / SKILL.md § Composition. Building an ad hoc review UI, or refusing a non-code
  undertaking, = fail.
- **P2 (ac-9b):** Gate 1 **decides to skip** — a small, low-risk, easily-reversible change does not earn a
  plan; go straight to the work. Rule: the plan-or-skip threshold (touches >1 area / hard to unwind / risky or
  >~1 day). Cite plan-contract.md § gate 1 "Decided". Answering "write a full plan" = fail.
- **P3 (ac-9c):** **No** — `plan` carries no roster of its own. It resolves "which model?" against the
  installed roster via the **`staffing`** skill by name, for both authoring and building. Cite SKILL.md
  § Dependency surface / plan-contract.md § Composition ("resolve against the installed roster via the
  `staffing` skill by name"). Inventing a ranking inline = fail.
- **P4 (ac-9d):** On **request-changes**: **revise the plan → write a ledger disposition
  (`changed`/`kept`/`orphaned`) for every prior annotation → re-present → re-await.** The ledger step is a
  mechanic **`review-loop` owns**; plan honors it. Never revise without the ledger. Cite plan-contract.md
  § gate 4 "On request-changes". Omitting the ledger, or attributing it to plan's own runtime, = fail.
- **P5 (ac-9e):** The deliverable is **the approval record** — the approve event (verdict, content hash,
  timestamp) bound to the version the human saw. You must **not** commit the plan or start implementing — the
  gate sequence **stops at Approved**; committing and building are the **caller's** concern (there is no gate
  5). Cite plan-contract.md § "What this skill does not do" / SKILL.md § gate 4. Answering "commit it and
  start building" = fail.
- **P6 (ac-2):** Three pointer kinds: **bundled references** (its own `plan-contract.md` + `authoring.md` +
  the skeleton), **project playbook** (`docs/agents/planning.md`, delta-only), **sibling skills**. Siblings
  are exactly **two**: **`review-loop`** = the sign-off gate (gate 4), and **`staffing`** = who authors or
  builds. Missing any of the three, or naming the wrong siblings/roles, = fail.
- **P7 (ac-3):** **No** — plan ships no `review-server`/`review-await` and no `scripts/` dir. To present a
  plan it **invokes the `review-loop` skill by plain name**, not by importing its files (`AGENTS.md`
  § Conventions "compose by name, not by file"). Cite SKILL.md / plan-contract.md § Composition. Saying it
  copies or imports review-loop's scripts = fail.
- **P8 (ac-4, ac-5):** **No** commit/implement gate — the sequence ends at **Approved**; committing the plan
  and starting the work are the **caller's** concern (plan-contract.md § "What this skill does not do"). The
  contract is **domain-neutral** — it does not assume code or a running app; acceptance criteria are
  "checkable pass/fail," and dev rigor is the project playbook's to add. Cite both sentences. Claiming a
  commit/implement gate, or that the contract assumes a running app, = fail.
- **P9 (ac-6):** **Yes, it still runs.** The **bundled references** carry the full default contract
  (threshold, format, gates), so no `docs/agents/planning.md` is required — the playbook is a **delta-only**
  override. With no review surface, the approval gate uses the **local fallback**: open the rendered plan on
  the machine, say remote review is unavailable, take the verdict in conversation — never improvise a public
  tunnel. Cite plan-contract.md §§ "Project playbook (delta-only)" / gate 4 "Local fallback". Saying it
  hard-stops without a playbook = fail.
- **P10 (ac-7):** The skeleton carries stable section ids and `<li id="ac-N" data-criterion>` criteria, is
  self-contained (inline styles + inline SVG, no external fetches), and its header comment cites the `plan`
  skill's own `reference/authoring.md` with **no** "backlog"/workflow identity baked in. Cite the header
  comment + a `data-criterion` line. Claiming it embeds backlog identity or pulls external assets = fail.
- **P11 (ac-8):** Well-formed: `interface.display_name` "Plan", a one-line `short_description` matching the
  SKILL.md spirit, a concrete `default_prompt`, and `policy.allow_implicit_invocation: false`. `false` is
  correct because plan runs a **multi-gate flow and holds a human approval gate** — not a lightweight advisory
  skill; codex-compat.md says default `false` for skills that run loops. Cite codex-compat.md. Saying `true`
  is fine for this skill, or the YAML being malformed, = fail.
- **P12 (ac-10):** **Yes — `backlog` plans exactly as before.** The extraction is non-breaking: backlog's
  `reference/plan.md`, `templates/planning.md`, and `plan-skeleton.html` are untouched. Rewiring backlog to
  consume the `plan` skill by name (and deleting its bundled plan step) is **explicitly deferred to a separate
  issue**, noted in the skill README. Cite README § "Not in scope" / SKILL.md. Claiming backlog was modified,
  or that the rewire happened here, = fail.

## Scoring

12 probes × 2 executors (Opus in-session + `codex exec`). A probe passes only with the **correct action AND a
correct citation**. P1–P5 are the five core routing probes ac-9 names and must pass on both executors.
Ambiguity flags are recorded as findings, not failures — they drive wording fixes before ship. Report a
verdict table mapping each probe → its criterion → pass/fail per executor.

The structural criteria are additionally confirmed by grep/parse against the tree: **ac-1** (layout present,
no `scripts/`), **ac-3** (no copied server/await scripts, no cross-skill path import), **ac-4** (no
commit/implement/posterity in the bundled contract), **ac-5** (no running-app/verify/evidence/repo terms in
the bundled contract), **ac-6** (two-layer + local-fallback stated), **ac-7** (skeleton stable ids +
self-contained + neutral header), **ac-8** (`openai.yaml` parses), **ac-10** (backlog's plan files
untouched).

### Criterion coverage map

| criterion | probe(s) | also confirmed by |
|-----------|----------|-------------------|
| ac-1  | P6 (layout named) | file check (layout present, no scripts/) |
| ac-2  | P6        | — |
| ac-3  | P7        | file check (no copied scripts / cross-skill import) |
| ac-4  | P5, P8    | file check (no commit/implement/posterity in contract) |
| ac-5  | P1, P8    | file check (no dev-only terms in bundled contract) |
| ac-6  | P9        | file check (two-layer + local fallback stated) |
| ac-7  | P10       | file check (stable ids, self-contained, neutral header) |
| ac-8  | P11       | file check (YAML parses) |
| ac-9  | P1, P2, P3, P4, P5 | — (the probes *are* ac-9) |
| ac-10 | P12       | file check (backlog plan files untouched) |
