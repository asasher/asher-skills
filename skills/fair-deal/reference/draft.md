# draft — generate the Agreement Memo

Run only when `phase == "ready"` (or `accepted`) and both humans have reviewed the converged canvas. Produces
`AGREEMENT.md` — a plain-English deal memo both partners can read and agree, then hand to a lawyer. Business
terms only; **not legal advice**.

## Preconditions
- `state.json.phase` is `ready` or `accepted`, and ideally `accepted.A` and `accepted.B` are both true. If a
  human hasn't accepted yet, present the canvas for review first and capture acceptance (turn-protocol commit
  setting `accepted.<me> = true`).

## Steps
1. Read `canvas.json` (the agreed source of truth).
2. Write `AGREEMENT.md` from it, section by section, each stating a **mechanism neutrally** (the order of
   payments, how a price is set, who holds what) — not anyone's motive. Use this skeleton:
   1. **Parties & purpose** — who's in, the vehicle, what the deal is for.
   2. **The business** — customer, offer & price, channel, edge; how customers are reached (and **who owns
      the channel**); and how the venture is funded (whose money — self/customer-funded, or raised as debt or
      equity — and who provides it).
   3. **Contributions & durability** — each side's inputs, tagged and valued at market; reward weighted to
      lasting value.
   4. **How money flows** — the waterfall: costs → tax → market-rate pay → remaining profit split.
   5. **The split & vesting** — pegged to objective standards; vehicle; how a share vests.
   6. **Decisions & reserved matters** — one accountable owner per area; what needs both signatures.
   7. **What each owns** — background (licensed in) vs foreground (venture-owned, licensed back); customers,
      brand, data.
   8. **How it can end or change** — valuation method, leaver terms, deadlock ladder, exit split, any
      restriction (narrow, time-boxed, paid).
   9. **Goals & alignment** — each side's goal; that the deal beats each side's alternative.
   10. **Risks watched** — from the premortem.
   11. **Confidentiality & legal step** — business terms only; convert to formal documents before relying on it.
   Where the canvas leaves something open or *Pilot first*, write `[ ]` or note the pilot test plainly — don't
   invent terms.
3. Commit per the turn protocol (`fair-deal: draft <me> — agreement memo generated`).
4. Tell both humans: review `AGREEMENT.md` together, then take it to a lawyer to formalise for the
   jurisdiction. Reiterate this is the agreed business shape, not a binding contract.

## Guardrails
- Never pull anything from `private/` into the memo. It is built only from the shared `canvas.json`.
- Keep it neutral and plain — both partners should be able to read it without a lawyer in the room.
