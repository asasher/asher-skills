# Feel pass

Run this after the journeys work. The goal is predictable, immediate feedback—not decoration.

## Interaction audit

- Exercise every control rapidly and by keyboard. State changes remain visible, reversible where expected,
  and never depend on animation finishing.
- Frequent actions respond immediately. Use motion only when it explains entry, exit, movement, or state;
  keep it short and interruptible.
- Loading reads as intentional: skeleton or progress for reads, immediate pending/success/failure feedback for
  writes, and no unexplained frozen control.
- Menus originate near their trigger; dialogs remain spatially stable; exiting is quieter than entering.
- Updated numbers do not shift surrounding layout. Icons, labels, nested radii, and spacing align optically.

## Runtime gates

- Motion changes only composited properties where possible and honors `prefers-reduced-motion`.
- Hover-only behavior is unavailable on touch-only input; every hover affordance has a focus/tap equivalent.
- No transition hides a result, steals focus, delays a frequent action, or creates layout shift.
- Re-run the demo journey with slow network simulation and reduced motion. Both remain coherent.

Record each failure as a concrete state/transition pair, fix it, and re-run that pair plus the full journey.
