#!/usr/bin/env python3
"""Create and send a reviewer-only AgentMail handoff; dry-run unless --execute."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def dotenv_value(path: Path, name: str) -> str | None:
    if not path.is_file():
        return None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, value = line.partition("=")
        if separator and key.strip() == name:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            return value
    return None


def load_capability(workspace: Path) -> dict[str, Any]:
    path = workspace / "control-plane" / "communications" / "capabilities.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    rich = value.get("rich_email_delivery") if isinstance(value, dict) else None
    if not isinstance(rich, dict):
        raise ValueError("rich_email_delivery capability is missing")
    reviewer = rich.get("review_recipient")
    if rich.get("provider") != "agentmail-cli" or rich.get("status") != "verified":
        raise ValueError("AgentMail capability is not verified")
    if not isinstance(reviewer, str) or not reviewer:
        raise ValueError("review_recipient is missing")
    if rich.get("allowed_recipients") != [reviewer]:
        raise ValueError("AgentMail allowlist must contain only review_recipient")
    if not isinstance(rich.get("inbox_id"), str) or not rich.get("inbox_id"):
        raise ValueError("AgentMail inbox_id is missing")
    return rich


def extract_id(value: Any, preferred: tuple[str, ...]) -> str | None:
    if isinstance(value, dict):
        for key in preferred:
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate
        for child in value.values():
            candidate = extract_id(child, preferred)
            if candidate:
                return candidate
    elif isinstance(value, list):
        for child in value:
            candidate = extract_id(child, preferred)
            if candidate:
                return candidate
    return None


def invoke(command: list[str], env: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run(command, check=False, capture_output=True, text=True, env=env, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"AgentMail command failed with exit {result.returncode}")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("AgentMail did not return JSON") from error
    if not isinstance(value, dict):
        raise RuntimeError("AgentMail returned an unexpected response")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root", type=Path)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--html-file", type=Path, required=True)
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    try:
        workspace = args.workspace_root.resolve()
        capability = load_capability(workspace)
        token = dotenv_value(workspace / ".env", "AGENTMAIL_API_KEY")
        if not token:
            raise ValueError("AGENTMAIL_API_KEY is missing from workspace root .env")
        html = args.html_file.read_text(encoding="utf-8")
        text = args.text_file.read_text(encoding="utf-8")
        reviewer = capability["review_recipient"]
        inbox_id = capability["inbox_id"]

        if not args.execute:
            print(
                json.dumps(
                    {
                        "status": "dry_run",
                        "provider": "agentmail-cli",
                        "recipient": reviewer,
                        "client_id": args.client_id,
                        "actions": ["inboxes:drafts create", "inboxes:drafts send"],
                    },
                    indent=2,
                )
            )
            return 0

        executable = shutil.which("agentmail")
        if not executable:
            raise ValueError("agentmail CLI is not installed")
        env = dict(os.environ)
        env["AGENTMAIL_API_KEY"] = token
        create = [
            executable,
            "--format",
            "json",
            "inboxes:drafts",
            "create",
            "--inbox-id",
            inbox_id,
            "--client-id",
            args.client_id,
            "--to",
            reviewer,
            "--subject",
            args.subject,
            "--html",
            html,
            "--text",
            text,
        ]
        draft_response = invoke(create, env)
        draft_id = extract_id(draft_response, ("draft_id", "draftId", "id"))
        if not draft_id:
            raise RuntimeError("AgentMail create response did not contain a draft ID")
        send = [
            executable,
            "--format",
            "json",
            "inboxes:drafts",
            "send",
            "--inbox-id",
            inbox_id,
            "--draft-id",
            draft_id,
        ]
        send_response = invoke(send, env)
        message_id = extract_id(send_response, ("message_id", "messageId", "id"))
        print(
            json.dumps(
                {
                    "status": "sent_to_reviewer",
                    "provider": "agentmail-cli",
                    "recipient": reviewer,
                    "client_id": args.client_id,
                    "draft_id": draft_id,
                    "message_id": message_id,
                },
                indent=2,
            )
        )
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
