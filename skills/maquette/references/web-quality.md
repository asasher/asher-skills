# Web quality

<!-- Distilled from vercel-labs web-design-guidelines / react-best-practices / composition-patterns,
     filtered to what matters in a client-side maquette. -->

A maquette gets poked at by curious buyers — tab through it, resize it, click a link into it. Quality here
is part of the illusion, and it transfers straight into the real build.

## Semantics and accessibility

- Actions are `<button>`, navigation is `<a>`/`<Link>`. Icon-only buttons get `aria-label`; decorative
  icons get `aria-hidden`.
- Focus is always visible via `focus-visible`; never `outline-none` without a replacement. Tab through
  every demo journey once — presenters use keyboards.
- Async status regions use `aria-live="polite"`.

## Forms

- Every input: clickable label, correct `type`/`inputmode`/`autocomplete`, no paste blocking.
- Inline validation errors next to the field; focus the first error on submit.
- Warn on unsaved changes only where the journey makes losing work plausible.

## State and URLs

- **URL-backed state for filters, tabs, pagination, and selected records.** Deep links are demo
  infrastructure: the presenter can jump to any prepared screen instantly, and the demo script references
  URLs. This also survives an accidental refresh mid-meeting.
- Hydration guards for anything time-relative (fixture dates!): render timestamps after mount or format
  them deterministically, or the console fills with hydration errors during the demo.
- `Intl.NumberFormat`/`Intl.DateTimeFormat` for all numbers/dates/currency — locale-correct data reads
  as production.

## Rendering and performance

- Explicit dimensions on images; lazy-load below the fold.
- Lists of 50+ rows: virtualize or `content-visibility: auto` (fixture volumes will hit this).
- `next/dynamic` for heavy, off-journey components; derive state during render instead of effect-syncing;
  functional `setState`; refs for transient values.
- Explicit ternaries over `&&` in JSX (no stray `0`s in the UI).

## Composition

- Variants over boolean props: `ThreadComposer` / `EditMessageComposer` beats `showX`/`renderX` booleans —
  each boolean doubles the state space and the handoff inherits the mess.
- Compound components with context for anything with shared state across panels (composer + preview +
  dialog actions); providers expose `state`/`actions`, UI consumes the interface.
- React 19: `ref` as a normal prop (no `forwardRef`), `use(context)`.
