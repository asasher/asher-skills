# Review and approval

After rendering, run `scripts/build_review_sheet.py <repo-root> --run <run-dir>`. It writes canonical
`approval-manifest.json` and one `review.html`. The sheet embeds, rather than links, every message's actual
HTML and text, forced light/dark previews, sender, To, CC, evidence summary, template identity, field hashes,
and the canonical manifest. Before writing either artifact, the script verifies that the bag still matches the
consumer's structured audience, interest, section, sender, and recipient bindings. Give every reviewable block
a stable element ID.

Present the sheet's exact content to the user in chat: for each message, the sender, To, CC, subject and
template identity, the full body content as rendered, the evidence summary, and the review document hash —
plus the `review.html` path so the user can open it locally. The user's explicit in-chat approval of that
exact content authorizes it; any clear wording counts, and no magic token is required, but an ambiguous or
partial response is not approval. On approval, append a `chat_approval` event carrying `verdict` (`approve`
or `approve_with_nits`) and the current `doc_hash` to the run's `review-state/events.jsonl`. Appending that
event is itself gated: only the user's explicit in-chat approval of the exact current sheet permits it. Only
`approve` or `approve_with_nits` for the current document hash can authorize delivery. A nit that changes an
approved field requires a new render and review; do not treat a prior approval as transferable.

Before provider work, `agentmail_delivery.py` revalidates the bag against current structured bindings,
recomputes the full approval manifest from disk, and confirms it equals both `approval-manifest.json` and the
embedded canonical JSON. It also recomputes the review document hash and requires a matching approving event in
the run's `review-state/events.jsonl`.

Changing HTML, text, sender, To, CC, template identity, evidence manifest, or the review sheet invalidates
authorization. The only valid next action is append `superseded`, rebuild the sheet, and obtain a new in-chat
approval; zero AgentMail commands are allowed on mismatch.
