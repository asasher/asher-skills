#!/usr/bin/env python3
"""Replace the setup credential with an inbox-scoped AgentMail runtime key."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


def dotenv_value(path: Path, name: str) -> str | None:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if separator and key.strip() == name:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            return value
    return None


def replace_assignment(path: Path, name: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    replacement = f"{name}={value}"
    replaced = False
    output: list[str] = []
    for line in lines:
        candidate = line.strip()
        key, separator, _ = candidate.partition("=")
        if separator and key.strip() == name and not replaced:
            output.append(replacement)
            replaced = True
        else:
            output.append(line)
    if not replaced:
        output.append(replacement)
    data = ("\n".join(output) + "\n").encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(prefix=".env.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def find_string(value: Any, key: str) -> str | None:
    if isinstance(value, dict):
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
        for child in value.values():
            found = find_string(child, key)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_string(child, key)
            if found:
                return found
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        workspace = args.workspace_root.resolve()
        env_path = workspace / ".env"
        capabilities_path = workspace / "control-plane" / "communications" / "capabilities.json"
        capabilities = json.loads(capabilities_path.read_text(encoding="utf-8"))
        rich = capabilities["rich_email_delivery"]
        inbox_id = rich["inbox_id"]
        parent_key = dotenv_value(env_path, "AGENTMAIL_API_KEY")
        if not parent_key:
            raise ValueError("AGENTMAIL_API_KEY is missing from workspace root .env")
        if not isinstance(inbox_id, str) or not inbox_id:
            raise ValueError("AgentMail inbox_id is missing")
        if not args.execute:
            print(json.dumps({"status": "dry_run", "inbox_id": inbox_id, "scope": "inbox"}, indent=2))
            return 0
        executable = shutil.which("agentmail")
        if not executable:
            raise ValueError("agentmail CLI is not installed")
        env = dict(os.environ)
        env["AGENTMAIL_API_KEY"] = parent_key
        command = [
            executable,
            "--format",
            "json",
            "inboxes:api-keys",
            "create",
            "--inbox-id",
            inbox_id,
            "--name",
            "manage-communications-runtime",
            "--permissions.draft-read",
            "true",
            "--permissions.draft-create",
            "true",
            "--permissions.draft-send",
            "true",
        ]
        result = subprocess.run(command, check=False, capture_output=True, text=True, env=env, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"AgentMail key creation failed with exit {result.returncode}")
        response = json.loads(result.stdout)
        runtime_key = find_string(response, "api_key")
        if not runtime_key:
            raise RuntimeError("AgentMail response did not contain api_key")
        replace_assignment(env_path, "AGENTMAIL_API_KEY", runtime_key)
        print(
            json.dumps(
                {
                    "status": "rotated",
                    "inbox_id": inbox_id,
                    "api_key_id": find_string(response, "api_key_id"),
                    "prefix": find_string(response, "prefix"),
                    "permissions": ["draft_read", "draft_create", "draft_send"],
                },
                indent=2,
            )
        )
        return 0
    except (KeyError, OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
