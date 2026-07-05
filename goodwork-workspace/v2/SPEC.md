# Goodwork Career Ops v2 Spec

## Scope

Goodwork v2 turns the skill into a local operator: one project folder equals one person. It runs on the user's machine, keeps sensitive state local, uses connected services when available, and degrades to draft-and-instruct when no connector or browser path exists.

The agent is the only writer of state. The server is a local review surface: it renders projections from state and appends user request events.

## Architecture

- **Workspace:** `goodwork/` inside the project folder. It contains JSON/JSONL operational state, Markdown narrative state, vendored UI assets, a persistent Chrome profile, confirmation proofs, and a gitignored `.env`.
- **Agent:** reads state, validates gates, writes state, drains events, performs connector/browser/ATS/manual execution, and updates narrative files.
- **Server:** Python stdlib only, about 100 lines in the implementation phase. It binds `127.0.0.1` on a random port, serves regenerated HTML projections, and exposes one POST endpoint that appends request events.
- **Remote layer:** Tailscale `serve` proxies the local server onto the user's tailnet. `tailscale funnel` is banned.
- **Connectors:** Gmail creates drafts only; Calendar proposes slots or creates approved holds. Browser automation uses the persistent Chrome profile. WhatsApp Web is read-only and opt-in after risk disclosure.
- **UI assets:** `@pierre/diffs` is vendored during setup for the CV/application review page.

## State Contract

Operational state files are JSON/JSONL: `pipeline.json`, `leads.json`, `sources.json`, `targets.json`, `capabilities.json`, `metrics.json`, `evidence-inbox.json`, `approvals.jsonl`, and `events.jsonl`.

Narrative files are Markdown: `PROFILE.md`, `ODYSSEYS.md`, `EXPERIMENTS.md`, `NICHE.md`, and `JOURNAL.md`.

If a matcher or presentation layer consumes it, it lives in JSON. If the interview or person consumes it, it lives in Markdown. Every JSON record has a stable ID and cross-file references use IDs.

## Server Contract

### Startup

- Bind `127.0.0.1:0`; record the chosen port in process output, not state.
- Generate a 128-bit random session token at startup.
- Serve only while pending approvals or review items exist, then idle-timeout after the queue drains.
- On crash or restart, recover from `events.jsonl`; the next agent command drains events after the saved cursor.

### Token Scheme

Every application request requires the current session token. Accept it in a query parameter for GET pages and in the POST body for `/event`; clients may also send `X-Goodwork-Token`. Never accept cookie-only authentication.

The Tailscale host is stable and bookmarkable. A bookmark to the host root may hit a bootstrap route that serves no state and performs no action; it mints a fresh per-session token and redirects to the current tokenized page. All state-bearing GETs, static asset requests, and POSTs still validate the token. Responses set `Referrer-Policy: no-referrer` so tokenized URLs are not leaked through referrers.

### Endpoints

`GET /`
: Bootstrap only. If a session is live, redirects to the current tokenized review page; otherwise returns a no-state "not running" page. It never accepts actions.

`GET /health?token=...`
: Returns a minimal health page for the current session.

`GET /approval?token=...&item_id=...`
: Renders one approval item, with approve, reject-with-reason, edit-then-approve, and optional batch controls.

`GET /diff?token=...&artifact_id=...`
: Renders the CV/application diff page using vendored `@pierre/diffs`.

`GET /kanban?token=...`
: Renders the pipeline projection from `pipeline.json`.

`GET /static/...?...token=...`
: Serves vendored assets only when token is present.

`POST /event`
: The only POST endpoint. Validates the token, appends one event to `events.jsonl`, and returns an event ID. It never writes approvals or operational state.

### Event Schema

Events are user requests, not state changes.

```json
{
  "id": "evt_20260706_01H7VJ8M",
  "timestamp": "2026-07-06T09:15:22+04:00",
  "session_id": "sess_20260706_9b2c",
  "type": "approval_requested",
  "actor": "user",
  "page": "approval",
  "item_id": "art_cv_tailor_01H7VJ",
  "content_hash": "sha256:4f7f0c0a9b5a",
  "granularity": "item",
  "covers": [
    {
      "item_id": "art_cv_tailor_01H7VJ",
      "content_hash": "sha256:4f7f0c0a9b5a"
    }
  ],
  "payload": {
    "action": "approve",
    "reason": null
  },
  "tags": ["approval"]
}
```

Recognized event types: `approval_requested`, `rejection_requested`, `edit_then_approve_requested`, `batch_approval_requested`, `stage_change_requested`, `test_tap`, and `comment`.

