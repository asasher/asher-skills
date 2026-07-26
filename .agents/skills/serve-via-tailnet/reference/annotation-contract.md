# The annotation contract

The annotate→revise→approve contract. An artifact pausing for a verdict — a plan awaiting approval, a
prototype's answer sheet, a maquette, any reviewed document — is served through `scripts/review-server.py`,
not as a bare file, so the human can talk back. This doc is the contract the scripts implement. The CLI that
drives it is in [scripts](scripts.md); the surface it serves over and the hub are in
[surface-and-hub](surface-and-hub.md).

## Durable serve

The serve command returns only after a detached worker answers its authenticated health check; mechanics and
teardown in [scripts](scripts.md). The watcher only delivers an event after submission; serve and await
are separate processes, so ending an await leaves the server (and any landed verdict) intact.

## Serve-time chrome

The server injects the annotation layer (`scripts/pages/chrome.{css,js}`) into the artifact as it serves it;
the committed file on disk stays byte-pure — publish, don't fork, extended to the review UI itself. The
injection lands the chrome and a `window.__REVIEW_BOOTSTRAP__` blob just before `</body>`.

Annotations anchor to the artifact's **stable element ids**, never to text ranges. The human hovers a block
that carries an `id`, hits "+ comment", and the note binds to that id. Ids must never change across
revisions — that is what lets a round-2 tab still resolve a round-1 note. Any reviewable artifact must give
every reviewable element a stable id — sections and individually-reviewable items carry ids, and
acceptance criteria marked `<li id="ac-N" data-criterion>` are counted by the approval dialog. The
server serves any HTML that follows the convention.

## Batch feedback, three verdicts

Comments accumulate in the browser and submit as **one batch** carrying a verdict:

- **approve** — the artifact is accepted as-is. Requires no annotations; the approve dialog confirms first.
- **approve_with_nits** — accepted, but the agent applies the batched notes without a re-review round.
- **request_changes** — a full revision round; the agent revises and re-serves.

`approve_with_nits` and `request_changes` require at least one annotation with text; `approve` needs none.

## Hash-bound approval

An approval carries the **content hash** of the rendered document. The server recomputes the current hash on
every request and **rejects an approval whose `doc_hash` no longer matches** — HTTP 409 `{"error":"stale"}`
with the current hash, and the chrome banners "the document changed since you loaded it — reload latest" —
so the human can never sign off on a version they did not see. This is the load-bearing safety invariant.

## The verdict-coded await gate

The agent blocks on `scripts/review-await.py --state <dir> --timeout <secs>`. Its **exit code is the
verdict** — branch on it without parsing ([scripts](scripts.md)). The event log (`events.jsonl` in the run's state dir) is durable and **cursor-tracked**
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

## Verdicts outlive watchers

A verdict event is durable the moment it is written; **consuming it never requires a live watcher.** Any
resume — the same session, a later one, or an audited backlog resume — runs `review-await.py` against the
state dir and gets an already-landed verdict back immediately from the cursor; a dead watcher therefore
never loses a verdict, and a verdict landing seconds after its awaiting thread exits is consumed by whoever
resumes next, not re-requested from the human.

Durable state lives in **one canonical place per review**, outside any worktree or session scratch —
pass `--state` a path that survives teardown; this skill's convention is
`~/.backlog/reviews/<repo>/<scope>/state`, where `<scope>` is the issue number or artifact slug. When
the owning workflow keeps a durable run
root of its own, copy `events.jsonl` and `ledger.json` into it
before `--stop` — the raw event stream is part of the run's provenance and must survive review cleanup.

Each feedback event records **client evidence** (remote address, user agent, referer, server start time).
Audit heuristics for a suspect approval: a verdict seconds after server
start, a loopback/CLI client where a human browser is expected, or an approval on a route that was never
published are grounds to void and re-present. These checks are the guard.

## The approve event is the approval record

The approve event — verdict, content hash, timestamp, appended to `events.jsonl` — is the durable approval
record: a stronger provenance artifact than a chat "lgtm." Reconciliation is LLM audit over this event log
and the ledger. A caller that records posterity cites this event.
