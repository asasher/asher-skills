# targets - build and rank the employer list

`targets.json` is the operational source of truth for employers, projects, fellowships, agencies, open-source orgs with paid roles, or client segments (schema: [state.md](state.md)). `scout` handles posting sources and leads; this command handles who is worth pursuing.

## Build the List

Generate 40+ targets in one sitting. Sources: the niche's community map, employers of people the user admires, competitors/customers/vendors of past employers, best-places lists, conference sponsor pages, portfolio pages of relevant investors, who's-hiring threads, listening-tour referrals.

Verify each against current sources: the org exists, still does the relevant thing, no material blocker (layoffs, pivots, hiring freezes, visa mismatch, values conflict). List first, judge later.

## Score It

LAMP fields in `targets.json`:

| Field | Meaning | Score |
|---|---|---|
| `advocacy` | Do we have or can we plausibly get an insider? | 1-3 |
| `motivation` | Honest gut pull toward working there | 1-5 |
| `posting` | Live relevant opening, adjacent/regular hiring, or nothing visible | 1-3 |

Sort by Motivation, then Advocacy, then Posting. Profile veto pass over the top 15: strike any target violating a dealbreaker, decent-work floor, or gravity constraint; record the reason code.

## Work the Top 10

- Actively work the top 5 first: why-them research, two or three insider candidates, outreach.
- Targets 6-10 warm up next. Below 10 is bench.
- Replace, don't hoard: retire exhausted targets with reason codes, promote from the bench.
- Refill trigger: bench below 10 -> a 30-minute list-building block via `daily`.

## Output

Updated `targets.json`: full scored list, Top 10, why-them notes, insider candidates, retired targets with reason codes. Register the Top 5 as `pipeline.json` cards and hand off to `outreach` or `scout`.
