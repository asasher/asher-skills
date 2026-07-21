---
name: relay
description: Relay governed project communications through AgentMail. Use when preparing project updates or internal digests from bound evidence, reviewing exact email content and recipients, sending an approved AgentMail draft directly, reconciling delivery or replies, or resuming Relay state.
metadata:
  invocation: model
  execution: thread
  requires: [serve-via-tailnet]
  optional: []
  setup: reference/setup.md
---

# Relay

Turn project-bound evidence into immutable, human-approved email and track its AgentMail lifecycle. All
consumer policy, identity, recipients, templates, runs, and state live under `relay/` at the consumer
repository root; the project binding lives in `docs/agents/relay.md`. Never read or write a previous
communications instance.

## Commands

| Command | Result | Load |
|---|---|---|
| `setup` | Discover the repository, bind local choices, and reconcile the Relay instance | [setup](reference/setup.md) |
| `project update` / `internal digest` | Select attributable evidence into one bag or exclusion per eligible audience | [selection](reference/selection.md), [bag](reference/relay-bag.md) |
| `render` | Produce HTML, text, and authored light/dark previews from one bag | [rendering](reference/rich-email-contract.md) |
| `review` | Build one self-contained review sheet and hand it to `serve-via-tailnet` | [review and approval](reference/review-and-approval.md) |
| `send` | Create, verify, record, and send the exact approved AgentMail draft | [provider](reference/provider-adapter.md) |
| `reconcile` | Ingest provider facts, resolve ambiguity, and update lifecycle state | [lifecycle](reference/lifecycle-ledgers.md) |
| `status` | Report pending review, blocked sends, mixed delivery, and replies without mutation | [lifecycle](reference/lifecycle-ledgers.md) |

Each command's reference owns its detailed contract; load it before acting. A scheduled invocation may select,
render, and present review, but performs zero provider writes until the current exact review is approved.

## Run

1. Resolve the repository root, read `docs/agents/relay.md`, and run `scripts/validate_instance.py`. Stop on
   stale profile hashes, incomplete bindings, an unverified sender, or recipient/disclosure conflict.
2. Gather normalized facts only from the providers bound in `bindings.json`, since each audience's
   confirmed-send watermark. Never infer shipped, paid, committed, or stage-changed facts.
3. Produce exactly one validated immutable bag or explicit exclusion per eligible audience; never combine
   audiences.
4. Render HTML, text, and forced light/dark previews from the same bag, then build the self-contained review
   sheet with `scripts/build_review_sheet.py`.
5. Invoke `serve-via-tailnet` by name to serve the sheet and await its verdict.
6. Deliver with `scripts/agentmail_delivery.py`, which independently re-verifies approval before any provider
   write.
7. Reconcile provider facts with `scripts/ingest_agentmail_events.py`; report with `scripts/relay_status.py`.

## Hard boundaries

- Zero provider writes without an approving `serve-via-tailnet` verdict (`approve` / `approve_with_nits`) for the
  exact current sheet hash. Any change to HTML, text, sender, To, CC, or template identity invalidates
  authorization: append `superseded`, re-render, and re-review. Content-changing nits are such a change.
- One deterministic client/draft identity per approved manifest. Retries reuse it; an unresolvable send
  appends `blocked-ambiguous`. Never mint a new identity, resend, or reply automatically.
- All workflow, per-recipient delivery, reply, and watermark facts are append-only. A watermark advances only
  on confirmed send. "Delivered" means accepted by the receiving server, not opened; without an effect-verified
  receiver, lifecycle is manual reconciliation, never real time.
- AgentMail is the only delivery provider. No Outlook, forwarding, BCC, attachments, bulk campaigns,
  automatic replies, or scheduled future delivery.
- Read only `AGENTMAIL_API_KEY` from the repository-root `.env` with a dotenv parser; require the file
  Git-ignored and mode `0600`. Never source it, print the key, pass it in argv, or persist it under `relay/`.
- Append the configured operator to CC on external sends unless the named audience explicitly overrides.
  Header roles are explicit; internal/external labels imply nothing, and the sender is not a recipient unless
  listed.
- Setup preserves consumer files and modified templates. Changed package defaults become candidates; conflicts
  affecting disclosure, recipients, sender, or live delivery stop reconciliation.

## Dependency surface

- **Bundled:** setup, selection, bag, rendering, review, provider, and lifecycle contracts; deterministic
  scripts, instance templates, fixtures, tests, and probes.
- **Project:** `docs/agents/relay.md`, the repository-root `.env`, and `relay/` only.
- **Sibling:** required `serve-via-tailnet`, invoked by plain name for presentation, annotations, verdict, and wait.
- **Bound sources:** repository paths, commands, connectors, or optional sibling skills (such as
  `manage-tasks` or `manage-opportunities`) recorded by setup; none is a universal Relay dependency.
