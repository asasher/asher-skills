# research — anchor positions to objective data

The framework is benchmark-driven: every ask should rest on an impersonal standard (market rate, agency
margin, royalty range, comparable terms), not "what feels fair to a friend." This is where the agent earns its
keep for non-expert partners. Run during `interview` and `negotiate` whenever a position needs an anchor.

## How
- Spawn subagents for parallel lookups when there's more than one thing to find (e.g. market salary AND
  typical advisor equity AND data-royalty ranges). Keep each subagent's task tight; have it return the figure,
  a range, and the source.
- Prefer recent, citable sources. Capture the number, the range, the date, and where it came from.
- Sanity-check against the deal's specifics (geography, stage, industry) — a generic figure misapplied is
  worse than none.

## Where results go
- **Exploratory / one-sided / sensitive** research → `private/notes/` (gitignored). Anything that hints at your
  floor or strategy stays private.
- **Benchmarks you will actually cite** in a position → into `canvas.json` notes and your
  `negotiation/from-<me>/round-*.md`, **with the source**, so the other side sees the same objective anchor.
  Shared anchors are how two sides reach "fairness is a fact" instead of a tug of war.

## Examples of useful anchors
- Market salary / contractor rate for the labour each side brings (sets the Box 6 pay line).
- Agency or SaaS gross margins; typical delivery margins.
- Advisor equity norms (e.g. FAST levels), vesting/cliff conventions.
- Data-licensing royalty ranges; channel/sales commission ranges.
- Cost to rebuild a pre-existing asset (anchors a background-IP licence value).
- Comparable deal structures in the same space.

## Guardrails
- Don't fabricate or over-precise a number; a cited range beats a false point estimate.
- Don't leak strategy: the fact that you researched "how low can their BATNA go" belongs in `private/`, never
  in a committed file.
