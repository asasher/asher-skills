# pipeline - the search as a CRM

`pipeline.json` is the operational source of truth for live campaign work. UI pages are projections from this file; the server never writes it. Schema and ID rules: [state.md](state.md).

## Structure

One card per live thread: target, lead, outreach thread, application, interview process, or offer. Inbound replies are nested records on matched cards; low-confidence inbound goes to `unmatched_replies` until matched. Next action and due date are mandatory on every open card — a missing next action is a decision waiting to be made; flag it immediately.

## Operating Rules

- Update immediately on any event: reply, ghost, interview, rejection, user drag request, approval, draft, submission, follow-up — and append a plain-language `history` entry to the card each time. The history is what the user sees when they open a card on the board; it must read as the story of the relationship so far, not bookkeeping.
- Rejections and retirements get reason codes: `no_response`, `position_filled`, `failed_screen`, `withdrew_values`, `withdrew_energy`, `comp_below_floor`, `duplicate`, `not_now`.
- Reason codes are profile evidence. Repeated patterns go to `evidence-inbox.json`.
- Respect stage physics: one exciting interview must not freeze all other threads.
- Browser drag-and-drop in the kanban is a stage-change request event. The agent applies it after checking consistency and asking follow-ups when needed.

## Reply Compaction

Keep active cards small: preserve thread IDs, the newest decision-relevant reply summaries, and a `reply_digest` for older matched replies. On weekly review or card closure, compact stale reply details into the digest, retaining stage-changing reply IDs and source thread IDs. Unmatched replies stay only while pending user judgment; dismiss, match, or summarize during review.

## Funnel Diagnosis

Use `metrics.json` plus cards to find the narrowest constriction:

- No responses -> message or targeting problem (`outreach`, `targets`).
- Responses but no referrals/applications -> evidence or positioning problem (`niche`, `assets`).
- Applications but no screens -> targeting, evidence, or documents, in that order (`targets`, `assets`, `apply`).
- Interviews but no offers -> preparation problem (delegate interview mechanics when available).
- Offers but wrong offers -> targeting drifted from the profile (`profile`, `targets`).

Interviews per high-fit target is the metric that matters. Activity quotas are diagnostics, not the goal.

## Offer Stage

Comp research and negotiation scripts delegate to document/interview helpers when available. Goodwork adds profile scoring: energy fit, motivation conditions, values/dealbreakers, whole-life dashboard cost, decent-work floor.

## Output

Updated `pipeline.json`, today's due actions pushed to `daily`, evidence inbox entries added, one diagnosis with its routing.
