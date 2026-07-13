#!/usr/bin/env python3
"""Validate the portable comms-bag contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STATUSES = {"production_verified", "shipped_unverified", "in_progress", "pending", "planned"}
INTERNAL_SECTIONS = ["Delivery", "Pending", "Cash", "Growth"]


def valid_internal_sections(sections: list[Any]) -> bool:
    """Accept the lens layout or project/client delivery groups followed by Cash and Growth."""
    titles = [section.get("title") for section in sections if isinstance(section, dict)]
    if titles == INTERNAL_SECTIONS:
        return True
    if len(titles) < 3 or titles[-2:] != ["Cash", "Growth"]:
        return False
    delivery_sections = sections[:-2]
    return all(
        isinstance(section, dict)
        and nonempty(section.get("title"))
        and nonempty(section.get("subtitle"))
        and section.get("title") not in INTERNAL_SECTIONS
        for section in delivery_sections
    )


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["bag must be a JSON object"]
    if value.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for key in ("id", "generated_at", "subject", "preheader", "audience_id", "summary"):
        if not nonempty(value.get(key)):
            errors.append(f"{key} must be a non-empty string")
    if value.get("kind") not in {"project_update", "internal_digest"}:
        errors.append("kind must be project_update or internal_digest")
    if not isinstance(value.get("project_ids"), list) or not all(nonempty(item) for item in value["project_ids"]):
        errors.append("project_ids must be a list of non-empty strings")

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
            if item.get("status") not in STATUSES:
                errors.append(f"evidence[{index}] has invalid status")

    sections = value.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("sections must be a non-empty list")
        return errors
    if value.get("kind") == "internal_digest" and not valid_internal_sections(sections):
        errors.append(
            "internal_digest sections must be Delivery, Pending, Cash, Growth in order, "
            "or project/client sections followed by Cash and Growth"
        )
    for section_index, section in enumerate(sections):
        if not isinstance(section, dict) or not nonempty(section.get("title")):
            errors.append(f"sections[{section_index}] requires title")
            continue
        items = section.get("items")
        if not isinstance(items, list):
            errors.append(f"sections[{section_index}].items must be a list")
            continue
        for item_index, item in enumerate(items):
            prefix = f"sections[{section_index}].items[{item_index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            if item.get("status") not in STATUSES:
                errors.append(f"{prefix} has invalid status")
            for key in ("title", "detail"):
                if not nonempty(item.get(key)):
                    errors.append(f"{prefix}.{key} must be non-empty")
            refs = item.get("evidence_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{prefix}.evidence_ids must be non-empty")
            else:
                for evidence_id in refs:
                    if evidence_id not in evidence_ids:
                        errors.append(f"{prefix} references unknown evidence id: {evidence_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bag", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.bag.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "invalid", "errors": [str(error)]}, indent=2))
        return 1
    errors = validate(value)
    print(json.dumps({"status": "valid" if not errors else "invalid", "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
