---
name: backlog
description: Dispatch the backlog — groom fans needs-shaping tickets into shaping threads the user attends; build fans ready, unblocked tickets into worktree-isolated subagents it supervises. Setup installs the playbooks.
argument-hint: "[groom | build | setup] [ticket ids]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [build, shape, to-subagent, to-thread]
  optional: []
---

# Backlog

A dispatcher with two dispatch shapes. Grooming is interactive — human-in-the-loop work fans out as
threads the user attends, and no result flows back. Building is autonomous — it fans out as subagents
this session supervises to completion.

Nouns are roles: *ticket*, *label*, *change request* are bound to this repo's real tracker, review
surface, and version control by `docs/agents/platform.md`; label roles, dependency edges, and readiness
by `docs/agents/backlog-policy.md`. Missing playbooks: run `backlog setup` first — don't improvise them.

## groom

Sweep the tracker for tickets carrying the needs-shaping role, or take the ids given. Group tickets whose
decisions interlock into one subject; the rest stay one subject each. For each subject, mark it shaping
per the label roles — a subject never gets two threads — then spawn a thread via the `to-thread` skill — named for the subject, seeded with the ticket ids and the instruction to run
the `shape` skill on them. Report each thread and how to attach; status on request comes from the
tracker and the harness's thread listing. What happens inside the thread — and whether a spec or tickets
come out of it — is the user's call there, not this dispatcher's.

## build

Sweep for tickets carrying the ready role whose dependency edges are clear, or take the ids given. For
each: mark it building per the label roles — a dispatched ticket must never dispatch twice — then
dispatch the `build` skill on it via the `to-subagent` skill, in its own worktree. Isolation and
concurrency follow the environment playbook's verdicts (`docs/agents/environment.md` § Worktree
isolation, § Parallelism): a repo that can't isolate builds one ticket at a time in the main checkout.

This session babysits the fleet: each build's completion wakes it, and it relays the outcome — the
review-ready change request, or the failure, with a died-silent build reported, never dropped. Merging
the resulting change requests waits for explicit authorization.

## setup

Install or reconcile the project playbooks from `templates/`: `docs/agents/platform.md` (platform
bindings, with each verb verified live), `backlog-policy.md` (label roles, dependency edges, readiness
decision), `environment.md` (run/seed/check), `evidence.md` (the evidence bar). Reconcile with what
exists — a repo-owned playbook is edited, never blindly overwritten. Verify the label roles exist in the
tracker; create missing ones with the user's consent.
