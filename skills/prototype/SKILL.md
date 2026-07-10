---
name: prototype
description: Answer one design question with a throwaway artifact, then throw it away — keep the answer, delete the scaffolding. Usable anywhere, not only dev. Use to settle a state model, layout, UI, or document direction with real alternatives rather than argument — directly, or when a workflow skill hits a question paper can't settle. Not for building the real thing.
argument-hint: "<design question>"
user-invocable: true
---

# Prototype

A prototype is a **throwaway artifact that answers one design question.** The answer is the only deliverable;
the artifact is scaffolding you build to reach it and tear down after. The medium is usually code but need
not be — a rendered document, a layout, a maquette, a driven scenario all count. Throwaway from day one: keep
the answer, delete the artifact.

Prototype is a **thin composer.** It owns the technique for framing a question and building the smallest thing
that settles it; it does not own reviewing or staffing — it composes the `review-loop` and `staffing` skills
by name for those. The full technique — the two shapes and their rules, generalized beyond code — is in
[prototyping](reference/prototyping.md); repo-specific placement (task runner, where throwaway artifacts live,
the component library) is in the project playbook `docs/agents/prototyping.md`. Absent a playbook, the
technique's defaults apply — don't improvise repo structure.

## Entry points

- **Directly:** `prototype "<design question>"` — a user hands one explicit question.
- **From a skill:** `plan` hands over a logic or UI question its gates can't settle on paper (including one a
  reviewer requests during plan review), or another workflow skill (e.g. `backlog`) does the same from any
  branch; the caller folds the answer back in.

Invoked without a clear question, the first move is to extract one — a prototype answering a vague question is
pure waste.

## Gates

Walk these in order; each is the completion criterion for its step.

1. **Question stated** — one explicit design question, recorded at the prototype's location, and the shape
   picked per [prototyping](reference/prototyping.md) (behavior vs form). A prototype answering a vague or
   wrong question is pure waste — this gate is where that is caught.
2. **Built and handed over** — the prototype runs from one command or one URL, surfaces its state, and is
   presented for feedback. Build-out is dispatched to the model the **`staffing`** skill resolves. A
   form-shape prototype, or any answer that is a document a human should mark up, is served through the
   **`review-loop`** skill (don't fork a review UI); a live interactive prototype is driven directly. Either
   way the pause message ends with the artifact's URL and the hub URL, so the human can drive it from
   wherever they are. Extend it on request; prototypes evolve.
3. **Answer captured** — the decision and its why are written somewhere durable: into the consuming plan when
   called from planning (with variant captures for form shapes), otherwise into the record the playbook
   names. The prototype itself is never the record.
4. **Cleaned up** — the prototype is deleted, or its validated core (a pure behavior module, a winning
   variant) is properly absorbed into real work. Nothing throwaway is left behind.

## How it composes

- **`review-loop`** presents the answer. A rendered artifact — a variant sheet, an answer write-up — is
  served through review-loop's server so feedback arrives as anchored annotations with a batched verdict, not
  prose in chat. Prototype invokes it by name and never reimplements the annotation/approval machinery. Where
  no presentation surface is recorded, review-loop degrades to a local open.
- **`staffing`** staffs the build. Framing the question and reading the answer stays with the invoking
  thread; building the artifact (a reducer + shell, a set of variants, draft sheets) is routed to the builder
  staffing resolves — mechanical build-out to the pinned mechanical model, taste-weighted build-out (a UI
  variant, a rendered document) to a taste-ranked model. Prototype asks; it does not hardcode the roster.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [prototyping](reference/prototyping.md),
  the authoritative technique (the two shapes, the throwaway rules, capture and cleanup), written to stand
  alone so the skill works outside dev. It imports no other skill's files.
- **Project playbook** — the repo-specific placement config at `docs/agents/prototyping.md`: the task runner
  and how to register a script, the routing/where-shared-UI-lives convention, where throwaway artifacts are
  kept, and the component library variants must use. Prototype reads it for the "where," never for the
  technique. A fresh install needs such a playbook to place prototypes idiomatically; absent one, the skill
  degrades to the technique's defaults (a self-contained artifact in a scratch/workspace dir) rather than
  improvising repo structure.
- **Sibling skills** — **`review-loop`** (present the answer for feedback) and **`staffing`** (staff the
  build), composed **by plain name, no imports**. Unlike the root primitives review-loop and staffing (which
  carry no load-bearing sibling dependency), **`prototype` is a composer** — these two siblings are
  load-bearing dependencies.
