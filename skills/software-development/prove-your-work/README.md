# Prove Your Work

Evidence packaging for a finished change: what changed and why, reproducible proof per claim (exact commands with trimmed output; screenshots for UI journeys), the runs of dropped scaffolding scripts, the per-stage token cost of producing it, and named gaps for anything unverified — posted on the change request where the merge decision happens. Evidence media is never committed: it uploads through `to-web` and embeds by URL — images and GIFs inline, videos as links. Obligation scales with the decider's absence: witnessed-live work compresses, AFK work carries the full package.

## When to use

- A change request is review-ready and the person merging won't have watched the work.

## Dependency surface

Composes with the optional `to-web` and `plain-language` siblings; reads the `platform.md`, `evidence.md`, and `environment.md` playbooks under `docs/agents/` when the repo has them.

## Provenance

No external sources.
