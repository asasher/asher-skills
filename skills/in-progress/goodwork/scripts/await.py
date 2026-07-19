#!/usr/bin/env python3
"""Block until requested Goodwork events arrive."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REJECTION_TYPES = {"rejection_requested"}


def parse_ids(values: list[str]) -> list[str]:
    ids: list[str] = []
    for value in values:
        ids.extend(part for part in value.replace(",", " ").split() if part)
    return ids


def load_cursor(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        value = int(path.read_text(encoding="utf-8").strip() or "0")
    except ValueError as exc:
        raise RuntimeError("malformed cursor") from exc
    return max(0, value)


def save_cursor(path: Path, offset: int) -> None:
    path.write_text(str(offset), encoding="utf-8")


def match_ids(event: dict, wanted: set[str]) -> set[str]:
    matched = set()
    if event.get("id") in wanted:
        matched.add(event["id"])
    if event.get("item_id") in wanted:
        matched.add(event["item_id"])
    for cover in event.get("covers") or []:
        if isinstance(cover, dict) and cover.get("item_id") in wanted:
            matched.add(cover["item_id"])
    return matched


def read_new_events(log_path: Path, offset: int):
    if not log_path.exists():
        return [], offset
    events = []
    with log_path.open("rb") as fh:
        fh.seek(offset)
        while True:
            start = fh.tell()
            line = fh.readline()
            if not line:
                return events, fh.tell()
            try:
                text = line.decode("utf-8")
                event = json.loads(text)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"malformed event log at byte {start}") from exc
            if not isinstance(event, dict):
                raise RuntimeError(f"malformed event log at byte {start}")
            events.append(event)


def output(status: str, requested: list[str], seen: dict[str, dict], rejection: dict | None = None) -> None:
    missing = [item_id for item_id in requested if item_id not in seen]
    payload = {
        "status": status,
        "requested": requested,
        "matched_event_ids": [event["id"] for event in seen.values()],
        "matched": list(seen.values()),
        "missing_ids": missing,
    }
    if rejection:
        payload["rejection"] = rejection
    print(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", nargs="+", required=True)
    parser.add_argument("--timeout", type=float, required=True)
    parser.add_argument("--workspace", default="goodwork")
    args = parser.parse_args()
    requested = parse_ids(args.ids)
    if not requested:
        print("no ids requested", file=sys.stderr)
        return 2
    workspace = Path(args.workspace)
    log_path = workspace / "events.jsonl"
    cursor_path = workspace / ".await-cursor"
    try:
        offset = load_cursor(cursor_path)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    wanted = set(requested)
    seen: dict[str, dict] = {}
    deadline = time.monotonic() + max(0, args.timeout)
    while True:
        try:
            events, new_offset = read_new_events(log_path, offset)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        for event in events:
            for matched_id in match_ids(event, wanted):
                seen.setdefault(matched_id, event)
            if match_ids(event, wanted) and event.get("type") in REJECTION_TYPES:
                save_cursor(cursor_path, new_offset)
                output("rejected", requested, seen, event)
                return 10
        if new_offset != offset:
            save_cursor(cursor_path, new_offset)
            offset = new_offset
        if all(item_id in seen for item_id in requested):
            output("matched", requested, seen)
            return 0
        if time.monotonic() >= deadline:
            output("timeout", requested, seen)
            return 124
        time.sleep(0.1)


if __name__ == "__main__":
    raise SystemExit(main())
