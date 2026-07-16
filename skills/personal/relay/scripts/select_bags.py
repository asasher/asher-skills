#!/usr/bin/env python3
"""Select normalized evidence into audience-isolated Relay bags."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from relay_common import instance_root, load_json, normalize_address, normalize_recipients, now, pretty_json, read_jsonl
from validate_relay_bag import validate


def latest_watermarks(instance: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for event in read_jsonl(instance / "state" / "watermarks.jsonl"):
        audience, observed = event.get("audience_id"), event.get("observed_through")
        if isinstance(audience, str) and isinstance(observed, str):
            values[audience] = max(values.get(audience, ""), observed)
    return values


def select(repo: Path, evidence_path: Path, output: Path) -> dict[str, Any]:
    instance = instance_root(repo)
    bindings = load_json(instance / "bindings.json")
    policy = load_json(instance / "policy.json")
    evidence_value = json.loads(evidence_path.read_text(encoding="utf-8"))
    if not isinstance(evidence_value, list):
        raise ValueError("evidence input must be a JSON array")
    watermarks = latest_watermarks(instance)
    output.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for audience_id in bindings.get("audiences", []):
        audience = load_json(instance / "audiences" / f"{audience_id}.json")
        interest = load_json(instance / str(audience["interest_file"]))
        projects = set(audience.get("project_ids", []))
        features = set(interest.get("features", []))
        sections = set(interest.get("sections", []))
        disclosure = set(audience.get("allowed_disclosure", ["internal"] if audience.get("kind") == "internal" else ["external"]))
        watermark = watermarks.get(audience_id, "")
        selected: list[dict[str, Any]] = []
        for item in evidence_value:
            if not isinstance(item, dict):
                continue
            if item.get("project_id") not in projects or item.get("feature") not in features:
                continue
            if item.get("section") not in sections or item.get("disclosure") not in disclosure:
                continue
            if str(item.get("observed_at", "")) <= watermark:
                continue
            selected.append(item)
        if not selected:
            exclusion = {"schema_version": 1, "audience_id": audience_id, "state": "excluded", "reason": "no-eligible-evidence"}
            (output / f"{audience_id}.excluded.json").write_bytes(pretty_json(exclusion))
            results.append(exclusion)
            continue
        headers: dict[str, list[str]] = {"to": [], "cc": []}
        for recipient in audience["recipients"]:
            headers[recipient["header"]].append(normalize_address(recipient["address"]))
        if audience.get("kind") == "external" and audience.get("operator_cc", "default") != "disabled" and policy["delivery"].get("operator_cc_default"):
            headers["cc"].append(normalize_address(policy["delivery"]["operator_address"]))
        headers = {key: normalize_recipients(value) for key, value in headers.items()}
        if set(headers["to"]) & set(headers["cc"]):
            raise ValueError(f"{audience_id}: recipient appears in To and CC")
        recipe = audience.get("section_recipe") or bindings["section_recipes"][audience["message_kind"]]
        section_values = []
        used_ids: set[str] = set()
        for title in recipe:
            items = []
            for fact in selected:
                if fact["section"] != title:
                    continue
                used_ids.add(fact["id"])
                items.append({key: fact[key] for key in ("status", "title", "detail") } | {"evidence_ids": [fact["id"]], **({"visibility": fact["visibility"]} if fact.get("visibility") else {})})
            section_values.append({"title": title, "items": items})
        used = [item for item in selected if item["id"] in used_ids]
        if not used:
            exclusion = {"schema_version": 1, "audience_id": audience_id, "state": "excluded", "reason": "no-evidence-in-section-recipe"}
            (output / f"{audience_id}.excluded.json").write_bytes(pretty_json(exclusion))
            results.append(exclusion)
            continue
        bag = {
            "schema_version": 2, "id": f"{audience_id}-{str(now())[:10]}-001", "kind": audience["message_kind"],
            "generated_at": now(), "subject": audience["subject"], "preheader": audience["preheader"],
            "audience_id": audience_id, "project_ids": sorted(projects), "sender": audience["sender"],
            "recipients": headers, "summary": audience["summary"], "sections": section_values,
            "evidence": [{key: fact.get(key) for key in ("id", "source", "observed_at", "status", "project_id", "feature")} for fact in used],
        }
        errors = validate(bag)
        if errors:
            raise ValueError(f"{audience_id}: " + "; ".join(errors))
        target = output / audience_id / "bag.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(pretty_json(bag))
        results.append({"audience_id": audience_id, "state": "selected", "bag": str(target), "evidence_count": len(used)})
    return {"status": "ok", "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = select(args.repository_root, args.evidence, args.out)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
