#!/usr/bin/env python3
"""Block until the next feedback_submitted event arrives in state/events.jsonl.

Prints the event as JSON and exits with a verdict-coded status:
  0   approve
  3   approve_with_nits
  10  request_changes
  124 timeout
Cursor-tracked (state/.await-cursor), so feedback submitted while no agent
was waiting is picked up by the next await.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

EXIT_CODES = {"approve": 0, "approve_with_nits": 3, "request_changes": 10}


def load_cursor(path: Path) -> int:
    try:
        return max(0, int(path.read_text(encoding="utf-8").strip() or "0"))
    except (FileNotFoundError, ValueError):
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default="state")
    parser.add_argument("--timeout", type=float, required=True)
    args = parser.parse_args()

    state = Path(args.state)
    log_path = state / "events.jsonl"
    cursor_path = state / ".await-cursor"
    offset = load_cursor(cursor_path)
    deadline = time.monotonic() + max(0.0, args.timeout)

    while True:
        if log_path.exists():
            with log_path.open("rb") as fh:
                fh.seek(offset)
                while True:
                    line = fh.readline()
                    if not line:
                        offset = fh.tell()
                        break
                    try:
                        event = json.loads(line.decode("utf-8"))
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        offset = fh.tell()
                        continue
                    if isinstance(event, dict) and event.get("type") == "feedback_submitted":
                        cursor_path.write_text(str(fh.tell()), encoding="utf-8")
                        print(json.dumps(event, ensure_ascii=False, indent=1))
                        return EXIT_CODES.get(event.get("verdict"), 10)
                    offset = fh.tell()
            cursor_path.write_text(str(offset), encoding="utf-8")
        if time.monotonic() >= deadline:
            print(json.dumps({"status": "timeout"}))
            return 124
        time.sleep(0.2)


if __name__ == "__main__":
    raise SystemExit(main())
