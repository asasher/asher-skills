---
name: backlog
description: Dispatch the backlog — groom fans needs-shaping tickets into shaping threads the user attends; build fans ready, unblocked tickets into build threads. Setup installs the playbooks.
argument-hint: "[groom | build | setup] [ticket ids]"
user-invocable: true
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [build, shape, to-thread]
  optional: []
---

# Backlog

A dispatcher: it fans tickets out into harness-native threads and reports how to attach. No result flows
back — status on request comes from the tracker and the harness's thread listing.

Nouns are roles: *ticket*, *label*, *change request* are bound to this repo's real tracker, review
surface, and version control by `docs/agents/platform.md`; label roles, dependency edges, and readiness
by `docs/agents/backlog-policy.md`. Missing playbooks: run `backlog setup` first — don't improvise them.

## groom

Sweep the tracker for tickets carrying the needs-shaping role, or take the ids given. Group tickets whose
decisions interlock into one subject; the rest stay one subject each. For each subject, spawn a thread
via the `to-thread` skill — named for the subject, seeded with the ticket ids and the instruction to run
the `shape` skill on them. Report each thread and how to attach. What happens inside the thread — and
whether a spec or tickets come out of it — is the user's call there, not this dispatcher's.

## build

Sweep for tickets carrying the ready role whose dependency edges are clear, or take the ids given. For
each: mark it in-flight per the label roles — a dispatched ticket must never dispatch twice — then spawn
a worktree-isolated thread via the `to-thread` skill, named for the ticket, seeded to run the `build`
skill on it. Report each thread and how to attach. Merging the resulting change requests waits for
explicit authorization.

## setup

Install or reconcile the project playbooks from `templates/`: `docs/agents/platform.md` (platform
bindings, with each verb verified live), `backlog-policy.md` (label roles, dependency edges, readiness
decision), `environment.md` (run/seed/check), `evidence.md` (the evidence bar). Reconcile with what
exists — a repo-owned playbook is edited, never blindly overwritten. Verify the label roles exist in the
tracker; create missing ones with the user's consent.
