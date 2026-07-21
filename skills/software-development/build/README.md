# Build

One ticket → one review-ready change request, with this session as owner and fixer: implement
(dispatched), verify-and-fix loop (verifier reports, owner fixes, until clean), change request with the
ticket's closing reference, adversarial review to LGTM, evidence package posted. Merging stays a human
authorization.

## When to use

- A single ready ticket needs building end to end — typically in its own session with its own worktree.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Project:** platform verbs in `docs/agents/platform.md`.
- **Siblings (required, by name):** `implement`, `verify-your-work`, `prove-your-work`,
  `adversarial-review`, `to-subagent`.

## Provenance

No external sources.
