#!/usr/bin/env python3
"""Shared stdlib primitives for Relay's deterministic scripts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SECRET_KEYS = {"api_key", "apikey", "access_token", "refresh_token", "secret", "token"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def pretty_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def now() -> str:
    fixed = os.environ.get("RELAY_NOW")
    return fixed or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    values: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{number}: expected object")
        values.append(value)
    return values


def append_event(path: Path, value: dict[str, Any]) -> bool:
    key = value.get("idempotency_key")
    if key and any(item.get("idempotency_key") == key for item in read_jsonl(path)):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (canonical_json(value) + "\n").encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return True


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


def normalize_address(value: str) -> str:
    normalized = value.strip().lower()
    if not EMAIL.fullmatch(normalized):
        raise ValueError("invalid email address")
    return normalized


def normalize_recipients(values: Iterable[str]) -> list[str]:
    return sorted({normalize_address(value) for value in values})


def recipient_hash(address: str) -> str:
    return sha256_bytes(normalize_address(address).encode())


def recipient_manifest_hash(to: list[str], cc: list[str]) -> str:
    return sha256_bytes(canonical_json({"to": normalize_recipients(to), "cc": normalize_recipients(cc)}).encode())


def find_secret_keys(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            location = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower().replace("-", "_") in SECRET_KEYS:
                findings.append(location)
            findings.extend(find_secret_keys(child, location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_secret_keys(child, f"{prefix}[{index}]"))
    return findings


def instance_root(repo: Path) -> Path:
    return repo.resolve() / "relay"


def local_template_identity(instance: Path) -> dict[str, Any]:
    binding = load_json(instance / "bindings.json").get("template", {})
    files: dict[str, str] = {}
    for root in (instance / "templates", instance / "scripts"):
        if root.is_dir():
            for path in sorted(root.rglob("*")):
                if path.is_file() and ".setup-candidate" not in path.name and "__pycache__" not in path.parts and path.suffix != ".pyc":
                    files[path.relative_to(instance).as_posix()] = sha256_file(path)
    config = instance / "template-config.json"
    if config.is_file():
        files[config.relative_to(instance).as_posix()] = sha256_file(config)
    return {"id": binding.get("id"), "version": binding.get("version"), "files": files}


def build_approval_manifest(repo: Path, run: Path) -> dict[str, Any]:
    repo = repo.resolve()
    run = run.resolve()
    instance = instance_root(repo)
    bag = load_json(run / "bag.json")
    html = run / "rendered-email.html"
    text = run / "rendered-email.txt"
    light = run / "rendered-email-light.html"
    dark = run / "rendered-email-dark.html"
    for path in (html, text, light, dark):
        if not path.is_file():
            raise ValueError(f"missing rendered artifact: {path.name}")
    to = normalize_recipients(bag.get("recipients", {}).get("to", []))
    cc = normalize_recipients(bag.get("recipients", {}).get("cc", []))
    if set(to) & set(cc):
        raise ValueError("recipient appears in both To and CC")
    evidence = bag.get("evidence", [])
    evidence_summary = [
        {key: item.get(key) for key in ("id", "source", "observed_at", "status", "project_id", "feature")}
        for item in evidence if isinstance(item, dict)
    ]
    manifest = {
        "schema_version": 1,
        "communication_id": bag.get("id"),
        "audience_id": bag.get("audience_id"),
        "project_ids": bag.get("project_ids"),
        "subject": bag.get("subject"),
        "sender": normalize_address(str(bag.get("sender", ""))),
        "recipients": {"to": to, "cc": cc},
        "recipient_hash": recipient_manifest_hash(to, cc),
        "content": {"html_sha256": sha256_file(html), "text_sha256": sha256_file(text)},
        "previews": {"light_sha256": sha256_file(light), "dark_sha256": sha256_file(dark)},
        "bag_sha256": sha256_file(run / "bag.json"),
        "evidence": evidence_summary,
        "evidence_sha256": sha256_bytes(canonical_json(evidence_summary).encode()),
        "template": local_template_identity(instance),
    }
    manifest["manifest_sha256"] = sha256_bytes(canonical_json(manifest).encode())
    manifest["client_id"] = "relay-" + manifest["manifest_sha256"][:32]
    return manifest


def workflow_event(repo: Path, manifest: dict[str, Any], state: str, **facts: Any) -> dict[str, Any]:
    basis = {"state": state, "communication_id": manifest["communication_id"], **facts}
    return {
        "schema_version": 1,
        "timestamp": now(),
        "communication_id": manifest["communication_id"],
        "audience_id": manifest["audience_id"],
        "state": state,
        "manifest_sha256": manifest["manifest_sha256"],
        "idempotency_key": sha256_bytes(canonical_json(basis).encode()),
        **facts,
    }
