P1

Next action: run discovery only, inspect both projects, Git release evidence, the task tracker, repository/editorial/template sources, root `.env`, runtime/tooling, and AgentMail reachability. Governing sentence: `skills/personal/relay/reference/setup.md` — “Run `python3 scripts/setup_instance.py <repo-root> --discover`. Inspect the report for repositories, project registries, trackers, release evidence, mailbox sources, existing editorial/template material, optional source skills, Node/npm, root `.env`, and AgentMail CLI reachability.”

Before materialization, confirm the authoritative evidence providers; the two projects and section recipes; each audience’s membership, explicit To/CC roles, interests, disclosure, cadence, and coalescing; operator CC policy; editorial/template choices; AgentMail inbox and verified sender/domain; and webhook versus manual reconciliation. Governing sentence: `skills/personal/relay/reference/setup.md` — “Confirm authoritative evidence providers for shipped, pending, cash, growth, and commitments; projects and their section recipes; audience membership, explicit To/CC roles, interests, disclosure, cadence, and coalescing; operator CC; editorial rules; template choice; AgentMail inbox, verified sender/domain, and webhook or manual reconciliation.”

Only after those choices form a complete binding may the binding-mode setup run. Governing sentence: `skills/personal/relay/reference/setup.md` — “Write those non-secret choices to a complete binding JSON shaped by `templates/instance/bindings.json`, then run `python3 scripts/setup_instance.py <repo-root> --binding <binding.json>`.”

The script may materialize only the new Relay instance and project playbook: `control-plane/relay/` and `docs/agents/relay.md`. Governing sentence: `skills/personal/relay/reference/setup.md` — “Setup studies the consumer repository, confirms its choices, and materializes only `control-plane/relay/` plus `docs/agents/relay.md`.”

Live validation and delivery remain blocked because root `.env` is not Git-ignored and is mode `0644`; fix both before a live check. Governing sentence: `skills/personal/relay/reference/setup.md` — “Before a live check require `.env` to be ignored by Git and mode `0600`.”

Live sending also remains blocked until a sender is selected and verified. Governing sentences: `skills/personal/relay/reference/setup.md` — “A selected unverified sender blocks live send.” And: “Completion criterion: the instance validator passes with complete projects, providers, recipes, audiences, header roles, operator policy, cadence, sender, template, and reconciliation mode; all deliberate local values remain byte-identical on rerun; the credential exists only in the protected root `.env`; and no provider resource or message was created without separate authorization.”

Ambiguity: the probe does not say whether `.env` contains `AGENTMAIL_API_KEY`; if absent, setup may provision only that variable while preserving unrelated assignments. Governing sentence: `skills/personal/relay/reference/setup.md` — “Read or provision only `AGENTMAIL_API_KEY` in `<repo-root>/.env`; preserve unrelated assignments.”

P2

Next action: keep both validated bags immutable, retain their rendered HTML/text/light/dark artifacts, build the self-contained review sheet, invoke `review-loop`, and wait for a current-hash verdict. Governing sentences: `skills/personal/relay/SKILL.md` — “A scheduled invocation may select, render, and present review.” `skills/personal/relay/reference/review-and-approval.md` — “Invoke the required `review-loop` sibling by name with `review.html`.”

Provider writes: zero—do not create a draft, submit a send, or otherwise invoke AgentMail for a write. Governing sentence: `skills/personal/relay/SKILL.md` — “It performs zero provider writes until the current exact review has an approving `review-loop` event.”

Ledger facts: preserve the workflow facts already reached (`selected` and `rendered`) and the review-loop state, but do not append provider lifecycle facts (`draft-created`, `send-submitted`, or `sent`). A no-verdict presentation does not authorize a `reviewed` delivery transition. Governing sentence: `skills/personal/relay/reference/lifecycle-ledgers.md` — “`workflow.jsonl` — selected, rendered, reviewed, draft-created, send-submitted, sent, excluded, rejected, superseded, blocked, and blocked-ambiguous transitions;”

Watermarks do not advance. Governing sentence: `skills/personal/relay/reference/lifecycle-ledgers.md` — “Advance a watermark exactly once after matching `message.sent` or unique sent-message reconciliation.”

Ambiguity: the prose contract enumerates `reviewed` but does not expressly define whether mere presentation without a verdict earns that state; the approval contract makes authorization verdict-bound, so the conservative next action is to leave `reviewed` absent until an approving current-hash event exists. Governing sentence: `skills/personal/relay/reference/review-and-approval.md` — “Only `approve` or `approve_with_nits` for the current document hash can authorize delivery.”

P3

For the HTML change: append `superseded`, rebuild/render the sheet, and obtain a new verdict; AgentMail may not be invoked.

For the plain-text change: append `superseded`, rebuild/render the sheet, and obtain a new verdict; AgentMail may not be invoked.

For the sender change: append `superseded`, rebuild/render the sheet, and obtain a new verdict; AgentMail may not be invoked.

For the To change: append `superseded`, rebuild/render the sheet, and obtain a new verdict; AgentMail may not be invoked.

For the CC change: append `superseded`, rebuild/render the sheet, and obtain a new verdict; AgentMail may not be invoked.

Governing sentences for all five cases: `skills/personal/relay/reference/review-and-approval.md` — “Changing HTML, text, sender, To, CC, template identity, evidence manifest, or the review sheet invalidates authorization.” And: “The only valid next action is append `superseded`, rebuild the sheet, and obtain a new verdict; zero AgentMail commands are allowed on mismatch.”

P4

