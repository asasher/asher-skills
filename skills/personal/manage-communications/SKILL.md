---
name: manage-communications
description: Prepare governed stakeholder communications from workspace and project evidence. Use when creating client project updates, internal delivery digests, communication bags, rich email review drafts, or reconciling draft and sent history, and when another skill needs the communications policy or ledger contract.
metadata:
  invocation: model
  execution: thread
  requires: [manage-opportunities, manage-tasks]
  optional: []
  setup: reference/setup.md
---

# Manage Communications

Own planned, evidence-backed communications from selection through sent-state reconciliation. Keep the
portable skill free of client names, addresses, paths, credentials, and mutable state; load those from the
consumer instance and its project playbook.

## Commands

| Command | Result | Load |
|---|---|---|
| `setup` | Reconcile the consumer instance and validate both runtime capabilities | [setup](reference/setup.md) |
| `project update` | Build one external comms bag per eligible client audience | [selection](reference/selection.md), then [comms bag](reference/comms-bag.md) |
| `internal digest` | Build one richer internal bag across delivery, pending work, cash, and growth | [selection](reference/selection.md), then [comms bag](reference/comms-bag.md) |
| `render` | Render a validated bag to HTML and plain text | [rich email](reference/rich-email-contract.md) |
| `review` | Open the rendered messages in a browser and hold for explicit approval | [rich email](reference/rich-email-contract.md) |
| `handoff` | Deliver an approved message to the configured reviewer and create an Outlook forward draft | [capabilities](reference/capability-contract.md), then [providers](reference/provider-adapters.md) |
| `reconcile` | Resolve draft, superseded, and sent state without duplicate delivery | [ledger](reference/delivery-ledger.md) |
| `status` | Report pending review, blocked capability, and sent history without mutation | [ledger](reference/delivery-ledger.md) |

Infer an unambiguous command. A scheduled invocation defaults to project-update selection plus any due
internal digest, but may deliver only to the configured reviewer; it never sends to stakeholders.

## Workflow

1. Resolve the consuming workspace root and read `docs/agents/communications.md`,
   `control-plane/communications/policy.json`, capabilities, audiences, interests, watermarks, and ledger.
   Run `python3 scripts/validate_instance.py <workspace-root> --require-token --check-cli` before a live
   handoff. A missing or unverified capability stops only the provider phase; selection and rendering may
   continue as a dry run.
2. Gather evidence since the audience watermark. Read the Project note and its repository, invoke
   `manage-tasks` by name for pending delivery facts, invoke `manage-opportunities` by name for internal
   pipeline facts, and use the delegated mailbox capability for relevant prior communications. Never infer
   deployment, payment, commitment, or opportunity stage from weak signals.
3. Normalize each fact to an evidence ID, observed time, source, project, feature, status, and confidence.
   Apply the audience interest map and disclosure rules before drafting prose.
4. Build one immutable comms bag per audience. Validate it with
   `python3 scripts/validate_comms_bag.py <bag.json>`. Do not combine clients merely because they share a
   project.
5. Compute audience, evidence, and content hashes. If the ledger already has the same unit in
   `awaiting_review` or `sent`, reuse/report it instead of creating a duplicate. New evidence supersedes an
   older review item; never silently patch it.
6. Render HTML and plain text from the same bag. Preserve evidence IDs in the run manifest, not in visible
   copy. Open a browser review surface containing every message in scope; do not perform a provider write.
7. Hold at the browser review gate until the reviewer explicitly approves the exact rendered artifacts.
   Record the approval in the run manifest and append `reviewed`. Requested changes supersede the render
   and require another browser review; never hand off unreviewed bytes.
8. For a live handoff, AgentMail may send only to the configured reviewer. Then use the Outlook capability
   to locate that message and create one forward draft with every approved external and internal
   stakeholder in `To`. Do not send the Outlook draft.
9. Append state transitions. Advance a watermark only after exactly one matching message is found in Sent
   Items or the user explicitly confirms the send.

Completion criterion: every eligible audience has exactly one validated bag or one explicit exclusion;
every live handoff has explicit browser approval for the exact rendered artifacts; every provider action is
correlated in the ledger; no stakeholder message was sent automatically; and no watermark advanced on draft
creation alone.

## Hard boundaries

- Read `AGENTMAIL_API_KEY` only from `<workspace-root>/.env` with a dotenv parser. Never shell-source the
  file, pass the token in argv, or copy it into config, artifacts, logs, or the ledger.
- Treat the root `.env` as a shared secret store. Read only the named key and preserve unrelated entries.
- Put all approved recipients in Outlook `To`; the visible forward wrapper is intentional AI provenance.
- Do not call AgentMail or create an Outlook draft before explicit approval at the browser review gate.
- Keep external copy inside the audience interest map and verified disclosure level. Internal copy may be
  richer, but payment and opportunity claims still require their authoritative owner.
- Keep AgentMail and Outlook as setup-validated agent capabilities, not sibling skill source. Outlook is a
  connector capability, not a local adapter file.

## Dependency surface

- **Bundled:** comms-bag, selection, rich-email, capability, provider, setup, and ledger contracts; setup,
  validation, and reviewer-only AgentMail scripts; instance and playbook templates.
- **Project:** `docs/agents/communications.md` and the consumer-owned
  `control-plane/communications/` instance.
- **Siblings:** required `manage-tasks` and `manage-opportunities`, invoked by name for their authoritative
  shapes and facts.
