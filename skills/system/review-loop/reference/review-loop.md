# The review loop

The annotate→revise→approve contract. An artifact pausing for a verdict — a plan awaiting approval, a
prototype's answer sheet, a maquette, any reviewed document — is served through `scripts/review-server.py`,
not as a bare file, so the human can talk back. The scripts implement this contract; this doc *is* the
contract. The CLI that drives it is in [scripts](scripts.md); the surface it serves over and the hub are in
[surface-and-hub](surface-and-hub.md).

## Durable serve

The public serve command returns only after a detached worker answers its authenticated health check. Its OS
session, closed inherited descriptors, state-scoped log, and atomic PID/port/instance record make the endpoint
independent of the issuing exec session, PTY, agent turn, and watcher. Teardown is explicit and idempotent:
`--stop --state <dir>` verifies the live instance before signaling and removes its hub row. The watcher only
delivers an event after submission; it never owns the server that must receive that event.

## Serve-time chrome

The server injects the annotation layer (`scripts/pages/chrome.{css,js}`) into the artifact as it serves it;
the committed file on disk stays byte-pure — publish, don't fork, extended to the review UI itself. The
injection lands the chrome and a `window.__REVIEW_BOOTSTRAP__` blob just before `</body>`.

Annotations anchor to the artifact's **stable element ids**, never to text ranges. The human hovers a block
that carries an `id`, hits "+ comment", and the note binds to that id. Ids must never change across
revisions — that is what lets a round-2 tab still resolve a round-1 note. Any reviewable artifact must give
every reviewable element a stable id; the plan skeleton under `templates/` is one example of that
convention (sections and items carry ids; acceptance criteria are `<li id="ac-N" data-criterion>`, which the
approval dialog counts), but the server serves any HTML that follows it, not only plans.

## Batch feedback, three verdicts

Comments accumulate in the browser and submit as **one batch** carrying a verdict:

- **approve** — the artifact is accepted as-is. Requires no annotations; the approve dialog confirms first.
- **approve_with_nits** — accepted, but the agent applies the batched notes without a re-review round.
- **request_changes** — a full revision round; the agent revises and re-serves.

`approve_with_nits` and `request_changes` require at least one annotation with text; `approve` needs none.

## Hash-bound approval

An approval carries the **content hash** of the rendered document. The server recomputes the current hash on
every request and **rejects an approval whose `doc_hash` no longer matches** — HTTP 409 `{"error":"stale"}`
with the current hash, and the chrome banners "the document changed since you loaded it — reload latest."
Editing the artifact after a page load invalidates any prior-hash approval, so the human can never sign off
on a version they did not see. This is the load-bearing safety invariant.

## The verdict-coded await gate

The agent blocks on `scripts/review-await.py --state <dir> --timeout <secs>`. Its **exit code is the
verdict**: `0` approve, `3` approve_with_nits, `10` request_changes, `124` timeout — branch on it without
parsing. The event log (`events.jsonl` in the run's state dir) is durable and **cursor-tracked**
(`state/.await-cursor`), so feedback submitted while no agent was listening is drained by the next await. On
timeout, end the turn with the pause message's two links (see [surface-and-hub](surface-and-hub.md)); the
next invocation re-awaits from the cursor.

## The response ledger

On a revision, every prior annotation gets a written **disposition** in the run's `ledger.json` — `changed`
(what changed), `kept` (why it stands), or `orphaned` (the section is gone). The server joins the ledger to
the past feedback rounds and the chrome renders them as resolved threads the next round, so the human can
verify each note was addressed rather than trust it. **A revision without a ledger is a contract
violation.** After a request_changes verdict the required sequence is: revise the artifact → write the
ledger disposition for each note → re-serve → re-await.

## Open tabs follow

The chrome polls the server's version endpoint; when the hash changes it auto-reloads an idle tab and
banners a tab that has unsent comments (drafts are kept). A revision therefore reaches an already-open tab
without the human reloading by hand.

## The approve event is the approval record

The approve event — verdict, content hash, timestamp, appended to `events.jsonl` — is the durable approval
record: a stronger provenance artifact than a chat "lgtm." Reconciliation is LLM audit over this event log
and the ledger; there are no version stamps. A caller that records posterity cites this event.
