# Prototype — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `skills/prototype/SKILL.md` in context, plus the one `reference/`
file the probe names (probes that test whether a reference stands alone withhold `SKILL.md`). Require the
executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a
valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade
pass/fail against the key. **The answer key is written before any runs** and graded against the plan's
acceptance criteria (`plans/5-prototype-composer.html`, ids ac-1..ac-9) — the plan is the source of truth.

Two probes (P7, P8) are the load-bearing behavioral scenarios: an executor drives a real design question end
to end. P7 is a **code** question, P8 a **non-code / outside-dev** question — together they prove the skill
generalizes beyond code (ac-5, ac-8) and preserves the flow (ac-7). The structural criteria (ac-1, ac-2,
ac-3, ac-4, ac-9) are additionally confirmed by grep/parse against the tree.

## Probes

**P1 (ac-1).** Read `skills/prototype/SKILL.md`. List the files the skill ships under `skills/prototype/`
(SKILL, README, the `reference/` technique, `agents/openai.yaml`, `evals/probes.md`). Does the layout match
the shipped siblings `skills/staffing/` and `skills/review-loop/`?

**P2 (ac-2).** From `SKILL.md` frontmatter alone: is `prototype` a user-invocable skill, and does its
description identify it as a **thin composer** that produces a **throwaway artifact answering one design
question**, usable **beyond code**? Quote the phrase that settles each.

**P3 (ac-3).** A skill author wants to depend on `prototype`. From `SKILL.md`, list the three kinds of
dependency pointer it declares, and state exactly what it says about **sibling** skills — including whether
`prototype` is a root primitive or a composer, and which siblings it names.

**P4 (ac-4).** Do any of `prototype`'s files import or path-reference another skill's files (e.g.
`skills/review-loop/…` or `skills/staffing/…`)? How does it refer to review-loop and staffing instead? Cite
what you checked.

**P5 (ac-5).** Read `skills/prototype/reference/prototyping.md` **without** `SKILL.md`. Does it frame a
prototype as throwaway *code* only, or as a throwaway *artifact* that may be a document/layout? Give the
non-code worked example it provides for at least one shape. Cite the sentence.

**P6 (ac-6).** From the skill, name the four gates in order and quote the phrase that states the
"throwaway from day one — keep the answer, delete the artifact" framing. Is the prototype ever the durable
record of the decision? Cite it.

**P7 (ac-7) — behavioral, code.** Scenario: *You are planning an enhancement. Discussion hasn't settled
whether a retry state machine should allow a transition from `failed` back to `pending`; the choice is
expensive to reverse. Use the `prototype` skill.* Walk the full flow: what is the one question, which shape,
what do you build, who builds it, how is it presented, where does the answer go, and what happens to the
artifact at the end?

**P8 (ac-8) — behavioral, non-code / outside dev.** Scenario: *You are writing a one-page project brief.
There is no codebase, no dev stack, no component library. You can't decide how to lay it out. Use the
`prototype` skill.* Walk the full flow. What must you **not** assume, given there is no repo?

**P9 (ac-9).** You just built the standalone `prototype` skill. *For this probe only, you may also read
`.claude/skills/backlog/reference/prototype.md` and `docs/agents/prototyping.md` and run `git diff --stat`.*
Did you modify `backlog`'s `reference/prototype.md` or `docs/agents/prototyping.md`? Does backlog's prototype
step still resolve its technique? What is explicitly deferred? Cite it.

## Answer key

- **P1 (ac-1):** Files present: `SKILL.md`, `README.md`, `reference/prototyping.md`, `agents/openai.yaml`,
  `evals/probes.md`. Layout matches the siblings (SKILL + README + reference/ + agents/openai.yaml +
  evals/probes.md). Missing a file, or claiming a mismatch, = fail.
- **P2 (ac-2):** `user-invocable: true`, `name: prototype`; the description calls it a **thin composer** and a
  **throwaway artifact that answers one design question**, and says **usable anywhere / not only dev / not
  only code**. Missing user-invocable, or missing the composer/throwaway/beyond-code framing, = fail.
- **P3 (ac-3):** Three pointer kinds — **bundled references** (`reference/prototyping.md`, the technique),
  **project playbook** (`docs/agents/prototyping.md`, repo placement only), **sibling skills**. On siblings
  it must say **`prototype` is a composer** (NOT a root primitive) with two load-bearing siblings named:
  **`review-loop`** and **`staffing`**, composed by plain name, no imports. Getting the composer/root
  distinction wrong, or missing a sibling, = fail.
