# Staffing — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `SKILL.md` in context, plus the one `reference/` file named by the
probe when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the
executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a
valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade
pass/fail against the key. **The answer key is written before any runs** and graded against the plan's
acceptance criteria (`plans/1-extract-staffing.html`, ids ac-1..ac-11) — the plan is the source of truth; do
not grade against looser criteria.

Each probe names the criterion it exercises. Between them the 14 probes cover ac-1..ac-11.

## Probes

**P1 (ac-1).** Read `skills/staffing/SKILL.md`. Does its frontmatter identify it as an invocable,
global-capable staffing primitive, and do any of the skill's files import or read another skill's files? Cite
what you checked.

**P2 (ac-2).** A composer skill wants to depend on `staffing`. From `SKILL.md`, list the three kinds of
dependency pointer the skill declares, and state exactly what it says about sibling skills.

**P3 (ac-3).** A ui change is ready but the model that fills the **ui builder** role cannot be reached from
the current harness. Who takes the change? Give the concrete rule and cite it.

**P4 (ac-4).** You must route a task that drives a real browser (navigate, click, scrape a page). Walk the
resolution and name, by their location, each structure you consult and in what order. Which structure
decides the browser requirement, and where does the `intelligence > taste > cost` tie-break enter?

**P5 (ac-5).** "Who should do a large mechanical find-and-replace across the whole codebase?" Give the model
and the exact basis for the choice. Is this a ranking derivation or something else?

**P6 (ac-4, explanatory).** A teammate proposes adding a `browser-use` column (values yes/no) directly to the
rankings table to simplify things. Per the skill, is that allowed, and what specifically goes wrong if you
do it? Cite the sentence.

**P7 (ac-6).** You are installing `staffing` on a **fresh machine that has no Codex CLI and a different model
lineup** than any example in the skill. Following the audit procedure, outline the table you would write and
say where its cost/intelligence/taste numbers come from. May you ship the four-model gpt-5.5/sonnet-5/…
table as the roster? Cite the rule.

**P8 (ac-6).** In `reference/machine-audit.md`, what status does the four-model table (gpt-5.5, sonnet-5,
opus-4.8, fable-5) have? Quote the label the file gives it.

**P9 (ac-7).** Install `staffing` for a project that is identical to the machine default **except it forbids
staffing below a higher floor**. What does the project override file contain? Cite the rule about what an
override may and may not hold.

**P10 (ac-8, branch A).** You run `setup` and detect that **global staffing rules already exist** in
`~/.claude/CLAUDE.md`. What does the scope-decision flow tell you to do? Cite it.

**P11 (ac-8, branch B).** You run `setup` and detect **no staffing rules anywhere**. What does the flow tell
you to do, and what must you get from the user before writing anything global? Cite it.

**P12 (ac-9).** A user re-invokes `reconcile`. The installed global base still lists a model the current
harness can no longer reach, and the project override has re-pasted the entire base table. How does the skill
detect and report this, and — specifically — does it rely on a `vNN` version stamp to notice? Cite the
mechanism.

**P13 (ac-10).** Read `skills/staffing/agents/openai.yaml`. Is it well-formed per
`docs/patterns/codex-compat.md`, and is `allow_implicit_invocation` set correctly for an operator/config
primitive? State the value and why it is right.

**P14 (ac-4).** A task needs **user-facing onboarding copy and a public API surface designed** — no browser
or other capability required. Walk the resolution order and name, by location, each structure and gate you
consult and in what order. Suppose the roster's highest-intelligence reachable model sits at taste 5 while a
lower-intelligence model clears taste ≥ 7: which one gets the work, and at exactly which step is the taste-5
model removed from contention? Does the `intelligence > taste > cost` tie-break ever get to reconsider it?

## Answer key

- **P1 (ac-1):** Frontmatter has `name: staffing`, `user-invocable: true`, and a `description` that reads as
  a global-capable staffing primitive invoked by name by siblings and directly by users — **pass**. No file
  imports another skill's files (the dependency surface says the references "import no other skill's files"
  and siblings are "none — root primitive"); a grep for cross-skill paths finds none. Claiming a cross-skill
  import exists = fail.
