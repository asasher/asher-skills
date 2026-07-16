# AgentMail delivery

Use `scripts/agentmail_delivery.py`. It is dry-run unless `--execute` is supplied. The script independently:

1. validates the Relay instance, protected root credential, and verified sender;
2. recomputes HTML, text, sender, To, CC, template, and canonical manifest hashes;
3. verifies the identical manifest is embedded in the self-contained review sheet;
4. finds an approving `review-loop` event whose `doc_hash` matches the current sheet;
5. derives `relay-<sha256>` client identity from the approved canonical manifest;
6. creates or reuses that deterministic draft, verifies its subject/sender/To/CC/body hashes, and appends the
   draft ID to the workflow ledger before send;
7. appends `send-submitted`, sends only that draft ID, then records the returned message/thread correlation.

The credential enters only the child process environment. Addresses and body content are required provider
arguments, but the key is never argv. Keep provider debug output off and redact failures.

On retry, derive the same client ID and read append-only workflow state. A known draft ID is reused. A create
timeout repeats only deterministic create. Once send submission may have reached the provider, perform unique
reconciliation by client/draft/message correlation. If uniqueness is unavailable, append
`blocked-ambiguous`; never create a new identity or resend automatically.

No provider write may occur before exact approval. Any mismatch appends `superseded` and exits before invoking
AgentMail. Unknown permission names, provider version, or custom-domain status likewise keep live delivery
blocked while local selection, rendering, and review continue.
