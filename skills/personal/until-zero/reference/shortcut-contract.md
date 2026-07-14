# Capture to Runway Shortcut contract

Delegate authoring to the external `shortcuts-playground` capability. Generate source XML and signed output in
the consumer instance; this skill ships no plist template.

The Shortcut is named **Capture to Runway**, accepts Apple Transaction automation input, and posts one JSON
envelope:

```json
{
  "version": 1,
  "source": "ios-wallet",
  "captured_at": "<ISO timestamp>",
  "client": "<non-secret device label>",
  "transaction": {
    "amount_minor": "<signed integer>",
    "currency": "<ISO code>",
    "description": "<merchant>",
    "date_iso": "<YYYY-MM-DD>",
    "external_id": "<required stable transaction id>",
    "category": "",
    "card": {"last4": "<digits when available>", "label": "<card label when available>"}
  }
}
```

Use the Apple Transaction identifier when exposed; otherwise derive one deterministically from the immutable
automation input fields before posting. Never use a random retry identifier. Use import questions for API URL
and the append-only producer token. Treat HTTP 201 as a new capture and HTTP 200 with `duplicate: true` as an
idempotent retry; both require `ok: true` and the same ID. Do not embed secrets in committed XML or logs.

Invoke Shortcuts Playground to build the smallest plist, validate unsigned XML cleanly, archive, sign, and
verify a non-empty importable `.shortcut`. Record version, capability, source checksum, validation/signing
result, output path, and no secret. Then guide the Apple-owned step: import it, create a personal Transaction
automation for selected cards, choose Run Immediately, pass Transaction input to the Shortcut, and perform a
live capture. Missing capability stops this phase; never invent plist actions as a fallback.
