#!/usr/bin/env python3
"""Validate a schema-version-2 Relay bag."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from relay_common import normalize_address

STATUSES = {"production_verified", "shipped_unverified", "in_progress", "pending", "planned"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["bag must be a JSON object"]
    if value.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    for key in ("id", "generated_at", "subject", "preheader", "audience_id", "sender", "summary"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    try:
        normalize_address(str(value.get("sender", "")))
    except ValueError:
        errors.append("sender must be a valid address")
    if value.get("kind") not in {"project_update", "internal_digest"}:
        errors.append("kind must be project_update or internal_digest")
    if not isinstance(value.get("project_ids"), list) or not value["project_ids"] or not all(nonempty(item) for item in value["project_ids"]):
        errors.append("project_ids must be a non-empty string list")
    recipients = value.get("recipients")
    if not isinstance(recipients, dict):
        errors.append("recipients must be an object")
    else:
        normalized: dict[str, set[str]] = {}
        for header in ("to", "cc"):
            items = recipients.get(header)
            if not isinstance(items, list) or (header == "to" and not items):
                errors.append(f"recipients.{header} must be {'a non-empty' if header == 'to' else 'a'} list")
                continue
            try:
                addresses = [normalize_address(str(item)) for item in items]
            except ValueError:
                errors.append(f"recipients.{header} contains an invalid address")
                continue
            if addresses != sorted(set(addresses)):
                errors.append(f"recipients.{header} must be normalized, unique, and sorted")
            normalized[header] = set(addresses)
        if normalized.get("to", set()) & normalized.get("cc", set()):
            errors.append("To and CC must be disjoint")
    evidence = value.get("evidence")
    evidence_ids: set[str] = set()
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict) or not nonempty(item.get("id")):
                errors.append(f"evidence[{index}] requires id")
                continue
            if item["id"] in evidence_ids:
                errors.append(f"duplicate evidence id: {item['id']}")
            evidence_ids.add(item["id"])
            for key in ("source", "observed_at", "project_id", "feature"):
                if not nonempty(item.get(key)):
                    errors.append(f"evidence[{index}].{key} is required")
            if item.get("status") not in STATUSES:
                errors.append(f"evidence[{index}] has invalid status")
    sections = value.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections must be a non-empty list")
        return errors
    for s_index, section in enumerate(sections):
        if not isinstance(section, dict) or not nonempty(section.get("title")):
            errors.append(f"sections[{s_index}] requires title")
            continue
        items = section.get("items")
        if not isinstance(items, list):
            errors.append(f"sections[{s_index}].items must be a list")
            continue
        for i_index, item in enumerate(items):
            prefix = f"sections[{s_index}].items[{i_index}]"
            if not isinstance(item, dict) or item.get("status") not in STATUSES:
                errors.append(f"{prefix} has invalid status")
                continue
            if not nonempty(item.get("title")) or not nonempty(item.get("detail")):
                errors.append(f"{prefix} requires title and detail")
            refs = item.get("evidence_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{prefix}.evidence_ids must be non-empty")
            elif any(ref not in evidence_ids for ref in refs):
                errors.append(f"{prefix} references unknown evidence")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bag", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.bag.read_text(encoding="utf-8"))
        errors = validate(value)
    except (OSError, json.JSONDecodeError) as error:
        errors = [str(error)]
    print(json.dumps({"status": "valid" if not errors else "invalid", "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
