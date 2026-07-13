#!/usr/bin/env python3
"""Materialize a consumer-owned manage-communications instance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


TEMPLATE_VERSION = "1.0.0"


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def candidate_path(target: Path, data: bytes) -> Path:
    candidate = target.with_name(f"{target.name}.setup-candidate")
    index = 1
    while candidate.exists() and candidate.read_bytes() != data:
        candidate = target.with_name(f"{target.name}.setup-candidate.{index}")
        index += 1
    if not candidate.exists():
        atomic_write(candidate, data)
    return candidate


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


def template_files(root: Path) -> list[Path]:
    return [
        path.relative_to(root)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name not in {".DS_Store", ".env"}
    ]


def setup(workspace: Path, instance_relative: Path) -> dict[str, Any]:
    workspace = workspace.resolve()
    if not workspace.is_dir():
        raise ValueError(f"workspace does not exist: {workspace}")
    if instance_relative.is_absolute() or ".." in instance_relative.parts:
        raise ValueError("--instance must be workspace-relative")

    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "templates" / "instance"
    instance = workspace / instance_relative
    report: dict[str, Any] = {
        "created": [],
        "preserved": [],
        "candidates": [],
        "credential": {},
    }
    records: dict[str, Any] = {}

    for relative in template_files(template_root):
        source = template_root / relative
        target = instance / relative
        data = source.read_bytes()
        digest = sha256(data)
        if not target.exists():
            atomic_write(target, data, source.stat().st_mode & 0o777)
            report["created"].append(str(target))
            status = "current"
        elif target.read_bytes() == data:
            report["preserved"].append(str(target))
            status = "current"
        else:
            candidate = candidate_path(target, data)
            report["preserved"].append(str(target))
            report["candidates"].append(str(candidate))
            status = "consumer_modified"
        records[relative.as_posix()] = {"template_sha256": digest, "status": status}

    for directory in ("audiences", "interests", "state", "runs"):
        (instance / directory).mkdir(parents=True, exist_ok=True)
    ledger = instance / "state" / "message-ledger.jsonl"
    if not ledger.exists():
        atomic_write(ledger, b"")
        report["created"].append(str(ledger))

    manifest = instance / "template.json"
    manifest_was_missing = not manifest.exists()
    manifest_data = json_bytes(
        {
            "schema_version": 1,
            "source": "templates/instance",
            "template_version": TEMPLATE_VERSION,
            "files": records,
        }
    )
    if not manifest.exists() or manifest.read_bytes() != manifest_data:
        atomic_write(manifest, manifest_data)
        report["created" if manifest_was_missing else "preserved"].append(str(manifest))

    playbook_source = skill_root / "templates" / "communications.md"
    playbook = workspace / "docs" / "agents" / "communications.md"
    if not playbook.exists():
        atomic_write(playbook, playbook_source.read_bytes())
        report["created"].append(str(playbook))
    else:
        report["preserved"].append(str(playbook))

    env_path = workspace / ".env"
    ignored = False
    gitignore = workspace / ".gitignore"
    if gitignore.is_file():
        ignored = any(line.strip() == ".env" for line in gitignore.read_text(encoding="utf-8").splitlines())
    report["credential"] = {
        "file": ".env",
        "exists": env_path.is_file(),
        "gitignored": ignored,
        "mode_0600": env_path.is_file() and (env_path.stat().st_mode & 0o777) == 0o600,
        "AGENTMAIL_API_KEY": "present" if dotenv_value(env_path, "AGENTMAIL_API_KEY") else "missing",
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root", type=Path)
    parser.add_argument("--instance", type=Path, default=Path("control-plane/communications"))
    args = parser.parse_args()
    try:
        report = setup(args.workspace_root, args.instance)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2
    print(json.dumps({"status": "ok", **report}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
