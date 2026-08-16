# Build Change

One unit of work — a ready ticket, or a spec'd piece of work with no ticket — to one review-ready change request in one worktree, with this session as owner, fixer, and bookkeeper: implement (dispatched), verify-and-fix loop (verifier reports, owner fixes, until clean), change request (the ticket's closing reference, or the record itself when no ticket exists), adversarial review to LGTM, evidence package posted carrying the session's per-stage token ledger. Stage dispatch is synchronous — blocking calls, concurrent within a turn, never walk-away-and-get-notified. When a ticket exists, the outcome lands on the tracker as the claim's outcome comment. Merging stays a human authorization.

## When to use

- A single ticket, or a spec'd piece of work without one, needs building end to end in the project-prepared worktree supplied at dispatch.

## Dependency surface

Composes with the `implement`, `verify-your-work`, `prove-your-work`, `adversarial-review`, and `to-subagent` siblings (optionally `diagnosing-bugs`, `plain-language`), and reads the `platform.md` and `environment.md` playbooks under `docs/agents/`.

## Provenance

No external sources.
