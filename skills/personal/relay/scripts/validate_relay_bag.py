#!/usr/bin/env python3
"""Validate a schema-version-2 Relay bag."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from relay_common import instance_root, load_json, normalize_address, normalize_recipients

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


def validate_against_instance(value: Any, repository_root: Path) -> list[str]:
    """Validate a structurally valid bag against consumer-owned Relay bindings."""
    if not isinstance(value, dict):
        return ["bag must be a JSON object"]
    instance = instance_root(repository_root)
    try:
        bindings = load_json(instance / "bindings.json")
        policy = load_json(instance / "policy.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"cannot load Relay bindings: {error}"]
    audience_id = value.get("audience_id")
    if not isinstance(audience_id, str) or audience_id not in bindings.get("audiences", []):
        return ["audience_id is not present in bindings.audiences"]
    try:
        audience = load_json(instance / "audiences" / f"{audience_id}.json")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [f"cannot load audience binding {audience_id}: {error}"]
    errors: list[str] = []
    if audience.get("id") != audience_id:
        errors.append("audience manifest id does not match audience_id")
    if value.get("kind") != audience.get("message_kind"):
        errors.append("kind does not match audience binding")
    expected_projects = sorted(set(audience.get("project_ids", [])))
    if value.get("project_ids") != expected_projects:
        errors.append("project_ids do not match audience binding")
    for field in ("subject", "preheader", "summary"):
        if value.get(field) != audience.get(field):
            errors.append(f"{field} does not match audience binding")
    try:
        expected_sender = normalize_address(str(audience.get("sender", "")))
        actual_sender = normalize_address(str(value.get("sender", "")))
        if actual_sender != expected_sender:
            errors.append("sender does not match audience binding")
    except ValueError:
        errors.append("audience binding contains an invalid sender")

    expected_headers: dict[str, list[str]] = {"to": [], "cc": []}
    try:
        for recipient in audience.get("recipients", []):
            if isinstance(recipient, dict) and recipient.get("header") in expected_headers:
                expected_headers[recipient["header"]].append(normalize_address(str(recipient.get("address", ""))))
        delivery = policy.get("delivery", {})
        if (
            audience.get("kind") == "external"
            and audience.get("operator_cc", "default") != "disabled"
            and delivery.get("operator_cc_default")
        ):
            expected_headers["cc"].append(normalize_address(str(delivery.get("operator_address", ""))))
        expected_headers = {header: normalize_recipients(addresses) for header, addresses in expected_headers.items()}
    except ValueError:
        errors.append("audience or operator binding contains an invalid recipient")
        expected_headers = {"to": [], "cc": []}
    actual_headers = value.get("recipients")
    if isinstance(actual_headers, dict):
        try:
            actual_headers = {
                header: normalize_recipients(actual_headers.get(header, []))
                for header in ("to", "cc")
            }
        except ValueError:
            actual_headers = None
    if actual_headers != expected_headers:
        errors.append("recipients do not match audience and operator bindings")

    recipe = audience.get("section_recipe") or bindings.get("section_recipes", {}).get(audience.get("message_kind"))
    sections = value.get("sections")
    actual_titles = [section.get("title") for section in sections if isinstance(section, dict)] if isinstance(sections, list) else []
    if actual_titles != recipe:
        errors.append("section order does not match audience binding")

    interest_file = audience.get("interest_file")
    interest_path = Path(str(interest_file))
    if interest_path.is_absolute() or ".." in interest_path.parts:
        errors.append("audience interest_file must stay inside the Relay instance")
        return errors
    try:
        interest = load_json(instance / interest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"cannot load audience interest binding: {error}")
        return errors
    allowed_features = set(interest.get("features", []))
    allowed_projects = set(expected_projects)
    for index, item in enumerate(value.get("evidence", [])):
        if not isinstance(item, dict):
            continue
        if item.get("project_id") not in allowed_projects:
            errors.append(f"evidence[{index}].project_id is outside the audience binding")
        if item.get("feature") not in allowed_features:
            errors.append(f"evidence[{index}].feature is outside the interest binding")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bag", type=Path)
    parser.add_argument("--repository-root", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.bag.read_text(encoding="utf-8"))
        errors = validate(value)
        if not errors and args.repository_root:
            errors.extend(validate_against_instance(value, args.repository_root))
    except (OSError, json.JSONDecodeError) as error:
        errors = [str(error)]
    print(json.dumps({"status": "valid" if not errors else "invalid", "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
