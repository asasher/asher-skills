# Provider adapters

## AgentMail CLI

Use `scripts/agentmail_handoff.py`. It parses only `AGENTMAIL_API_KEY` from the workspace root `.env`, reads
the reviewer/inbox/allowlist from `capabilities.json`, and uses the exact CLI surface:

```text
agentmail inboxes:drafts create --inbox-id … --client-id … --to … --subject … --html … --text …
agentmail inboxes:drafts send --inbox-id … --draft-id …
```

The script defaults to a no-network dry run; `--execute` is required for reviewer delivery. Keep `--debug`
off. The reviewer must be the only allowed recipient.

Use `scripts/provision_agentmail_key.py` only during setup or deliberate rotation. It creates an
inbox-scoped whitelist-permission key, atomically replaces only the `AGENTMAIL_API_KEY` assignment in the
shared root `.env`, preserves every other assignment, and never prints the returned credential.


## Outlook connector

Invoke the installed Outlook Email capability by name. Search using the AgentMail message ID, deterministic
subject marker, reviewer, and a narrow creation window. Create a forward draft from the rich source message,
put the complete approved recipient set in `To`, and add no generated wrapper text beyond the provider's
forward provenance. Never send it.

Record the source message ID and forward-draft ID. Reconciliation later searches Sent Items with the same
correlation data; do not use subject alone.
