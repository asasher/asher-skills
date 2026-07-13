#!/usr/bin/env python3
"""Focused local tests for setup materialization and queue draining."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

SKILL = Path(__file__).resolve().parents[1]
SETUP = SKILL / "scripts" / "setup_instance.py"
DRAIN = SKILL / "scripts" / "drain_capture_queue.py"
API_APP = SKILL / "assets" / "capture-api" / "src" / "app.js"


def run_script(script: Path, *arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class SetupTests(unittest.TestCase):
    def test_materializes_fresh_instance_and_reruns_without_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            first = run_script(SETUP, "--project", str(project))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((project / "Inbox" / "INBOX.md").is_file())
            self.assertTrue((project / "control-plane" / "capture-to-inbox" / "api" / "src" / "app.js").is_file())
            self.assertTrue((project / "control-plane" / "config.json").is_file())
            self.assertTrue((project / "control-plane" / "state" / "intake-ledger.json").is_file())
            self.assertTrue((project / "control-plane" / "state" / "setup.json").is_file())
            self.assertTrue((project / "control-plane" / "capture-to-inbox" / "deployment.json").is_file())
            shortcut = project / "control-plane" / "capture-to-inbox" / "shortcut"
            self.assertEqual(list(shortcut.iterdir()), [])
            self.assertEqual(list(project.rglob("*.xml")), [])

            before = tree_bytes(project)
            second = run_script(SETUP, "--project", str(project))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(tree_bytes(project), before)

    def test_preserves_inbox_and_consumer_api_edits_with_candidate_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            inbox = project / "Inbox" / "INBOX.md"
            inbox.parent.mkdir(parents=True)
            inbox.write_text("consumer inbox\n", encoding="utf-8")
            first = run_script(SETUP, "--project", str(project))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(inbox.read_text(encoding="utf-8"), "consumer inbox\n")

            target = project / "control-plane" / "capture-to-inbox" / "api" / "src" / "app.js"
            target.write_text(target.read_text(encoding="utf-8") + "\n// consumer edit\n", encoding="utf-8")
            edited = target.read_bytes()
            rerun = run_script(SETUP, "--project", str(project))
            self.assertEqual(rerun.returncode, 3)
            self.assertIn("consumer edit preserved", rerun.stdout)
            self.assertEqual(target.read_bytes(), edited)
            candidate = target.with_name("app.js.setup-candidate")
            self.assertEqual(candidate.read_bytes(), API_APP.read_bytes())


class FakeQueueHandler(BaseHTTPRequestHandler):
    server: "FakeQueueServer"

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def send_json(self, status: int, value: dict[str, Any]) -> None:
        data = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def authorized(self) -> bool:
        if self.headers.get("Authorization") == "Bearer test-token":
            return True
        self.send_json(401, {"error": "unauthorized"})
        return False

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if not self.authorized():
            return
        if self.path == "/queue/items":
            self.send_json(200, {"ok": True, "items": list(self.server.items.values())})
            return
        prefix = "/queue/items/"
        if self.path.startswith(prefix) and self.path.endswith("/payload"):
            identifier = self.path[len(prefix) : -len("/payload")]
            payload = self.server.payloads.get(identifier)
            if payload is None:
                self.send_json(404, {"error": "queue_payload_not_found"})
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_json(404, {"error": "not_found"})

    def do_DELETE(self) -> None:  # noqa: N802 - stdlib handler API
        if not self.authorized():
            return
        prefix = "/queue/items/"
        identifier = self.path[len(prefix) :] if self.path.startswith(prefix) else ""
        if identifier not in self.server.items:
            self.send_json(404, {"error": "queue_item_not_found"})
            return
        del self.server.items[identifier]
        self.server.deleted.append(identifier)
        self.send_json(200, {"ok": True, "id": identifier, "deleted": True})


class FakeQueueServer(ThreadingHTTPServer):
    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), FakeQueueHandler)
        self.items: dict[str, dict[str, Any]] = {}
        self.payloads: dict[str, bytes] = {}
        self.deleted: list[str] = []


def queue_item(identifier: str, payload: bytes | None = None, digest: str | None = None) -> dict[str, Any]:
    data = payload or b""
    return {
        "id": identifier,
        "received_at": "2026-07-13T08:00:00Z",
        "captured_at": "2026-07-13T07:59:00Z",
        "source": "ios-shortcut",
        "client": "test-phone",
        "context": f"capture {identifier}",
        "shared_item": "https://example.com/capture",
        "payload": {
            "filename": "note.txt" if data else None,
            "original_name": "note.txt" if data else None,
            "mime_type": "text/plain" if data else None,
            "size": len(data),
            "sha256": digest if digest is not None else (hashlib.sha256(data).hexdigest() if data else None),
            "path": "note.txt" if data else None,
        },
        "fields": {},
    }


class DrainTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = FakeQueueServer()
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name)
        (self.project / "Inbox").mkdir()
        (self.project / "Inbox" / "INBOX.md").write_text("raw inbox\n", encoding="utf-8")
        capture_root = self.project / "control-plane" / "capture-to-inbox"
        capture_root.mkdir(parents=True)
        (self.project / "control-plane" / "config.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "paths": {"inbox": "Inbox/INBOX.md", "attachments": "Attachments/Captures"},
                    "capture_to_inbox": {
                        "deployment": "control-plane/capture-to-inbox/deployment.json",
                        "token_env": "CAPTURE_TOKEN",
                    },
                }
            ),
            encoding="utf-8",
        )
        (capture_root / "deployment.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "provider": "test",
                    "api_url": f"http://127.0.0.1:{self.server.server_port}",
                    "provider_binding": {},
                }
            ),
            encoding="utf-8",
        )
        self.env = dict(os.environ, CAPTURE_TOKEN="test-token")

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temporary.cleanup()

    def drain(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return run_script(DRAIN, "--project", str(self.project), *arguments, env=self.env)

    def test_preserves_dry_run_limit_keep_remote_and_queue_id_idempotency(self) -> None:
        first = "11111111-1111-4111-8111-111111111111"
        second = "22222222-2222-4222-8222-222222222222"
        self.server.items[first] = queue_item(first)
        self.server.items[second] = queue_item(second)

        preview = self.drain("--dry-run", "--limit", "1")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("1 of 2", preview.stdout)
        self.assertEqual(self.server.deleted, [])
        self.assertNotIn(first, (self.project / "Inbox" / "INBOX.md").read_text(encoding="utf-8"))

        kept = self.drain("--keep-remote", "--limit", "1")
        self.assertEqual(kept.returncode, 0, kept.stderr)
        inbox = (self.project / "Inbox" / "INBOX.md").read_text(encoding="utf-8")
        self.assertEqual(inbox.count(f"Queue ID: `{first}`"), 1)
        self.assertIn(first, self.server.items)

        completed = self.drain("--limit", "1")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        inbox = (self.project / "Inbox" / "INBOX.md").read_text(encoding="utf-8")
        self.assertEqual(inbox.count(f"Queue ID: `{first}`"), 1)
        self.assertEqual(self.server.deleted, [first])
        self.assertIn(second, self.server.items)

    def test_verifies_payload_before_local_success_and_remote_delete(self) -> None:
        identifier = "33333333-3333-4333-8333-333333333333"
        payload = b"verified payload"
        self.server.items[identifier] = queue_item(identifier, payload)
        self.server.payloads[identifier] = payload
        result = self.drain()
        self.assertEqual(result.returncode, 0, result.stderr)
        inbox = (self.project / "Inbox" / "INBOX.md").read_text(encoding="utf-8")
        self.assertIn(f"Queue ID: `{identifier}`", inbox)
        attachment = next((self.project / "Attachments" / "Captures").rglob("*.txt"))
        self.assertEqual(attachment.read_bytes(), payload)
        self.assertEqual(self.server.deleted, [identifier])

    def test_checksum_failure_neither_appends_nor_deletes(self) -> None:
        identifier = "44444444-4444-4444-8444-444444444444"
        expected = b"expected bytes"
        self.server.items[identifier] = queue_item(identifier, expected)
        self.server.payloads[identifier] = b"tampered bytes"
        result = self.drain()
        self.assertEqual(result.returncode, 1)
        inbox = (self.project / "Inbox" / "INBOX.md").read_text(encoding="utf-8")
        self.assertNotIn(identifier, inbox)
        self.assertEqual(self.server.deleted, [])
        self.assertIn(identifier, self.server.items)


if __name__ == "__main__":
    unittest.main()
