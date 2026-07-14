# Delivery ledger

`state/message-ledger.jsonl` is append-only. One JSON object records one transition:

`selected → rendered → reviewed → handoff_drafted → handoff_sent → outlook_drafted → sent`

Alternative terminal or supersession states are `excluded`, `blocked`, and `superseded`. A draft is never a
sent communication.

Each event records `timestamp`, `comms_id`, `audience_id`, `project_ids`, `state`, `evidence_hash`,
`content_hash`, `recipient_hash`, and only the provider IDs relevant to that transition. Never record message
bodies, addresses, tokens, or raw mailbox payloads. Compute `recipient_hash` as SHA-256 over the compact JSON
array of normalized lowercase addresses in lexical order.

`reviewed` records the approved rendered-content hash, `approval_surface: "browser"`, and the approval time.
It authorizes provider writes only for those exact rendered bytes. A content or template change after review
must append `superseded` and return to `rendered`; approval never transfers to a changed artifact.

Before a provider write, search for the same audience/evidence/content tuple:

- `rendered` without `reviewed` — reopen the browser review surface; do not call a provider.
- `reviewed`, `handoff_sent`, or `outlook_drafted` — reuse/report the existing approved unit instead of
  creating a duplicate.
- `sent` — report already sent and do not recreate it.
- changed evidence or content while a draft awaits review — append `superseded`, then create a new comms ID;
  never silently patch the old draft.

Advance `state/watermarks.json` only after exactly one matching Sent Items message is found or the user
explicitly confirms the send. Ambiguous matches block reconciliation. A `sent` event records the actual Sent
Items `recipient_hash`. When it differs from the reviewed manifest, also record `approved_recipient_hash`;
never rewrite the historical manifest. A user-made removal or addition is historical fact, while an
unexpected connector-made addition blocks automatic reconciliation until the user confirms it.
