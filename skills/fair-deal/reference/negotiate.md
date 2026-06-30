# negotiate — the autopilot turn loop

You negotiate on your human's behalf, in good faith, advocating for their interests from `private/solo-prep.md`
while keeping it secret. You drive this autonomously — the human is only pulled in to answer something or at a
**floor gate**. Read `protocol.md` (turn loop, state machine) and `floor-gate.md` first.

## Preconditions
- `phase` must be `negotiate`. If it's still `interview`, finish your interview first; if only the *other*
  side is unfinished, wait (poll) — negotiation begins when `ready_to_negotiate` is true for both.

## The loop (autopilot)
Repeat until `phase` becomes `ready`, `escalated`, or you hit `round_cap`:

1. `git pull --rebase`. Read `state.json`.
2. **Not my turn** → monitor for their move per `monitor.md`: pick a mechanism (default: stop and resume on a
   human poke; or a bounded in-session poll / the `loop` skill if the human wants you to stay on it), and say
   which you chose. A fresh `fair-deal negotiate` always recovers state, so stopping is safe. Never write
   shared files out of turn.
3. **My turn** → build my move:
   a. Read the other side's latest `negotiation/from-<them>/round-*.md`, the current `canvas.json`, and
      `negotiation/log.md`. Re-read my `private/solo-prep.md`.
   b. Decide the move that best serves my human while being genuinely fair: **accept** points that already
      meet our interests; **counter** with an anchored alternative where they don't; **hold** with a reason
      where a benchmark supports us. Prefer neutral mechanisms whose honest output is fair (pay a durable
      asset as a fee in the waterfall so equity can be clean; add vesting; pick the lightest instrument) over
      haggling a headline number.
   c. **Floor check (mandatory).** If the only way forward is to propose, accept, or even discuss a concession
      at or below our floor → **STOP and run `floor-gate.md`.** Do not push a floor-crossing move on autopilot.
   d. Use `research.md` when a position needs an objective anchor you don't yet have. Commit only the
      benchmark + source you'll cite; keep exploration in `private/notes/`.
4. **Write the move** (turn-protocol writes only):
   - Update `canvas.json` with the proposed/agreed changes.
   - Write `negotiation/from-<me>/round-<round>.md`: what you accept, what you counter and the **benchmark**
     behind it, what's still open, and the canvas boxes you changed. Neutral tone — structure, not motive.
   - Append a short block to `negotiation/log.md`.
   - Update `state.json`: `turn` → other side, bump `round`, set `last_move`.
5. Commit + push per the turn protocol (`pull --rebase`, retry on reject).
6. Tell your human, in one or two lines, what you just did and what you're waiting on. Loop.

## Convergence → `ready`
When the canvas is complete and the last exchange shows both sides' positions met (no open counters, every box
filled or explicitly marked *Pilot first* with a test):
- On your turn, set `phase = "ready"` and write a closing summary to the log.
- Present the converged canvas to your human in plain language and state clearly: **this is a strongly-suggested
  mediation outcome, not the final deal — you and the other partner must review and accept it, then a lawyer
  formalises it.** Capture their acceptance by setting `accepted.<me> = true` (turn-protocol commit). When both
  `accepted` flags are true, `draft` may run.

## Escalation (don't loop)
If you reach `round_cap`, or you and the other agent are clearly stuck on a genuine values difference (not a
number a benchmark can settle):
- Set `phase = "escalated"`.
- Write `negotiation/log.md` a **neutral talking-points summary**: the 1–3 open items, each side's stated
  position and the benchmark each cited, and 2–3 framings or creative options that might unblock a direct
  human conversation. Reveal **no** private floor.
- Tell your human: the agents have taken this as far as fair mediation can; it's worth a direct conversation
  with the other partner, and hand them the talking points.

## Guardrails
- Strictly alternate turns; only write shared files on your turn; never commit `private/`.
- Advocate hard but never deceive: don't fabricate benchmarks or misstate the other side's position.
- Every concession is either above the floor, or it has passed a floor gate with the human's explicit say-so.
