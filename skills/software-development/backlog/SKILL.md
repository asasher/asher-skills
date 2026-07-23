---
name: backlog
description: Dispatch the backlog — groom sweeps unlabeled and needs-shaping tickets into user-confirmed batches and fans them into shaping threads; build fans ready, unblocked tickets into worktree-isolated subagents it supervises. Setup installs the playbooks.
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

Sweep the tracker for unlabeled tickets and tickets carrying the needs-shaping role, or take the ids
given. Route first — as a plan, not as writes: a ticket whose decisions are already settled routes to
the ready role, one owing reporter facts or human-only work to its parked role per the label roles, a
duplicate or dead ticket to closure — the rest are shaping work. Group that rest twice: tickets whose
decisions interlock form one **subject**; subjects that belong together (same subsystem, same domain
area) form one **batch**, sized to what one thread can hold.

**Confirm before anything changes.** Present the plan — which tickets, which batches, what each is
about, and every proposed tracker mutation (role labels, closures, new tickets, body rewrites) — and
adjust to the user's edits. The confirmation is the gate for all of it: until they approve, the tracker
is untouched and no thread exists. Then execute the approved mutations and, per approved batch: mark
its tickets shaping per the label roles — a ticket never gets two threads — and spawn one thread via
the `to-thread` skill, named for the batch, seeded with the ticket ids (subjects marked) and the
instruction to run the `shape` skill on them. A single batch spawns nothing: this session becomes the
shaping thread and runs the `shape` skill itself.

Report each thread and how to attach; status on request comes from the tracker and the harness's thread
listing. Inside the thread, shaping ends with a spec on each ticket and the user's blessing makes it
ready — that endgame belongs to the `shape` skill, not this dispatcher.

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
decision), `environment.md` (run/seed/check), `evidence.md` (the evidence bar),
`change-description.md` (the change-request body outline). Reconcile with what
exists — a repo-owned playbook is edited, never blindly overwritten. Verify the label roles exist in the
tracker; create missing ones with the user's consent.
