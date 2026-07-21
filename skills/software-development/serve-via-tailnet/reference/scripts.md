# The bundled scripts

The CLI surface of `scripts/review-server.py` and `scripts/review-await.py`. Both are stdlib-only Python 3
and are part of serve-via-tailnet's bundled-reference contract — a caller invokes them from this doc without
reading the source. The loop they implement is in [annotation-contract](annotation-contract.md); the surface and hub are in
[surface-and-hub](surface-and-hub.md).

## `review-server.py`

Starts one detached worker and exits with the review metadata as JSON. The worker serves chrome, writes feedback to `<state>/events.jsonl`, binds approvals
to the document hash, and maintains the hub independently of the issuing exec session and verdict watcher.

| flag | default | meaning |
|---|---|---|
| `--doc` | — | HTML document under review. Required unless `--sweep`. |
| `--title` | — | title shown in the chrome and the hub row. Required unless `--sweep`. |
| `--issue` | `?` | free-form scope tag — issue, ticket, or any grouping key. Forms the registry entry id (`<issue>-<doc-stem>`) and the hub row's `#` field. |
| `--kind` | `plan` | free-form artifact kind label (plan / prototype / maquette / doc / …); rendered dynamically by the chrome. A non-plan/prototype value is **not** rejected. |
| `--state` | `state` | durable review dir: events/ledger/cursor plus `server.json` and `server.log`. |
| `--surface` | `surface` | repo-scoped surface dir holding `registry.json` and the generated `index.html` (the hub). |
| `--port` | `0` | loopback port; `0` picks a free one (read the printed `port`). |
| `--token` | random | access token; auto-generated (`token_urlsafe(16)`) if omitted. |
| `--public-url` | local URL | the URL base the human opens (e.g. the tailnet path proxy to this port); the token is appended. Defaults to the local loopback URL. |
| `--hub-url` | this server's `/hub` | hub URL used in the chrome and the pause message. Defaults to this server's local `/hub` fallback. |
| `--surface-label` | `""` (none) | optional suffix shown in the hub heading, e.g. a repo name. |
| `--idle-timeout` | `0` | seconds of inactivity before the server exits; `0` = never. |
| `--sweep` | off | probe registry entries, drop the dead, regenerate the index, exit. |
| `--stop` | off | verify and stop the worker recorded by `--state`; idempotent. |
| `--foreground` | off | diagnostic mode: serve in the invoking process instead of detaching. |

**Startup output** (one JSON line on stdout, flushed):

```json
{"url":"...","local_url":"http://127.0.0.1:<port>/?token=...","hub":"...","port":<port>,"token":"...","pid":<pid>,"instance_id":"...","state":"...","log":"..."}
```

Serve returns only after `/version` answers with the same `pid` and random `instance_id`. The worker starts in
a new OS session with stdin closed, inherited descriptors closed, and stdout/stderr redirected to
`<state>/server.log`; its atomic, mode-0600 lifecycle record is `<state>/server.json`. A second serve on the
same state returns the verified live record instead of spawning a duplicate. A live but unverifiable record is
a hard failure—never signal a bare PID.

**Stop:** `review-server.py --stop --state <dir>` authenticates `/version` and matches both `pid` and
`instance_id` before signaling. It then removes the lifecycle record and hub row. Missing or already-dead
workers are cleaned as an idempotent success. Different state directories may serve concurrently on one
surface; registry/index updates are serialized by the surface lock.

**Endpoints** (routing is **suffix-tolerant** — each matches on the path *suffix*, so the server works
whether a proxy strips the mount prefix or preserves it):

- `GET /` (or any path ending `/`) — the artifact with chrome injected. Requires the token
  (`X-Review-Token` header, `?token=`, or body).
- `GET …/version` — current document `hash` plus worker `pid` and `instance_id`; the chrome polls the hash and
  lifecycle commands verify the identity. Requires the token.
- `POST …/event` — submit a batched `feedback_submitted` event `{token, type, verdict, doc_hash,
  annotations[]}`. An approve verdict whose `doc_hash` ≠ the current hash returns **HTTP 409
  `{"error":"stale","current_hash":"…"}`**. A valid submit appends to `events.jsonl` and returns
  `{"id": "evt_…"}`.
- `GET …/hub` — the generated `index.html` (local fallback). **No token required.**

**Sweep mode** — `review-server.py --sweep --surface <dir>` probes each registry entry's URL, drops the
unreachable, regenerates the index, and prints `{"swept":[<dropped ids>],"remaining":[<live ids>]}`.

## `review-await.py`

Blocks until the next `feedback_submitted` event lands in `<state>/events.jsonl`, prints it as JSON, and
exits with a verdict-coded status.

| flag | default | meaning |
|---|---|---|
| `--state` | `state` | the same run-scoped dir the server writes to. |
| `--timeout` | — (required) | seconds to block before giving up. |

**Exit codes:** `0` approve · `3` approve_with_nits · `10` request_changes · `124` timeout. It is
**cursor-tracked** (`state/.await-cursor`), so a verdict submitted while no await was running is picked up
by the next call.

## Typical invocation (serve behind a path prefix, then block)

```sh
# Serve; the launcher returns after the detached worker is healthy.
python3 scripts/review-server.py \
  --doc plan.html --title "Plan #2" --issue 2 --kind plan \
  --state ./run/state --surface ~/.surface/asher-skills --port 0 \
  --public-url https://host.tail.ts.net/asher-skills/2/review
# Proxy the loopback port under the mount prefix (strips /asher-skills/2/review before forwarding):
tailscale serve --bg --set-path /asher-skills/2/review http://localhost:<port>

# Block on the verdict; branch on the exit code.
python3 scripts/review-await.py --state ./run/state --timeout 1800
case $? in
  0)   echo "approved" ;;
  3)   echo "approved with nits — apply them" ;;
  10)  echo "changes requested — revise + write ledger, then re-serve/re-await" ;;
  124) echo "timeout — end the turn with the two links; re-await next turn" ;;
esac

# Explicit teardown; safe to repeat.
python3 scripts/review-server.py --stop --state ./run/state
```
