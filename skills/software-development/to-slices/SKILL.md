---
name: to-slices
description: Split a decided direction — a spec'd ticket, a plan document, or the current conversation — into backlog-ready tracer-bullet tickets with blocking edges, presenting a justified split and landing shape for the user to edit and approve before publishing to the bound tracker in dependency order; a split parent ticket takes the spec work-type over its slices. Runs only on the user's explicit call. Not for writing the direction itself.
argument-hint: "[<spec'd ticket id or spec path, or nothing to use the conversation>]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: [plain-language]
---

# To-Slices

To-slices owns one move: **take a decided direction and split it into backlog-ready tickets with blocking edges.** It reads a direction, drafts vertical slices, presents the split as a **justified recommendation the user edits**, then — on approval — publishes the tickets into the bound tracker in dependency order. When the direction is a spec'd ticket, the split **parents it over its slices**: each slice is attached as a child, and the parent converts to the `spec` work-type — it stays alive as the shared context the slices inherit from, undispatchable while any child is open and undelivered, and its remaining work is the closing coverage check. Its spec text is never touched. To-slices runs only on the user's explicit call — recommending a split is someone else's move; performing one is never self-initiated.

The defining posture: **recommend with reasons, then let the user edit.** Every slice carries one or two sentences of rationale (why this boundary, why demoable alone), every blocking edge is justified in words, and the recommended **landing shape** is justified too. The user edits the draft; nothing publishes before their approval. Each ticket is a **tracer bullet**, with a **wide-refactor** exception for mechanical, high-blast-radius changes — both defined under § What a ticket is.

User-facing text follows the `plain-language` sibling — ASD-STE100 plain language, `CONTEXT.md` as the dictionary, no bare ticket or PR numbers. Absent it, write plainly and say the standard was not loaded.

## Command surface

- **`to-slices [<spec'd ticket id or spec path>]`** — split the given direction into tickets. The primary input is a **ticket carrying a spec projection** (the spec read from its artifact branch at the blessed hash); a spec document path is the no-tracker alternate. With no argument, use the current conversation as the direction (or a plan, if one is on the table).

Load [slicing](reference/slicing.md) for the method (what to read, the vertical-slice default, the wide-refactor exception, the justified recommendation, the landing shape, dependency ordering and the playbook's edge convention, the readiness default, the no-stale-content rule, parenting the slices) and [template-guide](reference/template-guide.md) for what each ticket carries and what the pre-publish split draft shows the user.

## How a split happens

The full method is in [slicing](reference/slicing.md); the shape:

1. **Read the direction.** The primary input is a **spec'd ticket** — its projection names the blessed hash; read the spec file from the artifact branch at that hash. A spec document, a **plan**, or the **raw current conversation** are accepted alternates, read the same way — mine the decided direction, the actors, and the surface. Never modify the spec text.
2. **Draft vertical slices, with rationale.** Cut the work into tracer-bullet tickets — or, for a wide refactor, into its expand→migrate-in-batches→contract sequence (§ What a ticket is) — each slice carrying its one-or-two-sentence justification.
3. **Recommend the landing shape** (slicing § The landing shape): **stacked** (the default for split specs) or **direct**, with the justification stated.
4. **Present for edit and approval — the human-confirmation step.** One draft document: the slices with their rationale, the edges justified in words, the landing shape, and the blessed spec hash the slices were cut from. The user edits; iterate until they approve. 4b. **Audit each ticket for readiness** (slicing § Audit each ticket for readiness) — a ticket failing the audit is fixed or dropped, never published thin.
5. **Order and wire the edges.** Sort the approved tickets into dependency order — **blockers first** — so each dependency edge resolves to a real, earlier id. Wire each edge exactly as the repo's recorded convention (slicing § Order and wire).
6. **Publish in the bound tracker's format.** Create the tickets through the tracker binding recorded in `docs/agents/platform.md`, blockers first, per slicing § Publish; readiness is left unset by default (slicing § Readiness).
7. **Parent a split ticket over its slices.** When the input was a spec'd ticket, attach every slice as its child through the parent/child relation the platform playbook records, and convert the parent to the `spec` work-type per the label roles (slicing § Parent the slices) — tracker state changes plus a pointer comment; the spec text stays untouched. The policy's open-children rule keeps the parent undispatchable until every child is **closed or delivered**.
8. **Readback.** Verify against the live tracker: every approved draft maps to exactly one created ticket, every wired dependency edge — native relation or recorded marker — resolves to a real, earlier ticket id, and every slice of a split parent reads back as its child. Fix any miss before reporting the split done.

## What a ticket is (and isn't)

- **A tracer bullet, not a task list.** A ticket is a narrow-but-complete path through every layer — demoable on its own, sized to one fresh context window — not a horizontal layer ("all the models," "all the UI") that can't be demoed alone. The one exception is a **wide refactor** — a mechanical, high-blast-radius change.
- **Generic vocabulary.** A **ticket** is the unit of pickup-able work; it is exactly the tracker's "issue" role, in a tracker-agnostic word. Say "ticket" throughout — the skill's own text never assumes GitHub's vocabulary.
- **No file paths or code snippets** — sole exception the prototype-validated snippet (slicing § No stale content).
- **The spec text is never rewritten** — a split parent's conversion to the `spec` work-type is a tracker state change, a child relation per slice, and a pointer comment, not an edit to the direction (slicing § Parent the slices).

## Dependency surface

- **Project playbooks** — the repo's conventions, read from `docs/agents/` across the split steps: the **dependency convention** (`backlog-policy.md` § Dependencies — the edge wiring in step 5), the **`spec` work-type, `delivered` role, and open-children rule** (`backlog-policy.md` § Label roles — the parenting in step 7), and the **tracker and branch bindings** (`platform.md` — ticket creation in step 6, the child relation in step 7, the feature-branch convention for stacked landings). Absent a recorded binding, state the gap and ask the user before publishing anything.
