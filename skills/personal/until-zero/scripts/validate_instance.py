#!/usr/bin/env python3
"""Validate an Until Zero consumer instance without mutating it."""

from __future__ import annotations

import argparse
import json
import stat
import sys
from datetime import datetime
from pathlib import Path

from runway_core import COLLECTIONS, StateError, load_collection, load_json, validate_semantics
from until_zero import instance_paths, read_jsonl


def validate(project: Path, instance_argument: str) -> list[str]:
    findings: list[str] = []
    try:
        instance, state_dir, config = instance_paths(project, instance_argument)
    except (OSError, StateError, ValueError) as error:
        return [str(error)]
    for collection in COLLECTIONS:
        try:
            load_collection(state_dir, collection)
        except (OSError, StateError) as error:
            findings.append(str(error))
    for name in ("approvals", "audit"):
        try:
            read_jsonl(state_dir / f"{name}.jsonl")
        except (OSError, StateError) as error:
            findings.append(str(error))
    try:
        validate_semantics(state_dir, config)
    except (OSError, StateError, ValueError) as error:
        findings.append(str(error))
    if (state_dir / "apply-journal.json").exists():
        findings.append("incomplete apply journal exists; stop writers and use until_zero.py recover for the interrupted proposal")
    if (state_dir / "capture-journal.json").exists():
        findings.append("incomplete capture journal exists; rerun the capture operation to recover it")
    env_file = project.resolve() / str(config.get("capture", {}).get("token_file") or ".env")
    if not env_file.exists():
        findings.append(f"missing private token file: {env_file}")
    elif stat.S_IMODE(env_file.stat().st_mode) & 0o077:
        findings.append(f"private token file must be mode 0600: {env_file}")
    deployment = load_json(instance / "deployment.json")
    if not isinstance(deployment, dict) or deployment.get("schema_version") != 1:
        findings.append("deployment.json must be a schema_version 1 object")
    report = instance / "reports" / "current.html"
    if not report.exists():
        findings.append("reports/current.html is missing")
    else:
        document = report.read_text(encoding="utf-8")
        if "<script src=" in document or "<link rel=" in document:
            findings.append("reports/current.html must be self-contained")
    manifest = load_json(instance / "template.json")
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        findings.append("template.json must be a schema_version 1 object")
    setup = load_json(instance / "setup.json")
    expected_gates = {"materialized", "external_dependency", "deployment", "shortcut", "live_capture", "statement_reconciliation"}
    if not isinstance(setup, dict) or not isinstance(setup.get("gates"), dict):
        findings.append("setup.json must contain explicit effect gates")
    elif set(setup["gates"]) != expected_gates:
        findings.append("setup.json gates must match the current contract")
    else:
        for gate, record in setup["gates"].items():
            if not isinstance(record, dict) or record.get("status") not in {"pending", "complete", "blocked"} or not isinstance(record.get("evidence"), list):
                findings.append(f"setup gate {gate} must contain status and evidence")
            elif record["status"] in {"complete", "blocked"} and not record["evidence"]:
                findings.append(f"setup gate {gate} requires evidence for status {record['status']}")
            elif gate == "materialized" and not any(
                isinstance(item, dict) and item.get("kind") == "local_materialization" and item.get("template_version")
                for item in record["evidence"]
            ):
                findings.append("setup gate materialized requires template evidence")
            elif gate != "materialized" and record["status"] in {"complete", "blocked"} and not all(
                isinstance(item, dict) and str(item.get("kind") or "") and str(item.get("observed_at") or "")
                for item in record["evidence"]
            ):
                findings.append(f"setup gate {gate} contains invalid evidence")
            elif gate != "materialized" and record["status"] in {"complete", "blocked"}:
                try:
                    for item in record["evidence"]:
                        datetime.fromisoformat(str(item["observed_at"]).replace("Z", "+00:00"))
                except ValueError:
                    findings.append(f"setup gate {gate} evidence requires ISO observed_at timestamps")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--instance", default="until-zero")
    arguments = parser.parse_args(argv)
    try:
        findings = validate(arguments.project, arguments.instance)
    except (OSError, StateError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        return 1
    print("PASS: Until Zero instance is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
