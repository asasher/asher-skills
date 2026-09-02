---
name: to-slices
description: Split a decided direction — an approved spec on a GitHub issue, a spec or plan document, or the current conversation — into ready tracer-bullet child issues with blocking edges. Runs only on the user's explicit call. Not for writing the direction itself.
disable-model-invocation: true
metadata:
  optional: [technical-writing]
---

# To-Slices

To-slices owns one move: **take a decided direction and split it into ready issues with blocking edges.** It reads a direction, drafts vertical slices, and publishes the approved issues in dependency order. When the direction is a spec'd issue, the split parents it over its slices: each slice a sub-issue, the parent blocked by each, the parent relabeled `spec`. To-slices runs only on the user's explicit call: a spec may recommend a split, but nothing splits until the user approves it.

The defining posture: **recommend with reasons, then let the user edit.**

Issue and split-draft text follows the `technical-writing` sibling. Absent it, write plainly and say the standard was not loaded.

## Command surface

- **`to-slices [<spec'd issue id or spec path>]`**: split the given direction into issues.

## How a split happens

The full method is in [slicing](reference/slicing.md); the shape:

1. **Read the direction** (slicing § Read the direction). Done when you can name every actor, every surface the change touches, and every acceptance criterion the direction settles.
2. **Draft vertical slices, with rationale.** Cut the work into tracer-bullet issues, or, for a wide refactor, into its expand, migrate-in-batches, contract sequence, each slice carrying its rationale (slicing § Draft vertical slices).
3. **Present the split draft** ([template-guide](reference/template-guide.md) § The split draft), the confirmation gate. The user edits; iterate until they approve.
4. **Audit each issue**: ready, or not published (slicing § Audit each issue).
5. **Order and wire the edges**: dependency order, blockers first, each edge a native `blocked_by` (slicing § Order and wire).
6. **Publish** with `gh issue create`, blockers first, each child `ready-for-agent` with its work-type (slicing § Publish).
7. **Parent a split issue over its slices**: sub-issues, the parent's `blocked_by` edges, the `spec` label, the pointer comment (slicing § Parent the slices).
8. **Readback.** Verify against GitHub: every approved draft maps to exactly one created issue, every wired edge resolves to a real earlier issue, every slice of a split parent reads back as its sub-issue and as its blocker. Fix any miss before reporting the split done.

## What an issue is (and isn't)

- **A tracer bullet, not a task list**: the definition and the wide-refactor exception live in slicing § Draft vertical slices.
- **No file paths or code snippets**, with the sole exception of a prototype-validated snippet (slicing § No stale content).
