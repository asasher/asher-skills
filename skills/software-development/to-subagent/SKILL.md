---
name: to-subagent
description: Dispatch a unit of non-interactive work to a subagent — staffed from the roster, run as a blocking call, deliverable validated before acceptance. Use whenever work should run outside this session without the user attending it.
argument-hint: "<the unit of work to dispatch>"
user-invocable: true
metadata:
  invocation: model
  execution: orchestrator
  requires: [worktree]
  optional: [staffing, plain-language]
---

# To Subagent

Dispatch one unit of non-interactive work to one subagent, block until it returns, validate its deliverable, and relay the result.

## Synchronous only

A dispatch is a blocking call: issue it, wait for it to return, judge what came back. There is no walk-away-and-get-notified variant — completion notifications for background children are lost or misroute past their parent to the root session, so nothing in this skill may depend on a routed wake, a scheduled timer, or a watcher. Parallelism survives intact: several blocking calls issued in one turn run concurrently and return together — fan out by issuing them together, never by walking away. Because no level depends on a routed completion message, nesting is safe at every depth: a worker may run this skill for its own sub-units under the same contract.

## The dispatch declaration

Every dispatch opens with a declaration in the transcript, posted before the call goes out:

> Dispatching <work> — model <X>, effort <Y>, harness <Z>, deadline <absolute time>.

It is a statement, never a question: the human can interrupt it, nobody must approve it, and the transcript is the staffing audit trail. The deadline is an absolute time, not a duration, so anyone reading later can see whether it has passed. User-facing text follows the `plain-language` sibling.

## Staffing

Resolve the subagent's model and effort through the `staffing` sibling — bars, then cheapest: filter out the models below the task's quality bars, take the cheapest survivor. Absent the roster, run the subagent on this session's own model and effort; never downgrade on a guess.

## The prompt

Self-contained — the subagent sees nothing of this conversation. State the goal, the inputs by path or id, what done looks like, the deliverable by name and location, and that its final message is the deliverable itself: the data asked for, not a status note. When the result must be structured, state the exact shape. Before sending, check the brief survived assembly — it ends where you meant it to end; and a subagent handed an evidently truncated or garbled brief halts and reports it rather than working from the fragment.

## Permission envelope

Name the child's permission mode with the dispatch, matched to the role's contract: an advisory or checker role gets a read-only mode where the harness has one, and a role whose contract requires commands the envelope would block gets the envelope that allows them — a brief demanding what the sandbox forbids fails as a staffing error, loudly, at dispatch.

## Directory and isolation

Dispatch in the supplied directory exactly. Worktree policy belongs to the workflow that owns the unit's lifecycle; do not infer a new worktree from the brief's edit intent. A workflow that prepared a worktree passes that path and retains cleanup ownership.

On direct invocation, create isolation only when the user explicitly requests it. Use the `worktree` skill before dispatch, then pass its returned directory. This parent remains cleanup owner through the child's completion; the dispatch declaration and report record branch, path, and owner. Without an explicit isolation request, run in the supplied checkout and make that directory visible in the report.

## Deliverable validation

Never accept an exit code alone. When the call returns, check that the promised deliverable exists — the file at its stated path, the commits on the branch, the comment on the thread, the structured data in the final message — and that it is sane: non-empty, the stated shape, actually answering the brief. A clean exit with a missing, empty, or garbled deliverable is a failed dispatch, reported as such — never relayed as success.

## Cross-harness workers

Work sent to another harness runs as a foreground CLI subprocess of this session — the same blocking call by other means. Close its stdin, send its output to a log file, and set the subprocess timeout from the declared deadline. The log exists for observation — a human or the recovery audit reading what happened — never for control flow: success is judged by the returned call plus deliverable validation, not by scraping the log. A worker killed by its timeout surfaces as a stage failure that gets the recovery audit below, never a silent retry.

## Relay

Report the result in this session's own words at the altitude the next decision needs — never a pasted transcript. A subagent that died, timed out, or came back empty is a reported outcome, not a silent gap. User-facing text follows the `plain-language` sibling.

## Recovery

Recovery is pull-based: it starts from state this session reads after a blocking call returns bad — a failure, a timeout, a missing deliverable — never from a wake it was owed. Audit reality first: the worktree's status, the branch tip, partial commits, anything posted to the durable surface — reality outranks the worker's last narrative. Committed work is adopted on its branch, not redone; only the genuinely unfinished remainder is re-dispatched, as a fresh blocking call under a fresh declaration.

A worker lost to its harness — a session or usage limit, a route that stops answering mid-unit — is a route loss, not a defect in the unit of work. The same audit comes first; then the unfinished remainder is restaffed onto the roster's succession fallback, resolved via the `staffing` sibling where installed — never the whole unit re-run. Report the route loss so the roster's reachability row gets re-examined; absent the `staffing` sibling, the loss rides the relay as a reported outcome for the owner to act on.

## Dependency surface

- **Sibling (required, by name):** `worktree` — explicit direct isolation; prepared workflow directories are accepted as supplied.
- **Sibling (optional, by name):** `staffing` — bars-then-cheapest model and effort resolution; succession on route loss. Absent it, the subagent runs on this session's model and effort.
- **Sibling (optional, by name):** `plain-language` — the standard for the declaration, relays, and reports. Absent it, write plainly and say the standard was not loaded.
