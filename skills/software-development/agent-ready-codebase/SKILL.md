---
name: agent-ready-codebase
description: The repo-readiness standard for parallel agent builds. Cite it when certifying a repo, judging whether a repo may dispatch builds, or deciding whether a ticket uses or changes a shared singleton.
---

# Agent-ready codebase

The standard a repo must meet before parallel agent builds dispatch into it — a reference skill: the workflow that certifies a repo cites this standard by name.

## The checklist

A repo is agent-ready when all four items pass:

1. **Worktrees.** The project's worktree mechanics can create, inspect, and remove working copies here.
2. **Stack per worktree.** Each working copy brings up its own dev stack beside the others.
3. **Auth per worktree.** An agent can mint a session in each copy independently.
4. **Seed.** Seed data exists and exercises everything the app offers. A ticket that adds a feature extends the seed; a seed that misses a feature is drift.

## Certification

Exercise each item in this repo — an item passes only when demonstrated. Report a pass, or a punch list naming every failed item. Punch-list gaps become tickets in the tracker. The repo records its checklist answers, shared-singleton table (see Use ≠ change), and punch list in `docs/agents/environment.md` when certification runs. Readiness is binary — agent-ready or not. Readiness is upkeep — re-certify on demand.

## Use ≠ change

A shared singleton — one auth tenant, one staging target — serves many parallel builds that **use** it. A ticket that **changes** it is marked at the tracker: slice the work so the change is isolated first; add a dependency edge only when a later ticket cannot proceed until the change lands.
