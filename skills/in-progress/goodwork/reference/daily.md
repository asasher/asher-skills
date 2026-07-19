# daily - today's actions and the journal

The sustain loop, run at the start (queue) and end (journal) of a working day. Minutes, not a meeting: the queue exists to manufacture a visible small win every day, because searches die of momentum loss more than rejection.

## First - reconcile

Start every `daily` with the [reconcile.md](reconcile.md) sweep, unless one already ran today (`capabilities.json` → `reconcile.last_run_at`) or the user declines it: inbound replies change today's queue before new outbound work is chosen. The recorded cadence governs *standalone* reconcile scheduling only — it never exempts `daily` from sweeping first.

## Morning — the action queue

Build from `pipeline.json`, `leads.json`, `targets.json`, `metrics.json`, and open narrative commitments — smallest sufficient set (default 3–5 items, ≤90 minutes unless the user wants a heavy day):

1. **Due follow-ups** from `pipeline.json` (the 3-day/7-day cadence, promised thank-yous) — commitments go first.
2. **One pipeline-advancing action**: an outreach message, conversation prep, a high-fit application step.
3. **One compounding action**: proof-of-work artifact progress, community participation, or a prototype step from `EXPERIMENTS.md`.
4. **Refill work only if a trigger fired** (bench below 10 targets, lead bench stale, artifact queue empty).

Each item: concrete, time-boxed, with its pipeline row named. Low-energy day → shrink the queue rather than skip it; one follow-up keeps the streak alive. Never generate busywork; an honest 2-item day beats padding.

## Evening — the Good Time Journal (60 seconds)

Three lines in `goodwork/JOURNAL.md`:

```
2026-07-03 | did: [what actually happened] | win: [smallest real progress] | energy: [what energized / what drained, one phrase each] | flow: [y/n, during what]
```

Instrumentation, not a diary: the energy/flow fields feed `review`'s pattern detection and keep testing the profile's energy map against reality — including the search activities themselves (lighting up during informational interviews but dreading solo artifact work is data about the next role).

## Cadence flags (raise, don't nag)

- 3+ days with no journal entry → ask once whether to shrink the daily footprint or pause the campaign honestly (a declared pause beats a silent fade).
- A week of completed queues with zero energy-positive entries → flag for `review`: the search design itself may be misfit.
- Name streaks plainly ("12 straight days") — momentum is a real asset; no fake celebration.

## Output

Today's queue (with pipeline IDs), `pipeline.json` next actions updated, tonight's journal line appended, cadence flags routed to `review`.
