# Watch Until

Waits on external state cheaply: a target, a decidable condition, a relay instruction, and a timeout, satisfied by the cheapest mechanism available (the ladder is in SKILL.md). A watch ends triggered, or timed out with the condition unmet.

## When to use

- A session must react to something it doesn't control: a review verdict landing, CI concluding, a file or thread changing.
- A convergence loop needs a wait step ("watch the change request until no new findings").

## Provenance

No external sources.
