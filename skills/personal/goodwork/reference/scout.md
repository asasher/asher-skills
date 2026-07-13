# scout - maintain sources and sweep leads

`scout` finds postings; `targets` manages employers. Keep them separate. A source is a place to search. A target is an employer, project, or segment the user wants to work.

## Inputs

Read `PROFILE.md`, `targets.json`, `sources.json`, `leads.json`, and the Top 10 targets before sweeping. If the profile is missing, run the short-form interview first.

## Maintain Sources

Build or update `sources.json` with boards, newsletters, community job channels, saved searches, recruiter lists, and niche-specific feeds. For each source record type, URL/query, niche tags, auth requirement, cadence, last sweep, and whether it is still alive.

Add sources from `NICHE.md` communities and from listening-tour recommendations. Retire sources that go stale, duplicate another source, or produce repeated low-fit leads.

## Sweep

For each due source, collect current postings and verify they are live. Create or update `leads.json` records with stable IDs; do not duplicate a lead already seen through another source.

Score leads against:
- Top 10 target match or adjacent employer value.
- Profile fit: energy map, values, constraints, decent-work floor.
- Evidence readiness against must-have requirements.
- Freshness and source credibility.
- Warmth path: insider, community, recruiter, or referral route.

High-score leads flow into the bench, not directly into applications. Leads become pipeline cards only when selected for outreach or apply.

## Learning Loop

Lead approvals, dismissals, and reason codes are profile evidence. Queue repeated patterns in `evidence-inbox.json` so `profile` or `review` can confront drift.

## Output

Updated `sources.json` and `leads.json`, a ranked lead bench with reason codes, and any Top 10 target or profile drift flagged for `targets` or `profile`.
