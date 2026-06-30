# {{DEAL_NAME}} — a Fair Deal

A private, agent-mediated negotiation between **{{PARTY_A}}** and **{{PARTY_B}}**, using the Fair Deal Canvas.

## How this works
Each of us runs our own agent. Our agents interview us *privately*, research the objective benchmarks, and
negotiate a fair structure with each other — by taking turns committing to this repo. We don't have to argue
across a table; we just answer our own agent's questions honestly. The filled **canvas is the review surface**
we both look at.

**Whatever the agents agree is a strongly-suggested starting point, not the final deal.** We both review it,
accept it, and then a lawyer formalises it.

## Your part (it's small)
1. Accept the GitHub invite and **clone this repo**.
2. Open it with your agent (Claude, Codex, whatever you use) and run **`fair-deal join`**, then
   **`fair-deal interview`**.
3. Answer your agent's questions honestly — especially your real goals, worries, and the line you won't cross.
   Your private answers live in `private/` on your machine and are **never** shared.
4. When both of us have finished, the agents negotiate automatically. Your agent will only interrupt you to
   ask something or when a decision touches your floor — and even then it'll suggest creative options first.
5. Review the result on the canvas. Accept it, then take `AGREEMENT.md` to a lawyer.

## What's here
- `canvas.html` — open in a browser and **Import `canvas.json`** to see the current deal.
- `canvas.json` — the shared, agreed structure (filled by the agents).
- `negotiation/` — the turn state, the log, and each side's arguments (the deal's audit trail).
- `private/` — **your** scratchpad. Gitignored. Never committed. Each of us has our own.
- `AGREEMENT.md` — appears when the canvas is ready: a plain-English memo for a lawyer.

*Business-structure guidance, not legal advice.*
