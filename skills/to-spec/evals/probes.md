# To-Spec — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `SKILL.md` in context, plus the one `reference/` file named by the
probe when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the
executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a
valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade pass/fail
against the key. **The answer key is written before any runs** and graded against the plan's acceptance
criteria (`plans/8-to-spec.html`, ids ac-1..ac-11) — the plan is the source of truth; do not grade against
looser criteria.

Each probe names the criterion it exercises. Between them the 13 probes cover ac-1..ac-11.

## Probes

**P1 (ac-1).** Read `skills/to-spec/SKILL.md`. Does its frontmatter identify it as a user-invocable
synthesis skill whose job is turning the current conversation into a spec (no interview), and does any file in
the skill import or read another skill's files? Cite what you checked, and note whether the directory carries
the shipped-primitive layout (SKILL.md, README.md, agents/, reference/, templates/, evals/).

**P2 (ac-2).** From `SKILL.md`, list the three kinds of dependency pointer the skill declares, and state
exactly what it says about **sibling skills** — how many, which, and whether the dependency is hard or
optional.

**P3 (ac-3).** During the conversation the user never settled whether the spec should cover a secondary flow —
it was raised and left hanging. When you synthesize the spec, do you stop and ask the user to decide? Give the
rule and cite it.

**P4 (ac-4).** What artifact does to-spec produce, and where is it written? Is it a ticket? Who consumes it?
Cite the sentence.

**P5 (ac-5).** A teammate writing a spec calls the downstream units "issues" throughout. Per the skill, is
that right? What is the correct word, and why does the skill avoid "issue"? Cite it.

**P6 (ac-6).** List the sections the spec template carries. Which are always present and which are dev-only,
and what does the guide say to do with the dev-only ones on a spec where they don't apply? Cite the guide.

**P7a (ac-7, non-dev).** You're synthesizing a spec for a **non-dev** change — a revision to a team operating
process, no code. Do you write the Test seams section and run the "sketch the seams, prefer the highest
existing seam" step? Give the rule and cite it.

**P7b (ac-7, dev).** You're synthesizing a spec for a **dev** change — a new code path. Do you run the seams
step, and what does it tell you to prefer? Cite the sentence, and name where this step is adapted from.

**P8 (ac-8).** Drafting a spec, you're tempted to paste the exact path of the module you'll change and a
short code fragment showing the call. Does the skill allow file paths and code in the spec? What is the single
exception, and how should the non-excepted case be written instead? Cite the rule.

**P9a (ac-9, AFK).** The user has stepped away from the machine but wants to approve the spec before you move
on. How does to-spec get sign-off, and what must it do to the markdown spec first? Cite it. Is `review-loop` a
hard dependency?

**P9b (ac-9, present).** The user is sitting right there. How is the spec approved? If `review-loop` were
unavailable, could you still ship a valid spec? Cite the sentence.

**P10 (ac-10).** Read `skills/to-spec/agents/openai.yaml`. Is it well-formed per `docs/patterns/codex-compat.md`,
and is `allow_implicit_invocation` set correctly for a synthesis operator skill that writes repo docs? State
the value and why it's right.

**P11 (ac-11).** Read `skills/to-spec/evals/probes.md`. Does a pre-written answer key exist covering
ac-1..ac-10, and is the method dual-executor (Opus in-session + `codex exec`) per `docs/patterns/probe-evals.md`?
State what you checked.

## Answer key

- **P1 (ac-1):** Frontmatter has `name: to-spec`, `user-invocable: true`, and a `description` that reads as a
  pure-synthesis conversation→spec skill (no interview) — **pass**. No file imports another skill's files (the
  dependency surface says the skill is "self-contained at the file level" and "no file here imports or reads
  another skill's files"; a grep for cross-skill paths finds none). Directory carries the shipped layout
  (SKILL.md, README.md, agents/openai.yaml, reference/, templates/, evals/). Claiming a cross-skill import
  exists, or that it interviews, = fail.
- **P2 (ac-2):** The three pointer kinds: **bundled references** (own `reference/` + `templates/spec-skeleton.html`),
  **project playbooks** (the repo's spec-location/vocabulary convention, default `docs/specs/`; the
  presentation-surface config when review-loop is used), **sibling skills**. On siblings it must say
  **optional `review-loop` only**, explicitly **not a hard dependency** (skipping it still yields a valid
  spec), and no other sibling. Missing any of the three, or getting the sibling answer wrong, = fail.
