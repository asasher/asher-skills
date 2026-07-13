#!/usr/bin/env python3
"""Integration tests for review-loop's detached server lifecycle."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SERVER = HERE / "scripts" / "review-server.py"
AWAIT = HERE / "scripts" / "review-await.py"


class LifecycleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.surface = self.root / "surface"
        self.states: list[Path] = []

    def tearDown(self):
        for state in self.states:
            subprocess.run(
                [sys.executable, str(SERVER), "--stop", "--state", str(state)],
                capture_output=True, text=True, timeout=10,
            )
        self.tmp.cleanup()

    def launch(
        self, name: str, *, doc_name: str | None = None, issue: str | None = None
    ) -> tuple[Path, dict]:
        doc = self.root / f"{doc_name or name}.html"
        doc.write_text(f"<html><body><h1 id='scope'>{name}</h1></body></html>", encoding="utf-8")
        state = self.root / f"state-{name}"
        self.states.append(state)
        result = subprocess.run(
            [
                sys.executable, str(SERVER), "--doc", str(doc), "--title", name,
                "--issue", issue or name, "--state", str(state), "--surface", str(self.surface),
            ],
            capture_output=True, text=True, timeout=10, check=True,
        )
        meta = json.loads(result.stdout)
        self.assertTrue((state / "server.log").is_file())
        self.assertTrue((state / "server.json").is_file())
        return state, meta

    @staticmethod
    def version(meta: dict) -> dict:
        url = f"http://127.0.0.1:{meta['port']}/version?token={meta['token']}"
        with urllib.request.urlopen(url, timeout=2) as response:
            return json.load(response)

    def approve(self, state: Path, meta: dict) -> dict:
        version = self.version(meta)
        body = json.dumps({
            "token": meta["token"], "type": "feedback_submitted", "verdict": "approve",
            "doc_hash": version["hash"], "annotations": [],
        }).encode()
        request = urllib.request.Request(
            f"http://127.0.0.1:{meta['port']}/event", data=body,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            self.assertEqual(response.status, 200)
        event = json.loads((state / "events.jsonl").read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(event["verdict"], "approve")
        self.assertEqual(event["doc_hash"], version["hash"])
        return event

    def stop(self, state: Path) -> dict:
        result = subprocess.run(
            [sys.executable, str(SERVER), "--stop", "--state", str(state)],
            capture_output=True, text=True, timeout=10, check=True,
        )
        return json.loads(result.stdout)

    def test_parent_exit_external_submit_and_idempotent_stop(self):
        state, meta = self.launch("parent-exit")
        self.assertEqual(self.version(meta)["instance_id"], meta["instance_id"])
        self.approve(state, meta)
        self.assertTrue(self.stop(state)["stopped"])
        self.assertTrue(self.stop(state)["already_stopped"])
        registry = json.loads((self.surface / "registry.json").read_text(encoding="utf-8"))
        self.assertNotIn(meta["entry_id"], registry["entries"])

    def test_lifetime_is_independent_of_watcher(self):
        state, meta = self.launch("watcher")
        watcher = subprocess.Popen(
            [sys.executable, str(AWAIT), "--state", str(state), "--timeout", "5"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        event = self.approve(state, meta)
        stdout, stderr = watcher.communicate(timeout=8)
        self.assertEqual(watcher.returncode, 0, stderr)
        self.assertEqual(json.loads(stdout)["id"], event["id"])
        self.assertTrue(self.version(meta)["hash"])

    def test_two_concurrent_servers_share_one_registry(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(self.launch, "one")
            second = pool.submit(self.launch, "two")
            (state_one, meta_one), (state_two, meta_two) = first.result(), second.result()
        registry = json.loads((self.surface / "registry.json").read_text(encoding="utf-8"))
        self.assertEqual(set(registry["entries"]), {meta_one["entry_id"], meta_two["entry_id"]})
        self.approve(state_one, meta_one)
        self.approve(state_two, meta_two)
        self.assertTrue(self.stop(state_one)["stopped"])
        self.assertEqual(set(json.loads((self.surface / "registry.json").read_text())["entries"]), {meta_two["entry_id"]})
        self.assertTrue(self.stop(state_two)["stopped"])

    def test_old_same_artifact_cleanup_cannot_remove_new_instance(self):
        old_state, old_meta = self.launch("old", doc_name="same", issue="42")
        new_state, new_meta = self.launch("new", doc_name="same", issue="42")
        self.assertNotEqual(old_meta["entry_id"], new_meta["entry_id"])
        self.assertTrue(self.stop(old_state)["stopped"])
        entries = json.loads((self.surface / "registry.json").read_text())["entries"]
        self.assertNotIn(old_meta["entry_id"], entries)
        self.assertIn(new_meta["entry_id"], entries)
        self.assertEqual(entries[new_meta["entry_id"]]["instance_id"], new_meta["instance_id"])
        self.assertTrue(self.version(new_meta)["hash"])
        self.assertTrue(self.stop(new_state)["stopped"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
