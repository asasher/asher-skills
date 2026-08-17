# Prove Your Work

Evidence packaging for a finished change, posted on the change request where the merge decision happens. Evidence media uploads through `to-web` and embeds by URL instead of entering the repo; SKILL.md holds the package contents and the bar each part must meet.

## When to use

- A change request is review-ready and the decider won't have watched the work.

## Dependency surface

Composes with the optional `to-web` and `writing-for-humans` siblings; reads the `platform.md`, `evidence.md`, and `environment.md` playbooks under `docs/agents/` when the repo has them.

## Provenance

No external sources.
