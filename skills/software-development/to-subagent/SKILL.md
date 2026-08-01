---
name: to-subagent
description: Dispatch a unit of non-interactive work to a subagent — staffed from the roster, with a wake path. Use whenever work should run outside this session without the user attending it.
argument-hint: "<the unit of work to dispatch>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [worktree]
  optional: [staffing, watch-until]
---

# To Subagent

Dispatch one unit of work to one non-interactive agent and relay its result.

## Staffing

Pick the subagent's model and effort from the project's staffing roster, matched to the kind of work — mechanical, review, orchestration. Absent the roster, run the subagent on this session's own model and effort; never downgrade on a guess.

## The prompt

Self-contained — the subagent sees nothing of this conversation. State the goal, the inputs by path or id, what done looks like, and that its final message is the deliverable itself: the data asked for, not a status note. When the result must be structured, state the exact shape. Before sending, check the brief survived assembly — it ends where you meant it to end; and a subagent handed an evidently truncated or garbled brief halts and reports it rather than working from the fragment.

## Permission envelope

Name the child's permission mode with the dispatch, matched to the role's contract: an advisory or checker role gets a read-only mode where the harness has one, and a role whose contract requires commands the envelope would block gets the envelope that allows them — a brief demanding what the sandbox forbids fails as a staffing error, loudly, at dispatch.

## Directory and isolation

Dispatch in the supplied directory exactly. Worktree policy belongs to the workflow that owns the unit's lifecycle; do not infer a new worktree from the brief's edit intent. A workflow that prepared a worktree passes that path and retains cleanup ownership.

On direct invocation, create isolation only when the user explicitly requests it. Use the `worktree` skill before dispatch, then pass its returned directory. This parent remains cleanup owner through the child's completion; the harness child record plus the dispatch report record branch, path, and owner. Report the branch and path with the child. Without an explicit isolation request, run in the supplied checkout and make that directory visible in the dispatch report.

## Wake path

Prefer the harness-tracked child: its completion wakes the dispatcher, so never poll it. Work the harness cannot track (an external process, another harness) follows the roster's wake-path ladder — a watcher on the cheapest model the roster allows, at low effort. With neither, poll at the cadence the work actually changes.

The wake contract is edge-local: a finishing child reports to its direct parent, never an ancestor. A worker's own workers are legitimate; each parent owns its own parent–child edges, so reliability is arranged per edge, not per depth. Verify at dispatch that the return path resolves — that this child's completion will actually reach this session. An unverifiable return path is a dispatch-time decision, never dispatch-and-hope: take blocking transport for that edge, or deliberately arrange the ledger-and-watch fallback below. Blocking transport — holding this session in the foreground until the child returns — is a per-edge option suited to short bounded workers, never a mandate.

## Ledger and bounded watch

A parent dispatching in the background records its live children — which units are out, where, due to deliver what — and pairs the wait with a bounded watch on the durable surface (the change-request thread or equivalent), so a lost wake degrades to a poll this parent owns. Nothing escalates upward by default: each level orchestrates its own children. Run the watch via the `watch-until` sibling — target the durable surface, condition on the child's result landing, a timeout at the unit's expected span, relay on trigger; absent that sibling, this parent polls the durable surface itself, bounded, at the cadence the work changes. The never-poll rule covers the tracked child, not the surface — the bounded watch is what catches the wake that never comes.

Every background brief tells the worker to post results to the durable surface as they land, not only in its final message; that posting is what keeps the poll always possible. A wake that never arrives while the poll finds the result posted is a delivered unit, not a route loss; a child the surface shows silent past its bound gets the Recovery audit before anything is re-dispatched.

## Relay

Report the result in this session's own words at the altitude the next decision needs — never a pasted transcript. A subagent that died or came back empty is a reported outcome, not a silent gap.

## Recovery

Before resuming or replacing a dead child, audit what actually happened: the worktree's status, the branch tip, any partial commits — reality outranks the last narrative. Committed work is adopted on its branch, not redone; only the genuinely unfinished part is re-dispatched.

A worker lost to its harness — a session or usage limit, a route that stops answering mid-unit — is a route loss, not a defect in the unit of work. The same audit comes first; then the genuinely unfinished remainder is restaffed onto the roster's succession fallback — resolved via the `staffing` sibling where installed — never the whole unit re-run. Report the route loss so the roster's reachability row for that route gets re-examined; absent the `staffing` sibling, the loss rides the relay as a reported outcome for the owner to act on.

## Dependency surface

- **Sibling (required, by name):** `worktree` — explicit direct isolation; prepared workflow directories are accepted as supplied.
- **Sibling (optional, by name):** `staffing` — model, effort, and wake-path resolution; succession and route-loss records on worker death.
- **Sibling (optional, by name):** `watch-until` — the bounded watch on the durable surface behind a background wait; absent it, this parent polls the durable surface itself, bounded, at the cadence the work changes.