- **P2 (ac-2):** The three pointer kinds: **bundled references** (own `reference/` contract), **project
  playbooks** (installed into the target repo's `docs/agents/`), **sibling skills**. On siblings it must say
  **"none — `staffing` is a root primitive"** (invoked by siblings, depends on none). Missing any of the
  three, or getting the sibling answer wrong, = fail.
- **P3 (ac-3):** The **fallback ladder** governs: the next most capable **reachable** model with sufficient
  taste for ui work (taste ≥ 7) steps into the ui builder role via the succession line; if the only reachable
  qualifier is the orchestrator, it takes the ui build itself; if none clears the ui bar, run on the current
  model in a subagent and **report the staffing gap** — never default it to the backend builder, never skip
  the change. Cite `reference/roles-and-fallback.md` (worked example / fallback ladder). Handing it to the
  backend builder or stopping = fail.
- **P4 (ac-4):** Order is pin → capability gate → rank. The **capability matrix** (a separate structure)
  decides the browser requirement: filter to models marked `browser-use: true`. The `intelligence > taste >
  cost` tie-break enters **only after**, ranking the survivor set — not the full roster. Executor must point
  to the capability matrix and the rankings table as **distinct** structures by location
  (`reference/rankings-and-routing.md`). Ranking first, or treating browser-use as a rankings column, = fail.
- **P5 (ac-5):** The **mechanical/bulk task-pin** returns the pinned bulk model; resolution **stops at step
  1** and skips ranking. It is a **pin**, not a ranking derivation — "a pin short-circuits the ranking." Cite
  the task-pins section / step 1 of the resolution order in `reference/rankings-and-routing.md`. Deriving the
  answer from the table = fail.
- **P6 (ac-4):** **Not allowed.** A capability is a *kind*, not a *degree*; folding `browser-use` into the
  higher-is-better table either lets a browser-capable-but-dumber model outrank a smarter one, or lets
  intelligence override a hard requirement and pick a model that physically can't do the job — either way the
  `intelligence > taste > cost` ordering stops meaning what it says. Capabilities **gate**, never **rank**.
  Cite the "Why they must stay separate" sentence. Saying it's fine = fail.
- **P7 (ac-6):** Follow the audit: enumerate **this machine's** reachable models as the rows, seed
  cost/intelligence/taste from the documented default and mark them "tune these", omit the Codex CLI mechanics
  block (Codex absent), and set capability booleans + pins per what's reachable. You **may not** ship the
  four-model table as the roster — it is labeled example output, and the roster is compiled from *this*
  machine. Cite `reference/machine-audit.md` (the audit procedure / "compiled from the current machine, never
  shipped fixed"). Reproducing Asher's table as the roster, or inventing reachable models, = fail.
- **P8 (ac-6):** It is an **example of audit output for one machine — explicitly NOT the shipped/authoritative
  roster** (the file labels it "Example of audit output (illustrative only — NOT the shipped roster)" and
  "audit output for one environment"). Calling it the canonical table = fail.
- **P9 (ac-7):** The override contains **only the delta** — the raised floor — and nothing else; it must
  **not** re-copy the rankings table, pins, or capability matrix (those resolve from the base via the
  resolver). Cite `reference/install-and-reconcile.md` ("carries only deltas … never re-copies the base" /
  the stricter-floor worked example). A full-table copy = fail.
- **P10 (ac-8):** Branch A — **show the existing global rules to the user and offer to add a project
  override**; do not silently overwrite the base. Cite the scope-decision flow. Overwriting the base, or
  asking global-vs-project as if nothing existed, = fail.
- **P11 (ac-8):** Branch B — **ask the user which shape**: global-with-overrides vs project-only. Before any
  **global** write you must have the user's consent via this flow ("global writes are gated on consent" /
  "never automatically"). Cite it. Writing the global base without asking = fail.
- **P12 (ac-9):** `reconcile` is an **LLM audit**: read the installed base + overrides, compare to the
  skill's definition, and **report the drift/conflict in prose** — here, both the unreachable-model staleness
  and the override's full-table re-copy. It relies on **no `vNN` version stamp** (a deliberate departure from
  backlog's stamp approach; "Staffing introduces no such stamp or marker"). A grep for `vNN`/version markers
  finds none. Answering "compare version numbers" or proposing to add a stamp = fail.
- **P13 (ac-10):** Well-formed: `interface.display_name` "Staffing", a one-line `short_description` matching
  the SKILL.md spirit, a concrete `default_prompt`, and `policy.allow_implicit_invocation: false`. `false` is
  correct because staffing is an operator/config primitive (it writes global memory), not a lightweight
  advisory skill — codex-compat.md says default `false` for operator-style skills. Saying `true` is fine, or
  the YAML being malformed, = fail.
- **P14 (ac-4):** Order is pin → gates → rank. No pin matches (step 1). At the **gates** (step 2) the task is
  user-facing, so the **taste gate** applies: filter the candidates to **taste ≥ 7**, which **removes the
  taste-5 model from contention before any ranking**. (No capability gate triggers — no browser/computer
  requirement.) Only then does step 3 rank the survivors by `intelligence > taste > cost`, so the
  **lower-intelligence, taste-≥7 model gets the work**; the taste-5 model's higher intelligence is
  irrelevant because it was already dropped in step 2 and ranking **never resurrects a gated-out model**.
  The taste ≥ 7 floor is a **hard gate, not a soft default** — cite the taste gate in the resolution order
  (`reference/rankings-and-routing.md`, step 2) and its "ranking never resurrects a model a gate removed"
  clause. Answering that the taste-5 model wins on intelligence, treating taste ≥ 7 as a mere tie-break or
  soft default, or applying the floor only after ranking = fail.

## Scoring

14 probes × 2 executors (Opus in-session + `codex exec`). A probe passes only with the **correct action AND
a correct citation**. Ambiguity flags are recorded as findings, not failures — they are the most valuable
output and should drive wording fixes before ship. Report a verdict table mapping each probe → its criterion
→ pass/fail per executor. Structural criteria are additionally confirmed by file check: ac-1 (frontmatter +
grep no cross-skill imports), ac-9 (grep finds no `vNN`/version stamp), ac-10 (YAML parses).

### Criterion coverage map

| criterion | probe(s)              |
|-----------|-----------------------|
| ac-1      | P1                    |
| ac-2      | P2                    |
| ac-3      | P3                    |
| ac-4      | P4, P6, P14           |
| ac-5      | P5                    |
| ac-6      | P7, P8                |
| ac-7      | P9                    |
| ac-8      | P10, P11              |
| ac-9      | P12                   |
| ac-10     | P13                   |
| ac-11     | this file (the eval)  |
