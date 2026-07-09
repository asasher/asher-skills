# Review surface with await gate

## Problem

A skill produces an artifact (a plan, a prototype, a career-workspace change) that a human must review
before the agent proceeds. Pasting the artifact into chat loses layout and forces the human to describe
locations in prose; asking "approve?" in chat gives no structure to the feedback and no protection against
approving a version that has since changed.

## When to use

Any skill where the agent must **block on structured human feedback about a rendered document** — approve /
request-changes verdicts, per-element annotations, or typed workspace requests. Not needed when a plain
chat question suffices (single yes/no with no artifact to point at).

## Shape

Three cooperating pieces, all stdlib-only Python plus static HTML/JS:

1. **Server** — a local `http.server` process that serves the artifact with annotation chrome, and appends
   every human action as an event to an append-only `state/events.jsonl`.
2. **Await script** — the agent-side gate. Blocks (with `--timeout`) until the next relevant event appears
   in the log, prints it as JSON, and exits with a **verdict-coded status** so the agent's Bash call can
   branch without parsing: `0` approve, `3` approve_with_nits, `10` request_changes, `124` timeout. A
   cursor file (`state/.await-cursor`) tracks the read position, so feedback submitted while no agent was
   waiting is picked up by the next await.
3. **Pages/chrome** — the in-page feedback UI (`pages/`), injected at serve time so the committed artifact
   file stays pure.

## Invariants — keep these when adopting

- **Stdlib only.** No pip installs; the skill must run anywhere Python 3 exists.
- **Append-only event log, cursor-tracked await.** The server never mutates state files; history is never
  rewritten.
- **The agent is the sole writer of state.** The server may only append *request* events; the agent
  validates and applies them (goodwork states this explicitly in its SKILL.md).
- **Approvals bind to a content hash.** An approval carries the hash of the document as reviewed; if the
  document changed since, the approval is stale and rejected (backlog returns 409; goodwork has a dedicated
  `validate_approval.py`). This is the load-bearing safety property — without it, an approval can silently
  authorize content the human never saw.
- **Chrome injected at serve time.** The reviewed file on disk contains no review UI.
- **Clean lifecycle.** Register on start, deregister on clean exit, and provide a sweep that probes
  registered URLs and drops dead entries (backlog's `--sweep` mode, run by setup's health check).

## Canonical implementation

**backlog** — the single-document annotate → revise → approve loop:

- `skills/backlog/scripts/review-server.py` (~420 lines) — serves one document, collects batched feedback,
  hash-bound approvals, repo-scoped hub (`registry.json` + generated `index.html`), sweep mode.
- `skills/backlog/scripts/review-await.py` (~70 lines) — the verdict-coded blocking gate.
- `skills/backlog/scripts/pages/chrome.{js,css}` — the annotation chrome.
- Contract doc: `skills/backlog/reference/presenting.md` § Review loop.

**Variant: goodwork** — a multi-page workspace surface rather than one document:

- `skills/goodwork/scripts/server.py` — serves `pages/{kanban,approval,diff,health}.html`; accepts only a
  fixed set of typed request events (`ALLOWED_TYPES`).
- `skills/goodwork/scripts/await.py` — blocks on specific requested event ids, not just "next event".
- `skills/goodwork/scripts/validate_approval.py` — hash validation split into its own step because
  approvals can cover batches of files.

Start from backlog when the review target is one document; start from goodwork when the surface is a
persistent multi-page workspace.

## How to adopt

1. Copy the canonical scripts and `pages/` into the new skill's `scripts/`; add an
   `Adapted from skills/backlog/scripts/...` line to each header docstring.
2. Rename the state directory and event types for the new domain; keep the event-log/cursor/hash mechanics
   untouched.
3. Write the review-loop contract into one of the skill's reference docs (as backlog does in
   `presenting.md`) — the scripts implement the contract, the reference doc *is* the contract.

## Gotchas

- Await calls can outlive Bash tool timeouts. Pass an explicit `--timeout` and prefer running the await in
  the background for long human turns.
- Don't let the server write anything except event appends — the moment it edits state files you have two
  writers and no authority.
- Test the stale-approval path (edit the doc after the page is open, then approve) — it's the invariant
  most likely to be broken by refactoring.

## Instances

backlog (canonical), goodwork (variant). maquette is the likely third adopter for prototype review.
