# pipeline — the search as a CRM

One file, `goodwork/PIPELINE.md`, is the single source of truth for the campaign. `daily` reads it every morning; `review` reads it every week. Keep it current or the whole ops layer rots.

## Structure

**Active table** — one row per live target/thread:

| Target | Role | Stage | Warmth | Last touch | Next action | Due | Notes |
|---|---|---|---|---|---|---|---|

- **Stage**: researching → outreach → conversation → referral → applied → screen → interview → offer → closed(won/lost/retired).
- **Warmth**: cold / weak tie / insider / referral-committed.
- **Next action + due date are mandatory.** A row without a next action is a decision waiting to be made — flag it. This is the anti-anxiety design: every open loop has a pre-decided next step, so the user never has to improvise from worry.

**Conversation log** — appended debriefs from `outreach` (who, date, what was learned, promised follow-ups).

**Metrics block** — running counts per week: new targets, outreach sent, response rate, conversations held, referrals, applications, screens, interviews, offers; plus source-of-interview (which channel actually produces).

## Operating rules

- Update immediately on any event (reply, ghost, interview, rejection) — stale pipelines lie.
- Rejections and retirements get a **reason code** (no response / position filled / failed screen / withdrew—values / withdrew—energy / comp below floor). Reason codes are profile evidence: three "withdrew—energy" codes in a month is the profile talking.
- Respect stage physics: don't let one exciting interview freeze all other threads — offers negotiate best with alternatives alive, and searches die of single-thread hope.
- **Funnel math over feelings.** Diagnose the narrowest constriction, top-down: no responses → message/targeting problem (`outreach`, `targets`); responses but no referrals/applications converting → evidence/positioning problem (`niche`, `assets`); interviews but no offers → preparation problem (route to eloquent `interview` if available); offers but wrong offers → targeting drifted from the profile (`profile`, `targets`).
- Interviews per high-fit target is the metric that matters. Activity quotas are diagnostics, not the goal.

## Offer stage

When offers approach: comp research and negotiation scripts delegate to eloquent (`salary`, `compare-offers`) if available. goodwork adds the profile scoring: energy fit, motivation conditions, values/dealbreakers, whole-life dashboard cost, and the decent-work floor as the hard floor under any negotiation. Remember Never Search Alone's widest finding: negotiate budget, resources, and support for success in the role, not just salary.

## Output

An updated `PIPELINE.md`, today's due actions pushed to `daily`, and any diagnosis with its routing (which command fixes the constriction).
