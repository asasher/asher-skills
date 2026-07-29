# The board — `goodwork/board.html`

One self-contained HTML page generated from `PROFILE.md` and `opportunities.json`. It is a projection:
regenerated whole, never hand-edited, never a source of truth, and never served — no server, no
JavaScript state, no external fetches (inline styles, system fonts).

## When to regenerate

The agent regenerates the board **whenever there is new information worth seeing**, unprompted — the
person is not technical and won't ask for a rebuild:

- during and after an interview session, as profile sections land (seeing it build is the reinforcement);
- after a scout sweep, a stage change, an approved send, or a closed opportunity;
- at every `checkin`.

Cheap to rebuild, so when in doubt, rebuild.

## How to show it

Prefer the harness's native presentation surface — an artifact, a rendered preview, a hosted page —
whichever this session actually has. Absent one, say plainly: "I've updated your board — open
`goodwork/board.html` in your browser." Never stand up a server for it.

## What it shows

Plain language throughout — the person's words from the profile, no schema or framework vocabulary:

1. **Profile snapshot** — who they are and what they're looking for, their weighting of what matters,
   and how well-evidenced the profile is (in words: "well-tested" / "mostly from our conversations so
   far"), with the parameters (roles, location, floor) visible.
2. **The pipeline** — opportunities grouped by stage as columns or sections; each card: company, role,
   fit score with its why, the next action and date, and the latest history line.
3. **This week** — the few current next actions with dates, and anything waiting on the person's OK.

Keep it honest: an empty pipeline shows as an empty pipeline with the suggested next step, not filler.
