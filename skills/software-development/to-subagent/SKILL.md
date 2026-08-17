---
name: to-subagent
description: Dispatch one unit of non-interactive work to a subagent as a blocking call. Use whenever work should run outside this session without the user attending it.
argument-hint: "<the unit of work to dispatch>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [worktree]
  optional: [staffing, writing-for-humans]
---

# To Subagent

Dispatch one unit of non-interactive work to one subagent, block until it returns, validate its deliverable, and relay the result.

## Synchronous only

A dispatch is a blocking call. There is no fire-and-forget variant — completion notifications for background children are lost or misroute past their parent to the root session, so nothing in this skill may depend on a routed wake, a scheduled timer, or a watcher. Parallelism survives intact: fan out by issuing several blocking calls in one turn — they run concurrently and return together. Because no level depends on a routed wake, nesting is safe at every depth: a worker may run this skill for its own sub-units under the same contract.

## The dispatch declaration

Every dispatch opens with a declaration in the transcript, posted before the call goes out:

> Dispatching <work> — model <X>, effort <Y>, harness <Z>, deadline <absolute time>.

It is a statement, never a question: the human can interrupt it, nobody must approve it, and the transcript is the staffing audit trail. The deadline is an absolute time, not a duration, so anyone reading later can see whether it has passed. User-facing text — here and in every relay and report — follows the `writing-for-humans` sibling; absent it, write plainly and say the standard was not loaded.

## Staffing

Resolve the subagent's model and effort through the `staffing` sibling — bars, then cheapest. Absent the roster, run the subagent on this session's own model and effort; never downgrade on a guess.

## The brief

The brief is self-contained — the subagent sees nothing of this conversation. State the goal, the inputs by path or id, what done looks like, the deliverable by name and location, and that its final message is the deliverable itself: the data asked for, not a status note. When the result must be structured, state the exact shape. Before sending, check the brief survived assembly — it ends where you meant it to end — and put the guard in the brief itself: on an evidently truncated or garbled brief, halt and report it rather than work from the fragment.

## Permission envelope

Name the child's envelope — its permission mode — in the dispatch declaration, matched to the role's contract: an advisory or checker role gets a read-only envelope where the harness has one, and a role whose contract requires commands the envelope would block gets the envelope that allows them — a brief demanding what the envelope forbids fails as a staffing error, loudly, at dispatch.

## Directory and isolation

Dispatch in the supplied directory exactly. Worktree policy belongs to the workflow that owns the unit's lifecycle; do not infer a new worktree from the brief's edit intent. A workflow that prepared a worktree passes that path and retains cleanup ownership.

On direct invocation, two branches: an explicit isolation request runs the `worktree` skill before dispatch and passes its returned directory — this parent stays cleanup owner through the child's completion, and the declaration and report record branch, path, and owner. Otherwise run in the supplied checkout and make that directory visible in the report.

## Deliverable validation

Never accept an exit code alone. When the call returns, check that the promised deliverable exists — the file at its stated path, the commits on the branch, the comment on the thread, the structured data in the final message — and that it is sane: non-empty, the stated shape, actually answering the brief. A clean exit that fails this check is a failed dispatch.

## Cross-harness workers

Work sent to another harness runs as a foreground CLI subprocess of this session — the same blocking call by other means. Close its stdin, send its output to a log file, and set the subprocess timeout from the declared deadline. The log exists for observation — a human or the recovery audit reading what happened: success is judged by the returned call plus deliverable validation, never by scraping the log. A worker killed by its timeout surfaces as a failed dispatch that gets the recovery audit below, never a silent retry.

## Relay

Report the outcome (success or failed dispatch), the deliverable's location, and what the next decision must act on — in this session's own words, never a pasted transcript.

## Recovery

Recovery starts when a blocking call returns bad — a failure, a timeout, a missing deliverable. Audit reality first: the worktree's status, the branch tip, partial commits, anything posted to the durable surface — reality outranks the worker's last narrative. Committed work is adopted on its branch, not redone; only the genuinely unfinished remainder is re-dispatched, as a fresh blocking call under a fresh declaration.

A worker lost to its harness — a session or usage limit, a route that stops answering mid-unit — is a route loss, not a defect in the unit of work. The same audit comes first; then the unfinished remainder is restaffed onto the next survivor above the same bars, resolved via the `staffing` sibling where installed. Report the route loss so the route gets re-examined; absent the `staffing` sibling, the loss rides the relay as a reported outcome for the owner to act on.
