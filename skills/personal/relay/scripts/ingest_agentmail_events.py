#!/usr/bin/env python3
"""Idempotently append normalized AgentMail lifecycle and reply facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from relay_common import append_event, instance_root, now, read_jsonl, recipient_hash, sha256_bytes

DELIVERY = {"message.delivered": "receiving-server-delivered", "message.bounced": "bounced", "message.complained": "complained", "message.rejected": "rejected"}


def load_events(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = [json.loads(line) for line in text.splitlines() if line.strip()]
    if isinstance(value, dict):
        value = value.get("events", [value])
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError("event input must be a JSON array, object, or JSONL")
    return value


def correlation(workflow: list[dict[str, Any]], event: dict[str, Any]) -> tuple[str, str] | None:
    if event.get("communication_id") and event.get("audience_id"):
        return str(event["communication_id"]), str(event["audience_id"])
    for item in reversed(workflow):
        if (event.get("message_id") and item.get("message_id") == event["message_id"]) or (event.get("thread_id") and item.get("thread_id") == event["thread_id"]):
            return str(item["communication_id"]), str(item["audience_id"])
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--mode", choices=["manual", "webhook"], default="manual")
    parser.add_argument("--signature-verified", action="store_true")
    args = parser.parse_args()
    try:
        if args.mode == "webhook" and not args.signature_verified:
            raise ValueError("webhook input requires verified Svix signature")
        instance = instance_root(args.repository_root)
        workflow_path = instance / "state" / "workflow.jsonl"
        workflow = read_jsonl(workflow_path)
        appended, ignored, blocked = 0, 0, 0
        for event in load_events(args.events):
            event_id, event_type = event.get("id"), event.get("type")
            if not isinstance(event_id, str) or not isinstance(event_type, str):
                blocked += 1
                continue
            linked = correlation(workflow, event)
            if not linked:
                blocked += 1
                continue
            communication_id, audience_id = linked
            timestamp = str(event.get("timestamp") or now())
            if event_type == "message.sent":
                fact = {"schema_version": 1, "timestamp": timestamp, "communication_id": communication_id, "audience_id": audience_id, "state": "sent", "provider_event_id": event_id, "message_id": event.get("message_id"), "thread_id": event.get("thread_id"), "confirmation": args.mode, "idempotency_key": f"provider:{event_id}"}
                changed = append_event(workflow_path, fact)
                watermark = {"schema_version": 1, "timestamp": timestamp, "communication_id": communication_id, "audience_id": audience_id, "observed_through": str(event.get("observed_through") or timestamp), "provider_event_id": event_id, "idempotency_key": f"watermark:{event_id}"}
                append_event(instance / "state" / "watermarks.jsonl", watermark)
            elif event_type in DELIVERY:
                recipients = event.get("recipients") or ([event["recipient"]] if event.get("recipient") else [])
                changed = False
                for address in recipients:
                    hashed = recipient_hash(str(address))
                    fact = {"schema_version": 1, "timestamp": timestamp, "communication_id": communication_id, "audience_id": audience_id, "recipient_hash": hashed, "state": DELIVERY[event_type], "provider_event_id": event_id, "message_id": event.get("message_id"), "idempotency_key": sha256_bytes(f"delivery:{event_id}:{hashed}".encode())}
                    changed = append_event(instance / "state" / "delivery.jsonl", fact) or changed
                if event_type == "message.rejected":
                    changed = append_event(workflow_path, {"schema_version": 1, "timestamp": timestamp, "communication_id": communication_id, "audience_id": audience_id, "state": "rejected", "provider_event_id": event_id, "message_id": event.get("message_id"), "idempotency_key": f"workflow-rejected:{event_id}"}) or changed
            elif event_type == "message.received":
                fact = {"schema_version": 1, "timestamp": timestamp, "communication_id": communication_id, "audience_id": audience_id, "state": "reply-received", "provider_event_id": event_id, "message_id": event.get("message_id"), "thread_id": event.get("thread_id"), "source_message_id": event.get("source_message_id"), "automatic_reply": False, "idempotency_key": f"reply:{event_id}"}
                changed = append_event(instance / "state" / "replies.jsonl", fact)
            else:
                blocked += 1
                continue
            if changed:
                appended += 1
            else:
                ignored += 1
            workflow = read_jsonl(workflow_path)
        print(json.dumps({"status": "ok", "mode": args.mode, "appended": appended, "duplicates_ignored": ignored, "uncorrelated_or_unsupported": blocked, "real_time": args.mode == "webhook"}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
