# pipeline - the search as a CRM

`pipeline.json` is the operational source of truth for live campaign work. UI kanban pages are projections from this file; the server never writes it. See [state.md](state.md) for the schema and ID rules.

## Structure

One card per live thread: target, lead, outreach thread, application, interview process, or offer. Field names, stage enum, warmth enum, draft records, reply records, and ID rules live in [state.md](state.md).

Inbound replies are nested stable records on matched cards. Low-confidence inbound goes to `unmatched_replies` until the user or agent can match it. Next action and due date are mandatory for every open card. A missing next action is a decision waiting to be made; flag it immediately.

## Operating Rules

- Update immediately on any event: reply, ghost, interview, rejection, user drag request, approval, draft, submission, or follow-up.
- Rejections and retirements get reason codes: `no_response`, `position_filled`, `failed_screen`, `withdrew_values`, `withdrew_energy`, `comp_below_floor`, `duplicate`, `not_now`.
- Reason codes are profile evidence. Repeated patterns go to `evidence-inbox.json`.
- Respect stage physics: do not let one exciting interview freeze all other threads.
- Browser drag-and-drop in the kanban is a stage-change request event. The agent applies it after checking consistency and asking follow-ups when needed.

## Reply Compaction

Keep active cards small: preserve thread IDs, the newest decision-relevant reply summaries, and a `reply_digest` for older matched replies. On weekly review or card closure, compact stale reply details into the digest while retaining any stage-changing reply IDs and source thread IDs. Low-confidence unmatched replies stay only while pending user judgment; dismiss, match, or summarize them during review.

## Funnel Diagnosis

Use `metrics.json` plus cards to find the narrowest constriction:

- No responses -> message or targeting problem (`outreach`, `targets`).
- Responses but no referrals/applications -> evidence or positioning problem (`niche`, `assets`).
- Applications but no screens -> targeting, evidence, or documents, in that order (`targets`, `assets`, `apply`).
- Interviews but no offers -> preparation problem (delegate interview mechanics when available).
- Offers but wrong offers -> targeting drifted from the profile (`profile`, `targets`).

Interviews per high-fit target is the metric that matters. Activity quotas are diagnostics, not the goal.

## Offer Stage

When offers approach: comp research and negotiation scripts delegate to document/interview helpers when available. Goodwork adds profile scoring: energy fit, motivation conditions, values/dealbreakers, whole-life dashboard cost, and the decent-work floor.

## Output

Updated `pipeline.json`, today's due actions pushed to `daily`, any evidence inbox entries added to `evidence-inbox.json`, and one diagnosis with its routing.
