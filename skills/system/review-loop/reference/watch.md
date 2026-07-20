# The delegated watch

Who holds the wait for a verdict, and how the verdict wakes the parent. The low-level exit-code contract —
what `review-await.py` returns and what each verdict requires next — is in [review-loop](review-loop.md)
§ The verdict-coded await gate; this doc layers the *operational* contract on top: the watch is **not held by
the orchestrator blocking inline** — it rides the harness's cheapest verified wake path (§ The wake-path
roster). The same contract covers the plan/prototype approval gate and the PR-merge watch.

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

## The wake-path roster — cheapest verified wake first

The watch is a staffing decision with its own roster: the machine staffing module publishes a **Wake paths**
table — per harness, the cheapest wake mechanism the audit verified, and the fallback. Pick the top verified
row:

1. **Harness-tracked wake — no model at all.** Where the harness re-invokes the session when a tracked
   background process exits (background tasks, subagent completions, monitors), the await script is its own
   watcher: launch `review-await.py` as a tracked background task; its verdict-coded exit *is* the wake,
   carrying the code and comments. On `124`, re-arm — the same loop-until-verdict below, zero tokens spent
   waiting.
2. **Floor-staffed watcher subagent** (next section) — where no tracked wake exists or the exit cannot be
   observed.
3. **Degrade** per SKILL.md — the watch on the current model in a subagent; never skip the gate.

## Who holds it — a floor-staffed watcher subagent

Where no harness-tracked wake exists, the caller spawns a **dedicated watcher subagent** whose *only* task is
to hold the watch. Because holding it
*is* its whole job, it never abandons the wait to save tokens, and it is cheap enough to park for a long
time without draining the orchestrator's budget or context.

- **The watcher's model is a staffing decision, never hardcoded — staff it at the roster Floor.** Compose the
  `staffing` skill by name and take the watcher's model from the roster's **Floor** — the cheapest capability
  class staffing names (`roles-and-fallback.md`: the minimum, "nothing staffs below it"). The watch task
  justifies the Floor exactly: it needs no intelligence, taste, or capability above the minimum — it only
  runs `review-await.py` and reports an exit code. **Do not resolve the watcher with a generic
  `staffing route` of the watch task:** a generic route returns the **most capable** reachable model — the
  opposite of a cheap park (why: staffing's `rankings-and-routing.md`). Read the Floor value the roster
  publishes instead. Do **not** bake in a model name: read the Floor from the current harness's
  effect-verified reachability graph. A Codex-driven run may include Claude through sibling harness dispatch
  (`claude -p`, never `--bare`), but a failure removes only that direction and may change the reachable
  Floor. On route loss follow staffing's succession ladder; absent staffing, degrade per SKILL.md. (The
  watcher reads the existing Floor; it does not add a pin or role.)
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
blocks — or while the watcher is spending a turn to re-invoke — is not missed. Both ceilings become re-arm
boundaries, so an arbitrarily long AFK review survives.

## The wake — completion carries the verdict, no polling

When the watcher gets a real verdict it **returns it as its final message**. The subagent's completion is the
wake signal: the Agent-tool result carries the verdict (and its code) back to the parent, which resumes the
gate — proceed on `approve`/`approve_with_nits`, revise on `request_changes`. **The parent never polls
`events.jsonl` itself.**

`events.jsonl` + `.await-cursor` remain the **durable backstop**, not the primary path. If the watcher dies
before waking the parent, nothing is lost: the verdict is already appended to the log, and a fresh watcher
re-drains it from the cursor. The event log is the crash-safe record; the watcher's completion is the live
wake.

## Both gates

The same delegated watch covers every place a thread pauses for an out-of-band signal:

- **The plan/prototype approval gate** — the watcher holds `review-await.py` for the served artifact and
  wakes the parent on the verdict.
- **The PR-merge watch** — the watcher holds the merge poll (named in the owning workflow's platform
  playbook, where one exists) and wakes the parent when the PR merges. The merge watch belongs to the
  owning workflow; it reuses this watch *shape* — loop-until-signal, wake on completion, orchestrator never
  parked — not these scripts.
