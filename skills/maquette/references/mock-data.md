# Mock data: realism is engineered

Data realism is the single biggest fidelity lever. Buyers don't inspect your animation curves; they read
the rows. Three rows of "John Doe — $100.00" reads as a mockup. Forty-seven rows of plausible,
cross-referenced, domain-correct records reads as a product someone already uses.

## Schema first

- All domain types live in `lib/schema.ts`. This file **is** the future database schema — name fields the
  way the domain names them (from the intake vocabulary), not the way React finds convenient.
- IDs look like production IDs (`ord_8k3j2`, `INV-2024-0847`), not `1, 2, 3`.
- Model states/enums fully even if only some appear in the demo — the handoff inherits them.

## Seeded generation, not hand-typed rows

Fixtures come from generator functions using a seeded PRNG so every run of the demo is identical.

```ts
// lib/fixtures/rng.ts
export function mulberry32(seed: number) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
export const rng = mulberry32(20260706); // one fixed seed for the whole app
```

## Relative dates — never hardcode

A demo with hardcoded "March 2026" timestamps looks dead by July. Generate every date as an offset from
now: `daysAgo(3)`, `hoursAgo(2)`, `inDays(14)`. The demo is perpetually alive.

```ts
export const daysAgo = (n: number) => new Date(Date.now() - n * 864e5);
```

Rendering caveat: relative-to-now dates cause SSR/client hydration mismatches. Render timestamps inside a
hydration guard (mounted-state check) or format deterministically — see web-quality reference.

## Distributions and volumes

- **Volume:** enough rows that lists scroll — ~30–80 for primary entities, a handful for config-like ones.
  Match intake magnitudes (if they said "200 orders a day", a list of 12 is a tell).
- **Distribution:** not uniform. Most records normal, some aging, a few outliers: 2 overdue invoices, one
  order stuck in a weird state, one customer who accounts for 30% of revenue. Skew is what real data looks
  like.
- **Precision:** real numbers are ragged — `$1,847.50`, not `$1,000.00`. Quantities, weights, and rates
  should carry domain-plausible precision and units.
- **Names:** domain-plausible, varied, culturally mixed. Company names that sound like the industry
  (freight brokers do not have customers named "Acme Corp"). Use intake's real-world examples as style
  templates. No lorem ipsum anywhere, ever — placeholder text in a rendered screen fails the build.
- **One deliberate edge case per entity type** — a very long name, a zero-quantity line, a cancelled
  record. They make tables look lived-in and demo how the UI handles mess.

## Coherence

- **Cross-reference everything.** The customer on the invoice exists in the customers list, appears in the
  activity feed, has a history consistent with their account age. Generators should build the object graph
  together, not per-table.
- **Lived-in history:** dashboards get ~3 months of backstory (activity feeds, trend charts with believable
  seasonality). A product with history looks bought; empty states look like homework.
- **Deliberate empty states:** pick one or two places to show a designed empty state (it proves you
  designed one) — everywhere else, populated.
- **The current user is a persona**, with a name, an avatar (initials are fine), assigned records, and
  recent activity of their own.

## Simulated time (optional beat)

If the demo benefits from "here's month one vs month three", make generators take a reference date so the
demo panel can time-jump. Only build this if it serves a demo beat from the brief.
