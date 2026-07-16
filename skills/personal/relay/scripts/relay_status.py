#!/usr/bin/env python3
"""Report Relay workflow, delivery, watermark, and reply state without mutation."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from relay_common import instance_root, read_jsonl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    args = parser.parse_args()
    try:
        state = instance_root(args.repository_root) / "state"
        workflow = read_jsonl(state / "workflow.jsonl")
        delivery = read_jsonl(state / "delivery.jsonl")
        replies = read_jsonl(state / "replies.jsonl")
        watermarks = read_jsonl(state / "watermarks.jsonl")
        communication_ids = sorted({str(item.get("communication_id")) for item in workflow if item.get("communication_id")})
        reports: list[dict[str, Any]] = []
        for communication_id in communication_ids:
            workflow_items = [item for item in workflow if item.get("communication_id") == communication_id]
            delivery_items = [item for item in delivery if item.get("communication_id") == communication_id]
            latest: dict[str, str] = {}
            for item in delivery_items:
                if item.get("recipient_hash") and item.get("state"):
                    latest[str(item["recipient_hash"])] = str(item["state"])
            intended = {str(item["recipient_hash"]) for item in delivery_items if item.get("state") == "pending"}
            all_delivered = bool(intended) and all(latest.get(recipient) == "receiving-server-delivered" for recipient in intended)
            reports.append({
                "communication_id": communication_id,
                "workflow_state": workflow_items[-1].get("state"),
                "recipient_outcomes": latest,
                "all_delivered": all_delivered,
                "reply_count": sum(item.get("communication_id") == communication_id for item in replies),
                "watermark_confirmed": any(item.get("communication_id") == communication_id for item in watermarks),
            })
        print(json.dumps({"status": "ok", "communications": reports}, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
