#!/usr/bin/env python3
"""Durable, shared backlog run events and projections (stdlib only)."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {
    "type", "issue", "stage", "role", "model_route", "capacity_pool", "worktree",
    "checkpoint", "expected_return", "escalation_successor", "status",
}

# Spawn events additionally carry staffing telemetry: the actual model and effort
# the child runs with (asserted against the staffed role before dispatch) and the
# worker session id where the route has one (codex/claude CLI workers; null for
# native children). Resume audits and the roster assertion read these.
SPAWN_REQUIRED = {"model", "effort", "worker_session"}

TERMINAL_STATUSES = {"complete", "blocked", "deferred", "returned", "interrupted"}


class StateError(ValueError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def run_root(repo: Path, run_id: str) -> Path:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True, text=True, check=True,
    )
    root = Path(result.stdout.strip()) / "backlog" / "runs" / run_id
    root.mkdir(parents=True, exist_ok=True)
    return root


def load_events(path: Path) -> list[dict]:
    events = []
    if not path.exists():
        return events
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise StateError(f"{path}:{number}: invalid JSON") from exc
        if event.get("sequence") != number:
            raise StateError(f"{path}:{number}: non-monotonic sequence")
        events.append(event)
    return events


def project(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".projection.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _project_unlocked(root)


def _project_unlocked(root: Path) -> dict:
    streams = sorted((root / "events").glob("*.jsonl")) if (root / "events").exists() else []
    all_events = [event for stream in streams for event in load_events(stream)]
    latest = {}
    for event in all_events:
        latest[event["parent_id"]] = event
    status = {
        "run_id": root.name,
        "event_count": len(all_events),
        "parents": dict(sorted(latest.items())),
        "generated_at": now(),
    }
    atomic_write(root / "status.json", json.dumps(status, indent=2, sort_keys=True) + "\n")
    rows = ["# Backlog run status", "", "| Parent | Issue | Stage | Route | Status |", "|---|---|---|---|---|"]
    rows.extend(
        f"| {parent} | {event['issue']} | {event['stage']} | {event['model_route']} | {event['status']} |"
        for parent, event in sorted(latest.items())
    )
    atomic_write(root / "board.md", "\n".join(rows) + "\n")
    return status


def append(root: Path, parent: str, payload: dict) -> dict:
    missing = REQUIRED - set(payload)
    if payload.get("type") == "spawn":
        missing |= SPAWN_REQUIRED - set(payload)
    if missing:
        raise StateError("event missing: " + ", ".join(sorted(missing)))
    events = root / "events"
    events.mkdir(parents=True, exist_ok=True)
    stream = events / f"{parent}.jsonl"
    lock_path = events / f"{parent}.lock"
    with lock_path.open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        sequence = len(load_events(stream)) + 1
        event = dict(payload, run_id=root.name, parent_id=parent, sequence=sequence, timestamp=now())
        with stream.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, separators=(",", ":"), sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        project(root)
    return event


def verify_owner(record: dict) -> tuple[bool, str]:
    try:
        pid = int(record["pid"])
        os.kill(pid, 0)
    except (KeyError, TypeError, ValueError, ProcessLookupError, PermissionError):
        return False, "dead-or-invalid-pid"
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "lstart=", "-o", "command="],
        capture_output=True, text=True,
    )
    observed = result.stdout.strip()
    if not observed:
        return False, "missing-process"
    if record.get("process_start") and not observed.startswith(record["process_start"]):
        return False, "process-start-mismatch"
    command = record.get("command")
    if command and command not in observed:
        return False, "command-mismatch"
    return True, "verified"


def verify_terminal(root: Path) -> tuple[bool, dict]:
    """Completion gate: fresh projection, handoff written, every parent terminal."""
    status = project(root)
    problems = []
    if not (root / "handoff.md").exists():
        problems.append("missing-handoff")
    for parent, event in status["parents"].items():
        if event.get("status") not in TERMINAL_STATUSES:
            problems.append(f"non-terminal:{parent}:{event.get('status')}")
    return not problems, {"ok": not problems, "problems": problems, "event_count": status["event_count"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("append", "project", "verify-owner", "handoff", "verify-terminal"))
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--parent")
    parser.add_argument("--payload", help="JSON object")
    args = parser.parse_args()
    try:
        root = run_root(args.repo, args.run_id)
        if args.command == "append":
            if not args.parent or not args.payload:
                raise StateError("append requires --parent and --payload")
            print(json.dumps(append(root, args.parent, json.loads(args.payload))))
        elif args.command == "project":
            print(json.dumps(project(root)))
        elif args.command == "verify-terminal":
            ok, report = verify_terminal(root)
            print(json.dumps(report))
            return 0 if ok else 1
        elif args.command == "verify-owner":
            if not args.payload:
                raise StateError("verify-owner requires --payload")
            valid, reason = verify_owner(json.loads(args.payload))
            print(json.dumps({"valid": valid, "reason": reason}))
            return 0 if valid else 1
        else:
            if not args.payload:
                raise StateError("handoff requires --payload")
            data = json.loads(args.payload)
            required = {"state_pointers", "protocols", "environment", "cleanup_debts", "blocked", "not_before"}
            missing = required - set(data)
            if missing:
                raise StateError("handoff missing: " + ", ".join(sorted(missing)))
            lines = ["# Backlog run handoff", ""] + [
                f"## {key.replace('_', ' ').title()}\n\n{json.dumps(data[key], indent=2, sort_keys=True)}"
                for key in sorted(required)
            ]
            atomic_write(root / "handoff.md", "\n\n".join(lines) + "\n")
            print(json.dumps({"handoff": str(root / "handoff.md")}))
    except (StateError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
