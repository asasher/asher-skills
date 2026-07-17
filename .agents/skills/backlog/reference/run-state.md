# Run state

Load this reference when `run` creates a child, waits, resumes, adopts work, reports status, or hands off.
Tracker state remains lifecycle truth; this shared administrative record makes that truth reconstructible.
Use `scripts/run-state.py append|project|verify-owner|handoff`; do not hand-edit streams or projections.

## Shared root

Resolve `git rev-parse --path-format=absolute --git-common-dir`, then use
`<git-common-dir>/backlog/runs/<run-id>/`. Every worktree resolves the same root. A non-git binding must name
an equivalent shared root in `platform.md`; never write run state inside an issue worktree.

Each parent owns one append-only `events/<parent-id>.jsonl` stream. Distinct parents never share a writer.
Append one complete JSON line under an advisory stream lock, flush and fsync it, then atomically regenerate
derived views. Adoption records the prior owner and takes the stream lock before writing.

## Canonical events

Every event carries `run_id`, monotonic per-parent `sequence`, timestamp, parent/child ids, issue and stage,
role/model/route and capacity pool, worktree, checkpoint, expected return, escalation successor, and status.
Spawn records the pre-spawn staffing decision before a child exists — including the **actual model, effort,
and worker session id** (`model`, `effort`, `worker_session`; null session for native children), asserted
against the staffed role before dispatch (a mismatch blocks dispatch). Return records the durable artifact or
the child's final text, not a claim that a message was probably delivered.

Deliberate completion is gated: `run-state.py verify-terminal` refuses a terminal report while `handoff.md`
is missing or any parent's latest status is non-terminal
(`complete | blocked | deferred | returned | interrupted`).

`status.json` and the human board are projections rebuilt from all streams plus tracker roles, refs,
worktrees, review events, and verified processes. A stale or missing board is never canonical.

## Checkpoint and wait

Before any external wait, parked gate, quota pause, or thread exit, write a checkpoint containing current
HEAD, worktree, lifecycle stage, completed/remaining criteria, owned resources, review state/cursor, fixture
leases, cleanup debts, next actor, and `not_before` when applicable. A wait is valid only when its owner and
wakeup/event source are recorded. Do not park a capable model merely to poll.

## Process identity

A PID alone proves nothing. A live owner record binds PID plus process start time, command, worktree, task,
parent, and heartbeat/milestone path. Resume rejects a mismatch, a stale heartbeat, a dead review endpoint,
or an unsupported agent self-report. Transfer and stale-owner adoption are explicit events; only one fixer
may own a worktree at a time.

## Audited resume and handoff

Resume rebuilds state from tracker roles/dependencies, refs and HEADs, worktrees, event streams, review
cursors/endpoints, fixture leases, and verified process identities; it compares the projection with the last
checkpoint before dispatching anything.

At deliberate completion, interruption, or exhaustion, write the tracker handoff table and atomic
`handoff.md` in the shared run root. Include state pointers, learned protocols, environment/resources,
cleanup debts, blocked reasons, `not_before`, and the earliest safe continuation. The next session begins with the same
audited resume; it never asks chat memory to reconstruct the run.
