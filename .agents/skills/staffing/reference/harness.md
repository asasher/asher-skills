# Codex harness mechanics

Harness truth and doctrine — identical on every machine running this harness, so it ships with the skill and
is reviewed with it. What differs per machine (which routes are verified, which aliases work, which models
are eligible) lives in the project's staffing playbook, never here.

## Dispatch

Native Codex work uses watched native agent threads; no fire-and-forget shells. Thread and depth limits come
from the Codex config, and a thread cap that blocks a real worker is answered by freeing a completed thread,
queueing, or reporting blocked — never by dropping the wrapper.

Codex→Claude work runs only inside a watched Codex wrapper named for the external Claude model and task, such
as `claude-opus:review-auth`. Staff that relay with the cheapest native Codex model the floor allows. The
parent owns the prompt, the judgment, and the effect verification; the wrapper only supervises the bounded
process and relays its raw output and lifecycle status — it is **never repurposed to edit or build**. From
inside the target worktree it runs:

```
claude -p --model <probed-alias> '<self-contained prompt>' </dev/null
```

with the permission envelope the playbook's recorded machine policy grants — in the command itself, never in
the prompt text — and it never adds `--bare`.

**A roster name is not a CLI alias.** Pass only a name the alias probe accepted; the playbook records the
mapping, and where the probes support a rule ("this CLI rejects versioned names, accepts bare names") apply
the rule rather than a memorized pair. Re-probe after any CLI upgrade — an alias set is a property of the
installed version, not of the roster.

If native spawn cannot select or report the wrapper model, the route may remain observable and usable, but
floor/cost compliance is unproven and must be reported red.

## Wake paths

Codex children are bounded and untracked, so there is no native completion wake to lean on. Hold an
out-of-band wait — review verdicts, merge watches — on a watched native subagent loop staffed at the floor,
never on the orchestrator itself. Watchers wait and relay only; they carry no judgment.

Where the sibling harness tracks its own waits, prefer its tracked wake over any watcher model when the wait
is running there.

## Cross-harness discipline

- **Effect-class probe first.** Before the first substantive dispatch on any cross-harness route, run a
  reversible probe matching the role's effect class: a one-line file write, then reverted, for a builder; a
  read for a reviewer. Exit 0 with the effect denied quarantines the route *directionally* — build dead is
  not review dead — and reroutes immediately. A text-only echo probe verifies nothing about effects.
- **Session identity.** Capture the worker's session id at launch and resume by id, never `resume --last` —
  parallel wrappers collide on it.
- **Minimal context.** Spawn children with a self-contained task packet: issue, role, worktree, gate,
  expected return. Never a full-history fork.
- **Telemetry.** Record the spawned model, effort, role, route, and session id wherever the dispatching
  run keeps its state — a run log, the ticket thread, whatever the caller already writes to —
  and assert model and effort against the staffed role before dispatch. A mismatch is a dispatch blocker, not
  a note. Children inherit the picker's current model, so verify the orchestrator's own model against the
  roster before any wave dispatch.

## Providers

ChatGPT-in-Chrome, Computer Use, and native Imagegen are Codex harness and tool providers, not model traits.
Read the selected provider skill fully before use, and record its effect-probed route and fallback in the
playbook before ranking an eligible executor.