- **P4 (ac-4):** **No file imports another skill's files** — review-loop and staffing are referenced **by
  plain name** only (SKILL.md § How it composes / Dependency surface says "by plain name, no imports" and
  "imports none of their files"). A grep for `skills/review-loop/` or `skills/staffing/` paths finds none.
  Claiming a cross-skill file import exists = fail.
- **P5 (ac-5):** It frames a prototype as a throwaway **artifact** ("a rendered document, a layout, a
  maquette, a driven scenario … a prototype when it exists only to settle a question"), **not code only**.
  Non-code example: the **behavior shape's** hand-driven state table / scenario run, or the **form shape's**
  structurally different rendered drafts of a document/layout (self-contained HTML variant sheets). Answering
  "code only," or unable to give a non-code example, = fail.
- **P6 (ac-6):** Gates: **1 Question stated → 2 Built and handed over → 3 Answer captured → 4 Cleaned up.**
  Framing quote: "**Throwaway from day one: keep the answer, delete the artifact.**" The prototype is **never
  the record** ("The prototype itself is never the record"). Wrong order, or claiming the prototype is the
  record, = fail.
- **P7 (ac-7):** One question: *may the retry machine transition `failed` → `pending`?* Shape: **behavior**
  (a state model → behavior, per the technique). Build: a **pure reducer / explicit state machine module**
  behind a **tiny terminal shell** (one command, one stable frame per action, state surfaced) — driven
  through the awkward sequences. Who builds it: dispatched to the builder the **`staffing`** skill resolves
  (by name). Presented: driven directly as a live interactive prototype (its URL announced on the surface);
  if the answer is written up as a doc, served via **`review-loop`**. Answer goes: **into the consuming
  plan**, with the decision and why. Artifact at the end: **deleted**, the validated state-machine module
  lifted into real code. Skipping the shape choice, hardcoding who builds it instead of asking staffing,
  forking a review UI, or leaving the throwaway in the repo, = fail.
- **P8 (ac-8):** One question: *which layout/structure for this brief?* Shape: **form**. Build: **3
  structurally different, self-contained rendered variants** of the same content (different layout/hierarchy,
  not color/copy) — standalone HTML, inline styles, no external assets. Presented: served via **`review-loop`**
  by name so feedback arrives as annotations; end with URL + hub URL. Answer: the winner captured (rendered
  sheet) into the decision record; losing variants deleted. Must **NOT assume** a codebase, task runner,
  `?variant=` route, or component library — with no playbook it uses the technique's **defaults** (a
  self-contained artifact in a scratch/workspace dir). Assuming a dev stack / component library, or picking
  the behavior shape, = fail.
- **P9 (ac-9):** **No — backlog's files are untouched.** The standalone skill carries its **own** bundled
  copy of the technique (`skills/prototype/reference/prototyping.md`); backlog keeps `reference/prototype.md`
  and the full technique in `docs/agents/prototyping.md`, so its prototype step still resolves. Explicitly
  deferred to the backlog-dissolution work: **rewiring backlog to compose the new skill and slimming
  `docs/agents/prototyping.md` to repo-config-only** (plan dec-5 / out-of-scope). Claiming backlog was
  modified, or that the rewire happened here, = fail.

## Scoring

9 probes × 2 executors (Opus in-session + `codex exec`). A probe passes only with the **correct action AND a
correct citation**. Ambiguity flags are recorded as findings, not failures. Report a verdict table mapping
each probe → its criterion → pass/fail per executor.

The structural criteria are additionally confirmed outside the probes by **file check** (grep/parse against
the tree): **ac-1** (layout present), **ac-2** (`SKILL.md` frontmatter parses with `name`/`user-invocable`/
`argument-hint`/composer description), **ac-3** (three-part dependency surface names review-loop + staffing),
**ac-4** (no `skills/review-loop/` or `skills/staffing/` path in any skill file), **ac-9** (git diff shows
backlog's `reference/prototype.md` and `docs/agents/prototyping.md` untouched).

### Criterion coverage map

| criterion | probe(s) | also confirmed by |
|-----------|----------|-------------------|
| ac-1 | P1     | file check (layout) |
| ac-2 | P2     | file check (frontmatter parse) |
| ac-3 | P3     | file check (dependency surface) |
| ac-4 | P4     | file check (no cross-skill path) |
| ac-5 | P5, P8 | — |
| ac-6 | P6     | — |
| ac-7 | P7     | — |
| ac-8 | P8     | — |
| ac-9 | P9     | file check (backlog untouched) |
