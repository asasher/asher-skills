---
name: agent-ready-codebase
description: The repo-readiness standard for parallel agent builds — a four-item checklist (worktrees, stack per worktree, auth per worktree, maintained seed), the certification method, and the use-vs-change rule for shared resources. Cite it when certifying a repo, judging whether a gap blocks dispatch, or deciding if a ticket touches a shared singleton.
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Agent-ready codebase

The standard a repo must meet before parallel agent builds dispatch into it. This is a reference skill: it defines the standard; whatever workflow certifies the repo cites it by name. A project records its checklist answers and punch list in `docs/agents/environment.md`.

## The checklist

A repo is agent-ready when all four items pass:

1. **Worktrees.** The project's worktree mechanics can create, inspect, and remove working copies here.
2. **Stack per worktree.** Each working copy brings up its own dev stack beside the others.
3. **Auth per worktree.** An agent can mint a session in each copy independently.
4. **Seed.** Seed data exists and exercises everything the app offers, including new features. The seed is a maintained artifact: a ticket that adds a feature also extends the seed, in scope; a seed that misses a feature is drift.

## Certification

Walk the checklist and report either a pass or a punch list of gaps. Punch-list gaps become tickets in the tracker. No modes, no lanes: the repo is parallel-safe or it is not ready. Readiness is upkeep, not a one-time audit — re-certify on demand.

## Use ≠ change

A genuinely shared resource — one auth tenant, one staging target — serves many parallel builds that **use** it. A ticket that **changes** it is marked at the tracker: slice the work so the change is isolated first; add a dependency edge only for true residue.

## Dependency surface

- **Bundled:** none — this file is the whole standard.
- **Project playbooks:** `docs/agents/environment.md` carries the repo's checklist answers, singleton table, and punch list, written when the repo is certified.
- **Siblings:** `worktree` is what checklist item 1 exercises.
