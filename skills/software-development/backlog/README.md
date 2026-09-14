# Backlog

Reads all open tickets before proposing duplicates, consolidation, relationships, and routing. Selected shaping tickets and ready, unblocked builds each get their own worktree and thread. Groom exits after confirmed launches. Build drains its initial frontier; a selected spec or milestone continues in waves until complete or waiting for outside action. Tracker records carry worker progress.

Commands: `backlog groom`, `backlog build [ids]`, `backlog build spec <ticket>`, `backlog build milestone <name-or-number>`, `backlog status`, `backlog recap [time range]`, `backlog merge`, `backlog capture`, `backlog retro`, `backlog setup`. Groom always reads the full open backlog, even when the user names a focus. Merge without named selections produces a read-only shortlist.

`backlog recap last week`, `backlog recap last month`, and `backlog recap last 6 months` create a standalone HTML report for a non-developer. The report explains what changed for people and the system, why, recorded tradeoffs, and the situation at the period's end. It links its sources and separates confirmed shipping from merges whose release is unconfirmed. The default period is the past week; exact dates work too. Recap requires no setup and returns a local file, with publication available on request.

The skill declares its dependency surface in SKILL.md. Setup reconciles the environment playbook, labels, and five readiness capabilities, including artifact publication.

A frontier is the ready, unblocked work at invocation. Shaping and building have no default concurrency limit; the human operator chooses any limit. Scoped runs discover later frontiers after confirmed merges, preserve approval and recovery gates, and report PR review waits truthfully. Human merge selection remains required.
