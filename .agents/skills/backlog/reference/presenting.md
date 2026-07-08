# Presenting to the Human

Interactive review — a plan awaiting approval, a prototype awaiting driving — reaches the human through the repo's **presentation surface**, chosen by where the human is, not where the agent runs. The surface contract lives in the Presenting section of `docs/agents/environment.md`, written by `backlog setup`. Evidence is not presented here: it is durable proof and follows `docs/agents/evidence.md` into the repo and the PR.

## Contract

- **One surface, one root.** Everything reviewable lives under a single stable URL root — documents as static paths, live prototypes as port proxies, one grammar. The shipped default is a tailnet surface (`tailscale serve`): private to the human's own devices, persistent config, no public exposure — Funnel stays off. Where the platform's tailscale client cannot serve file paths (the sandboxed macOS app), the document half is a small local static server rooted at a surface directory, proxied once — publishing is symlinking the committed file in.
- **The pause is the notification.** Any step that stops for a human ends its message with two links, always both: the surface URL of the thing to review first, the hub URL second — so the review is findable even without the message. The harness's own notification tells the human the thread stopped; the URLs in the message are what they tap. Mirror the direct URL to the issue when the tracker is also a review channel.
- **Publish, don't fork.** A presented document is the committed file, served in place — never a diverging copy.
- **Reap with the worktree.** A worktree's path handlers are removed at its teardown, alongside its stack; an orphaned handler on a tailnet surface is clutter, not exposure — the setup health check also sweeps them.
- **Local fallback.** When no surface is recorded, or the section says local-only, open the rendered file or running app on the machine and say remote review is unavailable — never improvise a public tunnel.
- **The surface is only as awake as the machine.** That is the accepted default — harnesses hold sleep assertions while runs are active, and an awake machine serves. Whether to keep it awake beyond that (long pauses, lid-closed on battery) is the user's setup-time choice, recorded as the environment playbook's keep-awake line.

## Review loop

A document pausing for a verdict — a plan awaiting approval, a prototype's answer sheet — is served through the skill's review server (`scripts/review-server.py`), not as a bare file, so the human can talk back:

- **Serve-time chrome.** The server injects the annotation layer (`scripts/pages/`) into the document as it serves it; the committed file stays pure — publish, don't fork, extended to the review UI itself. Annotations anchor to the document's stable element ids (the plan skeleton's convention), never to text ranges; ids never change across revisions.
- **Batch feedback, three verdicts.** Comments accumulate in the browser and submit as one batch with a verdict: **approve**, **approve with nits** (agent applies them, no re-review), or **request changes** (full revision round). An approval carries the content hash of the rendered document; the server rejects an approval of a version the human didn't see (stale tab → refuse and prompt reload). Approve confirms before sending.
- **The agent blocks on `scripts/review-await.py`.** Exit code is the verdict (0 approve, 3 nits, 10 changes, 124 timeout); the event log (`events.jsonl` in the run's state dir) is durable and cursor-tracked, so feedback submitted while no agent was listening is drained by the next await. On timeout, end the turn with the two links per the pause contract — the next invocation re-awaits.
- **Response ledger.** On a revision, every annotation gets a written disposition in the run's `ledger.json` — `changed` (what changed), `kept` (why), or `orphaned` (the section is gone) — which the chrome renders as resolved threads next round. A revision without a ledger is a contract violation: the human must be able to verify each note was addressed, not trust it.
- **Open tabs follow.** The chrome polls the server's version endpoint; a revision auto-reloads an idle tab and banners one with unsent comments.
- **The approve event is the approval record.** Verdict, content hash, timestamp — a stronger provenance artifact than a chat "lgtm"; the plan step's posterity write cites it.

## Hub

The surface root serves a repo-scoped review inbox — one bookmarkable URL listing everything awaiting the human:

- **A static file, not a daemon.** The hub is `index.html` at the surface directory root, regenerated from `registry.json` beside it. Each review server registers itself on start and removes itself on exit (approval, teardown, idle) — atomic writes, no lifecycle owner, no new port. Whatever already serves the surface serves the hub.
- **Dumb, read-only, derived.** Rows show title, kind, issue, state, and age, linking to the direct URL — nothing more. No hub event log, no approve-from-the-hub (approval binds to a rendered document's hash), no history: the durable record of an approval is the tracker posterity write. Nothing reads the hub but the human; registry loss degrades to an empty index while every direct URL keeps working.
- **Swept, not trusted.** A crashed run leaves an orphaned registry entry — clutter, not exposure. The setup health check runs `review-server.py --sweep`, which probes each entry and drops the dead.
