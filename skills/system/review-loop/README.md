# Review Loop

Gets a human to sign off on a **rendered HTML artifact** — a plan, prototype, maquette, or doc — and blocks
the agent until they do. Serves the committed file over the presentation surface, lets the human annotate it
in-page, and gates the agent on a verdict-coded await. One primitive so any skill that produces a reviewable
artifact composes it by name instead of forking the review machinery.

## When to use

- **Presenting an artifact for sign-off** — serve any HTML with stable element ids and let the human mark it
  up in-page (a sibling skill like backlog/maquette/prototype invokes this by name; a user can ask directly).
- **Blocking on a verdict** — the agent proceeds only on an explicit approve and revises on request-changes.
- **Surviving the issuing turn** — serve launches a detached, health-checked worker with explicit idempotent
  stop; endpoint lifetime does not depend on the launcher, PTY, or watcher.
- **Sweeping the hub** — drop dead entries from the repo-scoped review inbox.

## Shape

- **Artifact-agnostic.** The server serves any HTML carrying stable element ids; the chrome renders the
  artifact's `kind` dynamically. No plan or backlog identity is baked in — `--kind` and `--issue` are
  free-form.
- **Serve-time chrome.** The annotation layer is injected as the file is served; the committed file on disk
  stays byte-pure. Publish, don't fork — extended to the review UI itself.
- **Batch verdicts + hash-bound approval.** Comments batch in the browser and submit as one verdict —
  approve, approve-with-nits, or request-changes. An approval carries the rendered document's content hash;
  the server refuses a stale-hash approval (409), so the human never approves a version they didn't see.
- **Response ledger.** On a revision the agent writes a disposition for every prior annotation
  (changed / kept / orphaned); a revision without a ledger is a contract violation.
- **Durable lifecycle.** Worker PID/port/instance metadata and logs live in the review state directory. Stop
  verifies the authenticated instance before signaling it; registry writes are locked across concurrent servers.
- **Tailnet surface + local /hub fallback.** One stable URL root, private to the human's own devices
  (`tailscale serve`, Funnel off), with a repo-scoped hub listing everything awaiting review. Where no
  surface is recorded, it degrades to local-only.
- **Reconcile by LLM audit, no version stamps.** The approve event (verdict, hash, timestamp) plus the
  ledger are the durable record; there is no `vNN` stamp.

## Layout

`SKILL.md` is the command surface (setup / serve / stop / await / sweep) and points into `reference/`:
`review-loop.md` (the loop contract), `surface-and-hub.md` (surface + hub), `scripts.md` (the CLI),
`watch.md` (the delegated-watch contract — who holds the await, on what model, how it wakes the parent).
`scripts/` holds `review-server.py`, `review-await.py`, and `pages/chrome.{css,js}`. `templates/` ships
`plan-skeleton.html` as one example caller template demonstrating the stable-id contract.
`agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the wording eval;
`evals/test_server_lifecycle.py` exercises detached start, external submit, watcher independence, concurrent
servers, and idempotent stop.

Self-contained at the file level; composes by name. **Sibling dependency: `staffing`, and only for the
watch** — the review machinery is a root primitive; the delegated watch composes `staffing` by name to pick
the watcher's (floor-class) model. Absent staffing the watch degrades to the current model in a subagent.

## Install

`npx skills add <repo-url> --skill review-loop`, then serve a rendered artifact and block on its verdict. On
a fresh repo it needs a `docs/agents/` surface-config playbook (the tailnet root, surface dir, proxy
commands); absent one it degrades to local-only review.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`fd11b35`](https://github.com/asasher/asher-skills/commit/fd11b35).
- **Authority moved:** the human review surface, verdict protocol, server, and annotation chrome moved here.
- **Local changes:** generalized callers, added delegated watching, setup ownership, and detached lifecycle control.
