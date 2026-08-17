# Build Change

Takes one unit of work to one review-ready change request in one worktree. The unit is a ready ticket, or a spec'd piece of work with no ticket — then the change request is the record. Use when a single unit needs building end to end in the project-prepared worktree supplied at dispatch. Merging stays a human authorization; mechanics live in `SKILL.md`.

## Dependency surface

Composes with the `implement`, `verify-your-work`, `prove-your-work`, `adversarial-review`, and `to-subagent` siblings (optionally `diagnosing-bugs`, `writing-for-humans`), and reads the `platform.md`, `environment.md`, and `change-description.md` playbooks under `docs/agents/`.

## Provenance

No external sources.
