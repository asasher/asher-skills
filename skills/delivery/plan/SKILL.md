---
name: plan
description: Turn an intent worth planning into a human-approved plan artifact — decide plan-or-skip, settle blocking design questions, write the plan with testable acceptance criteria, and hold it at the approval gate. Domain-neutral, not only code. Use when a goal — or a sibling workflow — needs an approved plan before work starts. Not for doing the work the plan describes.
argument-hint: "[<goal to plan> | skip-check <goal>]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [review-loop, staffing]
  optional: [prototype]
---

# Plan

Owns intent → approved plan. Committing, building, and tracker mirroring belong to the caller. The method is
domain-neutral; project-specific rigor comes from optional `docs/agents/planning.md` deltas.

## Commands

- **`<goal>`** — load [plan-contract](reference/plan-contract.md); at the writing gate also load
  [authoring](reference/authoring.md) and `templates/plan-skeleton.html`.
- **`skip-check <goal>`** — run only the plan-or-skip gate and return the decision plus reason.

## Gates

1. **Decide.** Apply the project threshold or bundled default. A small, low-risk, reversible change returns
   `skip`; otherwise continue.
2. **Settle design.** Label unfamiliar mechanism claims as hypotheses and falsify them before dependency.
   Invoke `prototype` by name for logic/UI questions that need an artifact; otherwise spike or research.
3. **Write.** Produce self-contained HTML whose stable `ac-N` criteria are checkable pass/fail and declare
   required data/tenant/scale/lifetime/observation. Use `staffing route <plan-author task>` for author selection.
4. **Approve.** Present through `review-loop`; disposition every annotation until the hash-bound verdict is
   approve. Stop here and return the plan plus approval event.

A failed falsification returns to design. Rejected review returns to writing. Missing `review-loop` degrades
to a local open/conversational verdict; missing `prototype` uses a recorded spike/research fallback; missing
`staffing` is reported rather than replaced with an invented roster.

## Dependency surface

- **Bundled:** the two references and HTML skeleton above; these are the complete default contract.
- **Project:** optional delta-only `docs/agents/planning.md`.
- **Siblings:** required `review-loop` and `staffing`; optional `prototype`, all invoked by name with no file imports.
