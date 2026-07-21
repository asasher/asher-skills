# Backlog

Dispatcher for the tracker. `groom` fans tickets carrying the needs-shaping role into interactive shaping
threads — one per subject, interlocked tickets grouped — each seeded to run the `shape` skill. `build`
fans ready, unblocked tickets into worktree-isolated build threads, each seeded to run the `build` skill,
marking tickets in-flight so nothing dispatches twice. Threads are harness-native sessions the user
attends; nothing reports back — status on request comes from the tracker and the thread listing.

Platform-bound, not bound-to-GitHub: *ticket*, *label*, and *change request* are roles, bound per repo by
`docs/agents/platform.md` and `backlog-policy.md`.

## Use

```bash
backlog groom            # sweep needs-shaping tickets into shaping threads
backlog groom 42 51      # just these tickets, grouped if their decisions interlock
backlog build            # sweep ready, unblocked tickets into build threads
backlog build 42         # just this ticket
backlog setup            # install or reconcile the project playbooks
```

Merging the change requests that build threads produce stays a separate, explicit human authorization —
the `merge-changes` skill.

## Dependency surface

- **Bundled:** `templates/` — the playbook baselines `setup` installs (shared `common/` plus per-domain
  packs; `software/` is the shipped default).
- **Project playbooks:** `docs/agents/platform.md` (platform bindings, verbs verified live),
  `backlog-policy.md` (label roles, dependency edges, readiness), `environment.md` (run/seed/check),
  `evidence.md` (the evidence bar) — owned by the repo once written; `setup` reconciles, never blindly
  overwrites.
- **Siblings (required, by name):** `to-thread` (thread spawning), `shape` (what a grooming thread runs),
  `build` (what a build thread runs).
