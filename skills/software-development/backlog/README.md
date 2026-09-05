# Backlog

Reads all open tickets before proposing duplicates, consolidation, relationships, and routing. Selected shaping tickets and ready, unblocked builds each get their own worktree and thread. The dispatcher exits after confirmed launches; tracker records carry progress.

Commands: `backlog groom`, `backlog build [ids]`, `backlog status`, `backlog merge`, `backlog capture`, `backlog retro`, `backlog setup`. Groom always reads the full open backlog, even when the user names a focus. Merge without named selections produces a read-only shortlist.

The skill declares its dependency surface in SKILL.md. Setup reconciles the environment playbook, labels, and five readiness capabilities, including artifact publication.
