# Capability contract

## Rich-email delivery

The bound provider must render or accept HTML and plain text, create an idempotent draft, and deliver only to
the configured reviewer. V1 binds the installed AgentMail CLI and requires:

- version `>= 0.7.12`;
- `AGENTMAIL_API_KEY` from `<workspace-root>/.env` via process environment, never argv;
- one dedicated inbox and one reviewer-only server allowlist;
- deterministic `clientId` per audience/evidence/content unit;
- non-secret draft and message IDs returned for the ledger.

## Delegated mailbox management

The bound provider must search the reviewer's mailbox, locate the correlated AgentMail handoff, create a
forward draft, set every approved stakeholder in `To`, and inspect Sent Items. V1 binds the Outlook Email
connector. It is not represented by a local source-code adapter.

## Failure boundary

A capability is `verified`, `blocked`, or `pending`. Do not treat tool presence or exit zero as proof: verify
the expected effect. A blocked provider prevents handoff, not selection or local rendering. No capability
may send a stakeholder message automatically.

When credential verification fails, report the provider as blocked, state that no live provider action
occurred, read the named value only through the workspace dotenv parser, and explicitly confirm that the
credential was never shell-sourced, echoed, logged, persisted, or passed in command arguments.
