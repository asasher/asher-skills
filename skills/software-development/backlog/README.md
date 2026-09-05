# Backlog

Dispatcher for a GitHub-tracked software backlog, with no supervisor. Every verb sweeps the issues for the units it applies to, confirms a plan with the user, and fans one run of a skill per unit: `capture` runs the `capture` skill on the conversation; `groom` routes and merges unrouted issues into subjects and fans one attended `shape` thread per subject; `build` claims ready, unblocked issues and fans one `deliver` thread per issue; `retro` runs the `retro` pass. `status` is the pure query over claims, worktrees, PRs, and deadlines, with the teardown sweep as its action arm; `setup` writes the environment playbook and creates the labels.

The verb skills work on one unit each and run on their own. Labels, claims, deadlines, and branch names are fixed in `reference/labels.md`; the repo's own facts live in the one playbook, `docs/agents/environment.md`.

## Use

```bash
backlog capture          # this conversation's loose items into issues
backlog groom            # route, merge, confirm, then fan shaping threads
backlog groom 42 51      # just these issues
backlog build            # claim ready issues, declare, fan build threads, exit
backlog build 42         # just this issue
backlog retro            # the friction pass
backlog status           # claims × worktrees × PRs × deadlines
backlog setup            # environment playbook, certification, labels
```

Merging stays a separate, explicit human authorization: the `merge` skill.

## Dependency surface

Composes with the `capture`, `shape`, `deliver`, `retro`, `to-thread`, and `worktree` siblings (optionally `merge`, `agent-ready-codebase`, `writing-for-humans`, `technical-writing`), and reads the `docs/agents/environment.md` playbook its `setup` installs and reconciles.
