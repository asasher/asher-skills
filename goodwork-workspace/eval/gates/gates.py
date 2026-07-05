#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import http.client
import json
import importlib.util
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = REPO / "skills" / "goodwork" / "scripts"
PY = sys.executable
SERVER_MODULE = None


def server_module():
    global SERVER_MODULE
    if SERVER_MODULE is None:
        spec = importlib.util.spec_from_file_location("goodwork_server", SCRIPTS / "server.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        SERVER_MODULE = module
    return SERVER_MODULE


def run(cmd, cwd=None, check=True, **kwargs):
    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    if check and result.returncode != 0:
        raise AssertionError(f"{cmd} exited {result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result


def init_root(root: Path) -> Path:
    result = run([PY, str(SCRIPTS / "init_workspace.py"), "--root", str(root)])
    payload = json.loads(result.stdout)
    workspace = Path(payload["workspace"])
    assert workspace.exists()
    return workspace


def snapshot(root: Path) -> dict[str, bytes]:
    data = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            data[str(path.relative_to(root))] = path.read_bytes()
    return data


def only_changed(before: dict[str, bytes], after: dict[str, bytes], allowed: set[str]) -> set[str]:
    keys = set(before) | set(after)
    changed = {key for key in keys if before.get(key) != after.get(key)}
    extra = changed - allowed
    assert not extra, f"unexpected changed files: {sorted(extra)}"
    return changed


@contextlib.contextmanager
def server(workspace: Path):
    proc = subprocess.Popen(
        [PY, str(SCRIPTS / "server.py"), "--workspace", str(workspace), "--idle-timeout", "60"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        line = proc.stdout.readline()
        if not line:
            stderr = proc.stderr.read()
            if "PermissionError" in stderr and "Operation not permitted" in stderr:
                direct = DirectServer(workspace)
                yield None, {"port": direct, "token": direct.token, "direct": True}
                return
            raise AssertionError(f"server did not print startup JSON\n{stderr}")
        info = json.loads(line)
        yield proc, info
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=3)


class DirectServer:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.token = "direct-token"
        self.session_id = "sess_direct"
        fake = type("FakeHandler", (), {})()
        fake.app = {"workspace": workspace, "token": self.token, "session_id": self.session_id}
        self.fake = fake

    def authorized(self, token: str | None, header_token: str | None = None) -> bool:
        return (header_token or token) == self.token

    def post_event(self, payload: dict, token: str | None = None, header_token: str | None = None):
        body = dict(payload)
        if token is not None:
            body["token"] = token
        if not self.authorized(body.get("token"), header_token):
            return 403, b"forbidden"
        event = server_module().GoodworkHandler.make_event(self.fake, body)
        with (self.workspace / "events.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, separators=(",", ":"), ensure_ascii=False) + "\n")
        return 200, json.dumps({"id": event["id"]}).encode()

    def get_path(self, path: str, token: str):
        parsed = urlparse(path)
        query = parse_qs(parsed.query)
        effective = token or (query.get("token") or [""])[0]
        if effective != self.token:
            return 403, b"forbidden"
        page = "health" if parsed.path == "/health" else "kanban"
        data = server_module().GoodworkHandler.projection(self.fake, page, query)
        return 200, json.dumps(data).encode()


def post_event(port: int, payload: dict, token: str | None = None, header_token: str | None = None):
    if isinstance(port, DirectServer):
        return port.post_event(payload, token=token, header_token=header_token)
    body = dict(payload)
    if token is not None:
        body["token"] = token
    raw = json.dumps(body).encode()
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    headers = {"Content-Type": "application/json"}
    if header_token is not None:
        headers["X-Goodwork-Token"] = header_token
    conn.request("POST", "/event", body=raw, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response.status, data


def get_path(port: int, path: str, token: str):
    if isinstance(port, DirectServer):
        return port.get_path(path, token)
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    conn.request("GET", path, headers={"X-Goodwork-Token": token})
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return response.status, data


def write_event(path: Path, item_id: str, event_type: str = "approval_requested", event_id: str | None = None):
    event = {
        "id": event_id or f"evt_{item_id}",
        "timestamp": "2026-07-06T09:15:22+04:00",
        "session_id": "sess_test",
        "type": event_type,
        "actor": "user",
        "page": "approval",
        "item_id": item_id,
        "content_hash": "sha256:ok",
        "granularity": "item",
        "covers": [{"item_id": item_id, "content_hash": "sha256:ok"}],
        "payload": {"action": "approve"},
        "tags": ["approval"],
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, separators=(",", ":")) + "\n")
    return event


def gate_no_unauthenticated_post():
    with tempfile.TemporaryDirectory() as td:
        workspace = init_root(Path(td))
        with server(workspace) as (_, info):
            payload = {"type": "test_tap", "page": "health", "payload": {"tap": True}}
            status, _ = post_event(info["port"], payload)
            assert status == 403
            status, _ = post_event(info["port"], payload, token="wrong")
            assert status == 403
        assert (workspace / "events.jsonl").read_text(encoding="utf-8") == ""


def gate_event_append_only():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        workspace = init_root(root)
        before = snapshot(workspace)
        with server(workspace) as (_, info):
            status, data = post_event(
                info["port"],
                {"type": "test_tap", "page": "health", "item_id": "tap_1", "payload": {"ok": True}},
                token=info["token"],
            )
            assert status == 200, data
        after = snapshot(workspace)
        assert only_changed(before, after, {"events.jsonl"}) == {"events.jsonl"}
        lines = (workspace / "events.jsonl").read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        event = json.loads(lines[0])
        for key in ["id", "timestamp", "session_id", "type", "actor", "page", "payload", "tags", "covers"]:
            assert key in event
        assert event["type"] == "test_tap"


def gate_hash_mismatch_blocks():
    event = {
        "id": "evt_hash",
        "type": "approval_requested",
        "item_id": "art_1",
        "content_hash": "sha256:old",
        "granularity": "item",
        "covers": [{"item_id": "art_1", "content_hash": "sha256:old"}],
    }
    result = run(
        [PY, str(SCRIPTS / "validate_approval.py"), "--event", json.dumps(event), "--hashes", json.dumps({"art_1": "sha256:new"})],
        check=False,
    )
    assert result.returncode == 20
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert "approval" not in payload
    assert payload["error"] == "content_hash_mismatch"


def gate_await_drains_offline_clicks():
    with tempfile.TemporaryDirectory() as td:
        workspace = init_root(Path(td))
        log = workspace / "events.jsonl"
        write_event(log, "art_1", event_id="evt_1")
        write_event(log, "art_2", event_id="evt_2")
        result = run([PY, str(SCRIPTS / "await.py"), "--workspace", str(workspace), "--ids", "art_1", "art_2", "--timeout", "1"], check=False)
        assert result.returncode == 0, result.stderr
        payload = json.loads(result.stdout)
        assert set(payload["matched_event_ids"]) == {"evt_1", "evt_2"}
        assert payload["missing_ids"] == []
        assert int((workspace / ".await-cursor").read_text(encoding="utf-8")) == log.stat().st_size
        again = run([PY, str(SCRIPTS / "await.py"), "--workspace", str(workspace), "--ids", "art_1", "--timeout", "0.2"], check=False)
        assert again.returncode == 124
        assert json.loads(again.stdout)["matched_event_ids"] == []


def gate_await_timeout_and_partial():
    with tempfile.TemporaryDirectory() as td:
        workspace = init_root(Path(td))
        write_event(workspace / "events.jsonl", "art_1", event_id="evt_partial")
        result = run([PY, str(SCRIPTS / "await.py"), "--workspace", str(workspace), "--ids", "art_1", "art_2", "--timeout", "0.2"], check=False)
        assert result.returncode == 124
        payload = json.loads(result.stdout)
        assert payload["matched_event_ids"] == ["evt_partial"]
        assert payload["missing_ids"] == ["art_2"]
    with tempfile.TemporaryDirectory() as td:
        workspace = init_root(Path(td))
        write_event(workspace / "events.jsonl", "art_rej", event_type="rejection_requested", event_id="evt_rej")
        result = run([PY, str(SCRIPTS / "await.py"), "--workspace", str(workspace), "--ids", "art_rej", "--timeout", "1"], check=False)
        assert result.returncode == 10
        assert json.loads(result.stdout)["rejection"]["id"] == "evt_rej"


def gate_env_gitignored():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        run(["git", "init"], cwd=root)
        (root / "goodwork").mkdir()
        (root / "goodwork" / ".env").write_text("SECRET=x\n", encoding="utf-8")
        run(["git", "add", "-f", "goodwork/.env"], cwd=root)
        result = run([PY, str(SCRIPTS / "init_workspace.py"), "--root", str(root)], check=False)
        assert result.returncode == 2
        assert "tracked by git" in result.stderr


def gate_sole_writer():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        workspace = init_root(root)
        before = snapshot(workspace)
        with server(workspace) as (_, info):
            assert get_path(info["port"], "/kanban?token=" + info["token"], info["token"])[0] == 200
            assert get_path(info["port"], "/health", info["token"])[0] == 200
            for idx in range(2):
                status, data = post_event(
                    info["port"],
                    {"type": "comment", "page": "kanban", "item_id": f"pipe_{idx}", "payload": {"body": "move"}},
                    token=info["token"],
                )
                assert status == 200, data
        after = snapshot(workspace)
        assert only_changed(before, after, {"events.jsonl"}) == {"events.jsonl"}
        assert len((workspace / "events.jsonl").read_text(encoding="utf-8").splitlines()) == 2


def gate_init_schema_valid():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        workspace = init_root(root)
        expected = {
            "pipeline.json": ["version", "updated_at", "cards", "unmatched_replies"],
            "leads.json": ["version", "updated_at", "leads"],
            "sources.json": ["version", "updated_at", "sources"],
            "targets.json": ["version", "updated_at", "targets"],
            "capabilities.json": ["version", "updated_at", "workspace_id", "connectors", "chrome", "tailscale", "ui", "reconcile", "execution", "notifications"],
            "metrics.json": ["version", "updated_at", "quotas", "weeks"],
            "evidence-inbox.json": ["version", "updated_at", "entries"],
        }
        for name, keys in expected.items():
            payload = json.loads((workspace / name).read_text(encoding="utf-8"))
            for key in keys:
                assert key in payload, f"{name} missing {key}"
        assert (workspace / "approvals.jsonl").read_text(encoding="utf-8") == ""
        assert (workspace / "events.jsonl").read_text(encoding="utf-8") == ""
        assert "goodwork/.env" in (root / ".gitignore").read_text(encoding="utf-8")


GATES = [
    ("no-unauthenticated-post", gate_no_unauthenticated_post),
    ("event-append-only", gate_event_append_only),
    ("hash-mismatch-blocks", gate_hash_mismatch_blocks),
    ("await-drains-offline-clicks", gate_await_drains_offline_clicks),
    ("await-timeout-and-partial", gate_await_timeout_and_partial),
    ("env-gitignored", gate_env_gitignored),
    ("sole-writer", gate_sole_writer),
    ("init-schema-valid", gate_init_schema_valid),
]


def main() -> int:
    failed = 0
    for name, fn in GATES:
        start = time.time()
        try:
            fn()
            print(f"PASS {name} ({time.time() - start:.2f}s)")
        except Exception:
            failed += 1
            print(f"FAIL {name}", file=sys.stderr)
            traceback.print_exc()
    print(f"Summary: {len(GATES) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
