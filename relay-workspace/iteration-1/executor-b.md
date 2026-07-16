## P1

Discover the two projects, project registries, task tracker, Git release evidence, mailbox/editorial/template material if any, optional source skills, Node/npm, the root `.env` condition, and AgentMail CLI reachability. Source: `skills/personal/relay/reference/setup.md` — “Inspect the report for repositories, project registries, trackers, release evidence, mailbox sources, existing editorial/template material, optional source skills, Node/npm, root `.env`, and AgentMail CLI reachability.”

After confirmation, setup may materialize only `control-plane/relay/` and `docs/agents/relay.md`; it has no migration path. Source: `skills/personal/relay/reference/setup.md` — “Setup studies the consumer repository, confirms its choices, and materializes only `control-plane/relay/` plus `docs/agents/relay.md`.” Source: same file — “It has no previous-instance migration branch.”

The operator must confirm the authoritative evidence providers; projects and section recipes; audience membership; explicit To/CC roles; interests, disclosure, cadence, and coalescing; operator CC; editorial rules; template; AgentMail inbox; verified sender/domain; and webhook versus manual reconciliation. Source: `skills/personal/relay/reference/setup.md` — “Confirm authoritative evidence providers for shipped, pending, cash, growth, and commitments; projects and their section recipes; audience membership, explicit To/CC roles, interests, disclosure, cadence, and coalescing; operator CC; editorial rules; template choice; AgentMail inbox, verified sender/domain, and webhook or manual reconciliation.”

Live validation is blocked because `.env` is neither Git-ignored nor mode `0600`. Source: `skills/personal/relay/reference/setup.md` — “Before a live check require `.env` to be ignored by Git and mode `0600`.”

Completion and live sending also remain blocked until a sender is selected and verified. Source: `skills/personal/relay/reference/setup.md` — “A selected unverified sender blocks live send.” Source: same file — “Completion criterion: the instance validator passes with complete projects, providers, recipes, audiences, header roles, operator policy, cadence, sender, template, and reconciliation mode; all deliberate local values remain byte-identical on rerun; the credential exists only in the protected root `.env`; and no provider resource or message was created without separate authorization.”

Ambiguity: the contract does not say whether an incomplete binding may be temporarily written before all choices are confirmed; it only directs setup to write a “complete binding JSON.” Source: `skills/personal/relay/reference/setup.md` — “Write those non-secret choices to a complete binding JSON shaped by `templates/instance/bindings.json`, then run `python3 scripts/setup_instance.py <repo-root> --binding <binding.json>`.”

## P2

The allowed next actions are to build the self-contained review sheet, invoke `review-loop`, serve it, and wait for a verdict. Source: `skills/personal/relay/reference/review-and-approval.md` — “After rendering, run `scripts/build_review_sheet.py <repo-root> --run <run-dir>`.” Source: same file — “Invoke the required `review-loop` sibling by name with `review.html`.” Source: same file — “It owns serving, annotations, verdict, hash-bound event, and awaiting.”

Provider writes are zero. Source: `skills/personal/relay/SKILL.md` — “A scheduled invocation may select, render, and present review.” Source: same file — “It performs zero provider writes until the current exact review has an approving `review-loop` event.”

The workflow ledger may contain the completed `selected` and `rendered` transitions, but it must not contain `draft-created`, `send-submitted`, or `sent` facts for this run. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “`workflow.jsonl` — selected, rendered, reviewed, draft-created, send-submitted, sent, excluded, rejected, superseded, blocked, and blocked-ambiguous transitions;” Source: `skills/personal/relay/reference/provider-adapter.md` — “No provider write may occur before exact approval.”

Neither audience watermark advances. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “Advance a watermark exactly once after matching `message.sent` or unique sent-message reconciliation.” Source: same file — “Draft creation, send submission, delivery, bounce, complaint, rejection, or reply never independently advances it.”

Ambiguity: the references enumerate a `reviewed` workflow transition but do not define whether review presentation without a verdict appends it; therefore no `reviewed` fact should be assumed solely from the stated scenario.

## P3

For each of the five cases—changed HTML, changed plain text, changed sender, changed To, and changed CC—the next action is identical: append `superseded`, rebuild the review sheet, obtain a new verdict, and invoke no AgentMail command. Source: `skills/personal/relay/reference/review-and-approval.md` — “Changing HTML, text, sender, To, CC, template identity, evidence manifest, or the review sheet invalidates authorization.” Source: same file — “The only valid next action is append `superseded`, rebuild the sheet, and obtain a new verdict; zero AgentMail commands are allowed on mismatch.”

No ambiguity.

## P4

Reuse the same deterministic client ID derived from the approved canonical manifest. Source: `skills/personal/relay/reference/provider-adapter.md` — “On retry, derive the same client ID and read append-only workflow state.” Source: same file — “derives `relay-<sha256>` client identity from the approved canonical manifest;”

The only operation that may be retried is deterministic draft creation. Source: `skills/personal/relay/reference/provider-adapter.md` — “A create timeout repeats only deterministic create.”

Never mint a new client identity or a new draft identity. Source: `skills/personal/relay/SKILL.md` — “Reuse identities on retry; reconcile an ambiguous send or append `blocked-ambiguous`—never mint a new client or draft identity.”

No ambiguity.

## P5

Append `blocked-ambiguous`. Source: `skills/personal/relay/reference/provider-adapter.md` — “If uniqueness is unavailable, append `blocked-ambiguous`; never create a new identity or resend automatically.”

Do not resubmit send, create a replacement draft, or mint a new identity. Source: `skills/personal/relay/reference/provider-adapter.md` — “Once send submission may have reached the provider, perform unique reconciliation by client/draft/message correlation.” Source: same file — “If uniqueness is unavailable, append `blocked-ambiguous`; never create a new identity or resend automatically.”

