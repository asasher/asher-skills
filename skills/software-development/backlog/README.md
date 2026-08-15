# Backlog

Dispatcher for the tracker, with no supervisor. `groom` sweeps no-readiness-role and needs-shaping tickets (a captured ticket arrives work-typed but unrouted), routes the already-settled and parked ones, proposes merges — many small related tickets absorbed into one shapeable subject — and, **after the user confirms the plan**, asks how many shaping threads to start (default 3) and fans one interactive thread per subject, each in its own project-owned worktree running the `shape` skill. `build` is pull, not push: it claims ready tickets whose children are all closed or delivered, posts each dispatch declaration as the claim comment (model, effort, harness, worktree, absolute deadline), fans one thread per ticket running the `build-change` skill, and exits — outcomes land on the tracker, not in a babysitting session. `status` is the pure query: claims × worktrees × change requests × deadlines → finished, stalled, abandoned (derived, never written), and orphans, with groom's teardown sweep as its action arm.

Platform-bound, not bound-to-GitHub: _ticket_, _label_, and _change request_ are roles, bound per repo by `docs/agents/platform.md` and `backlog-policy.md`.

## Use

```bash
backlog groom            # route, merge, confirm — then fan shaping threads
backlog groom 42 51      # just these tickets
backlog build            # claim ready tickets, declare, fan build threads, exit
backlog build 42         # just this ticket
backlog status           # the pure query over claims, worktrees, and deadlines
backlog setup            # bindings, choices, agent-readiness certification
```

Merging the change requests that builds produce stays a separate, explicit human authorization — the `merge-change` skill.

## Dependency surface

- **Bundled:** `reference/setup.md` — the setup procedure (declared as `metadata.setup`, so installers report it); `templates/` — the playbook baselines `setup` installs (shared `common/` plus per-domain packs; `software/` is the shipped default); `scripts/reconcile-labels.py` — the label-color reconciler.
- **Project playbooks:** `docs/agents/platform.md` (platform bindings, verbs verified live, artifact store), `backlog-policy.md` (label roles, dependencies, deadlines, readiness), `environment.md` (run/seed/check plus the agent-readiness answers), `codebase.md` (how the code is written and checked), `evidence.md` (the evidence bar) — owned by the repo once written; `setup` reconciles, never blindly overwrites.
- **Siblings (required, by name):** `worktree` (prepare, inspect, remove), `to-thread` (shaping and build threads), `to-subagent` (staffed dispatch inside builds), `shape` (what a shaping thread runs), `build-change` (what a build thread runs).
- **Siblings (optional, by name):** `merge-change` (the human merge gate), `retro` (friction notes), `plain-language` (the user-facing text standard), `agent-ready-codebase` (the readiness standard setup certifies against), `to-web` (evidence media and renders).
