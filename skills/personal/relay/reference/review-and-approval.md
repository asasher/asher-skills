# Review and approval

After rendering, run `scripts/build_review_sheet.py <repo-root> --run <run-dir>`. It writes canonical
`approval-manifest.json` and one `review.html`. The sheet embeds, rather than links, every message's actual
HTML and text, forced light/dark previews, sender, To, CC, evidence summary, template identity, field hashes,
and the canonical manifest. Give every reviewable block a stable element ID.

Invoke the required `serve-via-tailnet` sibling by name with `review.html`. It owns serving, annotations, verdict,
hash-bound event, and awaiting. Relay does not copy its scripts. Only `approve` or `approve_with_nits` for the
current document hash can authorize delivery. A nit that changes an approved field requires a new render and
review; do not treat a prior verdict as transferable.

Before provider work, `agentmail_delivery.py` recomputes the full approval manifest from disk and confirms it
equals both `approval-manifest.json` and the embedded canonical JSON. It also recomputes the review document
hash and requires a matching approving event in the run's `review-state/events.jsonl`.

Changing HTML, text, sender, To, CC, template identity, evidence manifest, or the review sheet invalidates
authorization. The only valid next action is append `superseded`, rebuild the sheet, and obtain a new verdict;
zero AgentMail commands are allowed on mismatch.
