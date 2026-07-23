# Staffing — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `SKILL.md` in context, plus the one `reference/` file named by the
probe when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the
executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a
valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade
pass/fail against the key. **The answer key is written before any runs** and graded against the plan's
acceptance criteria (`plans/1-extract-staffing.html`, ids ac-1..ac-11) — the plan is the source of truth; do
not grade against looser criteria.

The original fourteen probes protect ac-1..ac-11. P15–P17 cover owner-routed setup and sibling harness
dispatch.

## Probes

**P1 (ac-1).** Read `skills/system/staffing/SKILL.md`. Does its frontmatter identify it as an invocable,
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
say where its cost/intelligence/taste numbers come from. May you ship the five-model gpt-5.6-sol/gpt-5.6-terra/sonnet-5/…
table as the roster? Cite the rule.

**P8 (ac-6).** In `reference/machine-audit.md`, what status does the five-model table (gpt-5.6-sol,
gpt-5.6-terra, sonnet-5, opus-4.8, fable-5) have? Quote the label the file gives it.

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

**P13 (ac-10).** Read `skills/system/staffing/agents/openai.yaml`. Is it well-formed per
`AGENTS.md` § Conventions (the `agents/openai.yaml` rule), and does `allow_implicit_invocation` agree with
the canonical `metadata.invocation` declaration? State the value and why it is right.

**P14 (ac-4).** A task needs **user-facing onboarding copy and a public API surface designed** — no browser
or other capability required. Walk the resolution order and name, by location, each structure and gate you
consult and in what order. Suppose the roster's highest-intelligence reachable model sits at taste 5 while a
lower-intelligence model clears taste ≥ 7: which one gets the work, and at exactly which step is the taste-5
model removed from contention? Does the `intelligence > taste > cost` tie-break ever get to reconsider it?

**P15 (setup).** Invoke `staffing setup` where a global base already exists. Which bundled reference owns the
branch, what may change, and what must remain byte-for-byte unchanged without a separate user request?

**P16 (issue 49).** From a Codex parent, dispatch one bounded task to the Claude sibling harness. Give the
command shape, forbidden flag, required return/effect checks, and whether vendor-policy polling is a
precondition.

**P17 (issue 49).** Codex→Claude fails while Claude→Codex is healthy. What reachability state and fallback
does staffing record? Must it disable both directions?

**P18 (issue 48).** Route two issue-coordinator requests. Both include work type, surface, required
capabilities, class/reason, and known uncertainty. The first is `routine`; the second is
`orchestrator-required` for a named product decision. State the candidate set and resolution order for each.
Does routine mean cheapest reachable model?

**P19 (issue 60).** From each provider package, route one cross-harness worker. Who owns prompt/judgment/effect
verification, what may the native wrapper do, how is it named/staffed/bounded, and what remains unproven when
native spawn cannot select or report its model?

**P20 (global modules).** Reconcile an approved global roster while a Presentation section already exists.
Which canonical templates render the module/pointer, which is written first, what does unreadable-module
behavior do, and may staffing rewrite Presentation bytes?

**P21 (provider pilot).** Compare staffing's current unified reconcile load with each compiled provider load.
Does each clear 20%, and does either loaded path contain a conditional branch intended only for the other
harness? Use the checked-in structural test as evidence.

**P22 (situated pointer).** In one compiled provider package, exercise a non-routing leaf edit and every
pointer trigger: model choice, delegation, child/worktree creation, browser/computer/imagegen work, watcher,
and route-loss fallback. When does the module load, when are project deltas applied, and what happens if the
module is unreadable?

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
- **P4 (ac-4):** Order is pin → provider/fallback → eligible executor → taste gate → rank. A matching
  provider pin selects the named effect-verified route. Otherwise the capability-provider registry resolves
  `browser-use` to its effect-verified primary then recorded fallback; only executors able to operate that
  route enter the candidate set. `intelligence > taste > cost` ranks those survivors only. Treating browser
  access as a model boolean or ranking before provider selection = fail.
- **P5 (ac-5):** The **mechanical/bulk task-type pin** returns the pinned bulk model; resolution **stops at
  step 1** and skips ranking. It is a **pin**, not a ranking derivation — "a pin short-circuits the ranking."
  Cite the Pins section / step 1 of the resolution order in `reference/rankings-and-routing.md`. Deriving the
  answer from the table = fail.
- **P6 (ac-4):** **Not allowed.** Browser use is an effect supplied by a named harness/tool provider, not a
  model trait or ranked degree. Resolve provider reachability first, then form the eligible executor set;
  putting a boolean on model rows invents access when tooling/session state is absent. Cite the provider
  registry contract. Saying the model column is authoritative = fail.
