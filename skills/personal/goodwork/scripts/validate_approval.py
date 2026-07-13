#!/usr/bin/env python3
"""Validate a Goodwork approval request against current content hashes."""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

APPROVAL_TYPES = {"approval_requested", "batch_approval_requested"}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json_arg(value: str):
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


def normalize_hashes(raw) -> dict[str, str]:
    if isinstance(raw, dict):
        return {str(k): str(v) for k, v in raw.items()}
    if isinstance(raw, list):
        hashes = {}
        for item in raw:
            if isinstance(item, dict) and item.get("item_id") and item.get("content_hash"):
                hashes[str(item["item_id"])] = str(item["content_hash"])
        return hashes
    raise ValueError("hashes must be an object or list")


def event_covers(event: dict) -> list[dict]:
    if event.get("granularity") == "session_batch" or event.get("type") == "batch_approval_requested":
        covers = event.get("covers") or []
    else:
        covers = [{"item_id": event.get("item_id"), "content_hash": event.get("content_hash")}]
    if not covers:
        raise ValueError("approval event has no covers")
    normalized = []
    for cover in covers:
        if not isinstance(cover, dict) or not cover.get("item_id") or not cover.get("content_hash"):
            raise ValueError("invalid cover entry")
        normalized.append({"item_id": str(cover["item_id"]), "content_hash": str(cover["content_hash"])})
    return normalized


def make_approval(event: dict, covers: list[dict], channel: str, expires_hours: float | None) -> dict:
    timestamp = now_iso()
    expires_at = None
    if expires_hours is not None:
        expires_at = (datetime.now(timezone.utc).astimezone() + timedelta(hours=expires_hours)).isoformat(timespec="seconds")
    return {
        "id": "appr_" + datetime.now().strftime("%Y%m%d_") + secrets.token_hex(4),
        "timestamp": timestamp,
        "item_id": event.get("item_id") or covers[0]["item_id"],
        "channel": channel,
        "granularity": event.get("granularity") or ("session_batch" if len(covers) > 1 else "item"),
        "content_hash": event.get("content_hash") or covers[0]["content_hash"],
        "covers": covers,
        "source_event_id": event.get("id"),
        "approved_by": "user",
        "expires_at": expires_at,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", required=True, help="Event JSON or path to event JSON")
    parser.add_argument("--hashes", required=True, help="Current hash JSON object/list or path")
    parser.add_argument("--channel", default="manual")
    parser.add_argument("--expires-hours", type=float)
    args = parser.parse_args()
    try:
        event = load_json_arg(args.event)
        hashes = normalize_hashes(load_json_arg(args.hashes))
        if not isinstance(event, dict) or event.get("type") not in APPROVAL_TYPES:
            raise ValueError("not an approval event")
        covers = event_covers(event)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 2
    mismatches = []
    for cover in covers:
        current = hashes.get(cover["item_id"])
        if current != cover["content_hash"]:
            mismatches.append({"item_id": cover["item_id"], "event_hash": cover["content_hash"], "current_hash": current})
    if mismatches:
        print(json.dumps({"ok": False, "error": "content_hash_mismatch", "mismatches": mismatches}, separators=(",", ":")))
        return 20
    print(json.dumps({"ok": True, "approval": make_approval(event, covers, args.channel, args.expires_hours)}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
