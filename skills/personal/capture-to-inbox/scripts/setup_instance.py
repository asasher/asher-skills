#!/usr/bin/env python3
"""Materialize or reconcile a consumer-owned Capture to Inbox instance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

TEMPLATE_VERSION = "1.0.0"
INBOX_SEED = (
    "Dump unprocessed thoughts, tasks, links, reminders, emails, follow-ups, and vague notes here.\n"
)


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def ensure_local_secret_store(project: Path, created: list[str], updated: list[str]) -> None:
    env_path = project / ".env"
    if not env_path.exists():
        atomic_write(env_path, b"CAPTURE_TOKEN=\n", mode=0o600)
        created.append(str(env_path))
    else:
        current_mode = env_path.stat().st_mode & 0o777
        if current_mode != 0o600:
            os.chmod(env_path, 0o600)
            updated.append(f"{env_path}: permissions 0600")

    gitignore = project / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    ignored = any(line.strip() == ".env" for line in current.splitlines())
    if not ignored:
        separator = "" if not current or current.endswith("\n") else "\n"
        atomic_write(gitignore, f"{current}{separator}.env\n".encode("utf-8"))
        (updated if current else created).append(str(gitignore))


def candidate_path(path: Path, data: bytes) -> Path:
    base = path.with_name(f"{path.name}.setup-candidate")
    candidate = base
    index = 1
    while candidate.exists() and candidate.read_bytes() != data:
        candidate = base.with_name(f"{base.name}.{index}")
        index += 1
    if not candidate.exists():
        atomic_write(candidate, data)
    return candidate


def load_json_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def deep_defaults(current: Any, defaults: Any) -> Any:
    if not isinstance(current, dict) or not isinstance(defaults, dict):
        return current
    merged = dict(current)
    for key, value in defaults.items():
        if key not in merged:
            merged[key] = value
        elif isinstance(value, dict):
            merged[key] = deep_defaults(merged[key], value)
    return merged


def valid_config(value: dict[str, Any]) -> bool:
    paths = value.get("paths")
    capture = value.get("capture_to_inbox")
    token_file = capture.get("token_file") if isinstance(capture, dict) else None
    return (
        value.get("schema_version") == 1
        and isinstance(paths, dict)
        and all(isinstance(paths.get(key), str) and paths[key] for key in ("inbox", "attachments"))
        and isinstance(capture, dict)
        and all(
            isinstance(capture.get(key), str) and capture[key]
            for key in ("deployment", "token_env")
        )
        and (token_file is None or isinstance(token_file, str) and token_file)
    )


def valid_deployment(value: dict[str, Any]) -> bool:
    binding = value.get("provider_binding")
    return (
        value.get("schema_version") == 1
        and isinstance(value.get("provider"), str)
        and isinstance(value.get("api_url"), str)
        and isinstance(binding, dict)
        and all(isinstance(binding.get(key), str) for key in ("project", "environment", "service", "volume"))
    )


def valid_state(value: dict[str, Any]) -> bool:
    return value.get("schema_version") == 1


def ensure_json_skeleton(
    path: Path,
    defaults: dict[str, Any],
    validator: Callable[[dict[str, Any]], bool],
    created: list[str],
    conflicts: list[str],
) -> None:
    expected = json_bytes(defaults)
    if not path.exists():
        atomic_write(path, expected)
        created.append(str(path))
        return

    current = load_json_object(path)
    if current is not None and validator(current):
        return

    proposed = deep_defaults(current or {}, defaults)
    candidate = candidate_path(path, json_bytes(proposed if validator(proposed) else defaults))
    conflicts.append(f"{path}: invalid or incomplete JSON; candidate {candidate}")


def template_files(template_root: Path) -> list[Path]:
    files = []
    for path in sorted(template_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(template_root)
        if "node_modules" in relative.parts or path.name in {".env", ".DS_Store"}:
            continue
        files.append(relative)
    return files


def reconcile_api(
    template_root: Path,
    api_root: Path,
    manifest_path: Path,
    created: list[str],
    updated: list[str],
    conflicts: list[str],
) -> dict[str, Any]:
    previous = load_json_object(manifest_path) or {}
    previous_files = previous.get("files") if isinstance(previous.get("files"), dict) else {}
    records: dict[str, dict[str, Any]] = {}

    for relative in template_files(template_root):
        source = template_root / relative
        target = api_root / relative
        source_data = source.read_bytes()
        source_hash = sha256_bytes(source_data)
        old_record = previous_files.get(relative.as_posix(), {})
        old_managed_hash = old_record.get("managed_sha256") if isinstance(old_record, dict) else None

        if not target.exists():
            atomic_write(target, source_data, source.stat().st_mode & 0o777)
            created.append(str(target))
            managed_hash = source_hash
            status = "current"
        else:
            target_hash = sha256_file(target)
            if target_hash == source_hash:
                managed_hash = source_hash
                status = "current"
            elif old_managed_hash and target_hash == old_managed_hash:
                atomic_write(target, source_data, source.stat().st_mode & 0o777)
                updated.append(str(target))
                managed_hash = source_hash
                status = "current"
            else:
                candidate = candidate_path(target, source_data)
                conflicts.append(f"{target}: consumer edit preserved; candidate {candidate}")
                managed_hash = old_managed_hash
                status = "conflict"

        records[relative.as_posix()] = {
            "managed_sha256": managed_hash,
            "status": status,
            "template_sha256": source_hash,
        }

    return {
        "schema_version": 1,
        "template_version": TEMPLATE_VERSION,
        "source": "assets/capture-api",
        "files": records,
    }


def project_relative_path(project: Path, raw: str, flag: str) -> tuple[Path, str]:
    relative = Path(raw)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{flag} must be a project-relative path")
    resolved = (project / relative).resolve()
    if resolved != project and project not in resolved.parents:
        raise ValueError(f"{flag} resolves outside the project")
    return resolved, relative.as_posix().rstrip("/")


def setup(project: Path, instance_arg: str) -> tuple[int, dict[str, list[str]]]:
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")
    instance, instance_relative = project_relative_path(project, instance_arg, "--instance")
    capture_root = instance / "capture-to-inbox"
    api_root = capture_root / "api"
    shortcut_root = capture_root / "shortcut"
    template_manifest = capture_root / "template.json"
    template_root = Path(__file__).resolve().parents[1] / "assets" / "capture-api"
    if not template_root.is_dir():
        raise ValueError(f"API template is missing: {template_root}")

    report: dict[str, list[str]] = {"created": [], "updated": [], "conflicts": []}
    created = report["created"]
    updated = report["updated"]
    conflicts = report["conflicts"]

    ensure_local_secret_store(project, created, updated)

    inbox = project / "Inbox" / "INBOX.md"
    if not inbox.exists():
        atomic_write(inbox, INBOX_SEED.encode("utf-8"))
        created.append(str(inbox))

    shortcut_root.mkdir(parents=True, exist_ok=True)
    manifest = reconcile_api(template_root, api_root, template_manifest, created, updated, conflicts)
    atomic_write(template_manifest, json_bytes(manifest))

    deployment_relative = f"{instance_relative}/capture-to-inbox/deployment.json"
    config_defaults = {
        "schema_version": 1,
        "paths": {
            "attachments": "Attachments/Captures",
            "inbox": "Inbox/INBOX.md",
        },
        "capture_to_inbox": {
            "deployment": deployment_relative,
            "token_env": "CAPTURE_TOKEN",
            "token_file": ".env",
        },
    }
    deployment_defaults = {
        "schema_version": 1,
        "provider": "railway",
        "api_url": "",
        "provider_binding": {
            "project": "",
            "environment": "production",
            "service": "capture-api",
            "volume": "",
        },
    }
    ledger_defaults = {
        "schema_version": 1,
        "sources": {"capture-to-inbox": {"seen": []}},
    }
    setup_defaults = {
        "schema_version": 1,
        "capture_to_inbox": {
            "materialized": True,
            "local_secret": "pending",
            "external_dependency": "pending",
            "deployment": "pending",
            "shortcut": "pending",
            "smoke_test": "pending",
        },
    }

    ensure_json_skeleton(instance / "config.json", config_defaults, valid_config, created, conflicts)
    ensure_json_skeleton(capture_root / "deployment.json", deployment_defaults, valid_deployment, created, conflicts)
    ensure_json_skeleton(instance / "state" / "intake-ledger.json", ledger_defaults, valid_state, created, conflicts)
    ensure_json_skeleton(instance / "state" / "setup.json", setup_defaults, valid_state, created, conflicts)

    return (3 if conflicts else 0), report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="consumer project root")
    parser.add_argument(
        "--instance", default="control-plane", help="project-relative instance directory (default: control-plane)"
    )
    args = parser.parse_args(argv)
    try:
        status, report = setup(args.project, args.instance)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    for label in ("created", "updated", "conflicts"):
        for value in report[label]:
            print(f"{label[:-1] if label.endswith('s') else label}: {value}")
    if status:
        print("setup stopped at reconciliation conflicts; consumer files were preserved", file=sys.stderr)
    else:
        print("capture instance materialized; deployment, Shortcut build, and smoke test remain setup gates")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
