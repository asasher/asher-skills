#!/usr/bin/env python3
"""Materialize or reconcile a consumer-owned Until Zero instance."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from runway_core import atomic_write, atomic_write_json, canonical_bytes, sha256_file

TEMPLATE_VERSION = "1.0.0"
SECRET_LINES = ("RUNWAY_PRODUCER_TOKEN=", "RUNWAY_DRAIN_TOKEN=", "RUNWAY_API_ORIGIN=")
GATES = ("materialized", "external_dependency", "deployment", "shortcut", "live_capture", "statement_reconciliation")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def candidate_path(path: Path, data: bytes) -> Path:
    candidate = path.with_name(f"{path.name}.setup-candidate")
    index = 1
    while candidate.exists() and candidate.read_bytes() != data:
        candidate = path.with_name(f"{path.name}.setup-candidate.{index}")
        index += 1
    if not candidate.exists():
        atomic_write(candidate, data)
    return candidate


def project_relative(project: Path, value: str) -> tuple[Path, str]:
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("--instance must be a project-relative path")
    resolved = (project / relative).resolve()
    if resolved != project and project not in resolved.parents:
        raise ValueError("--instance resolves outside the project")
    return resolved, relative.as_posix().rstrip("/")


def ensure_secrets(project: Path, instance_relative: str, created: list[str], updated: list[str]) -> None:
    env_file = project / ".env"
    if env_file.exists():
        existing = env_file.read_text(encoding="utf-8")
        lines = existing.splitlines()
        additions = [line for line in SECRET_LINES if not any(item.startswith(line) for item in lines)]
        if additions:
            separator = "" if not existing or existing.endswith("\n") else "\n"
            atomic_write(env_file, f"{existing}{separator}{chr(10).join(additions)}\n".encode("utf-8"), 0o600)
            updated.append(str(env_file))
        elif env_file.stat().st_mode & 0o777 != 0o600:
            os.chmod(env_file, 0o600)
            updated.append(f"{env_file}: permissions 0600")
    else:
        atomic_write(env_file, ("\n".join(SECRET_LINES) + "\n").encode("utf-8"), 0o600)
        created.append(str(env_file))

    gitignore = project / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    required = [".env", f"{instance_relative}/shortcut/*.shortcut"]
    missing = [line for line in required if line not in current.splitlines()]
    if missing:
        separator = "" if not current or current.endswith("\n") else "\n"
        atomic_write(gitignore, f"{current}{separator}{chr(10).join(missing)}\n".encode("utf-8"))
        (updated if current else created).append(str(gitignore))


def template_files(root: Path) -> list[Path]:
    return [path.relative_to(root) for path in sorted(root.rglob("*")) if path.is_file() and "node_modules" not in path.parts]


def reconcile_api(template: Path, target: Path, manifest_path: Path, report: dict[str, list[str]]) -> dict[str, Any]:
    previous = load_object(manifest_path) or {}
    previous_files = previous.get("files") if isinstance(previous.get("files"), dict) else {}
    records: dict[str, dict[str, Any]] = {}
    for relative in template_files(template):
        source = template / relative
        destination = target / relative
        data = source.read_bytes()
        template_hash = sha256_bytes(data)
        old_record = previous_files.get(relative.as_posix(), {})
        old_managed_hash = old_record.get("managed_sha256") if isinstance(old_record, dict) else None
        if not destination.exists():
            atomic_write(destination, data, source.stat().st_mode & 0o777)
            report["created"].append(str(destination))
            managed_hash = template_hash
            status = "current"
        else:
            destination_hash = sha256_file(destination)
            if destination_hash == template_hash:
                managed_hash = template_hash
                status = "current"
            elif old_managed_hash and destination_hash == old_managed_hash:
                atomic_write(destination, data, source.stat().st_mode & 0o777)
                report["updated"].append(str(destination))
                managed_hash = template_hash
                status = "current"
            else:
                candidate = candidate_path(destination, data)
                report["conflicts"].append(f"{destination}: consumer edit preserved; candidate {candidate}")
                managed_hash = old_managed_hash
                status = "conflict"
        records[relative.as_posix()] = {"managed_sha256": managed_hash, "status": status, "template_sha256": template_hash}
    return {"schema_version": 1, "template_version": TEMPLATE_VERSION, "source": "assets/runway-api", "files": records}


def ensure_file(path: Path, data: bytes, report: dict[str, list[str]], mode: int = 0o644) -> None:
    if not path.exists():
        atomic_write(path, data, mode)
        report["created"].append(str(path))


def ensure_json(path: Path, default: dict[str, Any], report: dict[str, list[str]]) -> None:
    if not path.exists():
        atomic_write_json(path, default)
        report["created"].append(str(path))
        return
    current = load_object(path)
    if current is None or current.get("schema_version") != 1:
        candidate = candidate_path(path, canonical_bytes(default))
        report["conflicts"].append(f"{path}: invalid state preserved; candidate {candidate}")


def setup(project: Path, instance_argument: str) -> tuple[int, dict[str, list[str]]]:
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")
    instance, instance_relative = project_relative(project, instance_argument)
    skill = Path(__file__).resolve().parents[1]
    api_template = skill / "assets" / "runway-api"
    report: dict[str, list[str]] = {"created": [], "updated": [], "conflicts": []}
    ensure_secrets(project, instance_relative, report["created"], report["updated"])

    for directory in (instance / "state", instance / "proposals", instance / "reports", instance / "shortcut"):
        directory.mkdir(parents=True, exist_ok=True)
    manifest_path = instance / "template.json"
    manifest = reconcile_api(api_template, instance / "api", manifest_path, report)
    atomic_write_json(manifest_path, manifest)

    config = {
        "schema_version": 1,
        "base_currency": "AED",
        "buffer_minor": "0",
        "horizon_days": 365,
        "paths": {
            "state": f"{instance_relative}/state",
            "proposals": f"{instance_relative}/proposals",
            "reports": f"{instance_relative}/reports",
            "deployment": f"{instance_relative}/deployment.json",
            "shortcut": f"{instance_relative}/shortcut",
        },
        "capture": {
            "producer_token_env": "RUNWAY_PRODUCER_TOKEN",
            "drain_token_env": "RUNWAY_DRAIN_TOKEN",
            "token_file": ".env",
            "worker_id": "until-zero-local",
        },
    }
    deployment = {
        "schema_version": 1,
        "provider": "railway",
        "api_url": "",
        "verified_origin": "",
        "verification_status": "pending",
        "provider_binding": {"project": "", "environment": "production", "service": "runway-api", "volume": ""},
    }
    setup_state = {
        "schema_version": 1,
        "gates": {
            "materialized": {"status": "complete", "evidence": [{"kind": "local_materialization", "template_version": TEMPLATE_VERSION}]},
            "external_dependency": {"status": "pending", "evidence": []},
            "deployment": {"status": "pending", "evidence": []},
            "shortcut": {"status": "pending", "evidence": []},
            "live_capture": {"status": "pending", "evidence": []},
            "statement_reconciliation": {"status": "pending", "evidence": []},
        },
    }
    ensure_json(instance / "config.json", config, report)
    ensure_json(instance / "deployment.json", deployment, report)
    ensure_json(instance / "setup.json", setup_state, report)
    for name in ("accounts", "rules", "events", "fx_rates", "transactions", "pending_captures"):
        ensure_json(instance / "state" / f"{name}.json", {"schema_version": 1, "items": []}, report)
    ensure_file(instance / "state" / "approvals.jsonl", b"", report, 0o600)
    ensure_file(instance / "state" / "audit.jsonl", b"", report, 0o600)
    ensure_file(instance / "reports" / "current.html", (skill / "assets" / "initial-report.html").read_bytes(), report)
    return (3 if report["conflicts"] else 0), report


def update_gate(project: Path, instance_argument: str, gate: str, status: str, evidence_path: Path | None) -> dict[str, Any]:
    instance, _ = project_relative(project.resolve(), instance_argument)
    setup_path = instance / "setup.json"
    setup_state = load_object(setup_path)
    if not setup_state or setup_state.get("schema_version") != 1 or not isinstance(setup_state.get("gates"), dict):
        raise ValueError("run setup before updating an effect gate")
    if gate == "materialized" or gate not in GATES:
        raise ValueError("materialized is managed by setup; choose an external effect gate")
    evidence: dict[str, Any] | None = None
    if evidence_path is not None:
        evidence = load_object(evidence_path)
        if not evidence or not str(evidence.get("kind") or "") or not str(evidence.get("observed_at") or ""):
            raise ValueError("gate evidence must be an object with kind and observed_at")
        try:
            datetime.fromisoformat(str(evidence["observed_at"]).replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("gate evidence observed_at must be an ISO timestamp") from error
    if status in {"complete", "blocked"} and evidence is None:
        raise ValueError(f"{status} requires --evidence")
    record = setup_state["gates"].get(gate)
    if not isinstance(record, dict) or not isinstance(record.get("evidence"), list):
        raise ValueError(f"invalid existing gate record: {gate}")
    record["status"] = status
    if status == "pending":
        record["evidence"] = []
    elif evidence not in record["evidence"]:
        record["evidence"].append(evidence)
    atomic_write_json(setup_path, setup_state)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="consumer project root")
    parser.add_argument("--instance", default="until-zero", help="project-relative instance directory")
    parser.add_argument("--set-gate", choices=GATES[1:])
    parser.add_argument("--status", choices=("pending", "complete", "blocked"))
    parser.add_argument("--evidence", type=Path)
    arguments = parser.parse_args(argv)
    try:
        if arguments.set_gate:
            if not arguments.status:
                parser.error("--set-gate requires --status")
            record = update_gate(arguments.project, arguments.instance, arguments.set_gate, arguments.status, arguments.evidence)
            print(json.dumps({"gate": arguments.set_gate, **record}, indent=2, sort_keys=True))
            return 0
        if arguments.status or arguments.evidence:
            parser.error("--status and --evidence require --set-gate")
        status, report = setup(arguments.project, arguments.instance)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    for label in ("created", "updated", "conflicts"):
        for item in report[label]:
            print(f"{label[:-1]}: {item}")
    if status:
        print("setup stopped at reconciliation conflicts; consumer files were preserved", file=sys.stderr)
    else:
        print("until-zero instance materialized; external dependency, deployment, Shortcut, and live verification gates remain pending")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
