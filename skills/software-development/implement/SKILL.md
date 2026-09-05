---
name: implement
description: Implement a ticket or supplied brief in its prepared worktree; diagnose defects, test behavior, and commit coherent changes.
metadata:
  requires: [diagnosing-bugs, domain-modeling, principle-codebase-design, principle-type-system-discipline, tdd, to-thread]
  optional: [typescript-best-practices]
---

# Implement

Work in the supplied worktree and branch. If given a ticket from the primary checkout, use `to-thread` to continue this task in that ticket's worktree before editing. Otherwise require the worktree and branch to be identified. Keep the primary checkout unchanged.

Read the brief, existing changes, and `docs/agents/environment.md` for commands, generated files, and runner traps. Check load-bearing assumptions against the code. Preserve approved decisions; stop and record scope or product contradictions.

- Defects use `diagnosing-bugs`.
- New behavior uses `tdd` at the agreed public seams. Settled test choices need no repeat confirmation.
- Use `principle-codebase-design` for module decisions and `principle-type-system-discipline` for typed boundaries. Apply TypeScript guidance when relevant.
- Inherit shaping's context commits. Use `domain-modeling` only for new terms or decisions introduced by this work.

Regenerate generated files with the recorded recipe. Extend the seed for new features. Run applicable typecheck, touched tests, format, lint, and the full suite for behavioral changes. For non-behavioral work, run the relevant artifact checks and explain omissions. Serialize checks sharing mutable state.

Prove a pre-existing failure against the base, track it separately, and keep it out of this ticket's scope. Keep temporary probes and evidence media out of commits.

Commit and push coherent changes throughout the work and before handoffs or pauses. A failed push is a recorded continuity blocker. Return the pushed SHA, check commands and exit codes, decisions made, and residual risks.
