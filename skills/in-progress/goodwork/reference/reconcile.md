# reconcile - inbound sweep and stage updates

Runs before `daily` because inbound changes determine today's queue.

## Inputs

Read [state.md](state.md), [execution.md](execution.md), `capabilities.json`, `pipeline.json`, `approvals.jsonl`, and `events.jsonl`. Use only capabilities recorded as available.

## Sweep Order

1. Gmail via connector: replies, recruiter mail, interview logistics, rejections, sent/draft status.
2. LinkedIn messages through the authenticated Chrome profile when available.
3. WhatsApp Web read-only through the Chrome profile, only if setup recorded explicit user acceptance of the risk.

Do not send from any channel during the sweep.

## Match and Advance

Match inbound to pipeline cards by thread IDs, sender/domain, company, role, URLs, quoted content. Low confidence → create an unmatched reply record and ask before changing a stage.

Advance stages when the message is clear: reply, conversation booked, referral offered, application requested, screen, interview, offer, rejection, ghost, retirement. Record reason codes. Keep every open card with a next action and due date.

Interview requests trigger calendar-slot proposals through the calendar connector when available. Reply drafts, connector-sent email, calendar holds, and browser sends follow [execution.md](execution.md).

## Learning Loop

Tag profile-relevant patterns into the evidence inbox: repeated rejections for missing evidence, roles the user keeps dismissing, energizing conversations, compensation-floor conflicts, values/energy withdrawals.

## Output

Updated `pipeline.json`, Gmail draft replies for user send, calendar proposals needing approval when they create holds, unmatched inbound needing user judgment, today's changed priorities for `daily`.
