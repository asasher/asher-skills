#!/usr/bin/env python3
"""Review-loop server; stdlib only. Contract: reference/review-loop.md.

Serves ONE review artifact with the annotation
chrome injected at serve time — the committed file stays pure. Collects batched
feedback into <state>/events.jsonl, binds approvals to the document's content
hash (stale approval → 409), and maintains the repo-scoped hub — registry.json
plus a generated static index.html — in the surface directory. Deregisters on
clean exit. The agent side blocks on review-await.py.

The public serve command launches a detached worker and returns only after its
authenticated health endpoint answers. `--stop --state <dir>` stops that exact
worker idempotently. `--foreground` is the diagnostic worker mode.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import html
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

VERDICTS = ("approve", "approve_with_nits", "request_changes")
HERE = Path(__file__).resolve().parent
METADATA = "server.json"
LOG = "server.log"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def atomic_write(path: Path, text: str, *, private: bool = False) -> None:
    tmp = path.with_name(path.name + ".tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(tmp, flags, 0o600 if private else 0o666)
    if private:
        os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    tmp.replace(path)


def atomic_json(path: Path, value: dict, *, private: bool = False) -> None:
    atomic_write(path, json.dumps(value, indent=1, ensure_ascii=False), private=private)
    if private:
        path.chmod(0o600)


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def feedback_events(state: Path) -> list[dict]:
    path = state / "events.jsonl"
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("type") == "feedback_submitted":
            events.append(event)
    return events


def build_threads(state: Path) -> list[dict]:
    """Past feedback rounds joined with the agent's ledger dispositions."""
    ledger = load_json(state / "ledger.json", {"responses": {}})
    responses = ledger.get("responses", {})
    threads = []
    for event in feedback_events(state):
        replies = responses.get(event.get("id"), [])
        annotations = []
        for idx, ann in enumerate(event.get("annotations", [])):
            reply = replies[idx] if idx < len(replies) and isinstance(replies[idx], dict) else {}
            annotations.append({
                "anchor": ann.get("anchor"),
                "label": ann.get("label"),
                "quote": ann.get("quote"),
                "text": ann.get("text"),
                "disposition": reply.get("disposition"),
                "note": reply.get("note"),
            })
        threads.append({
            "id": event.get("id"),
            "verdict": event.get("verdict"),
            "timestamp": event.get("timestamp"),
            "annotations": annotations,
        })
    return threads


def current_round(state: Path) -> int:
    return sum(1 for e in feedback_events(state) if e.get("verdict") == "request_changes") + 1


# --- hub: registry + generated static index ---------------------------------
# The hub is derived state: dumb, read-only, regenerated on every registry
# change. Nothing depends on it; every direct URL works without it.

INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awaiting review</title>
<style>
:root {{ color-scheme: light dark; --fg: #1a1a1e; --muted: #71717a; --bg: #fafafa; --card: #fff; --line: #e4e4e7; --accent: #4f46e5; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fg: #e4e4e7; --muted: #8b8b94; --bg: #121216; --card: #1c1c22; --line: #2c2c34; --accent: #818cf8; }} }}
body {{ margin: 0; padding: 3rem 1.25rem; background: var(--bg); color: var(--fg); font: 16px/1.5 -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 680px; margin: 0 auto; }}
h1 {{ font-size: 1.15rem; margin: 0 0 1.25rem; }}
h1 small {{ color: var(--muted); font-weight: 400; }}
.empty {{ color: var(--muted); padding: 2rem 0; }}
a.row {{ display: block; background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: .8rem 1rem; margin-bottom: .6rem; text-decoration: none; color: inherit; }}
a.row:hover {{ border-color: var(--accent); }}
.title {{ font-weight: 600; }}
.meta {{ color: var(--muted); font-size: .85rem; margin-top: .15rem; }}
.kind {{ display: inline-block; font-size: .72rem; text-transform: uppercase; letter-spacing: .05em; color: var(--accent); border: 1px solid currentColor; border-radius: 99px; padding: 0 .5rem; margin-right: .5rem; }}
footer {{ color: var(--muted); font-size: .8rem; margin-top: 1.5rem; }}
</style>
</head>
<body>
<main>
<h1>Awaiting review{label_suffix}</h1>
{rows}
<footer>Generated {generated} — derived state; every direct link works without this page.</footer>
</main>
</body>
</html>
"""


@contextlib.contextmanager
def registry_lock(surface: Path):
    surface.mkdir(parents=True, exist_ok=True)
    with (surface / ".registry.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def _regen_index(surface: Path, registry: dict) -> None:
    label = registry.get("label", "")
    label_suffix = (" <small>· " + html.escape(label) + "</small>") if label else ""
    entries = sorted(registry.get("entries", {}).values(), key=lambda e: e.get("started_at", ""))
    if entries:
        rows = "\n".join(
            '<a class="row" href="{url}"><div class="title"><span class="kind">{kind}</span>{title}</div>'
            '<div class="meta">#{issue} · {state} · since {started}</div></a>'.format(
                url=html.escape(e.get("url", "#"), quote=True),
                kind=html.escape(str(e.get("kind", "plan"))),
                title=html.escape(str(e.get("title", e.get("id", "untitled")))),
                issue=html.escape(str(e.get("issue", "?"))),
                state=html.escape(str(e.get("state", "awaiting review"))),
                started=html.escape(str(e.get("started_at", ""))[:16].replace("T", " ")),
            )
            for e in entries
        )
    else:
        rows = '<div class="empty">Nothing awaiting review.</div>'
    atomic_write(surface / "index.html", INDEX_TEMPLATE.format(rows=rows, generated=html.escape(now_iso()), label_suffix=label_suffix))


def regen_index(surface: Path) -> None:
    with registry_lock(surface):
        _regen_index(surface, load_json(surface / "registry.json", {"entries": {}}))


def update_registry(app: dict, **changes) -> None:
    surface = app["surface"]
    with registry_lock(surface):
        path = surface / "registry.json"
        registry = load_json(path, {"entries": {}})
        registry.setdefault("entries", {})
        registry["label"] = app.get("surface_label") or registry.get("label", "")
        entry = registry["entries"].get(app["entry_id"], {})
        entry.setdefault("started_at", now_iso())
        entry.update({
            "id": app["entry_id"], "title": app["title"], "kind": app["kind"],
            "issue": app["issue"], "url": app["url"], "instance_id": app["instance_id"],
        })
        entry.update(changes)
        registry["entries"][app["entry_id"]] = entry
        atomic_json(path, registry)
        _regen_index(surface, registry)


def remove_registry_entry(surface: Path, entry_id: str, instance_id: str | None = None) -> None:
    with registry_lock(surface):
        path = surface / "registry.json"
        registry = load_json(path, {"entries": {}})
        entry = registry.get("entries", {}).get(entry_id)
        if entry is not None and (instance_id is None or entry.get("instance_id") == instance_id):
            registry["entries"].pop(entry_id)
            atomic_json(path, registry)
        _regen_index(surface, registry)


def remove_registry(app: dict) -> None:
    remove_registry_entry(app["surface"], app["entry_id"], app["instance_id"])


def sweep(surface: Path) -> int:
    """Probe every registry entry; drop the dead; regenerate the index."""
    with registry_lock(surface):
        path = surface / "registry.json"
        registry = load_json(path, {"entries": {}})
        dead = []
        for entry_id, entry in list(registry.get("entries", {}).items()):
            url = entry.get("url", "")
            alive = False
            if url:
                try:
                    urllib.request.urlopen(url, timeout=3)
                    alive = True
                except urllib.error.HTTPError:
                    alive = True  # the server answered, whatever the status
                except (urllib.error.URLError, OSError, ValueError):
                    alive = False
            if not alive:
                dead.append(entry_id)
                registry["entries"].pop(entry_id)
        if dead:
            atomic_json(path, registry)
        _regen_index(surface, registry)
    print(json.dumps({"swept": dead, "remaining": sorted(registry.get("entries", {}))}))
    return 0


# --- request handling --------------------------------------------------------

class ReviewHandler(BaseHTTPRequestHandler):
    server_version = "ReviewLoop/1"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (now_iso(), fmt % args))

    @property
    def app(self):
        return self.server.app

    def _send(self, status: int, body: bytes, content_type: str = "text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: dict):
        self._send(status, json.dumps(payload, separators=(",", ":")).encode(), "application/json")

    def _authorized(self, query: dict, body: dict | None = None) -> bool:
        token = self.headers.get("X-Review-Token") or (body or {}).get("token") or (query.get("token") or [""])[0]
        return secrets.compare_digest(str(token), self.app["token"])

    def check_doc(self) -> str:
        """Recompute the doc hash; on change, flip registry state to revised."""
        current = content_hash(self.app["doc"])
        if current != self.app.get("last_hash"):
            self.app["last_hash"] = current
            events = feedback_events(self.app["state"])
            if events and events[-1].get("verdict") == "request_changes":
                update_registry(self.app, state=f"revised — round {current_round(self.app['state'])} awaiting review", doc_hash=current)
            else:
                update_registry(self.app, doc_hash=current)
        return current

    def do_GET(self):
        self.app["last_activity"] = time.monotonic()
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path.endswith("/hub") or parsed.path == "/hub":
            # Local fallback only — the real hub is surface/index.html served
            # statically at the surface root (reference/surface-and-hub.md § Hub).
            index = self.app["surface"] / "index.html"
            if not index.exists():
                regen_index(self.app["surface"])
            self._send(HTTPStatus.OK, index.read_bytes())
            return
        if not self._authorized(query):
            self._send(HTTPStatus.UNAUTHORIZED, b"<h1>Review server running</h1><p>Token required.</p>")
            return
        if parsed.path == "/" or parsed.path.endswith("/"):
            self.serve_doc()
        elif parsed.path.endswith("/version"):
            self._json(HTTPStatus.OK, {
                "hash": self.check_doc(), "instance_id": self.app["instance_id"], "pid": os.getpid(),
            })
        else:
            self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain; charset=utf-8")

    def serve_doc(self):
        doc_html = self.app["doc"].read_text(encoding="utf-8")
        bootstrap = {
            "token": self.app["token"],
            "docHash": self.check_doc(),
            "title": self.app["title"],
            "issue": self.app["issue"],
            "kind": self.app["kind"],
            "hubUrl": self.app["hub_url"],
            "threads": build_threads(self.app["state"]),
        }
        safe = json.dumps(bootstrap, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
        css = (HERE / "pages" / "chrome.css").read_text(encoding="utf-8")
        js = (HERE / "pages" / "chrome.js").read_text(encoding="utf-8")
        chrome = (
            "\n<style>\n" + css + "\n</style>\n"
            "<script>window.__REVIEW_BOOTSTRAP__ = " + safe + ";</script>\n"
            "<script>\n" + js + "\n</script>\n"
        )
        lower = doc_html.lower()
        cut = lower.rfind("</body>")
        page = doc_html[:cut] + chrome + doc_html[cut:] if cut != -1 else doc_html + chrome
        self._send(HTTPStatus.OK, page.encode("utf-8"))

    def do_POST(self):
        self.app["last_activity"] = time.monotonic()
        parsed = urlparse(self.path)
        if not parsed.path.endswith("/event"):
            self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain; charset=utf-8")
            return
        raw = self.rfile.read(int(self.headers.get("Content-Length", "0") or "0"))
        try:
            body = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid json"})
            return
        if not isinstance(body, dict) or not self._authorized(parse_qs(parsed.query), body):
            self._json(HTTPStatus.FORBIDDEN, {"error": "forbidden"})
            return
        if body.get("type") != "feedback_submitted":
            self._json(HTTPStatus.BAD_REQUEST, {"error": "unrecognized event type"})
            return
        verdict = body.get("verdict")
        if verdict not in VERDICTS:
            self._json(HTTPStatus.BAD_REQUEST, {"error": "unrecognized verdict"})
            return
        annotations = body.get("annotations", [])
        if not isinstance(annotations, list) or not all(isinstance(a, dict) and str(a.get("text", "")).strip() for a in annotations):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "annotations must be a list of {anchor, text}"})
            return
        if verdict != "approve" and not annotations:
            self._json(HTTPStatus.BAD_REQUEST, {"error": verdict + " requires at least one annotation"})
            return
        current = self.check_doc()
        if verdict.startswith("approve") and body.get("doc_hash") != current:
            self._json(HTTPStatus.CONFLICT, {"error": "stale", "current_hash": current})
            return
        event = {
            "id": "evt_" + datetime.now().strftime("%Y%m%d") + "_" + secrets.token_hex(4),
            "timestamp": now_iso(),
            "type": "feedback_submitted",
            "actor": "user",
            "verdict": verdict,
            "doc_hash": body.get("doc_hash"),
            "annotations": [
                {"anchor": a.get("anchor"), "label": a.get("label"), "quote": a.get("quote") or None, "text": str(a.get("text", "")).strip()}
                for a in annotations
            ],
        }
        with (self.app["state"] / "events.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, separators=(",", ":"), ensure_ascii=False) + "\n")
        states = {
            "approve": "approved",
            "approve_with_nits": "approved with nits — agent applying",
            "request_changes": "changes requested — agent revising",
        }
        update_registry(self.app, state=states[verdict], doc_hash=current)
        self._json(HTTPStatus.OK, {"id": event["id"]})


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, ValueError):
        return False


def probe_instance(meta: dict, timeout: float = 0.5) -> bool:
    try:
        url = f"http://127.0.0.1:{int(meta['port'])}/version?token={meta['token']}"
        with urllib.request.urlopen(url, timeout=timeout) as response:
            payload = json.load(response)
        return payload.get("instance_id") == meta.get("instance_id") and payload.get("pid") == meta.get("pid")
    except (KeyError, TypeError, ValueError, urllib.error.URLError, OSError, json.JSONDecodeError):
        return False


def unlink_metadata(path: Path, instance_id: str | None = None) -> None:
    current = load_json(path, {})
    if not instance_id or current.get("instance_id") == instance_id:
        path.unlink(missing_ok=True)


def cleanup_lifecycle(meta_path: Path, meta: dict) -> None:
    if meta.get("surface") and meta.get("entry_id"):
        remove_registry_entry(
            Path(meta["surface"]), str(meta["entry_id"]), meta.get("instance_id")
        )
    unlink_metadata(meta_path, meta.get("instance_id"))


def stop_detached(state: Path) -> int:
    meta_path = state / METADATA
    meta = load_json(meta_path, {})
    if not meta:
        print(json.dumps({"stopped": False, "already_stopped": True}))
        return 0
    pid = int(meta.get("pid", 0))
    if not pid_alive(pid):
        cleanup_lifecycle(meta_path, meta)
        print(json.dumps({"stopped": False, "already_stopped": True, "stale_pid": pid}))
        return 0
    if not probe_instance(meta):
        print(json.dumps({"error": "refusing to stop an unverified process", "pid": pid}), file=sys.stderr)
        return 2
    os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + 5
    while pid_alive(pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    if pid_alive(pid):
        os.kill(pid, signal.SIGKILL)
        for _ in range(20):
            if not pid_alive(pid):
                break
            time.sleep(0.05)
    cleanup_lifecycle(meta_path, meta)
    print(json.dumps({"stopped": True, "pid": pid, "instance_id": meta.get("instance_id")}))
    return 0


def launch_detached(args, state: Path) -> int:
    meta_path = state / METADATA
    existing = load_json(meta_path, {})
    if existing:
        if pid_alive(int(existing.get("pid", 0))) and probe_instance(existing):
            if existing.get("doc") != str(Path(args.doc).resolve()):
                print("state already owns a different live review server", file=sys.stderr)
                return 2
            print(json.dumps(existing))
            return 0
        if pid_alive(int(existing.get("pid", 0))):
            print("state metadata points at a live but unverifiable process; refusing to replace it", file=sys.stderr)
            return 2
        cleanup_lifecycle(meta_path, existing)

    log_path = state / LOG
    command = [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:], "--worker"]
    with log_path.open("a", encoding="utf-8") as log:
        log.write(f"\n{now_iso()} detached start\n")
        log.flush()
        proc = subprocess.Popen(
            command, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            close_fds=True, start_new_session=True,
        )
    deadline = time.monotonic() + 5
    meta = {}
    while time.monotonic() < deadline:
        meta = load_json(meta_path, {})
        if meta.get("pid") == proc.pid and probe_instance(meta):
            print(json.dumps(meta))
            return 0
        if proc.poll() is not None:
            break
        time.sleep(0.05)
    if proc.poll() is None:
        proc.terminate()
    tail = log_path.read_text(encoding="utf-8")[-2000:] if log_path.exists() else ""
    print(f"detached review server failed health check; see {log_path}\n{tail}", file=sys.stderr)
    return 1


def run_server(args, surface: Path, state: Path, managed: bool) -> int:
    doc = Path(args.doc).resolve()
    token = args.token or secrets.token_urlsafe(16)
    instance_id = secrets.token_hex(12)
    server = HTTPServer(("127.0.0.1", args.port), ReviewHandler)
    server.timeout = 0.5
    port = server.server_address[1]
    local_url = f"http://127.0.0.1:{port}/?token={token}"
    base = (args.public_url or "").rstrip("/")
    public_url = f"{base}/?token={token}" if base else local_url
    hub_url = args.hub_url or f"http://127.0.0.1:{port}/hub"
    entry_id = f"{args.issue}-{doc.stem}-{instance_id[:8]}"
    server.app = {
        "doc": doc, "state": state, "surface": surface, "token": token,
        "title": args.title, "issue": args.issue, "kind": args.kind,
        "entry_id": entry_id, "url": public_url, "hub_url": hub_url,
        "surface_label": args.surface_label, "instance_id": instance_id,
        "last_hash": None, "last_activity": time.monotonic(),
    }
    meta = {
        "url": public_url, "local_url": local_url, "hub": hub_url, "port": port,
        "token": token, "pid": os.getpid(), "instance_id": instance_id,
        "state": str(state), "surface": str(surface), "entry_id": entry_id,
        "doc": str(doc), "log": str(state / LOG), "started_at": now_iso(),
    }
    update_registry(server.app, state=f"awaiting review — round {current_round(state)}", doc_hash=content_hash(doc))
    server.app["last_hash"] = content_hash(doc)
    if managed:
        atomic_json(state / METADATA, meta, private=True)
    else:
        print(json.dumps(meta), flush=True)

    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(SystemExit(0)))
    try:
        while True:
            server.handle_request()
            if args.idle_timeout and time.monotonic() - server.app["last_activity"] >= args.idle_timeout:
                break
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        remove_registry(server.app)
        server.server_close()
        if managed:
            unlink_metadata(state / METADATA, instance_id)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", help="HTML document under review")
    parser.add_argument("--title")
    parser.add_argument("--issue", default="?")
    parser.add_argument("--kind", default="plan", help="artifact kind label, e.g. plan/prototype/maquette/doc (free-form)")
    parser.add_argument("--state", default="state", help="review state, lifecycle metadata, and log directory")
    parser.add_argument("--surface", default="surface", help="repo-scoped surface dir: registry.json, index.html")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--token", default=None)
    parser.add_argument("--public-url", default=None, help="URL the human opens (e.g. the tailnet path proxy to this port); token is appended. Default: the local URL")
    parser.add_argument("--hub-url", default=None, help="hub URL for the chrome and the pause message. Default: this server's /hub fallback")
    parser.add_argument("--surface-label", default="", help="optional suffix shown in the hub heading, e.g. a repo name; default none")
    parser.add_argument("--idle-timeout", type=float, default=0, help="seconds; 0 = never")
    parser.add_argument("--sweep", action="store_true", help="probe registry entries, drop the dead, regenerate the index, exit")
    parser.add_argument("--stop", action="store_true", help="idempotently stop the detached worker recorded by --state")
    parser.add_argument("--foreground", action="store_true", help="diagnostic mode: serve in this process")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.stop:
        state = Path(args.state).resolve()
        return stop_detached(state)

    surface = Path(args.surface).resolve()
    surface.mkdir(parents=True, exist_ok=True)
    if args.sweep:
        return sweep(surface)

    state = Path(args.state).resolve()
    state.mkdir(parents=True, exist_ok=True)

    if not args.doc or not args.title:
        print("--doc and --title are required (unless --sweep or --stop)", file=sys.stderr)
        return 2
    doc = Path(args.doc).resolve()
    if not doc.is_file():
        print(f"no such document: {doc}", file=sys.stderr)
        return 2
    if args.worker or args.foreground:
        return run_server(args, surface, state, managed=args.worker)
    return launch_detached(args, state)


if __name__ == "__main__":
    raise SystemExit(main())
