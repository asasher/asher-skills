# execution - ladder, gates, approvals

Single source of truth for executing outbound actions. Read before any command creates a Gmail draft, sends, submits, publishes, uses ATS endpoints, or automates authenticated browser work. Use `scripts/server.py`, `scripts/await.py`, and `scripts/validate_approval.py` from the project root — don't rewrite local equivalents.

## Execution Ladder

Consult `capabilities.json`; use the best available rung for the specific item.

1. **MCP connector.** Email is Gmail drafts only; the user sends from Gmail — a physical send gate. Calendar connectors may propose slots and create holds only after approval.
2. **ATS-direct.** Public Greenhouse, Lever, Ashby, or equivalent endpoints when available and safe.
3. **Authenticated Chrome.** The persistent local profile for logged-in job boards, LinkedIn, or sites without stable public endpoints. `.env` credentials are last resort.
4. **Manual fallback.** Final draft, field-by-field instructions, any files; the user performs the action.

When no rung is connected, degrade to draft-and-instruct. Never silently skip an execution attempt; record the chosen rung or the fallback.

## Artifacts

Write the final text of every outbound item to `goodwork/artifacts/<art_id>.md` before presenting it for approval. The approval page shows the user that file — never ask for approval on text they cannot see there or in the Gmail draft itself — and `content_hash` is computed over its exact bytes.

## Hard Gates

- **Approval gate.** Before any actual send, submit, publish, calendar hold, connector-sent email, or browser final action, `approvals.jsonl` must contain a matching approval record. Creating a Gmail draft needs no approval record: the draft is the review surface and Gmail's Send button is the physical gate.
- **Hash gate.** The approval `content_hash` must match the current artifact. A UI click is only a request; if content changed after render, re-present and do not approve.
- **Evidence gate.** Applications require evidenced profile support for about 70% of must-have requirements. On failure, stop and propose the cheapest proof artifact or prototype.
- **Quota gate.** The weekly application quota in `metrics.json` is a hard cap; exceed only after an explicit recorded quota change.
- **Truth gate.** Never invent experience, metrics, credentials, relationships, or evidence.
- **Proof gate.** Browser and ATS submissions require a confirmation screenshot or equivalent proof reference recorded to the pipeline card.

## Approval Records

Per-item approvals cover exactly one artifact. Session-batch approvals only when `covers` lists every item ID and content hash in the batch. Record schema: [state.md](state.md). Required: `id`, `timestamp`, `item_id`, `channel`, `granularity`, `content_hash`, `covers`, `approved_by`; include `source_event_id` when approval came from the UI.

## Gmail Drafts

Draft creation records metadata on the pipeline card: `draft_` ID, Gmail draft/thread ID when available, artifact ID, content hash, timestamp, status. Reconcile uses it to match later sent mail or replies. A future connector path that sends directly uses the approval and hash gates like any other send.

## Completion Criteria

An execution run is complete only when every requested outbound item has one recorded state on its pipeline card: executed with proof, Gmail draft created for user send, blocked by a named gate, or manual fallback produced.
