# execution - ladder, gates, approvals

This is the single source of truth for executing outbound Goodwork actions. Read it before any command creates a Gmail draft, sends, submits, publishes, uses ATS endpoints, or automates authenticated browser work.

## Execution Ladder

Consult `capabilities.json`; use the best available rung for the specific item.

1. **MCP connector.** Use connected services first. Email is Gmail drafts only; the user sends from Gmail, giving a physical send gate. Calendar connectors may propose slots and create holds only after approval.
2. **ATS-direct.** Use public Greenhouse, Lever, Ashby, or equivalent application endpoints when available and safe.
3. **Authenticated Chrome.** Use the persistent local Chrome profile for logged-in job boards, LinkedIn, or sites without stable public endpoints. `.env` credentials are last resort when a session cannot be held in the profile.
4. **Manual fallback.** Produce the final draft, field-by-field instructions, and any files. The user performs the action.

When no rung is connected, degrade to draft-and-instruct. Do not silently skip an execution attempt; record the chosen rung or the fallback.

## Hard Gates

- **Approval gate.** Before any actual send, submit, publish, calendar hold, connector-sent email, or browser final action, `approvals.jsonl` must contain a matching approval record. Creating a Gmail draft in the user's mailbox does not require an approval record because the draft is the review surface and Gmail's Send button is the physical gate.
- **Hash gate.** The approval `content_hash` must match the current artifact. A UI click is only a request; if content changed after render, re-present the artifact and do not approve.
- **Evidence gate.** Applications require evidenced profile support for about 70% of must-have requirements. If the gate fails, stop and propose the cheapest proof artifact or prototype.
- **Quota gate.** Weekly application quota in `metrics.json` is a hard cap. Do not exceed it without an explicit quota change recorded before execution.
- **Truth gate.** Never invent experience, metrics, credentials, relationships, or evidence.
- **Proof gate.** Browser and ATS submissions require a confirmation screenshot or equivalent proof reference recorded back to the pipeline card.

## Approval Records

Per-item approvals cover exactly one artifact. Session-batch approvals are allowed only when `covers` lists every item ID and content hash included in the batch.

Record schema lives in [state.md](state.md). Required fields: `id`, `timestamp`, `item_id`, `channel`, `granularity`, `content_hash`, `covers`, and `approved_by`. Include `source_event_id` when approval came from the UI.

## Gmail Drafts

Gmail draft creation records draft metadata on the pipeline card: `draft_` ID, Gmail draft/thread ID when available, artifact ID, content hash, timestamp, and status. Reconcile uses that metadata to match later sent mail or replies. If a future connector path sends email directly instead of creating a user-sent draft, it uses the approval and hash gates like any other send.

## Completion Criteria

An execution run is complete only when every requested outbound item has one of these states recorded against its pipeline card: executed with proof, Gmail draft created for user send, blocked by a named gate, or manual fallback produced.
