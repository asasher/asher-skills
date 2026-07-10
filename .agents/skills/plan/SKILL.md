---
name: plan
description: Turn an intent worth planning into a human-approved plan artifact — decide plan-or-skip, settle blocking design questions, write the plan with testable acceptance criteria, and hold it at the approval gate. Domain-neutral, not only code. Use when a goal — or a sibling workflow — needs an approved plan before work starts. Not for doing the work the plan describes.
argument-hint: "[<goal to plan> | skip-check <goal>]"
user-invocable: true
---

# Plan

Plan owns one capability: get from *an intent worth planning* to *an approved plan* — and no further. It
decides whether a plan is warranted at all, settles the design questions paper can't, writes a reviewable
plan artifact with explicit testable acceptance criteria, and holds that artifact at a human approval gate.
The deliverable is **the approval record** — a human-approved plan and the approve event that binds it. What
happens after approval (commit it, build from it, track it) belongs to the caller, not here.

It is a **thin composer** — no runtime of its own, no server, no scripts. It authors an artifact and borrows
three capabilities from sibling skills: the sign-off gate from **`review-loop`**, "who should author or
build this" from **`staffing`**, and design-question artifacts from **`prototype`** (how, and what happens
when a sibling is absent, is the dependency surface below).

Plan is **domain-neutral.** A plan can be for a research sprint, an ops migration, a product bet, or a code
change. The bundled contract assumes none of these; acceptance criteria are "checkable pass/fail," not
"against a running app." Dev-specific rigor is layered on top by a project playbook, never baked into the
default.

## Command surface

- **`<goal>`** (default) — run the gates for an intent worth planning: decide plan-or-skip, settle blocking
  design questions, write the plan, and present it for approval. Load [plan-contract](reference/plan-contract.md)
  (the gates + threshold + the sibling compositions) and [authoring](reference/authoring.md) (what a plan covers +
  the house format) when you reach the writing gate.
- **`skip-check <goal>`** — run only gate 1: return a plan-or-skip decision against the threshold, with the
  reason. For a caller that wants the decision without committing to the whole flow. Load
  [plan-contract](reference/plan-contract.md).

Invoked with no argument on a stated goal, run the full gate sequence.

## How the gates resolve

The full contract is in [plan-contract](reference/plan-contract.md); the sequence is four gates, and it
**stops at Approved**:

1. **Decide** — a stated plan-or-skip decision grounded in the playbook's threshold (or the bundled default).
   A small, low-risk, easily-reversible change skips planning; the composer says so and returns.
2. **Design questions answered** — any question the plan can't settle on paper is settled first and folded
   into the plan. Plan decides the shape: a logic question (a model that only feels right under real cases)
   or a UI question (something that must be seen) goes to the **`prototype`** skill by name; anything else
   falls to a spike or research. A reviewer can also send the plan back for a prototype during gate 4.
3. **Written** — the plan exists as a self-contained HTML document meeting [authoring](reference/authoring.md),
   with the definition of done stated as explicit, testable acceptance criteria (`<li id="ac-N" data-criterion>`),
   each a checkable pass/fail. Start from `templates/plan-skeleton.html`.
4. **Approved** — the rendered plan is presented through the **`review-loop`** skill by name (serve → annotate
   → verdict-coded await); a human approves it, as-is or after revision rounds in which every annotation gets
   a ledger disposition (a mechanic review-loop owns). The approve event — verdict, content hash, timestamp —
   is the approval record. There is no gate 5: committing the plan and starting the work are the **caller's**
   concern.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory under `reference/`:
  [plan-contract](reference/plan-contract.md) (the four gates, the plan-or-skip threshold defaults, and the
  composition of review-loop, staffing, and prototype) and [authoring](reference/authoring.md) (what a plan covers and the
  house format), plus `templates/plan-skeleton.html` (the authoritative plan document shape). These carry the
  **full default contract** so the skill runs standalone; they import no other skill's files.
- **Project playbook** — an optional, **delta-only** override installed under `docs/agents/` (on this repo,
  `docs/agents/planning.md`). It overrides only what differs from the bundled default: the plan-size
  threshold, the plan-file location convention, the approval authority, and any domain-specific rigor (for a
  dev repo: acceptance criteria against a running app, test seams, verify/evidence, the post-approval
  commit-and-implement tail). Absent a playbook, the bundled default stands.
- **Sibling skills** — three, all composed by plain name, never imported:
  - **`review-loop`** — the **sign-off gate** (gate 4). Plan renders the artifact; review-loop serves it,
    injects the annotation layer, and blocks on a verdict-coded await. Absent it, plan degrades to the local
    fallback (open the rendered plan on the machine, take the verdict in conversation).
  - **`staffing`** — **who authors or builds.** Any "which model should do this?" question — who writes the
    plan, who implements what it describes — resolves against the installed roster via staffing. Absent it,
    plan states the need rather than inventing a roster.
  - **`prototype`** — **design-question artifacts** (gate 2), and any prototype a reviewer requests during
    the approval round. A soft dependency: absent it, settle the question by spike or research and record
    the gap in the plan's notes.