- **P3 (ac-3):** **No — do not ask.** To-spec is pure synthesis: capture what's decided and **record the
  undecided point as a line in the spec's Notes**, never bounce it back as a question. Cite
  `reference/synthesis.md` § "The one rule: synthesize, never interview" (or SKILL.md's synthesis contract).
  Stopping to interview the user = fail.
- **P4 (ac-4):** A **spec** — a self-contained HTML repo doc written to **`docs/specs/<name>.html`** — the high-level **direction**
  document that **`to-tickets`** consumes. It is **not** a ticket (and never a GitHub "issue"); it's coarser
  than a plan. Cite SKILL.md § "What a spec is (and isn't)" / `reference/synthesis.md` § Naming and placing.
  Calling it a ticket/issue or naming the wrong path = fail.
- **P5 (ac-5):** **Not right.** The correct word is **ticket** — the downstream unit `to-tickets` cuts. The
  skill avoids "issue" because that's one tracker's word and the pair is deliberately tracker-agnostic /
  generic. Cite SKILL.md § "What a spec is" or `reference/synthesis.md` § Vocabulary. A grep of the shipped
  skill finds no "issue"-as-unit-of-work. Endorsing "issues" = fail.
- **P6 (ac-6):** Core (always): **Problem, Solution, User stories, Implementation decisions, Out of scope,
  Notes**. Dev-only: **Testing decisions, Test seams**. The guide says to **skip the dev-only sections
  entirely when they don't apply** (non-dev spec) — don't manufacture prose to fill them. Cite
  `reference/template-guide.md` § "Dev-only sections — skip when N/A". Missing the dev-only marking, or listing
  them as always-present, = fail.
- **P7a (ac-7):** **No.** For a non-dev spec the dev-only sections (Testing decisions, Test seams) and the
  seams step are **skipped entirely**. Cite `reference/synthesis.md` § Classify the work / § Dev specs only
  ("For a non-dev spec this step does not run at all"). Running the seams step on a non-dev spec = fail.
- **P7b (ac-7):** **Yes.** For a dev spec, name the public seams and **prefer the highest existing seam** (the
  fewer the better); adapted from **Matt Pocock's `to-spec`**. Cite `reference/synthesis.md` § "Dev specs only
  — sketch the test seams". Skipping it on a dev spec, or missing the "highest existing seam" preference, =
  fail.
- **P8 (ac-8):** **No file paths and no code snippets** — they rot; the spec is direction, describe the module
  or contract **in prose** instead. The single exception is a **prototype-validated snippet** that encodes a
  decision more precisely than prose (state machine, schema, type shape). Cite SKILL.md / `reference/synthesis.md`
  § No stale content. Allowing arbitrary file paths/code, or dropping the prototype exception, = fail.
- **P9a (ac-9):** Present the spec through the optional **`review-loop`** sibling, first **rendering the
  markdown spec to a self-contained review HTML**; it's approved from the human's own device per the repo's
  presentation-surface config. `review-loop` is **not** a hard dependency. Cite SKILL.md § Dependency surface /
  `reference/synthesis.md` § Sign-off. Treating review-loop as required, or skipping the render step, = fail.
- **P9b (ac-9):** **Inline, in the conversation** — the default path, depending on no other skill. Yes, a
  valid spec still ships without review-loop (skipping sign-off still leaves a valid spec on disk). Cite
  `reference/synthesis.md` § Sign-off ("User present — take approval inline"). Saying review-loop is required
  = fail.
- **P10 (ac-10):** Well-formed: `interface.display_name` "To-Spec", a one-line `short_description` matching the
  SKILL.md spirit, a concrete `default_prompt`, and `policy.allow_implicit_invocation: false`. `false` is
  correct because to-spec is a synthesis operator skill that writes repo docs, not a lightweight advisory skill
  — codex-compat.md says default `false` for operator-style skills. Saying `true` is fine, or the YAML being
  malformed, = fail.
- **P11 (ac-11):** The file carries a **pre-written answer key** with a probe per ac-1..ac-10 (ac-7 probed both
  ways) and a coverage map; the method names **both** executors (Opus subagent + `codex exec --sandbox
  read-only`) per `docs/patterns/probe-evals.md`. A grep confirms an Answer key section and both executor
  names. Missing the key, or a single-executor method, = fail.

## Scoring

13 probes × 2 executors (Opus in-session + `codex exec`). A probe passes only with the **correct action AND a
correct citation**. Ambiguity flags are recorded as findings, not failures — they are the most valuable output
and should drive wording fixes before ship. Report a verdict table mapping each probe → its criterion →
pass/fail per executor. Structural criteria are additionally confirmed by file check: ac-1 (frontmatter + grep
no cross-skill imports), ac-5 (grep finds no "issue"-as-unit-of-work), ac-10 (YAML parses).

### Criterion coverage map

| criterion | probe(s)              |
|-----------|-----------------------|
| ac-1      | P1                    |
| ac-2      | P2                    |
| ac-3      | P3                    |
| ac-4      | P4                    |
| ac-5      | P5                    |
| ac-6      | P6                    |
| ac-7      | P7a, P7b              |
| ac-8      | P8                    |
| ac-9      | P9a, P9b              |
| ac-10     | P10                   |
| ac-11     | P11 (this file)       |