Reuse the same deterministic `client_id`, derived again from the unchanged approved canonical manifest. Governing sentence: `skills/personal/relay/reference/provider-adapter.md` — “On retry, derive the same client ID and read append-only workflow state.”

Retry only deterministic draft creation. Governing sentence: `skills/personal/relay/reference/provider-adapter.md` — “A create timeout repeats only deterministic create.”

Never mint a new client identity or a new draft identity. Governing sentence: `skills/personal/relay/SKILL.md` — “Reuse identities on retry; reconcile an ambiguous send or append `blocked-ambiguous`—never mint a new client or draft identity.”

P5

Append `blocked-ambiguous` and stop for reconciliation because send submission may have reached AgentMail and uniqueness is unavailable. Governing sentence: `skills/personal/relay/reference/provider-adapter.md` — “If uniqueness is unavailable, append `blocked-ambiguous`; never create a new identity or resend automatically.”

Forbidden provider action: do not resend the recorded draft, create a replacement draft, or mint a new identity. Governing sentence: `skills/personal/relay/reference/provider-adapter.md` — “Once send submission may have reached the provider, perform unique reconciliation by client/draft/message correlation.”

P6

Workflow result: `message.sent` establishes `sent`; later delivery remains mixed, not failed-as-a-whole and not all-delivered.

Recipient A result: `receiving-server-delivered`.

Recipient B result: `bounced`.

All-delivered result: false, because not every intended recipient has a delivery event and B has a failure fact. Governing sentence: `skills/personal/relay/reference/lifecycle-ledgers.md` — ““All delivered” is true only when every intended recipient has a receiving-server delivery event and none has a failure fact.”

Out-of-order and duplicate events do not alter those results: duplicate provider event IDs are ignored, and mixed outcomes remain mixed. Governing sentence: `skills/personal/relay/reference/lifecycle-ledgers.md` — “Duplicate and out-of-order provider events are safe: an already-recorded event ID is ignored, and mixed recipient outcomes remain mixed.”

Advance the audience watermark exactly once at the matching `message.sent`, not at delivery or bounce. Governing sentences: `skills/personal/relay/reference/lifecycle-ledgers.md` — “Advance a watermark exactly once after matching `message.sent` or unique sent-message reconciliation.” And: “Draft creation, send submission, delivery, bounce, complaint, rejection, or reply never independently advances it.”

Relay does not resend. Governing sentence: `skills/personal/relay/SKILL.md` — “Bounce, complaint, rejection, delivery, and reply facts never resend or reply automatically.”

P7

Ingest the explicit manual reconciliation result and append one `reply-received` fact keyed by provider event, message, thread, and source communication. Governing sentences: `skills/personal/relay/reference/lifecycle-ledgers.md` — “`replies.jsonl` — reply-received facts keyed by provider event, message, thread, and source communication;” And: “`scripts/ingest_agentmail_events.py` accepts signed-receiver output or an explicit manual reconciliation file.”

Follow-up is human/manual: Relay reports the reply for action but performs no automatic mutation or response. Governing command: `skills/personal/relay/SKILL.md` — “`status` | Report pending review, blocked sends, mixed delivery, and replies without mutation”.

Relay sends nothing. Governing sentence: `skills/personal/relay/reference/lifecycle-ledgers.md` — “A received reply appends a reply fact and never generates a reply.”

Describe tracking as manual reconciliation, not real-time tracking. Governing sentence: `skills/personal/relay/SKILL.md` — “A missing receiver means manual reconciliation, not real-time tracking.”

P8

Preserve the consumer’s modified accent, footer, renderer, and every other existing consumer file byte-for-byte; do not overwrite them with the package update. Governing sentences: `skills/personal/relay/reference/setup.md` — “Existing consumer files and templates are preserved.” And: “Completion criterion: the instance validator passes with complete projects, providers, recipes, audiences, header roles, operator policy, cadence, sender, template, and reconciliation mode; all deliberate local values remain byte-identical on rerun; the credential exists only in the protected root `.env`; and no provider resource or message was created without separate authorization.”

Emit changed package defaults as `.setup-candidate` files. Emit the changed discovery report as a candidate too; do not rewrite the confirmed binding. Governing sentences: `skills/personal/relay/reference/setup.md` — “Changed defaults produce `.setup-candidate` files.” And: “A changed discovery report becomes a candidate; it never rewrites a confirmed binding.”

Before the new evidence source affects selection, the operator must confirm it as authoritative and update the binding; rerun reconciliation/validation on that deliberate binding. Governing sentence: `skills/personal/relay/reference/setup.md` — “Confirm authoritative evidence providers for shipped, pending, cash, growth, and commitments; projects and their section recipes; audience membership, explicit To/CC roles, interests, disclosure, cadence, and coalescing; operator CC; editorial rules; template choice; AgentMail inbox, verified sender/domain, and webhook or manual reconciliation.”

Until bound, selection must ignore the new source. Governing sentence: `skills/personal/relay/SKILL.md` — “Gather normalized facts only from the evidence providers bound in `bindings.json`, since each audience's confirmed-send watermark.”

P9

Setup may inspect the repository through discovery, but it must not read the old `control-plane/communications/` instance. It may write only `control-plane/relay/` and `docs/agents/relay.md`. Governing sentences: `skills/personal/relay/SKILL.md` — “Never read or write a previous communications instance.” `skills/personal/relay/reference/setup.md` — “Setup studies the consumer repository, confirms its choices, and materializes only `control-plane/relay/` plus `docs/agents/relay.md`.”

The old tree remains completely untouched: no reads, writes, adoption, copying, deletion, or implicit migration. Governing sentence: `skills/personal/relay/reference/setup.md` — “It has no previous-instance migration branch.”
