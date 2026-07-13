# monitor — waiting for the other side's turn

During `negotiate`, after you push your move it becomes the *other* side's turn. Their agent may answer in
seconds or not until their human sits down tomorrow. You have to notice when they've moved and take your next
turn — without making your human babysit the loop.

**You pick the monitoring mechanism — whichever fits the situation.** The only hard requirement is that the
**human poke always works as a fallback**: if you've stopped, the human can say *"pull and take your turn"* (or
re-run `fair-deal negotiate`) and you resume from `state.json`. Nothing about your monitoring choice may depend
on staying alive — the repo is the source of truth, so a fresh invocation always recovers the full state.

## How to detect a move
A move from the other side is a new commit that flips `turn` to you. To check without disturbing the tree:

```
git fetch --quiet && git rev-parse @ @{u}    # local vs upstream HEAD; differ ⇒ they pushed
```

If upstream is ahead: `git pull --rebase`, read `state.json`; if `turn == me` and `phase == negotiate`, take
your turn (back to `negotiate.md` step 3). If `turn` is still the other side, they pushed something else
(rare) — keep waiting.

## Choosing a mechanism (simplest that fits)
1. **Stop and wait for a poke (default).** Cleanest and always correct. Tell the human in one line: *"My move
   is in; it's <other>'s turn. I'll resume when you tell me they've replied — just say 'take your turn' or run
   `fair-deal negotiate`."* Then end. Best when the other human isn't actively online.
2. **Bounded in-session poll.** If the other side is expected to reply within minutes and the human wants you
   to stay on it, loop `git fetch` on a sensible interval (e.g. 30–60s) for a bounded window (say up to
   10–15 min), then fall back to option 1 if nothing lands. Say what interval and window you chose. Don't spin
   forever — a session can't stay attended indefinitely.
3. **`loop` skill.** For longer unattended polling, the user can drive `negotiate` on a schedule —
   `/loop 5m fair-deal negotiate`. Each firing pulls, and if it's your turn, you move; if not, it logs and
   waits for the next tick. Suggest this when both sides want hands-off turnaround over hours.
4. **External watcher (advanced, optional).** A cron/launchd job or a git post-merge hook that re-invokes the
   agent on a fetch that flips the turn. More moving parts; only set up if the user explicitly wants a
   fully unattended pipeline, and only with their go-ahead.

Default to option 1 unless the human asks to stay on it; never silently spin. Whatever you pick, state it in a
line so the human knows how the turn will get taken — and that a poke always works.

## Guardrails
- Polling is **read-only** until it's your turn: `fetch`/`pull --rebase` only; never write or commit while
  waiting.
- Always `pull --rebase` and re-read `state.json` at the *moment* you act — never act on a stale read from
  before the wait.
- If a poll surfaces `phase == escalated` or `ready`, stop polling and handle per `negotiate.md`.
