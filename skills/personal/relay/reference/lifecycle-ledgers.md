# Append-only lifecycle

Relay state is four JSONL ledgers under `relay/state/`:

- `workflow.jsonl` — selected, rendered, reviewed, draft-created, send-submitted, sent, excluded,
  rejected, superseded, blocked, and blocked-ambiguous transitions;
- `delivery.jsonl` — pending, receiving-server-delivered, bounced, complained, or rejected per normalized
  recipient hash and unique provider event ID;
- `replies.jsonl` — reply-received facts keyed by provider event, message, thread, and source communication;
- `watermarks.jsonl` — confirmed-send selection watermark advances per audience.

Every event carries `schema_version`, timestamp, communication and audience IDs, and an idempotency key. Append
facts; never rewrite history. Do not store secrets, message bodies, raw mailbox payloads, or clear recipient
addresses in state. Recipient hash is SHA-256 of a normalized lowercase address; approved aggregate hashes are
SHA-256 of compact sorted To/CC arrays.

`scripts/ingest_agentmail_events.py` accepts signed-receiver output or an explicit manual reconciliation file.
Duplicate and out-of-order provider events are safe: an already-recorded event ID is ignored, and mixed
recipient outcomes remain mixed. “All delivered” is true only when every intended recipient has a
receiving-server delivery event and none has a failure fact.

Advance a watermark exactly once after matching `message.sent` or unique sent-message reconciliation. Draft
creation, send submission, delivery, bounce, complaint, rejection, or reply never independently advances it.
Later failures remain visible follow-up. A received reply appends a reply fact and never generates a reply.

Ambiguous correlation appends a blocked workflow fact and waits for reconciliation; it never triggers a new
send identity.

Run `scripts/relay_status.py <repo-root>` for a non-mutating aggregate of workflow state, latest per-recipient
outcomes, all-delivered truth, reply count, and confirmed watermark state.
