---
name: interview
description: Interview the user about an idea or problem until shared understanding is real. Use to elicit and settle the strategic decisions behind new work, directly or when a composing skill needs decisions settled. It asks and classifies; it writes nothing durable.
argument-hint: "<idea, problem, or reference to intake material>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: []
  optional: []
---

# Interview

Elicit the decisions behind a piece of work by walking its **decision tree**: every decision branches into
the decisions that hang off it. Work the tree in **rounds** over the **frontier** — every decision whose
prerequisites are already settled.

## Intake first

Before asking anything, read what was handed to this session — named files, pasted material, whatever
intake the caller provides. **Provided artifacts are read, not asked about.** Intake seeds the tree with
what is already settled and what the evidence leaves open.

## Facts are yours; decisions are the user's

- A **fact** lives in the environment. Look it up directly when this session can reach it; when it can't —
  an external source, a staffed lookup — classify the question **needs-lookup** and defer only what depends
  on it. Never ask the user for anything that can be found.
- A **decision** is the user's. Put each one to them and wait.
- A question paper cannot settle — a state model or presentation direction that needs something concrete to
  react to — is classified **needs-probe** and deferred the same way.
- Classified questions are the composer's to resolve between rounds; standalone, present them to the user
  as open threads.
- An interface's non-obvious presentation choices — the visual hierarchy, which actions are overt, what each
  journey step shows — are decisions, not taste calls: settle them here; implementation never invents them.

## Rounds

Ask the whole frontier in one numbered round. If a round balloons past comfortable answering, split it by
dependency cluster and say so — splitting is a courtesy to the reader, not a fixed limit. Each question
carries:

- the **evidence already in hand** (from intake or earlier answers);
- what the answer **unlocks** downstream;
- a **recommended hypothesis with its trade-off** — labelled provisional, never a nudged default;
- cheap affordances: **accept / modify / defer / unknown** — agreeing costs a word, disagreeing a sentence.

One topic per question; never a compound either-or. When the evidence already points one way,
**assert-then-confirm** ("this reads as X — confirm?") beats a menu. A question depending on another in the
same round isn't frontier yet — push it to a later round.

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

- the classification of **every thread**: *settled*, *delegated* (the executor may choose, boundary
  named), *deferred* (parked, with a home), or *blocking* (cannot proceed);
- the **depth call** — implement now, slice to tickets, or spec first — as a recommendation the user
  confirms or overrides.

This skill records nothing durable. Durable capture — glossary terms, decisions, spec input — belongs to
whatever composed the interview.
