# Feel: the details pass

<!-- Distilled from Emil Kowalski's design-eng skill and Jakub Krehel's "Details That Make Interfaces
     Feel Better". Run this as an explicit pass over working screens (pipeline phase 5). -->

Users don't notice these individually; the aggregate is what reads as "finished product" instead of
"prototype". That aggregate is what you're selling.

## Should it animate at all?

- Actions used **dozens of times a day → no animation or nearly none**; keyboard-initiated actions never
  animate. Frequent = instant.
- Occasional actions → standard animation. Rare/first-run moments → delight is allowed.
- Every animation needs a job: spatial continuity, state indication, feedback, or preventing a jarring
  change. "Looks cool" is not a job.

## Easing and timing

- Enter/exit: `ease-out`. Move/morph on screen: `ease-in-out`. Hover/color: `ease`. Constant motion:
  `linear`. Never `ease-in` for UI.
- Built-in curves are weak; prefer `cubic-bezier(0.23, 1, 0.32, 1)` (strong ease-out),
  `cubic-bezier(0.77, 0, 0.175, 1)` (movement), `cubic-bezier(0.32, 0.72, 0, 1)` (iOS-like drawers).
- Budgets: button press 100–160ms · tooltips/small popovers 125–200ms · dropdowns 150–250ms ·
  modals/drawers 200–500ms · everything else < 300ms.
- Springs only for drag/gesture/"alive" elements; bounce 0.1–0.3 and usually 0 in professional UI.

## Component motion rules

- Pressables scale on `:active`: `scale(0.97)` (range 0.95–0.98) — `scale()` shrinks label and icon
  together, which is the point.
- Never enter from `scale(0)`; start ≥ `scale(0.9)` + opacity.
- Popovers/dropdowns scale from their **trigger** (`--radix-popover-content-transform-origin`); modals stay
  center-origin.
- First tooltip has a delay; once one is open, siblings appear instantly with no animation.
- Icon swaps (copy→check etc.): crossfade with opacity + `scale(0.25→1)` + `blur(4px→0)`, ~300ms, spring
  bounce 0 — never a hard conditional swap.
- Enters: opacity + `translateY(8px)` + blur, staggered ~100ms per chunk (title, description, actions
  individually). **Exits subtler than enters** — e.g. keep position, fade + `blur(4px)` out.
- Use CSS **transitions, not keyframes**, for anything the user can toggle rapidly — transitions retarget
  mid-flight; keyframes make fast users feel the UI fighting them. Test by rapid-toggling every menu.

## Typography and optics

- `antialiased` on `body`; `text-wrap: balance` on headings, `text-wrap: pretty` on body copy.
- `tabular-nums` on **every number that updates or aligns** — counters, prices, timers, table columns.
- Concentric radii: nested rounded corners follow `outer = inner + padding`.
- Optical alignment beats geometric: nudge icon padding (play icons are the classic), prefer fixing the
  svg over per-use margin overrides.

## Depth

- Prefer layered translucent shadow over solid border for lightweight elevation:
  `0 0 0 1px rgb(0 0 0 / .06), 0 1px 2px -1px rgb(0 0 0 / .06), 0 2px 4px 0 rgb(0 0 0 / .04)`
  (hover: .08/.08/.06; include `box-shadow` in the transition).
- User-ish images get an inset outline: `outline: 1px solid rgb(0 0 0 / .1); outline-offset: -1px`
  (white 10% in dark mode).

## Perceived latency (pairs with the api seam)

- Every read shows a skeleton; every mutation gives instant feedback (button spinner/disable, or optimistic
  apply + toast). The 250–550ms simulated latency exists so these states are *seen* — that's what makes the
  network feel real.
- Numbers that change (totals, counts) may animate briefly; don't animate table rows the user re-sorts
  constantly.

## Performance and accessibility

- Animate only `transform` and `opacity`; never layout properties (height, padding, margin). Keep blur
  ≤ 20px (Safari).
- `prefers-reduced-motion`: drop movement, keep gentle opacity/color cues.
- Hover-only effects gated by `@media (hover: hover) and (pointer: fine)`.
- Review animations the next day at 2–5x slowdown in DevTools; check easing, origin, and opacity/transform
  sync.
