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

Composes with the `worktree`, `to-thread`, `to-subagent`, `shape`, and `build-change` siblings (optionally `merge-change`, `retro`, `plain-language`, `agent-ready-codebase`, `to-web`), and reads the `docs/agents/` playbooks its `setup` installs and reconciles.
