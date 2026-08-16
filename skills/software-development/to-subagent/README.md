# To Subagent

Dispatch adapter for non-interactive work, synchronous only: a dispatch is a blocking call, parallelism is several blocking calls issued in one turn that run concurrently and return together, and there is no walk-away-and-get-notified variant — so nesting is safe at every depth. Every dispatch opens with the dispatch declaration (model, effort, harness, absolute deadline) as a statement in the transcript, staffs the subagent from the roster via bars-then-cheapest (degrading to the parent's model when no roster is installed), requires a self-contained prompt whose final message is the deliverable, uses the workflow-supplied directory exactly, and never accepts an exit code alone — the promised deliverable must exist and be sane before the result is relayed. Cross-harness workers run as foreground CLI subprocesses with stdin closed, output to a log, and a timeout from the deadline; recovery is pull-based — audit reality, adopt committed work, re-dispatch only the unfinished remainder. Direct invocation creates a worktree only on an explicit isolation request; composing workflows retain worktree policy and cleanup ownership. One call dispatches one subagent; how many a piece of work needs is the caller's decision.

## When to use

- Any skill or session needs work done outside its own context — a lookup, a probe, a verification pass, an implementation — without the user attending it.
- It is the single sanctioned route to `staffing`: other skills dispatch "via `to-subagent`" instead of reading the roster themselves.

## Dependency surface

Composes with the `worktree` sibling (optionally `staffing` and `plain-language`).

## Provenance

No external sources.
