# The delegated watch

Who holds the wait for a verdict, and how the verdict wakes the parent. The low-level exit-code contract —
what `review-await.py` returns and what each verdict requires next — is in [review-loop](review-loop.md)
§ The verdict-coded await gate; this doc layers the *operational* contract on top: the watch is **not held by
the orchestrator blocking inline**, it is delegated to a dedicated, cheap watcher subagent. The same contract
covers the plan/prototype approval gate and the PR-merge watch.

## Why the orchestrator must not hold it inline

A human review can land in seconds or hours after the machine goes quiet. Parking the orchestrator on that
wait has two failure modes, both observed in practice:

- **A capable model rightly abandons the wait to preserve tokens.** An expensive, context-heavy model parked
  on an indefinite human wait is waste, so it (correctly) drops the watch — and then nothing is actively
  awaiting the round-trip. The verdict is recorded server-side but never reaches the agent.
- **A single timeout drops a long wait.** `review-await.py --timeout` returns `124`, and the harness
  Bash-tool has its own per-call ceiling (~10 min). Either one caps how long a single blocking call can hold,
  forcing premature exit or a re-poll that burns a full agent turn.

The verdict then strands: recorded in `events.jsonl`, but the thread that should resume never sees it, and we
fall back to approving in chat or hand-polling the log. The delegated watch closes that gap.

## Who holds it — a floor-staffed watcher subagent

The caller spawns a **dedicated watcher subagent** whose *only* task is to hold the watch. Because holding it
*is* its whole job, it never abandons the wait to save tokens, and it is cheap enough to park for a long
time without draining the orchestrator's budget or context.

- **The watcher's model is a staffing decision, never hardcoded.** Compose the `staffing` skill by name to
  route a watcher task to the **floor/watcher role** — the cheapest reachable model, no capability gate
  (the watcher only runs `review-await.py` and reports a code). Do **not** bake in a model name: the floor
  differs by harness. From **Claude Code** it resolves to the roster floor (`sonnet-5` on this repo — never
  Haiku); from a **Codex-driven** run, where Claude models are unreachable, it collapses onto `gpt-5.5`. If
  the floor is unreachable, staffing's fallback ladder steps to the next reachable model, and if none is
  reachable the watch runs on the current model in a subagent — never skip the watch.
- **Separation is by thread, not by model.** Even if the same model would nominally orchestrate and watch,
  delegating the watch into its own thread is what keeps the orchestrator free — not parked, not burning
  context on a wait.

## Loop-until-verdict — why no timeout can drop the wait

The watcher **loops-until-verdict** rather than relying on one long single-timeout:

1. Run `review-await.py --state <dir> --timeout <T>` with `T` set safely under the Bash-tool ceiling.
2. On exit **`124`** (no verdict yet) → **re-arm**: invoke it again. A timeout is *keep waiting*, never
   *give up*.
3. On exit **`0` / `3` / `10`** (a real verdict) → stop and report it to the parent.

Re-arm is **lossless** because `review-await.py` is cursor-tracked (`state/.await-cursor`): a verdict
submitted while no await was blocking is drained by the next call. So a verdict that lands *between* two
blocks — or while the watcher is spending a turn to re-invoke — is not missed. This defangs **both** ceilings
at once: the `--timeout` exit and the harness Bash-tool ceiling are just re-arm boundaries, not the end of
the watch, so an arbitrarily long AFK review survives. **No change to `review-await.py` is needed** — the
existing cursor already makes cross-turn re-arming safe; the loop lives in the watcher's contract, not the
script.

## The wake — completion carries the verdict, no polling

When the watcher gets a real verdict it **returns it as its final message**. The subagent's completion is the
wake signal: the Agent-tool result carries the verdict (and its code) back to the parent, which resumes the
gate — proceed on `approve`/`approve_with_nits`, revise on `request_changes`. **The parent never polls
`events.jsonl` itself.** This is the property the approval-delivery hardening turns on: an in-page `approve` /
`approve_with_nits` / `request_changes` reliably wakes the waiting thread without manual log-watching, and it
holds through a path-prefixed mount (the real deployment shape — see [surface-and-hub](surface-and-hub.md)
§ Path-prefix mounts), where the verdict POST reaches the server and fires the verdict-coded await regardless
of whether the proxy strips or preserves the prefix.

`events.jsonl` + `.await-cursor` remain the **durable backstop**, not the primary path. If the watcher dies
before waking the parent, nothing is lost: the verdict is already appended to the log, and a fresh watcher
re-drains it from the cursor. The event log is the crash-safe record; the watcher's completion is the live
wake.

## Both gates

The same delegated watch covers every place a thread pauses for an out-of-band signal:

- **The plan/prototype approval gate** — the watcher holds `review-await.py` for the served artifact and
  wakes the parent on the verdict.
- **The PR-merge watch** — the watcher holds the merge poll (the `ScheduleWakeup` / `Monitor` loop named in
  the platform binding) and wakes the parent when the PR merges. Same shape: a floor-staffed subagent
  loops-until-signal and wakes the parent on completion, so the orchestrator is not parked on the merge wait.

In both cases the rule is identical: don't park the orchestrator, delegate the hold to a cheap
staffing-resolved watcher, loop-until-signal, and wake the parent on completion.
