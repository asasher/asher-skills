# Watch Until

Waits on external state for cheap: a target, a condition the watcher can decide (mechanical or a
judgment), a relay instruction, and a timeout, satisfied by the cheapest mechanism available —
harness-tracked wake first, native watch facilities second, a watcher subagent third, self-polling last.
A watch ends with one of two reports: triggered, or timed out with the condition unmet.

## When to use

- A session must react to something it doesn't control: a review verdict landing, CI concluding, a file
  or thread changing.
- A convergence loop needs a wait step ("watch the change request until no new findings").

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (optional, by name):** `to-subagent` — dispatches the watcher when one is needed; absent it,
  the session polls at the target's own cadence.

## Provenance

No external sources.
