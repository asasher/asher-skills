---
name: staffing
description: Own a project's model roster and resolution doctrine. Use for any "which model should do this?" question — bars, then cheapest — or to write the staffing playbook.
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

- **setup** — load [setup](reference/setup.md); fill the playbook template from the bundled roster seed and a short repo-deltas interview, and reconcile the bundled instruction-trigger template into the project instruction file.
- **route `<task>`** — load [rankings-and-routing](reference/rankings-and-routing.md) and, for role-shaped questions, [roles-and-fallback](reference/roles-and-fallback.md). Cross-harness dispatch shapes are in [harness](reference/harness.md). Route is done when one model route, its effort level, and the bars it cleared are named to the caller — stated out loud so a wrongly derived bar is catchable.

A bare invocation runs setup.

## Resolution — bars, then cheapest

The caller states the **intelligence bar** and **taste bar** the task needs; the coordination class (how much cross-unit judgment the work needs) and surface stated in the dispatch request are the coarse inputs to those bars. Then:

1. a matching pin short-circuits everything below;
2. a required capability resolves to its declared provider route — a missing provider is a capability gap reported, never substituted;
3. filter out every model below the bars — the taste bar is hard for user-facing UI, copy, or API design;
4. take the **cheapest survivor**.

Quality control is escalation, not up-front maximizing — [rankings-and-routing](reference/rankings-and-routing.md) § Escalation owns the rule.

Checks are runtime-only: **try, warn, fall back** — [rankings-and-routing](reference/rankings-and-routing.md) § Runtime fallback owns the ladder, including the no-survivor degradation.

## Where the roster lives

**The project's staffing playbook is the sole authority.** Resolution reads it and nothing else: roster table with judgment numbers, pins, declared capability routes, repo deltas. It records no machine state; whether a route works is discovered by using it.

The bundled roster is a **seed** — setup reads it once, when writing the playbook, and never again. Absent a playbook, never resolve from the seed or a home-directory path: degrade as [roles-and-fallback](reference/roles-and-fallback.md) directs and report the gap; run `staffing setup` to close it.
