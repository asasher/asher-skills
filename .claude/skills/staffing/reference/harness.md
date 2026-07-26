# Claude Code harness mechanics

Harness truth and doctrine — identical on every machine running this harness, so it ships with the skill and
is reviewed with it. What differs per machine (which routes are verified, which aliases work, which models
are eligible) lives in the project's staffing playbook, never here.

## Dispatch

Native Claude work uses watched **Agent/Workflow** children — the harness's two native spawn paths: the
single-child `Agent` tool, and the `Workflow` tool that scripts many children deterministically. Both are
named because both prove the spawned child's model, which the wrapper-staffing rule below relies on.

Claude→Codex work runs only inside a watched Claude wrapper named for the external Codex model and task, such
as `gpt-5.6-sol:inspect-lock`. Staff that relay with the cheapest native Claude model the floor allows,
through the Agent/Workflow `model` parameter, at low effort. The parent owns the prompt, the judgment, and the
effect verification; the wrapper only supervises the bounded process and relays its raw output and lifecycle
status — it is **never repurposed to edit or build**. Under an explicit generous timeout it runs, from inside
the target worktree, with closed stdin and worktree isolation when parallel:

```
codex exec --cd <worktree> --sandbox <envelope> '<self-contained prompt>' </dev/null
```

The permission envelope comes from the playbook's recorded machine policy — the dispatch command grants it,
never the prompt text. **Never use `claude -p` from Claude Code**: the native Agent tool is the Claude-side
route, and `claude -p` is the shape a *Codex* parent uses to reach Claude.

A roster name is not a CLI alias. Where a model name crosses into an executable argument, use the mapping the
playbook records from its alias probe; a versioned roster name written straight into a command produces a
route that resolves cleanly and fails at the moment of use.

The native child request or returned metadata must prove the wrapper model. Where native spawn cannot accept
the resolved wrapper model or report the assigned one, keep agent-tree observability but record the staffing
gap and do not claim floor/cost compliance.

## Wake paths

**Native wake paths are the default — do not poll where the harness tracks.** Tracked background tasks,
subagent completions, and Monitor conditions re-invoke the session, so a Claude-led run satisfies the liveness
contract natively and must not adopt bounded-polling machinery built for harnesses without wakeups.

Only genuinely untracked waits — fire-and-forget shells, external CI, review verdicts — need an explicit
owner, deadline, and wake source. Hold those on the top verified row for the harness running the wait; on
Claude Code that is a tracked background process whose verdict-coded exit wakes the session, with no watcher
model at all. A model watcher is the last resort, waits and relays only, and never carries judgment.

## Cross-harness discipline

- **Effect-class probe first.** Before the first substantive dispatch on any cross-harness route, run a
  reversible probe matching the role's effect class: a one-line file write, then reverted, for a builder; a
  read for a reviewer. Exit 0 with the effect denied quarantines the route *directionally* and reroutes
  immediately — never spend a full worker turn discovering a permission wall. A text-only echo probe verifies
  nothing about effects.
- **Session identity.** Capture the Codex session id at launch and resume by id, never `resume --last` —
  parallel wrappers collide on it and can silently resume a sibling's session.
- **Telemetry.** Record the spawned model, effort, role, route, and session id wherever the dispatching
  run keeps its state — a run log, the ticket thread, whatever the caller already writes to —
  and assert model and effort against the staffed role before dispatch. A mismatch is a dispatch blocker, not
  a note.

## Providers

Claude Code has no native ChatGPT-in-Chrome, Computer Use, or image-generation provider. Name any machine
fallback or dispatched Codex provider explicitly, and never attribute its effect to Claude. Which provider
serves which need on this machine is the playbook's to record.
