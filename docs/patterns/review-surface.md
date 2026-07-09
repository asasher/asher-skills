# Review surface with await gate — superseded

**This is no longer a copyable pattern. The review surface has been extracted into the standalone
[`review-loop`](../../skills/review-loop/) skill.**

Serving an HTML artifact for human sign-off — annotate in-page, batch feedback into a verdict, block the
agent on a verdict-coded await, bind approvals to a content hash — is a capability that several skills
genuinely share. Per `AGENTS.md` § Conventions ("copy a pattern; **extract a primitive**"), that makes it a
skill, not a doc to copy from. Adopt it by **composing it by name** — "present it via the `review-loop`
skill" — never by copying its scripts into your skill. The contract lives in the skill's own references
(`skills/review-loop/reference/review-loop.md`, `surface-and-hub.md`, `scripts.md`).

## Existing forks (migrating)

Two skills still carry their own copy of the surface and are **deliberately left as-is** until their own
rewire issues land — the extraction ships non-breaking:

- **backlog** — its bundled `scripts/review-server.py`, `review-await.py`, `pages/`, and
  `reference/presenting.md` are untouched and it still presents plans exactly as before. Rewiring backlog to
  consume `review-loop` by name (and deleting its copy) is a separate deferred issue.
- **goodwork** — its multi-page workspace variant (`scripts/server.py`, `await.py`,
  `validate_approval.py`) migrates onto `review-loop` under its own issue; review-loop's first cut is the
  single-document loop.

Until those rewires land the duplication is intentional and tracked here, not drift.