- **P7 (ac-6):** Follow the audit: enumerate **this machine's** reachable models as the rows, seed
  cost/intelligence/taste from the documented default and mark them "tune these", omit the Codex CLI mechanics
  block (Codex absent), and effect-probe installed tools into a provider registry plus pins. You **may not** ship the
  five-model table as the roster — it is labeled example output, and the roster is compiled from *this*
  machine. Cite `reference/machine-audit.md` (the audit procedure / "compiled from the current machine, never
  shipped fixed"). Reproducing Asher's table as the roster, or inventing reachable models, = fail.
- **P8 (ac-6):** It is an **example of audit output for one machine — explicitly NOT the shipped/authoritative
  roster** (the file labels it "Example of audit output (illustrative only — NOT the shipped roster)" and
  "audit output for one environment"). Calling it the canonical table = fail.
- **P9 (ac-7):** The override contains **only the delta** — the raised floor — and nothing else; it must
  **not** re-copy the rankings table, pins, or capability-provider registry (those resolve from the base via the
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
  and the override's full-table re-copy. "That reading is the judgment mechanism"
  (install-and-reconcile.md § Reconciliation is a prose audit). Answering "compare version numbers" or
  proposing to add a stamp = fail.
- **P13 (ac-10):** Well-formed: `interface.display_name` "Staffing", a one-line `short_description` matching
  the SKILL.md spirit, a concrete `default_prompt`, and `policy.allow_implicit_invocation: true`. `true`
  matches `metadata.invocation: model`: a thread may reach for staffing when it encounters a routing choice,
  independent of whether the caller explicitly named it. Treating execution (`thread`) or global-write
  capability as a reason to disable ambient invocation, or accepting a mismatch, = fail.
- **P14 (ac-4):** Order is pin → provider/fallback → eligible executor → taste gate → rank. No pin matches
  (step 1), and no provider gate triggers (step 2; no browser/computer requirement). At the **taste gate**
  (step 3), the task is user-facing: filter to **taste ≥ 7**, which **removes the taste-5 model before any
  ranking**. Only then does step 4 rank the survivors by `intelligence > taste > cost`, so the
  **lower-intelligence, taste-≥7 model gets the work**; the taste-5 model's higher intelligence is
  irrelevant because it was already dropped in step 3 and ranking **never resurrects a gated-out model**.
  The taste ≥ 7 floor is a **hard gate, not a soft default** — cite the taste gate in the resolution order
  (`reference/rankings-and-routing.md`, step 3) and its "ranking never resurrects a model a gate removed"
  clause. Answering that the taste-5 model wins on intelligence, treating taste ≥ 7 as a mere tie-break or
  soft default, or applying the floor only after ranking = fail.
- **P15 (setup):** PASS only if `SKILL.md` routes setup to `reference/setup.md`; the executor preserves the
  existing global base, offers or reconciles only a project delta, and requires an explicit request before
  editing the base. Cite `reference/setup.md` and `reference/install-and-reconcile.md`.
- **P16 (issue 49):** PASS only for a watched native wrapper around bounded `claude -p` with no `--bare`,
  closed stdin, timeout, and raw durable return; the wrapper reports lifecycle and the parent verifies the
  effect. No vendor-policy or credit monitor is required. Cite the Codex package's `reference/harness.md` and
  common `reference/install-and-reconcile.md`.
- **P17 (issue 49):** PASS only if the failed Codex→Claude direction becomes unavailable, routing is rerun
  over remaining candidates, Claude→Codex remains healthy, and the graph is explicitly asymmetric. Cite
  `reference/roles-and-fallback.md` and `reference/machine-audit.md`.
- **P18 (issue 48):** PASS only if routine begins with the reachable coordinator-eligible set and applies
  pin → provider/fallback → eligible executor → taste gate → `intelligence > taste > cost`; cost is the final
  tie-break. `orchestrator-required` returns the orchestrator role at the coordinator pre-gate and records its
  succession. Missing inputs would be a grooming gap. Cite both routing and roles references.
- **P19 (issue 60):** PASS only if the parent owns prompt, judgment, and effect verification; the wrapper is
  a watched native child labeled with external model/task, staffed by the cheapest native model allowed by
  the floor, and limited to bounded process supervision plus raw output/lifecycle relay. If spawn cannot
  accept or report the wrapper model, observability may pass but floor/cost compliance remains red.
- **P20 (global modules):** PASS only if compiled `staffing.module.md` has one `{{COMMON}}` marker replaced by
  `staffing.common.md`, both provider modules enter the shared barrier with both Presentation modules, and no
  pointer applies before all four read back and hash-match. Both globals then pass Presentation preflight and
  apply before staffing may write; finalize verifies all four sections and removes the barrier. Unreadable
  modules or failed preflight leave both globals untouched; staffing preserves Presentation/user bytes. No eager import.
- **P21 (provider pilot):** PASS only with the checked-in baseline 10,391 bytes and current results at least
  20% smaller for both providers, plus no opposite-direction path/global-memory branch in the files loaded by
  reconcile. Cite `evals/test_provider_pilot.py`.
- **P22 (situated pointer):** PASS only if the leaf edit does not load the module; all named routing,
  capability, watcher, and fallback triggers load it before acting; readable resolution applies the project
  delta after the global module; and unreadable module stops dispatch. Cite the compiled provider pointer.

## Scoring

22 probes × 2 executors (one Claude route + one Codex route). A probe passes only with the **correct action AND
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
| issue 48  | P18                   |
| issue 49  | P16, P17              |
| issue 60  | P19                    |
| global    | P20                    |
| variants  | P21                    |
| pointers  | P22                    |
