---
name: interview
description: Interview the user about an idea or problem until shared understanding is real. Use to elicit and settle the strategic decisions behind new work, directly or when a workflow skill needs an intent sharpened before spec or tickets. It asks and classifies; it writes no durable artifacts — compose `interview-with-docs` for that.
argument-hint: "<idea, problem, or reference to intake material>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: [prototype, research, staffing]
---

# Interview

Elicit the decisions behind a piece of work by walking its **decision tree**: every decision branches into
the decisions that hang off it. Work the tree in **rounds** over the **frontier** — every decision whose
prerequisites are already settled.

## Intake first

Before asking anything, read what already exists: named files (a PDF, a brief, a doc), the repo, and the
durable context — `PRODUCT.md`, `DESIGN.md`, `CONTEXT.md`, ADRs, prior specs — wherever the project keeps
them. **Provided artifacts are read, not asked about.** Intake seeds the tree with what is already settled
and what the evidence leaves open.

## Facts are yours; decisions are the user's

- A **fact** lives in the environment — the filesystem, the code, a tool, an external source. Look it up:
  directly for the repo, through the `research` skill (by name) for external sources. Never ask the user for
  anything you could find.
- A running lookup is an unsettled prerequisite: only the questions downstream of it wait — ask the rest of
  the frontier now.
- A **decision** is the user's. Put each one to them and wait.
- A question paper cannot settle — a state model or form direction that needs something concrete to react
  to — goes to the `prototype` skill (by name) as a probe, not to another round of prose.

## Rounds

Ask the whole frontier in one numbered round. If a round balloons past comfortable answering, split it by
dependency cluster and say so — a cap is manners, not a rule. Each question carries:

- the **evidence already in hand** (from intake or earlier answers);
- what the answer **unlocks** downstream;
- a **recommended hypothesis with its trade-off** — labelled provisional, never a nudged default;
- cheap affordances: **accept / modify / defer / unknown** — agreeing costs a word, disagreeing a sentence.

One topic per question; never a compound either-or. When the evidence already points one way,
**assert-then-confirm** ("this reads as X — confirm?") beats a menu. Questions whose answers depend on
another question still open in this round belong to a later round.

After every round: **play back the delta** — what settled, what it unlocked, and any contradiction with
earlier answers or intake evidence — then recompute the frontier.

## Stopping

Two tests, both required:

1. **The frontier is empty** — no decision is askable that hasn't been asked.
2. **Coverage holds** — sweep the families relevant to this surface and risk profile: problem and current
   process; actors and permissions; desired outcomes; scenarios and failure states; data and privacy;
   non-functional qualities; rollout and migration; operations; UX register and design direction; testing
   and evidence; dependencies; non-goals. A family with a material unasked question reopens the frontier.
   "We feel aligned" is the sign-off, never the test.

Then present the full playback and ask for confirmation of shared understanding.

## Exit

State, in one confirmable line each:

- the classification of **every open thread**: *settled*, *delegated* (the executor may choose, boundary
  named), *deferred* (parked, with a home), or *blocking* (cannot proceed);
- the **depth call** — implement now, slice to tickets, or spec first — as a recommendation the user
  confirms or overrides.

This skill records nothing durable. When settled terms and decisions should outlive the conversation — a
glossary term, an ADR, spec input — run `interview-with-docs`.

## Dependency surface

- **Bundled:** none — this file is the whole contract.
- **Siblings (optional, by name):** `research` for external facts, `prototype` for paper-unsettleable
  questions, `staffing` when a lookup needs a staffed worker. Absent a sibling, state the gap and continue
  with direct lookups; never silently skip a fact.
