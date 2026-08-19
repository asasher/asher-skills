---
name: to-slices
description: Split a decided direction — a spec'd ticket, a spec or plan document, or the current conversation — into backlog-ready tracer-bullet tickets with blocking edges. Runs only on the user's explicit call. Not for writing the direction itself.
argument-hint: "[<spec'd ticket id or spec path, or nothing to use the conversation>]"
metadata:
  optional: [writing-for-humans]
---

# To-Slices

To-slices owns one move: **take a decided direction and split it into backlog-ready tickets with blocking edges.** It reads a direction, drafts vertical slices, and publishes the approved tickets into the bound tracker in dependency order. When the direction is a spec'd ticket, the split parents it over its slices: each slice a child, the parent converted to the `spec` work-type (slicing § Parent the slices). To-slices runs only on the user's explicit call — a spec may _recommend_ a split, but nothing splits until the user approves it.

The defining posture: **recommend with reasons, then let the user edit.**

User-facing text follows the `writing-for-humans` sibling. Absent it, write plainly and say the standard was not loaded.

## Command surface

- **`to-slices [<spec'd ticket id or spec path>]`** — split the given direction into tickets (inputs: step 1).

## How a split happens

The full method is in [slicing](reference/slicing.md); the shape:

1. **Read the direction** — the input forms and how each is read are in slicing § Read the direction. Done when you can name every actor, every surface the change touches, and every acceptance criterion the direction settles — the same list the draft's coverage bound then walks.
2. **Draft vertical slices, with rationale.** Cut the work into tracer-bullet tickets — or, for a **wide refactor**, into its expand→migrate-in-batches→contract sequence — each slice carrying its rationale (slicing § Draft vertical slices).
3. **Recommend the landing shape**, with the justification stated (slicing § The landing shape).
4. **Present the split draft ([template-guide](reference/template-guide.md) § The split draft) — the confirmation gate.** The user edits; iterate until they approve.
5. **Audit each ticket — backlog-ready or not published** (slicing § Audit each ticket).
6. **Order and wire the edges** — dependency order, **blockers first**, each edge wired exactly as the repo's recorded convention (slicing § Order and wire).
7. **Publish in the bound tracker's format** — through the tracker binding recorded in `docs/agents/platform.md`, blockers first, readiness left unset by default (slicing § Publish, § Readiness).
8. **Parent a split ticket over its slices** — child relations, the `spec` conversion, the pointer comment (slicing § Parent the slices).
9. **Readback.** Verify against the live tracker: every approved draft maps to exactly one created ticket, every wired dependency edge — native relation or recorded marker — resolves to a real, earlier ticket id, and every slice of a split parent reads back as its child. Fix any miss before reporting the split done.

## What a ticket is (and isn't)

- **A tracer bullet, not a task list** — the definition and the **wide-refactor** exception live in slicing § Draft vertical slices and § The wide-refactor exception.
- **Generic vocabulary.** A **ticket** is the unit of pickup-able work — the tracker's "issue" in a tracker-agnostic word; say "ticket" in everything you publish.
- **No file paths or code snippets** — sole exception the prototype-validated snippet (slicing § No stale content).

## Dependency surface

- **Project playbooks** — the repo's conventions, read from `docs/agents/` across the split steps: the **dependency convention** (`backlog-policy.md` § Dependencies — the edge wiring in step 6), the **`spec` work-type, `delivered` role, and open-children rule** (`backlog-policy.md` § Label roles — the parenting in step 8), and the **tracker and branch bindings** (`platform.md` — ticket creation in step 7, the child relation in step 8, the feature-branch convention for stacked landings).
