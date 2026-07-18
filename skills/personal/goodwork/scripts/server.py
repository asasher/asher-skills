#!/usr/bin/env python3
"""Local Goodwork review server; stdlib only."""

from __future__ import annotations

import argparse
import json
import mimetypes
import secrets
import sys
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ALLOWED_TYPES = {"approval_requested", "rejection_requested", "edit_then_approve_requested", "batch_approval_requested", "stage_change_requested", "test_tap", "comment"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def read_template(name: str) -> str:
    return (Path(__file__).resolve().parent / "pages" / name).read_text(encoding="utf-8")


def inject(template: str, data: dict) -> bytes:
    safe = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    return template.replace("__GOODWORK_BOOTSTRAP__", safe).encode("utf-8")


class GoodworkHandler(BaseHTTPRequestHandler):
    server_version = "GoodworkLocal/2"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (now_iso(), fmt % args))

    @property
    def app(self):
        return self.server.app

    def _send(self, status: int, body: bytes, content_type: str = "text/html; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _token(self, query: dict[str, list[str]] | None = None, body: dict | None = None) -> str:
        query = query or {}
        body = body or {}
        return self.headers.get("X-Goodwork-Token") or body.get("token") or (query.get("token") or [""])[0]

    def _authorized(self, query=None, body=None) -> bool:
        return secrets.compare_digest(str(self._token(query, body)), self.app["token"])

    def do_GET(self):
        self.app["last_activity"] = time.monotonic()
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path == "/":
            if self._authorized(query):
                self.send_response(302)
                self.send_header("Location", "/kanban?token=" + self.app["token"])
                self.send_header("Referrer-Policy", "no-referrer")
                self.end_headers()
                return
            self._send(HTTPStatus.UNAUTHORIZED, b"<h1>Goodwork server running</h1><p>Token required.</p>")
            return
        if not self._authorized(query):
            self._send(HTTPStatus.FORBIDDEN, b"forbidden", "text/plain; charset=utf-8")
            return
        pages = {"/health": ("health", "health.html"), "/approval": ("approval", "approval.html"), "/diff": ("diff", "diff.html"), "/kanban": ("kanban", "kanban.html")}
        if parsed.path in pages:
            page, template = pages[parsed.path]
            self._send(HTTPStatus.OK, inject(read_template(template), self.projection(page, query)))
        elif parsed.path.startswith("/static/"):
            self.serve_static(parsed.path[len("/static/") :])
        else:
            self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain; charset=utf-8")

    def do_POST(self):
        self.app["last_activity"] = time.monotonic()
        parsed = urlparse(self.path)
        if parsed.path != "/event":
            self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain; charset=utf-8")
            return
        body = self.read_body()
        if not self._authorized(parse_qs(parsed.query), body):
            self._send(HTTPStatus.FORBIDDEN, b"forbidden", "text/plain; charset=utf-8")
            return
        try:
            event = self.make_event(body)
        except ValueError as exc:
            self._send(HTTPStatus.BAD_REQUEST, str(exc).encode(), "text/plain; charset=utf-8")
            return
        events_path = self.app["workspace"] / "events.jsonl"
        with events_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, separators=(",", ":"), ensure_ascii=False) + "\n")
        self._send(HTTPStatus.OK, json.dumps({"id": event["id"]}).encode(), "application/json")

    def read_body(self) -> dict:
        raw = self.rfile.read(int(self.headers.get("Content-Length", "0") or "0"))
        if not raw:
            return {}
        ctype = self.headers.get("Content-Type", "")
        if "application/json" in ctype:
            value = json.loads(raw.decode("utf-8"))
            return value.get("event", value) if isinstance(value, dict) else {}
        form = parse_qs(raw.decode("utf-8"))
        return {key: values[-1] for key, values in form.items()}

    def make_event(self, body: dict) -> dict:
        event_type = str(body.get("type") or body.get("event_type") or "test_tap")
        if event_type not in ALLOWED_TYPES:
            raise ValueError("unrecognized event type")
        covers = body.get("covers", [])
        if isinstance(covers, str) and covers:
            covers = json.loads(covers)
        if not isinstance(covers, list):
            raise ValueError("covers must be a list")
        payload = body.get("payload", {})
        if isinstance(payload, str) and payload:
            payload = json.loads(payload)
        if not isinstance(payload, dict):
            payload = {}
        tags = body.get("tags", [])
        if isinstance(tags, str):
            tags = [tag for tag in tags.split(",") if tag]
        suffix = secrets.token_urlsafe(6).replace("-", "").replace("_", "")[:8]
        return {
            "id": f"evt_{datetime.now().strftime('%Y%m%d')}_{suffix}",
            "timestamp": now_iso(),
            "session_id": self.app["session_id"],
            "type": event_type,
            "actor": "user",
            "page": str(body.get("page") or "approval"),
            "item_id": body.get("item_id") or None,
            "content_hash": body.get("content_hash") or None,
            "granularity": body.get("granularity") or None,
            "covers": covers,
            "payload": payload,
            "tags": tags,
        }

    def projection(self, page: str, query: dict) -> dict:
        workspace = self.app["workspace"]
        pipeline = load_json(workspace / "pipeline.json", {"cards": []})
        leads = load_json(workspace / "leads.json", {"leads": []})
        targets = load_json(workspace / "targets.json", {"targets": []})
        items = collect_items(pipeline, leads, targets)
        for it in items:
            it["content"] = read_artifact(workspace / "artifacts", it.get("id"))
        item_id = (query.get("item_id") or query.get("artifact_id") or [""])[0]
        item = next((it for it in items if it["id"] == item_id), None) if item_id else (items[0] if items else None)
        return {
            "page": page,
            "token": self.app["token"],
            "session_id": self.app["session_id"],
            "item": item or {"id": item_id, "title": item_id or "No pending item", "content_hash": None},
            "items": items,
            "pipeline": pipeline,
            "leads": leads,
            "targets": targets,
        }

    def serve_static(self, raw_name: str):
        name = unquote(raw_name).lstrip("/")
        roots = [self.app["workspace"] / "vendor", self.app["workspace"] / "static"]
        for root in roots:
            path = (root / name).resolve()
            if root.resolve() in path.parents and path.is_file():
                data = path.read_bytes()
                ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                self._send(HTTPStatus.OK, data, ctype)
                return
        self._send(HTTPStatus.NOT_FOUND, b"not found", "text/plain; charset=utf-8")


