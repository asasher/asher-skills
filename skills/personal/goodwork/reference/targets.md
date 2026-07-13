# targets - build and rank the employer list

Steve Dalton's LAMP method, adapted. `targets.json` is the operational source of truth for employers, projects, fellowships, agencies, open-source orgs with paid roles, or client segments. See [state.md](state.md) for the schema. `scout` handles posting sources and leads; this command handles who is worth pursuing.

## Build the List

Generate 40+ targets in one sitting. Sources: the niche's community map, employers of people the user admires, competitors/customers/vendors of past employers, best-places lists, conference sponsor pages, portfolio pages of relevant investors, who's-hiring threads, and listening-tour referrals.

Verify each against current sources: the org exists, still does the relevant thing, and has no material blocker such as layoffs, pivots, hiring freezes, visa mismatch, or values conflict. List first, judge later.

## Score It

Use LAMP fields in `targets.json`:

| Field | Meaning | Score |
|---|---|---|
| `advocacy` | Do we have or can we plausibly get an insider? | 1-3 |
| `motivation` | Honest gut pull toward working there | 1-5 |
| `posting` | Live relevant opening, adjacent/regular hiring, or nothing visible | 1-3 |

Sort by Motivation, then Advocacy, then Posting. Run the profile veto pass over the top 15: strike any target that violates a dealbreaker, decent-work floor, or gravity constraint, and record the reason code.

## Work the Top 10

- Actively work the top 5 first: why-them research, two or three insider candidates, and outreach.
- Targets 6-10 warm up next. Below 10 is bench.
- Replace, don't hoard: retire exhausted targets with reason codes and promote from the bench.
- Refill trigger: bench below 10 -> schedule a 30-minute list-building block via `daily`.

## Output

Updated `targets.json`: full scored list, Top 10, why-them notes, insider candidates, retired targets with reason codes. Register the Top 5 as `pipeline.json` cards and hand off to `outreach` or `scout`.
