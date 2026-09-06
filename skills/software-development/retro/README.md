# Retro

Review recent local build and shaping sessions, find concrete friction, and compare it with open and closed project issues. Present proposed issues or comments for the user's selection; accepted findings enter the project's normal backlog.

The first sweep covers the latest three completed sessions. Later sweeps take the next three new or updated sessions. The user can change the scope or request another batch.

A small ignored `.retro/checkpoint.json` in the primary checkout records the reviewed boundary. Worktrees share it; machines keep separate checkpoints. Dismissed findings still count as reviewed. Project issues provide shared duplicate checking and retain accepted learnings.

[SKILL.md](SKILL.md) owns the workflow; [checkpoint.md](reference/checkpoint.md) defines coverage and migration. Install `retro` with its `capture` dependency. The first sweep initializes local state; no setup playbook is required.
