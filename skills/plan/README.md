# Plan

Turns an intent worth planning — a feature, a research effort, an ops change, any non-trivial undertaking —
into a **reviewed plan artifact**, and holds it at a human approval gate. A thin composer: it produces the
plan and borrows sign-off from the `review-loop` skill, role selection from the `staffing` skill, and
design-question artifacts from the `prototype` skill, all by name. Domain-neutral — not only for code.

## When to use

- **Planning something worth planning** — decide plan-or-skip against a threshold, then produce a
  self-contained HTML plan with explicit, testable acceptance criteria.
- **Getting a plan approved** — present it through `review-loop` and block on a human verdict before any work
  starts.
- **Just the decision** — `skip-check <goal>` returns plan-or-skip without committing to the whole flow.

Not for doing the work the plan describes — only for planning it and getting sign-off.

## Shape

- **Thin composer, no runtime.** Plan ships no server and no scripts. It authors an artifact and composes
  three siblings by plain name: `review-loop` for the sign-off gate, `staffing` for "who authors or builds,"
  and `prototype` for logic/UI design questions (gate 2, or on a reviewer's request at the approval gate).
- **Four gates, stops at Approved.** Decide → settle design questions → write → approve. The deliverable is
  the approval record (verdict, content hash, timestamp). Committing the plan and starting the work are the
  **caller's** concern — there is no gate 5.
- **Domain-neutral by default.** The bundled contract assumes no code, repo, or running app; acceptance
  criteria are "checkable pass/fail." A project playbook layers domain rigor on top.
- **Two-layer, standalone-usable.** The bundled references carry the full default contract (threshold, format,
  gates), so the skill runs with no project playbook; the playbook (`docs/agents/planning.md`) is a delta-only
  override.

## Layout

`SKILL.md` is the command surface (`<goal>` / `skip-check`) and points into `reference/`:
`plan-contract.md` (the four gates, the threshold, the sibling compositions) and `authoring.md` (what a plan
covers + the house format). `templates/plan-skeleton.html` is the authoritative plan document shape (stable
ids, `ac-N` criteria, self-contained). `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the
pre-deployment probe eval.

Self-contained at the file level; composes by name. **Sibling dependencies:** `review-loop` (sign-off gate),
`staffing` (who authors/builds), and `prototype` (design-question artifacts, soft) — invoked by name, never
imported.

## Install

`npx skills add <repo-url> --skill plan`, then invoke it on a goal. It expects the `review-loop`, `staffing`,
and `prototype` skills present in the project (the `setup-asher-skills` installer guarantees a skill's
siblings); absent `review-loop`, plan degrades to a local review fallback; absent `staffing`, it states the
role question rather than inventing a roster; absent `prototype`, design questions fall to spike/research
with the gap recorded. On a fresh repo with no `docs/agents/planning.md`, the bundled defaults stand.

## Not in scope (the caller's job)

Plan stops at an approved plan. **Committing** the plan to a branch or store, **building** what it describes,
and **mirroring** it to a tracker are the caller's concern — a dev workflow like `backlog` adds that tail
around the composer: `backlog`'s enhancement branch invokes this skill by name and keeps the
commit-and-implement dev-tail on its own side.
