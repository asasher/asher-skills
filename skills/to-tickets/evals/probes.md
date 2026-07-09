# To-Tickets — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `SKILL.md` in context, plus the one `reference/` file named by the probe
when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the executor
to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a valid
answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade pass/fail against
the key. **The answer key is written before any runs** and graded against the plan's acceptance criteria
(`plans/9-to-tickets.html`, ids ac-1..ac-12) — the plan is the source of truth; do not grade against looser
criteria.

Each probe names the criterion it exercises. Between them the 12 probes cover ac-1..ac-12. **The eval is
read-only / dry-run: executors describe the next concrete action and cite — nothing publishes to the live
tracker, and the sample split (ac-7) is rendered to a tickets file, never created as real issues.**

## Probes

**P1 (ac-1).** Read `skills/to-tickets/SKILL.md`. Does its frontmatter identify a user-invocable skill whose
job is splitting a spec (or plan, or conversation) into backlog-ready tickets with blocking edges? Does any file
in the skill import or read another skill's files? Cite what you checked, and note whether the directory carries
the shipped-primitive layout (SKILL.md, README.md, agents/, reference/, templates/, evals/).

**P2 (ac-2).** From `SKILL.md`, list the three kinds of dependency pointer the skill declares. State exactly
what it says about **sibling skills** (which inputs, composed how) and how it models **`backlog`** — as an
imported sibling, or as something else. Cite it.

**P3 (ac-3).** A user runs the skill and points it at a spec at `docs/specs/foo.md`. Is that the right primary
input? What two other inputs does the skill accept when there's no spec? Cite the sentence.

**P4 (ac-4).** You're splitting a spec for a feature that spans a data layer, business logic, and a UI. A
teammate proposes three tickets: "all the data models," "all the logic," "all the UI." Per the skill, is that
the right shape? What shape does the skill want instead, and what are its three properties? Cite it.

**P5 (ac-5).** The direction includes renaming a symbol used in ~120 call sites across the codebase — mechanical,
but everywhere. Do you draft this as a single vertical slice? If not, what does the skill tell you to do
instead, and what is the trigger that puts a change on this path? Cite the sentence.

**P6 (ac-6).** You've drafted the split. Do you publish the tickets now, or is there a step first? What is that
step, what two things does it settle, and how does this differ from `to-spec`'s posture? Cite it.

**P7 (ac-7) — load-bearing.** You are splitting a spec into exactly three tickets: **A** (a shared data model),
**B** (a feature that reads the model), and **C** (a second feature that also reads the model). B and C each
require A; B and C are independent of each other. The split is already approved by the user. State, as your next
concrete action: (a) in what **order** you create the tickets in the tracker and why; (b) the **exact edge line**
each dependent ticket carries and where it goes; (c) what effect those edges have on `backlog run`. Cite the
file and sentence for the convention and the ordering rule. (Do not actually create issues — describe the
action.)

**P8 (ac-8).** Through what do you publish the tickets, and in what format? On this repo, what is a "ticket"
concretely, and what word does the skill use in its own text? Cite the binding and the vocabulary rule.

**P9 (ac-9).** The split is approved. Do you apply the `ready-for-agent` readiness role to the new tickets
yourself? What is the default, what is the noted option, and whose posture is the option? Cite the sentence.

**P10 (ac-10).** Drafting a ticket, you're tempted to paste the path of the module it changes and a short code
fragment. Does the skill allow file paths and code in a ticket? What is the single exception? Separately: may
to-tickets edit the source spec or the parent issue? Cite both rules.

**P11 (ac-11).** Read `skills/to-tickets/agents/openai.yaml`. Is it well-formed per
`docs/patterns/codex-compat.md`, and is `allow_implicit_invocation` set correctly for an operator skill that
publishes to a tracker? State the value and why it's right.

**P12 (ac-12).** Read `skills/to-tickets/evals/probes.md`. Does a pre-written answer key exist covering
ac-1..ac-11, and is the method dual-executor (Opus in-session + `codex exec`) and read-only per
`docs/patterns/probe-evals.md`? State what you checked.

## Answer key

- **P1 (ac-1):** Frontmatter has `name: to-tickets`, `user-invocable: true`, and a `description` that reads as
  splitting a spec/plan/conversation into backlog-ready tickets with blocking edges — **pass**. No file imports
  another skill's files (the dependency surface says the skill is "self-contained at the file level" and "no file
  here imports or reads another skill's files"; a grep for cross-skill paths finds none). Directory carries the
  shipped layout (SKILL.md, README.md, agents/openai.yaml, reference/, templates/, evals/). Claiming a
  cross-skill import exists = fail.
- **P2 (ac-2):** The three pointer kinds: **bundled references** (own `reference/` + `templates/`), **project
  playbooks** (the dependency convention `backlog-policy.md` § Dependencies **and** the tracker binding
  `platform.md`), **sibling skills** (consumes `to-spec`'s output; also accepts a `plan` or a raw conversation,
  composed by name). On `backlog` it must say to-tickets emits **into** backlog's convention (a **project
  playbook**), **not** an imported sibling — keeping the skill self-contained. Missing any of the three, or
  calling backlog a sibling import, = fail.