def read_artifact(art_dir: Path, artifact_id) -> str | None:
    aid = str(artifact_id or "")
    if not aid.startswith("art_") or "/" in aid or "\\" in aid:
        return None
    path = art_dir / f"{aid}.md"
    try:
        if path.parent != art_dir or not path.is_file():
            return None
        return path.read_text(encoding="utf-8")[:20000]
    except OSError:
        return None


def collect_items(pipeline: dict, leads: dict, targets: dict) -> list[dict]:
    by_target = {t.get("id"): t for t in targets.get("targets", []) if isinstance(t, dict)}
    items: list[dict] = []
    for card in pipeline.get("cards", []):
        if not isinstance(card, dict) or card.get("status") == "closed":
            continue
        drafts = {d.get("artifact_id"): d for d in card.get("drafts", []) if isinstance(d, dict)}
        for artifact_id in card.get("artifact_ids", []) or []:
            draft = drafts.get(artifact_id, {})
            target = by_target.get(card.get("target_id"), {})
            items.append({"id": artifact_id, "title": card.get("role") or target.get("name") or artifact_id, "card_id": card.get("id"), "channel": draft.get("channel") or "manual", "destination": target.get("name") or card.get("lead_id") or "manual", "content_hash": draft.get("content_hash"), "next_action": card.get("next_action")})
    for lead in leads.get("leads", []):
        if isinstance(lead, dict) and lead.get("status") in {"queued", "bench", "promoted"}:
            items.append({"id": lead.get("id"), "title": f"{lead.get('title', 'Lead')} at {lead.get('org', '')}".strip(), "channel": "manual", "destination": lead.get("url"), "content_hash": lead.get("content_hash"), "next_action": lead.get("status")})
    return items


def has_pending(workspace: Path) -> bool:
    pipeline = load_json(workspace / "pipeline.json", {"cards": []})
    leads = load_json(workspace / "leads.json", {"leads": []})
    targets = load_json(workspace / "targets.json", {"targets": []})
    return bool(collect_items(pipeline, leads, targets))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", default="goodwork")
    parser.add_argument("--idle-timeout", type=float, default=30.0)
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    token = secrets.token_urlsafe(24)
    session_id = "sess_" + datetime.now().strftime("%Y%m%d_") + secrets.token_hex(2)
    server = HTTPServer(("127.0.0.1", 0), GoodworkHandler)
    server.timeout = 0.5
    server.app = {"workspace": workspace, "token": token, "session_id": session_id, "last_activity": time.monotonic()}
    port = server.server_address[1]
    print(json.dumps({"host": "127.0.0.1", "port": port, "token": token, "session_id": session_id}), flush=True)
    try:
        while True:
            server.handle_request()
            idle = time.monotonic() - server.app["last_activity"]
            if idle >= args.idle_timeout and not has_pending(workspace):
                break
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
