# AgentMail lifecycle capability — findings

**As of:** 2026-07-16

## Concise answer

Yes, with one important boundary. AgentMail documents direct send, a sent/delivered/bounced/complained/rejected lifecycle, inbound-reply events, and message/thread identifiers that make a provider-backed delivery ledger feasible. It does not remove the need for this skill's own durable, idempotent ledger. Automatic event intake additionally requires a configured webhook endpoint or a maintained WebSocket connection; the former must verify AgentMail's Svix signature. [I-1]

## Claim ledger

- **O-1 — Observation.** The AgentMail CLI documentation lists direct message sending and commands for drafts, threads, messages, webhooks, domains, and API keys. Source: [AgentMail CLI](https://docs.agentmail.to/integrations/cli), accessed 2026-07-16.
- **O-2 — Observation.** AgentMail documents message lifecycle events `message.sent`, `message.delivered`, `message.bounced`, `message.complained`, and `message.rejected`; the documented sent and delivered payloads contain an inbox ID, thread ID, message ID, timestamp, and recipients. Source: [Webhook events](https://docs.agentmail.to/events) and [message delivered payload](https://www.agentmail.to/docs/api-reference/webhooks/events/message-delivered), accessed 2026-07-16.
- **O-3 — Observation.** AgentMail documents `message.received` for a received message, says received-message payloads contain the message and thread, and says replies retain thread context through standard mail headers. Sources: [Webhook events](https://docs.agentmail.to/events) and [threaded conversations](https://docs.agentmail.to/knowledge-base/threaded-conversations), accessed 2026-07-16.
- **O-4 — Observation.** AgentMail recommends webhooks for production event processing; it also documents WebSockets as an alternative that does not need a public endpoint. Source: [Webhooks overview](https://docs.agentmail.to/webhooks-overview), accessed 2026-07-16.
- **O-5 — Observation.** AgentMail's webhook documentation says deliveries use Svix and provides signature verification headers. Source: [Verifying webhooks](https://docs.agentmail.to/webhook-verification), accessed 2026-07-16.
- **O-6 — Observation.** AgentMail emits a `domain.verified` event and documents domain management in its CLI. Sources: [Webhook events](https://docs.agentmail.to/events) and [AgentMail CLI](https://docs.agentmail.to/integrations/cli), accessed 2026-07-16.
- **O-7 — Observation.** AgentMail documents `client_id` idempotency for create operations, including drafts. Its duplicate-send guidance recommends creating a critical-send draft with a deterministic client ID; sending converts and deletes that draft, and a later send of the same draft fails rather than sending another message. Sources: [Idempotent requests](https://docs.agentmail.to/idempotency) and [Preventing duplicate sends](https://docs.agentmail.to/knowledge-base/preventing-duplicate-sends), accessed 2026-07-16.

## Inferences

- **I-1 — Inference (high confidence).** A local append-only communication ledger can correlate approved content and recipient hashes with AgentMail message and thread IDs, then record provider lifecycle events idempotently. This is supported by O-2 and O-3; the local ledger remains necessary because provider events alone do not encode the skill's evidence selection, human approval, or supersession decisions.
- **I-2 — Inference (high confidence).** Setup can offer a custom sending-domain verification path, but direct delivery must not be blocked solely because the optional domain was declined. This is supported by O-1 and O-6.
- **I-3 — Inference (high confidence).** A webhook receiver is optional only if the chosen installation accepts manual reconciliation or has a continuously maintained WebSocket consumer; no durable event receiver means lifecycle status must be reconciled on demand instead of claimed real time. This is supported by O-4 and O-5.
- **I-4 — Inference (high confidence).** The safe direct-delivery primitive is a deterministic, idempotently created AgentMail draft followed by sending that exact draft ID after approval—not the non-idempotent direct-message send endpoint. A retry must reuse the same client ID and draft ID; an ambiguous outcome is reconciled or blocked, never retried with a new identity. This is supported by O-7.

## Unknowns and consequences

- **U-1.** The exact current AgentMail permission names and minimum CLI version appropriate for direct stakeholder delivery were not established here. The implementation must pin them from the then-current official CLI/API reference and verify them in setup before live delivery.
- **U-2.** This research does not establish recipient-level delivery event semantics for multi-recipient messages. The plan therefore requires the provider-event schema to retain the documented recipients array and tests the chosen behavior before treating delivery as complete.
- **U-3.** This research does not establish open/click tracking. Those metrics are expressly out of scope for the first version.
- **U-4.** The documentation establishes create-draft idempotency and single-use draft send, but this pass did not establish a permanent provider lookup from a deleted draft's client ID to its resulting message after a lost send response. The implementation must effect-probe that recovery seam; until uniquely reconciled, an ambiguous send remains blocked rather than being recreated.

## Method and audit

Primary sources only: AgentMail official documentation listed above. Every material conclusion is an inference explicitly linked to observations; mutable documentation is bounded by the access date. Audit result: pass, with U-1 through U-3 retained as explicit implementation gates.
