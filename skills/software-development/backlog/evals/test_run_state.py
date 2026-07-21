#!/usr/bin/env python3
"""Executable probes for shared backlog run state."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/run-state.py"
SPEC = importlib.util.spec_from_file_location("backlog_run_state", SCRIPT)
assert SPEC and SPEC.loader
state = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(state)


class RunStateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.root = state.run_root(self.repo, "run-test")

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def payload(issue: str) -> dict:
        return {
            "type": "spawn", "issue": issue, "stage": "implement", "role": "builder",
            "model_route": "native", "capacity_pool": "unknown", "worktree": f"/tmp/{issue}",
            "checkpoint": "claimed", "expected_return": "commit", "escalation_successor": "root",
            "status": "running", "model": "sonnet-5", "effort": "medium",
            "worker_session": None,
        }

    def test_two_parents_append_concurrently_and_rebuild_one_board(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            events = list(pool.map(lambda item: state.append(self.root, item, self.payload(item)), ("p1", "p2")))
        self.assertEqual({event["parent_id"] for event in events}, {"p1", "p2"})
        (self.root / "status.json").unlink()
        (self.root / "board.md").unlink()
        rebuilt = state.project(self.root)
        self.assertEqual(rebuilt["event_count"], 2)
        self.assertEqual(set(rebuilt["parents"]), {"p1", "p2"})
        self.assertIn("| p1 |", (self.root / "board.md").read_text())

    def test_same_parent_sequence_is_locked(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda _: state.append(self.root, "parent", self.payload("48")), range(4)))
        events = state.load_events(self.root / "events/parent.jsonl")
        self.assertEqual([event["sequence"] for event in events], [1, 2, 3, 4])

    def test_stale_or_mismatched_process_is_rejected(self):
        valid, reason = state.verify_owner({"pid": 99999999, "command": "never"})
        self.assertFalse(valid)
        self.assertEqual(reason, "dead-or-invalid-pid")
        valid, reason = state.verify_owner({"pid": os.getpid(), "command": "definitely-not-this-command"})
        self.assertFalse(valid)
        self.assertEqual(reason, "command-mismatch")

    def test_handoff_requires_all_fields(self):
        command = [
            sys.executable, str(SCRIPT), "handoff", "--repo", str(self.repo), "--run-id", "run-test",
            "--payload", json.dumps({"state_pointers": []}),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("handoff missing", result.stderr)


class SpawnTelemetryAndTerminalGate(unittest.TestCase):
    setUp = RunStateTest.setUp
    tearDown = RunStateTest.tearDown
    payload = staticmethod(RunStateTest.payload)

    def test_spawn_without_telemetry_is_rejected(self):
        payload = self.payload("60")
        for key in ("model", "effort", "worker_session"):
            broken = {k: v for k, v in payload.items() if k != key}
            with self.assertRaises(state.StateError):
                state.append(self.root, "parent", broken)

    def test_non_spawn_event_does_not_require_telemetry(self):
        payload = {k: v for k, v in self.payload("61").items()
                   if k not in ("model", "effort", "worker_session")}
        payload["type"] = "return"
        state.append(self.root, "parent", payload)

    def test_verify_terminal_refuses_then_passes(self):
        running = self.payload("62")
        state.append(self.root, "p62", running)
        ok, report = state.verify_terminal(self.root)
        self.assertFalse(ok)
        self.assertIn("missing-handoff", report["problems"])
        self.assertTrue(any(p.startswith("non-terminal:p62") for p in report["problems"]))
        done = dict(running, type="return", status="complete")
        del done["model"], done["effort"], done["worker_session"]
        state.append(self.root, "p62", done)
        (self.root / "handoff.md").write_text("# Backlog run handoff\n")
        ok, report = state.verify_terminal(self.root)
        self.assertTrue(ok, report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
