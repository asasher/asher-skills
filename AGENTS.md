# Asher Skills

Read these files when needed:

- [CONTEXT](./CONTEXT.md) is the ubiquitous language for this repo, this is shared vocabulary for you and the user to have a shared understanding as you design and work on this repo.
- [GIVING-CREDIT](./docs/agents/GIVING-CREDIT.md) when we re-use or are heavily inspired by external content, we should credit the original source.
- [writing-for-humans](./skills/software-development/writing-for-humans/SKILL.md) for all user facing prose.
- Use bun as the package manager for this repo
- Run `bun format:fix` after significant edits
- Push early and often
- [SKILL-MECHANICS](./docs/agents/SKILL-MECHANICS.md) apply when authoring a skill
- When using a skill authored in this authoring repo we don't install it but use it directly from the `skills/` repo. We only install skills into this repo that are external and useful.
- The skill family ships from this repo: an external skill our skills depend on gets brought in — copied wholesale with credits, or rewritten as our own version — pinning the version we reviewed rather than an evolving copy upstream controls.
