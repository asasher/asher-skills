---
name: staffing
description: Own the model roster and its resolution doctrine for a project. Use to answer any "which model should do this?" question — state the intelligence and taste bars the task needs, drop every model below them, take the cheapest survivor — or to write the project's staffing playbook. Sibling skills cite it by name; it selects a route, and running the task stays with the caller.
argument-hint: "[setup | route <task>]"
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
---

# Staffing

A reference skill: the roster and the resolution doctrine, cited by name from sibling skills and consulted directly. It selects a route; running the task stays with the caller.

## Commands

- **setup** — load [setup](reference/setup.md); fill the playbook template from the bundled roster seed and a short repo-deltas interview, and install the bundled instruction-trigger template into the project instruction file.
- **route `<task>`** — load [rankings-and-routing](reference/rankings-and-routing.md) and, for role-shaped questions, [roles-and-fallback](reference/roles-and-fallback.md). Cross-harness dispatch shapes are in [harness](reference/harness.md).

No argument runs setup.

## Resolution — bars, then cheapest

The caller states the **intelligence bar** and **taste bar** the task needs; the coordination class and surface stated in the dispatch request are the coarse inputs to those bars. Then:

1. a matching pin short-circuits everything below;
2. a required capability resolves to its declared provider route — a missing provider is a capability gap reported, never substituted;
3. filter out every model below the bars — the taste bar is hard for user-facing UI, copy, or API design;
4. take the **cheapest survivor**.

Quality control is escalation, not up-front maximizing: **when cheaper output misses the bar, escalate to a more capable reachable route without asking.** Never rank survivors by capability — a bar either holds or it was stated wrong; restate it and re-resolve.

Checks are runtime-only. Try the route at the point of use; on failure **warn the user, fall back to the next-cheapest survivor, and continue** — the warning is the record. A route failing repeatedly across sessions is retro fodder, not a state machine's job. If no survivor is reachable, run the work on the current model in a subagent and report the staffing gap; never skip the stage.

## Where the roster lives

**The project's staffing playbook is the sole authority.** Resolution reads it and nothing else: roster table with judgment numbers, pins, declared capability routes, repo deltas. It records no machine state — no reachability rows, no probe records, no overlay; whether a route works is discovered by using it.

The bundled roster is a **seed** — setup reads it once, when writing the playbook, and never again. Absent a playbook, never resolve from the seed or a home-directory path: degrade as [roles-and-fallback](reference/roles-and-fallback.md) directs and report the gap; run `staffing setup` to close it.
