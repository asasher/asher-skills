#!/usr/bin/env python3
"""Validate a Relay instance without exposing credentials."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from relay_common import EMAIL, dotenv_value, find_secret_keys, instance_root, load_json, normalize_address

VERSION = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def version(raw: str) -> tuple[int, int, int] | None:
    match = VERSION.search(raw)
    return tuple(int(part) for part in match.groups()) if match else None


def safe_load(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        return load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"{path}: {error}")
        return {}


def validate_profile(instance: Path, value: dict[str, Any], label: str, errors: list[str]) -> tuple[str, str] | None:
    file_value, digest = value.get("profile_file"), value.get("profile_sha256")
    if file_value is None and digest is None:
        return None
    if not isinstance(file_value, str) or not file_value:
        errors.append(f"{label}: profile_file is required")
        return None
    relative = Path(file_value)
    if relative.is_absolute() or ".." in relative.parts:
        errors.append(f"{label}: profile_file must stay inside the Relay instance")
        return None
    profile = instance / relative
    if not profile.is_file() or not isinstance(digest, str):
        errors.append(f"{label}: profile binding is incomplete")
        return None
    actual = hashlib.sha256(profile.read_bytes()).hexdigest()
    if actual != digest:
        errors.append(f"{label}: stale profile_sha256")
    return file_value, str(digest)


def validate(repo: Path, require_token: bool, check_cli: bool, require_ready: bool) -> dict[str, Any]:
    repo = repo.resolve()
    instance = instance_root(repo)
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        instance / "bindings.json", instance / "policy.json", instance / "capabilities.json",
        instance / "template-config.json", instance / "state" / "schema.json",
        repo / "docs" / "agents" / "relay.md",
    ]
    required.extend(instance / "state" / name for name in ("workflow.jsonl", "delivery.jsonl", "replies.jsonl", "watermarks.jsonl"))
    for path in required:
        if not path.exists():
            errors.append(f"missing required path: {path}")
    bindings = safe_load(instance / "bindings.json", errors) if (instance / "bindings.json").exists() else {}
    policy = safe_load(instance / "policy.json", errors) if (instance / "policy.json").exists() else {}
    capabilities = safe_load(instance / "capabilities.json", errors) if (instance / "capabilities.json").exists() else {}
    for label, value in (("bindings", bindings), ("policy", policy), ("capabilities", capabilities)):
        for location in find_secret_keys(value):
            errors.append(f"{label} contains forbidden secret field: {location}")
    if bindings.get("schema_version") != 2:
        errors.append("bindings.schema_version must be 2")
    projects = bindings.get("projects")
    providers = bindings.get("evidence_providers")
    recipes = bindings.get("section_recipes")
    audience_ids = bindings.get("audiences")
    if not isinstance(projects, list) or not projects:
        errors.append("bindings.projects must be non-empty")
    elif any(not isinstance(item, dict) or not item.get("id") or not item.get("root") for item in projects):
        errors.append("every bound project requires id and root")
    if not isinstance(providers, list) or not providers:
        errors.append("bindings.evidence_providers must be non-empty")
    elif any(not isinstance(item, dict) or not item.get("id") or not item.get("type") or not item.get("location") or not item.get("classes") for item in providers):
        errors.append("every evidence provider requires id, type, location, and classes")
    if not isinstance(recipes, dict) or any(not isinstance(recipes.get(key), list) or not recipes[key] for key in ("project_update", "internal_digest")):
        errors.append("both section recipes must be non-empty lists")
    if not isinstance(audience_ids, list) or not audience_ids:
        errors.append("bindings.audiences must be non-empty")
        audience_ids = []
    template = bindings.get("template")
    if not isinstance(template, dict) or not template.get("id") or not template.get("version") or template.get("root") != "relay/templates":
        errors.append("bindings.template must identify the local Relay renderer")
    if bindings.get("reconciliation_mode") not in {"manual", "webhook"}:
        errors.append("bindings.reconciliation_mode must be manual or webhook")

    delivery = policy.get("delivery") if isinstance(policy, dict) else None
    if not isinstance(delivery, dict) or not EMAIL.fullmatch(str(delivery.get("operator_address", "")).lower()):
        errors.append("policy.delivery.operator_address must be valid")
    if isinstance(delivery, dict) and (delivery.get("automatic_resend") is not False or delivery.get("automatic_reply") is not False):
        errors.append("automatic resend and reply must be false")

    for audience_id in audience_ids:
        path = instance / "audiences" / f"{audience_id}.json"
        if not path.is_file():
            errors.append(f"missing audience manifest: {audience_id}")
            continue
        audience = safe_load(path, errors)
        binding = validate_profile(instance, audience, str(path), errors)
        recipients = audience.get("recipients")
        if not isinstance(recipients, list) or not recipients:
            errors.append(f"{path}: recipients must be non-empty")
        else:
            seen: set[str] = set()
            if not any(isinstance(item, dict) and item.get("header") == "to" for item in recipients):
                errors.append(f"{path}: at least one To recipient is required")
            for item in recipients:
                if not isinstance(item, dict) or item.get("header") not in {"to", "cc"}:
                    errors.append(f"{path}: every recipient requires header to|cc")
                    continue
                try:
                    address = normalize_address(str(item.get("address", "")))
                except ValueError:
                    errors.append(f"{path}: invalid recipient address")
                    continue
                if address in seen:
                    errors.append(f"{path}: duplicate recipient across headers")
                seen.add(address)
        interest_file = audience.get("interest_file")
        if not isinstance(interest_file, str) or not (instance / interest_file).is_file():
            errors.append(f"{path}: valid interest_file is required")
        else:
            interest = safe_load(instance / interest_file, errors)
            if validate_profile(instance, interest, interest_file, errors) != binding:
                errors.append(f"{path}: audience and interest must bind the same profile")

    agentmail = capabilities.get("agentmail") if isinstance(capabilities, dict) else None
    if not isinstance(agentmail, dict):
        errors.append("capabilities.agentmail must be an object")
        agentmail = {}
    for key, expected in (("provider", "agentmail-cli"), ("credential_file", ".env"), ("credential_env", "AGENTMAIL_API_KEY")):
        if agentmail.get(key) != expected:
            errors.append(f"capabilities.agentmail.{key} must be {expected!r}")
    if agentmail.get("event_mode") not in {"manual", "webhook"}:
        errors.append("AgentMail event_mode must be manual or webhook")
    if agentmail.get("event_mode") == "webhook" and agentmail.get("webhook_signature_verified") is not True:
        errors.append("webhook mode requires signature verification")
    if require_ready or agentmail.get("status") == "verified":
        for key in ("inbox_id", "sender"):
            if not isinstance(agentmail.get(key), str) or not agentmail[key]:
                errors.append(f"verified AgentMail requires {key}")
        if agentmail.get("sender_verified") is not True:
            errors.append("selected AgentMail sender is not verified")
        if agentmail.get("credential_scope") != "inbox" or not agentmail.get("permissions"):
            errors.append("verified AgentMail requires effect-verified inbox scope and permissions")
    else:
        warnings.append("AgentMail is not verified; live send remains blocked")

    env = repo / ".env"
    ignored = (repo / ".gitignore").is_file() and ".env" in {line.strip() for line in (repo / ".gitignore").read_text(encoding="utf-8").splitlines()}
    if not ignored:
        errors.append("repository-root .env must be ignored by Git")
    if env.is_file() and (env.stat().st_mode & 0o777) != 0o600:
        errors.append("repository-root .env must have mode 0600")
    token = dotenv_value(env, "AGENTMAIL_API_KEY")
    if require_token and not token:
        errors.append("AGENTMAIL_API_KEY is missing from repository-root .env")
    if check_cli:
        try:
            result = subprocess.run(["agentmail", "--version"], capture_output=True, text=True, timeout=10, check=False)
            installed, minimum = version(result.stdout + result.stderr), version(str(agentmail.get("minimum_version", "")))
            if result.returncode or installed is None or minimum is None or installed < minimum:
                errors.append("AgentMail CLI does not satisfy minimum_version")
        except (OSError, subprocess.TimeoutExpired) as error:
            errors.append(f"AgentMail CLI check failed: {error}")
    if require_ready:
        for command, minimum in (("node", (20, 0, 0)), ("npm", (10, 0, 0))):
            executable = shutil.which(command)
            minimum_text = ".".join(map(str, minimum))
            if not executable:
                errors.append(f"Relay renderer requires {command} >= {minimum_text}")
                continue
            try:
                result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10, check=False)
                installed = version(result.stdout + result.stderr)
                if result.returncode or installed is None or installed < minimum:
                    errors.append(f"Relay renderer requires {command} >= {minimum_text}")
            except (OSError, subprocess.TimeoutExpired) as error:
                errors.append(f"Relay renderer {command} check failed: {error}")
    return {"status": "valid" if not errors else "invalid", "errors": errors, "warnings": warnings, "checks": {"credential_present": bool(token), "project_count": len(projects or []), "provider_count": len(providers or []), "audience_count": len(audience_ids)}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--require-token", action="store_true")
    parser.add_argument("--check-cli", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    report = validate(args.repository_root, args.require_token, args.check_cli, args.require_ready)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
