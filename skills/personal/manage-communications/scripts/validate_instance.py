#!/usr/bin/env python3
"""Validate a manage-communications consumer instance without exposing secrets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VERSION = re.compile(r"(\d+)\.(\d+)\.(\d+)")
SECRET_KEYS = {"api_key", "apikey", "access_token", "refresh_token", "secret", "token"}


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path}: {error}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: expected a JSON object")
        return {}
    return value


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


def find_secret_key(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            location = f"{prefix}.{key}" if prefix else str(key)
            if normalized in SECRET_KEYS:
                findings.append(location)
            findings.extend(find_secret_key(child, location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_secret_key(child, f"{prefix}[{index}]"))
    return findings


def parse_version(raw: str) -> tuple[int, int, int] | None:
    match = VERSION.search(raw)
    return tuple(int(part) for part in match.groups()) if match else None


def validate_profile_binding(
    instance: Path, value: dict[str, Any], label: str, errors: list[str]
) -> tuple[str, str] | None:
    profile_value = value.get("profile_file")
    digest_value = value.get("profile_sha256")
    if profile_value is None and digest_value is None:
        return None
    if not isinstance(profile_value, str) or not profile_value:
        errors.append(f"{label}: profile_file must be a non-empty instance-relative path")
        return None
    relative = Path(profile_value)
    if relative.is_absolute() or ".." in relative.parts:
        errors.append(f"{label}: profile_file must stay inside the communications instance")
        return None
    if not isinstance(digest_value, str) or not re.fullmatch(r"[0-9a-f]{64}", digest_value):
        errors.append(f"{label}: profile_sha256 must be a lowercase SHA-256 digest")
        return None
    profile = instance / relative
    if not profile.is_file():
        errors.append(f"{label}: missing profile {profile_value}")
        return None
    actual = hashlib.sha256(profile.read_bytes()).hexdigest()
    if actual != digest_value:
        errors.append(f"{label}: stale profile_sha256 for {profile_value}")
    return profile_value, digest_value


def validate(workspace: Path, require_token: bool, check_cli: bool) -> dict[str, Any]:
    workspace = workspace.resolve()
    instance = workspace / "control-plane" / "communications"
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        instance / "policy.json",
        instance / "capabilities.json",
        instance / "state" / "schema.json",
        instance / "state" / "watermarks.json",
        instance / "state" / "message-ledger.jsonl",
        workspace / "docs" / "agents" / "communications.md",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"missing required path: {path}")

    policy = load_json(instance / "policy.json", errors) if (instance / "policy.json").exists() else {}
    capabilities = load_json(instance / "capabilities.json", errors) if (instance / "capabilities.json").exists() else {}
    for label, value in (("policy", policy), ("capabilities", capabilities)):
        for location in find_secret_key(value):
            errors.append(f"{label} contains forbidden secret field: {location}")

    rich = capabilities.get("rich_email_delivery")
    if not isinstance(rich, dict):
        errors.append("capabilities.rich_email_delivery must be an object")
        rich = {}
    expected = {
        "provider": "agentmail-cli",
        "credential_file": ".env",
        "credential_env": "AGENTMAIL_API_KEY",
    }
    for key, value in expected.items():
        if rich.get(key) != value:
            errors.append(f"rich_email_delivery.{key} must be {value!r}")
    reviewer = rich.get("review_recipient")
    allowlist = rich.get("allowed_recipients")
    if rich.get("status") == "verified":
        if not isinstance(rich.get("inbox_id"), str) or not rich.get("inbox_id"):
            errors.append("verified AgentMail capability requires inbox_id")
        if not isinstance(reviewer, str) or not EMAIL.match(reviewer):
            errors.append("verified AgentMail capability requires a valid review_recipient")
        if allowlist != [reviewer]:
            errors.append("AgentMail allowed_recipients must contain only review_recipient")
        if rich.get("credential_scope") != "inbox":
            errors.append("verified AgentMail capability requires an inbox-scoped credential")
        if rich.get("permissions") != ["draft_read", "draft_create", "draft_send"]:
            errors.append("AgentMail runtime permissions must be draft_read, draft_create, draft_send")
    else:
        warnings.append("AgentMail capability is not verified; live handoff remains blocked")

    mailbox = capabilities.get("delegated_mailbox_management")
    if not isinstance(mailbox, dict) or mailbox.get("provider") != "outlook-email":
        errors.append("delegated_mailbox_management.provider must be 'outlook-email'")
    elif mailbox.get("status") != "verified":
        warnings.append("Outlook capability is not verified; forward-draft creation remains blocked")

    env_path = workspace / ".env"
    gitignore = workspace / ".gitignore"
    ignored = gitignore.is_file() and any(
        line.strip() == ".env" for line in gitignore.read_text(encoding="utf-8").splitlines()
    )
    if not ignored:
        errors.append("workspace root .env must be ignored by Git")
    if env_path.is_file() and (env_path.stat().st_mode & 0o777) != 0o600:
        errors.append("workspace root .env must have mode 0600")
    token = dotenv_value(env_path, "AGENTMAIL_API_KEY")
    if require_token and not token:
        errors.append("AGENTMAIL_API_KEY is missing from workspace root .env")
    elif not token:
        warnings.append("AGENTMAIL_API_KEY is not configured")

    audiences = sorted((instance / "audiences").glob("*.json")) if (instance / "audiences").is_dir() else []
    if not audiences:
        warnings.append("no audience files are configured")
    for path in audiences:
        audience = load_json(path, errors)
        audience_binding = validate_profile_binding(instance, audience, str(path), errors)
        recipients = audience.get("recipients")
        if not isinstance(recipients, list) or not recipients:
            errors.append(f"{path}: recipients must be a non-empty list")
            continue
        for recipient in recipients:
            note_value = recipient.get("person_note") if isinstance(recipient, dict) else None
            if not isinstance(note_value, str) or not note_value:
                errors.append(f"{path}: every recipient requires person_note")
                continue
            note = workspace / note_value
            if not note.is_file():
                errors.append(f"{path}: missing People note {note_value}")
            elif not re.search(r"(?m)^email:\s*[^\s]+@[^\s]+$", note.read_text(encoding="utf-8")):
                errors.append(f"{path}: People note lacks frontmatter email: {note_value}")
        interest_value = audience.get("interest_file")
        if audience.get("kind") == "external":
            if not isinstance(interest_value, str) or not (instance / interest_value).is_file():
                errors.append(f"{path}: external audience requires a valid interest_file")
            else:
                interest_path = instance / interest_value
                interest = load_json(interest_path, errors)
                interest_binding = validate_profile_binding(instance, interest, str(interest_path), errors)
                if audience_binding != interest_binding:
                    errors.append(f"{path}: audience and interest manifests must bind the same profile")

    if check_cli:
        try:
            result = subprocess.run(
                ["agentmail", "--version"], check=False, capture_output=True, text=True, timeout=10
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            errors.append(f"AgentMail CLI check failed: {error}")
        else:
            installed = parse_version(result.stdout + result.stderr)
            minimum = parse_version(str(rich.get("minimum_version", "")))
            if result.returncode != 0 or installed is None or minimum is None or installed < minimum:
                errors.append("AgentMail CLI does not satisfy minimum_version")

    return {
        "status": "valid" if not errors else "invalid",
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "credential_file": ".env",
            "credential_present": bool(token),
            "audience_count": len(audiences),
            "profile_count": len(list((instance / "profiles").glob("*.md")))
            if (instance / "profiles").is_dir()
            else 0,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root", type=Path)
    parser.add_argument("--require-token", action="store_true")
    parser.add_argument("--check-cli", action="store_true")
    args = parser.parse_args()
    report = validate(args.workspace_root, args.require_token, args.check_cli)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
