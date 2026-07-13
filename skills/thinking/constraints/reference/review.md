# review — score the cards, check for movement, close the loop

Focusing Step 5 as a session. Run on a card's review date (lead with this on `resume` when the dashboard's
review date has passed), after any material change to the system, or on a standing cadence. The deliverables:
scored experiment cards, a has-it-moved verdict, and — when the constraint moved — a closed cycle in **Loop**.

## 1 — score each due card

Fill **Actual** next to **Predicted** and score the *prediction*, not the effort. Ask for the number first,
stories second. Then the pre-committed decision:

- **adopt** — prediction held; the change becomes standing policy (write it into Plan as adopted, checked).
- **adapt** — mechanism looks right, size or shape wrong; revise the card (new prediction, new date), don't
  stack a second change onto it.
- **abandon** — prediction failed and the mechanism story died with it. One-line epitaph on the card,
  `data-state="abandoned"`. Say it plainly: a clean kill that saves a quarter of misdirected effort is a *win*,
  and it's evidence about where the constraint isn't.
- **elevate** — exploit + subordinate ran honestly and the constraint still binds: open the elevate gate in
  Plan, test the option with ΔT vs ΔI+ΔOE, and card the elevation itself (an expensive change needs a
  prediction most of all).
- **re-identify** — results say the diagnosis was wrong (see interpretation traps below). Downgrade the
  verdict's mark, reopen Find, and take the strongest surviving suspect. Not a failure — the experiment did
  its job as the test of the diagnosis.

Interpretation traps ([framework.md](framework.md)): local metric up + throughput flat → wrong target or
failing subordination, not success. Guardrail broken → the "win" is a loss; adapt with the guardrail as a
constraint on the design.

## 2 — has the constraint moved?

Run the movement checks whether or not cards succeeded:

- Does the old constraint now have slack while a **different** stage accumulates the oldest WIP?
- Did the expediting, the waiting, the complaints relocate?
- Does extra capacity at the old constraint no longer raise throughput?
- Did the mix change (new offer, new season, new team shape) enough to re-deal the cards?

**Not moved** → the cycle continues: back to `plan` for the next exploit/subordinate move, or open the elevate
gate if the free moves are exhausted.

**Moved** → celebrate for one sentence, then close the cycle:

1. Prepend a `.cycle` entry to **Loop**: the constraint that was, cycle dates, what broke it (which cards),
   what the throughput metric did, and where the constraint went.
2. **Inertia sweep** — the step everyone skips, so never skip it: walk every subordination rule, buffer,
   priority policy, and metric adopted this cycle and ask *"does this still serve the new constraint?"*
   Retire what doesn't, in Plan and in the cycle entry. Yesterday's protective rule is today's policy
   constraint; unretired leftovers go on next cycle's suspects board first.
3. Reset for the new cycle: increment the dashboard cycle counter; set Find `active` (Plan and Experiments
   revert to `active` as they're reworked — adopted-and-still-serving policies stay listed as standing).
   The Goal and Map survive; re-annotate the map's queue counts and move the `:::constraint` tag when the new
   verdict lands. Then run [find.md](find.md) — with the map warm, second hunts are fast.

## 3 — close the session

As always: update statuses, dashboard, `Updated`, and the log entry — and end with one concrete next action
bearing a date (next measurement, next review, or the first hunt question of the new cycle). If the system has
plainly outgrown the page's boundary (the value stream split, the goal changed), say so and propose a fresh
`new` rather than stretching this page over two systems.
