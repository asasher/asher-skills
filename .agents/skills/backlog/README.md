# Backlog

Dispatcher for the tracker, with two dispatch shapes. `groom` sweeps unlabeled and needs-shaping
tickets, routes the already-settled and parked ones, groups the rest into subjects (interlocked tickets
together) and batches (related subjects, one thread's worth), and — **after the user confirms the batch
plan** — fans one interactive shaping thread per batch, each seeded to run the `shape` skill, its
tickets marked shaping; a single batch runs in the current session instead. Threads are harness-native
sessions the user attends, and nothing reports back.
`build` fans ready, unblocked tickets into worktree-isolated **subagents**, each running the `build`
skill, marked building so nothing dispatches twice — building is autonomous, so the dispatcher
babysits: completion wakes it and it relays each outcome.

Platform-bound, not bound-to-GitHub: *ticket*, *label*, and *change request* are roles, bound per repo by
`docs/agents/platform.md` and `backlog-policy.md`.

## Use

```bash
backlog groom            # sweep unlabeled + needs-shaping tickets into confirmed batches, then threads
backlog groom 42 51      # just these tickets, grouped if their decisions interlock
backlog build            # sweep ready, unblocked tickets into supervised build subagents
backlog build 42         # just this ticket
backlog setup            # install or reconcile the project playbooks
```

Merging the change requests that builds produce stays a separate, explicit human authorization —
the `merge-changes` skill.

## Dependency surface

- **Bundled:** `templates/` — the playbook baselines `setup` installs (shared `common/` plus per-domain
  packs; `software/` is the shipped default).
- **Project playbooks:** `docs/agents/platform.md` (platform bindings, verbs verified live),
  `backlog-policy.md` (label roles, dependency edges, readiness), `environment.md` (run/seed/check),
  `codebase.md` (how the code is written and checked), `evidence.md` (the evidence bar) — owned by the
  repo once written; `setup` reconciles, never blindly overwrites.
- **Siblings (required, by name):** `to-thread` (grooming threads), `to-subagent` (build dispatch),
  `shape` (what a grooming thread runs), `build` (what a build subagent runs).
