# Presentation evidence

Accepted evidence: `capture-1/transcript.json` and its readable transcript. Seven stored chat messages cover the opening question, deliberate resends, and repeated acceptance.

- `assistant:msg_0a5d1a50a95fe53b016aabcf15063887d0bdac16a6caa2e454`: the opening response uses a useful situation table, then several paragraphs about request idempotency, constraints, resends, and email delivery. The handoffs are described only in prose.
- `assistant:msg_0a5d1a50a95fe53b016aabd0755d9487d0b45fe0d3017a0ab2`: explains pending, unexpired, expired, and resent invitations in paragraphs. An invitation-state diagram could show the relationship once.
- `assistant:msg_0a5d1a50a95fe53b016aabd0b2348c87d0b1d28979c271e7ca`: describes repeated acceptance, existing membership, and revoked membership in bullets and prose. A branch sketch could expose the distinct outcomes.

Hypothesis: writing-for-humans guides voice but says nothing about choosing a representation. Add a small presentation section informed by Show Me. Preserve unslop and the existing voice guidance to keep this trial focused. The user authorized this direction and another conversation; no numeric rating was supplied.

Capture limitation: T3 reports a ready session with no active turn or streaming messages, but retains one unstarted pending row for the human's second follow-up. The visible assistant response addresses that follow-up. Capture preserves the row and records the acceptance of the visible transcript as-is; it does not rewrite T3 state or label that row completed.
