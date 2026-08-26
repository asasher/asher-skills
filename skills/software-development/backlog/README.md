# Backlog

Dispatcher for a software delivery tracker, with no supervisor. `groom` routes and merges unrouted and needs-shaping tickets into shapeable subjects and, **after the user confirms the plan**, fans one attended shaping thread per subject, each in its own worktree. `build` claims ready tickets, posts the dispatch declaration as the claim, fans one build thread per ticket, and exits. `status` is the pure query — claims × worktrees × change requests × deadlines → finished, stalled, abandoned, and orphans — with the teardown sweep as its action arm.

Platform-bound: _ticket_, _label_, and _change request_ are roles, bound per repo by `docs/agents/platform.md` and `backlog-policy.md`.

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

Composes with the `worktree`, `to-thread`, `shape`, and `build-change` siblings (optionally `merge-change`, `retro`, `writing-for-humans`, `agent-ready-codebase`), and reads the `docs/agents/` playbooks its `setup` installs and reconciles.
