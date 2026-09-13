# Backlog

Reads all open tickets before proposing duplicates, consolidation, relationships, and routing. Selected shaping tickets and ready, unblocked builds each get their own worktree and thread. Groom exits after confirmed launches. Build drains its initial frontier; a selected spec or milestone continues in waves until complete or waiting for outside action. Tracker records carry worker progress.

Commands: `backlog groom`, `backlog build [ids]`, `backlog build spec <ticket>`, `backlog build milestone <name-or-number>`, `backlog status`, `backlog merge`, `backlog capture`, `backlog retro`, `backlog setup`. Groom always reads the full open backlog, even when the user names a focus. Merge without named selections produces a read-only shortlist.

The skill declares its dependency surface in SKILL.md. Setup reconciles the environment playbook, labels, and five readiness capabilities, including artifact publication.

A frontier is the ready, unblocked work at invocation, drained under the repository-wide concurrency limit. Scoped runs discover later frontiers after confirmed merges, preserve approval and recovery gates, and report PR review waits truthfully. Human merge selection remains required.
