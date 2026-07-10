---
name: review-loop
description: Present a rendered HTML artifact — a plan, prototype, maquette, or doc — to a human for sign-off, and block until a verdict. Use to serve an artifact for review, await the verdict, or sweep dead hub entries — directly or from a sibling skill that needs a sign-off gate. Not for writing the artifact.
argument-hint: "[serve <artifact.html> | await | sweep]"
user-invocable: true
---

# Review Loop

Review-loop owns one capability: get a human to sign off on a **rendered HTML artifact**, and block the
agent until they do. It serves the committed file — a plan, a prototype's answer sheet, a maquette, any doc
with stable element ids — over the repo's presentation surface, injects an annotation layer as it serves,
and lets the human mark the page up and submit one batched verdict. The agent proceeds only on an explicit
approve and revises on request-changes. It is an operator primitive, not advice: it starts a server, holds a
public URL, and writes an event log and a hub.

The machinery is **artifact-agnostic.** The server serves any HTML that carries stable element ids; the
annotation chrome renders the artifact's `kind` dynamically. Nothing about a plan, a backlog issue, or any
one caller is baked in — callers pass a free-form `--kind` and `--issue` scope tag.

## Command surface

- **serve** — publish an artifact for review with `scripts/review-server.py`: it serves the committed file
  with chrome injected, registers in the hub, and prints its URL/hub/port/token as JSON. Point the human at
  the URL. Exact flags and defaults are in [scripts](reference/scripts.md); the loop it drives is in
  [review-loop](reference/review-loop.md).
- **await** — get the verdict from `scripts/review-await.py --state <dir> --timeout <secs>`. Exit code
  *is* the verdict: `0` approve, `3` approve-with-nits, `10` request-changes, `124` timeout. Branch on it.
  **Do not block the orchestrator on this inline.** Hold the watch on a **dedicated watcher subagent** that
  loops-until-verdict — its whole job is the wait, so it neither abandons it to save tokens nor drops it to a
  timeout ceiling. The watcher is **staffed at the roster Floor** — the cheapest class staffing names, read
  directly (*not* a generic capability-ranked `route`, which would return the most capable model) — and its
  completion wakes the parent with the verdict; no `events.jsonl` polling. The full contract, including the
  PR-merge watch, is in [watch](reference/watch.md).
- **sweep** — `scripts/review-server.py --sweep --surface <dir>` probes every hub entry, drops the dead,
  regenerates the index, and prints `{"swept":[…]}`. Run by a repo's setup health check.

Invoked with no argument on a rendered artifact, run `serve` then `await`.

## How the loop works

Detail is in [review-loop](reference/review-loop.md) and [surface-and-hub](reference/surface-and-hub.md);
the shape:

- **Serve-time chrome.** The server injects the annotation layer as it serves; the committed file on disk
  stays byte-pure. Annotations anchor to the artifact's stable element ids, never to text ranges.
- **Batch verdicts.** Comments accumulate in the browser and submit as one batch carrying one of three
  verdicts — approve, approve-with-nits, request-changes.
- **Hash-bound approval.** An approval carries the content hash of the rendered document; the server
  refuses an approval of a version the human didn't see (stale hash → HTTP 409, reload).
- **Response ledger.** On a revision the agent writes a disposition for every prior annotation
  (changed / kept / orphaned); the chrome renders them as resolved threads. A revision without a ledger is
  a contract violation.
- **Hub.** A repo-scoped static inbox of everything awaiting the human, derived from a registry the server
  registers into on start and drops out of on clean exit.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory: [review-loop](reference/review-loop.md)
  (the annotate→revise→approve loop), [surface-and-hub](reference/surface-and-hub.md) (one-surface-one-root,
  publish-don't-fork, local fallback, the hub), and [scripts](reference/scripts.md) (the CLI). The authority
  is these plus the scripts themselves — `scripts/review-server.py`, `scripts/review-await.py`, and
  `scripts/pages/chrome.{css,js}`. They import no other skill's files.
- **Project playbooks** — the repo-specific **surface config** installed under `docs/agents/`: the tailnet
  root URL, the surface directory, the publish/proxy commands, and the keep-awake choice. On this repo it
  resolves to the existing `docs/agents/environment.md` § Presenting to the human. A fresh install needs
  such a surface-config playbook; absent one, review-loop degrades to a local-only fallback (open the file
  on the machine, say remote review is unavailable) rather than improvising a public tunnel.
- **Sibling skills** — **`staffing` (by name), and only for the watch.** The serve/annotate/hash-bound
  review *machinery* is a root primitive — it imports no other skill's files and is invoked *by* sibling
  skills. The one composition is the **delegated watch** ([watch](reference/watch.md)): it composes
  `staffing` by name to staff the watcher at the roster Floor (see `await` above). Staffing degrades
  gracefully (missing roster → fallback + report), so this is a soft dependency; absent staffing the watch
  still runs on the current model in a subagent.