- **P3 (ac-3):** **Yes** — a spec at `docs/specs/<name>.md` (to-spec's output) is the **primary** input. The two
  alternates are a **plan** and the **raw current conversation**. Cite SKILL.md § "How a split happens" step 1 or
  `reference/slicing.md` § "Read the direction." Naming the wrong primary path, or missing the alternates, =
  fail.
- **P4 (ac-4):** **Not right** — "all the models / all the logic / all the UI" is the **horizontal layer**
  anti-pattern. The skill wants a **vertical slice / tracer bullet**, whose three properties are: a
  **narrow-but-complete path through every layer**, **demoable on its own**, and **sized to one fresh context
  window**. Cite `reference/slicing.md` § "Draft vertical slices" (or SKILL.md § "What a ticket is"). Endorsing
  the horizontal split, or missing the properties, = fail.
- **P5 (ac-5):** **No, not a single vertical slice.** A mechanical, high-blast-radius change is sequenced
  **expand → migrate-in-batches → contract**. The trigger is **both** conditions together — *mechanical* (little
  per-site judgement) **and** *high blast radius* (many sites). Cite `reference/slicing.md` § "The wide-refactor
  exception." Missing the three-phase shape, or the both-conditions trigger, = fail.
- **P6 (ac-6):** **Do not publish yet.** First **quiz the user** — the human-confirmation step — on **granularity**
  and **blocking edges**, iterating until approved; **nothing publishes before approval.** This differs from
  `to-spec`, which is pure synthesis and never interviews. Cite `reference/slicing.md` § "Quiz the user" (or
  SKILL.md). Publishing before the quiz, or missing the contrast with to-spec, = fail.
- **P7 (ac-7) — load-bearing:** (a) Create **A first**, then B and C — **blockers first** — because the tracker
  assigns an id at creation, so a dependent can only reference A once A exists. (b) B and C **each** carry a
  **`- [ ] depends on #<A's id>`** task-list line **in the ticket body** — the marker copied **verbatim** from
  backlog's recorded convention (`backlog-policy.md` § Dependencies records the literal lowercase
  `- [ ] depends on #123`); B and C carry **no** edge to each other (independent). (c) `backlog run`
  treats a ticket with any unchecked, unclosed dependency as **blocked and skips it**, so B and C are skipped
  until A closes. Cite `reference/slicing.md` § "Order and wire the edges" (convention + blockers-first) and
  `backlog-policy.md` § Dependencies. Wrong order (blocker last), a restyled marker that doesn't match the
  playbook's literal form, an edge between B and C, or omitting the run-skips-blocked effect = fail.
- **P8 (ac-8):** Publish through the **tracker binding in `docs/agents/platform.md`** — on this repo **GitHub via
  `gh`** (`gh issue create`), so a "ticket" is concretely a **GitHub issue** — **in dependency order, blockers
  first**. The skill's own text uses the generic word **"ticket"** (ticket == the tracker's issue role). Cite
  `reference/slicing.md` § "Publish in the bound tracker's format" and the vocabulary rule. Naming a hardcoded
  tracker in the skill's own vocabulary, or missing the binding, = fail.
- **P9 (ac-9):** **No — do not auto-apply `ready-for-agent`.** The **default** is to **leave readiness to
  `backlog groom`**; the **noted option** is to apply it on approval, which is **Matt Pocock's posture** (the
  quiz is the human confirmation). Cite `reference/slicing.md` § "Readiness alignment — leave it to groom" (or
  SKILL.md step 5). Auto-releasing by default = fail.
- **P10 (ac-10):** **No file paths and no code snippets** in a ticket — they rot; describe the module/contract
  **in prose**. The single exception is a **prototype-validated snippet** encoding a decision more precisely than
  prose (state machine, schema, type shape). And **no** — to-tickets **never modifies the source spec or the
  parent issue** (it only reads them). Cite `reference/slicing.md` § "No stale content" **and** § "Read the
  direction" / SKILL.md "The parent is never touched." Allowing arbitrary paths/code, dropping the exception, or
  saying it may edit the parent, = fail.
- **P11 (ac-11):** Well-formed: `interface.display_name` "To-Tickets", a one-line `short_description` matching the
  SKILL.md spirit, a concrete `default_prompt`, and `policy.allow_implicit_invocation: false`. `false` is correct
  because to-tickets is an operator skill that publishes to a tracker (spends/creates), not a lightweight
  advisory skill — codex-compat.md says default `false` for operator-style skills. Saying `true`, or malformed
  YAML, = fail.
- **P12 (ac-12):** The file carries a **pre-written answer key** with a probe per ac-1..ac-11 (this file is
  ac-12) and a coverage map; the method names **both** executors (Opus subagent + `codex exec --sandbox
  read-only`) and states it is **read-only / dry-run** per `docs/patterns/probe-evals.md`. A grep confirms an
  Answer key section, both executor names, and the read-only note. Missing the key, a single-executor method, or
  no read-only guarantee, = fail.

## Scoring

12 probes × 2 executors (Opus in-session + `codex exec`). A probe passes only with the **correct action AND a
correct citation**. Ambiguity flags are recorded as findings, not failures — they are the most valuable output
and should drive wording fixes before ship. Report a verdict table mapping each probe → its criterion →
pass/fail per executor. Structural criteria are additionally confirmed by file check: ac-1 (frontmatter + grep
no cross-skill imports), ac-2 (three-part surface present, backlog framed as playbook), ac-11 (YAML parses),
ac-12 (key + dual-executor + read-only present).

### Criterion coverage map

| criterion | probe(s)         |
|-----------|------------------|
| ac-1      | P1               |
| ac-2      | P2               |
| ac-3      | P3               |
| ac-4      | P4               |
| ac-5      | P5               |
| ac-6      | P6               |
| ac-7      | P7 (load-bearing)|
| ac-8      | P8               |
| ac-9      | P9               |
| ac-10     | P10              |
| ac-11     | P11              |
| ac-12     | P12 (this file)  |