No ambiguity.

## P6

The workflow result is `sent`, with mixed delivery outcomes retained rather than collapsed. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “`workflow.jsonl` — selected, rendered, reviewed, draft-created, send-submitted, sent, excluded, rejected, superseded, blocked, and blocked-ambiguous transitions;” Source: same file — “Duplicate and out-of-order provider events are safe: an already-recorded event ID is ignored, and mixed recipient outcomes remain mixed.”

Recipient A is `receiving-server-delivered`; recipient B is `bounced`. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “`delivery.jsonl` — pending, receiving-server-delivered, bounced, complained, or rejected per normalized recipient hash and unique provider event ID;”

“All delivered” is false. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — ““All delivered” is true only when every intended recipient has a receiving-server delivery event and none has a failure fact.”

The audience watermark advances exactly once when the matching `message.sent` fact is accepted, independently of the later delivery and bounce events. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “Advance a watermark exactly once after matching `message.sent` or unique sent-message reconciliation.” Source: same file — “Draft creation, send submission, delivery, bounce, complaint, rejection, or reply never independently advances it.”

Duplicate event IDs are ignored and out-of-order arrival does not alter those results. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “Duplicate and out-of-order provider events are safe: an already-recorded event ID is ignored, and mixed recipient outcomes remain mixed.”

Relay does not resend. Source: `skills/personal/relay/SKILL.md` — “Bounce, complaint, rejection, delivery, and reply facts never resend or reply automatically.”

No ambiguity.

## P7

Ingest the explicit manual reconciliation and append a `reply-received` fact keyed by provider event, message, thread, and source communication. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “`scripts/ingest_agentmail_events.py` accepts signed-receiver output or an explicit manual reconciliation file.” Source: same file — “`replies.jsonl` — reply-received facts keyed by provider event, message, thread, and source communication;”

Surface the reply in status for human follow-up; the lifecycle itself prescribes no automatic follow-up. Source: `skills/personal/relay/SKILL.md` — “`status` | Report pending review, blocked sends, mixed delivery, and replies without mutation.” Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “A received reply appends a reply fact and never generates a reply.”

Relay sends nothing. Source: `skills/personal/relay/reference/lifecycle-ledgers.md` — “A received reply appends a reply fact and never generates a reply.”

Tracking must be described as manual, not real-time. Source: `skills/personal/relay/reference/setup.md` — “Do not claim real-time events unless a signature-verified receiver was effect-tested; otherwise record `manual`.” Source: `skills/personal/relay/SKILL.md` — “A missing receiver means manual reconciliation, not real-time tracking.”

Ambiguity: the contract does not assign a human owner, deadline, or specific follow-up action beyond surfacing the reply and prohibiting an automatic reply.

## P8

Preserve the consumer’s accent, footer, renderer, and other deliberate local files byte-for-byte. Source: `skills/personal/relay/reference/setup.md` — “Existing consumer files and templates are preserved.” Source: same file — “Completion criterion: the instance validator passes with complete projects, providers, recipes, audiences, header roles, operator policy, cadence, sender, template, and reconciliation mode; all deliberate local values remain byte-identical on rerun; the credential exists only in the protected root `.env`; and no provider resource or message was created without separate authorization.”

Emit `.setup-candidate` files for changed package defaults rather than overwriting the local versions. Source: `skills/personal/relay/reference/setup.md` — “Changed defaults produce `.setup-candidate` files.”

Emit the changed discovery report as a candidate and leave the confirmed binding unchanged. Source: `skills/personal/relay/reference/setup.md` — “A changed discovery report becomes a candidate; it never rewrites a confirmed binding.”

The newly discovered evidence source must be explicitly confirmed and added to the binding before it can affect selection. Source: `skills/personal/relay/reference/setup.md` — “Confirm authoritative evidence providers for shipped, pending, cash, growth, and commitments; projects and their section recipes; audience membership, explicit To/CC roles, interests, disclosure, cadence, and coalescing; operator CC; editorial rules; template choice; AgentMail inbox, verified sender/domain, and webhook or manual reconciliation.” Source: `skills/personal/relay/SKILL.md` — “Gather normalized facts only from the evidence providers bound in `bindings.json`, since each audience's confirmed-send watermark.”

No ambiguity.

## P9

Setup may inspect the consumer repository for discovery, but it must never read the old `control-plane/communications/` instance. Source: `skills/personal/relay/reference/setup.md` — “Setup studies the consumer repository, confirms its choices, and materializes only `control-plane/relay/` plus `docs/agents/relay.md`.” Source: `skills/personal/relay/SKILL.md` — “Never read or write a previous communications instance.”

Its instance writes are limited to `control-plane/relay/` and `docs/agents/relay.md`; the sole separately stated credential location is the repository-root `.env`, where only `AGENTMAIL_API_KEY` may be read or provisioned. Source: `skills/personal/relay/reference/setup.md` — “Setup studies the consumer repository, confirms its choices, and materializes only `control-plane/relay/` plus `docs/agents/relay.md`.” Source: same file — “Read or provision only `AGENTMAIL_API_KEY` in `<repo-root>/.env`; preserve unrelated assignments.”

The old tree remains completely untouched and no migration occurs. Source: `skills/personal/relay/reference/setup.md` — “It has no previous-instance migration branch.” Source: `skills/personal/relay/SKILL.md` — “Never read or write a previous communications instance.”

Ambiguity: “materializes only” excludes ordinary instance output elsewhere, while the credential rule separately permits provisioning `AGENTMAIL_API_KEY` in root `.env`; the narrow `.env` exception should not be generalized to any other path.