The agent validates the current artifact hash before appending an approval record. For `session_batch`, `covers` must list every item ID and content hash in the batch. Hash mismatch means re-present the item.

## Await Bridge

`await --ids ... --timeout N` is a blocking CLI bridge used by the agent. It tails `events.jsonl` from `goodwork/.await-cursor`, waits for matching item IDs or event IDs, and exits when all requested events arrive, a rejection arrives, or timeout expires.

Exit codes:

- `0`: all requested events arrived and were parsed.
- `10`: at least one matching rejection arrived.
- `124`: timeout; output includes matched event IDs and missing IDs so the agent can record partial progress without treating the batch as approved.
- `2`: malformed event log or cursor.

Events clicked while no agent is listening are still appended. The next command drains events after the cursor before starting new work; malformed events do not advance the cursor.

## UI Pages

### Approval Flow

Mobile-first and one item per screen. Show the artifact, channel, destination, current content hash, and the exact action requested. Controls: approve, reject-with-reason, edit-then-approve, and batch checkboxes when a session-batch is being requested. Batch events include the exact `covers` list submitted for validation.

The UI click never approves directly. It appends an event; the agent validates gates and writes `approvals.jsonl`.

### CV/Application Review

Side-by-side diff using vendored `@pierre/diffs`, with word-level highlights. Each changed line links to profile evidence: section, claim, confidence mark, and source episode. Unsupported changes are marked as blocked until evidence exists or the wording is removed.

### Kanban

Columns come from `pipeline.json` stages. Cards show target/lead, next action, due date, staleness color, warmth, and badges for approval needed, reply waiting, proof missing, or evidence gap.

Mobile collapses to a list grouped by stage. Desktop drag-and-drop is allowed, but drag emits `stage_change_requested`; the agent applies it after consistency checks.

## Tailscale Integration

Setup verifies Tailscale, then exposes the local server with `tailscale serve` to the user's MagicDNS tailnet URL. The URL is for tailnet devices only. If the user declines Tailscale, Goodwork records `desk-only` and serves only on the local machine.

Never use `tailscale funnel`. Public internet exposure is outside the v2 contract.

Local push notifications say work is ready, for example "3 items pending". They do not need to include a link because the MagicDNS host is stable.

## Execution Rules

Execution uses the ladder in `skills/goodwork/reference/execution.md`: MCP connector, ATS-direct, authenticated Chrome, manual fallback. Approval, hash, evidence, quota, truth, and proof gates are hard preconditions.

Gmail execution creates drafts only and records draft metadata on the pipeline card; no approval record is required to create the draft. The user sends from Gmail. Any connector-sent email path, browser final send, ATS submission, or calendar hold requires approval and hash validation. Browser and ATS submissions record confirmation screenshots as proof.

## Gate Walkthroughs

- **Single application:** tailor from evidenced profile claims, render the diff/review page with the artifact hash, append an approval request event on click, validate the current hash, append `approvals.jsonl`, execute through the best available rung, capture proof for ATS/browser submissions, and update the pipeline card.
- **Batch approval:** render the batch with every item and hash, append a `session_batch` event with the exact `covers` list, validate every current hash before writing one batch approval record, then execute only the covered items.
- **Hash mismatch:** if any current artifact hash differs from the event or approval `covers`, write no approval and perform no send/submit; re-render the changed item for review.

## Security And Threat Notes

- **Localhost CSRF:** any webpage can POST to localhost. `/event` requires the session token in the POST body or header and rejects missing or wrong tokens. Origin checks are advisory only; token validation is the gate.
- **Token leakage:** tokenized URLs are per-session, responses use `Referrer-Policy: no-referrer`, and tokens are not written to git-tracked state.
- **Bookmark bootstrap:** the stable host root can mint a fresh token only for a top-level navigation, serves no private state before redirect, uses no cookies, and does not enable CORS.
- **Tailnet exposure:** Tailscale `serve` is allowed; `funnel` is banned.
- **State integrity:** server appends events only. The agent is the only writer of JSON, JSONL approvals, and Markdown.
- **`.env` hygiene:** `.env` is gitignored, local, and used only where a persistent profile cannot hold a session.
- **Chrome profile sensitivity:** the profile contains live sessions and must stay inside the workspace.
- **WhatsApp risk:** WhatsApp Web is read-only, opt-in, and disclosed as account-ban/Terms-of-Service risk. No automated sending.
- **Proof sensitivity:** screenshots can contain personal data; store them locally and reference by ID from pipeline cards.
