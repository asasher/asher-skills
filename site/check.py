#!/usr/bin/env python3
"""Drift check for the site's view manifests.

The app renders skill content and dependency edges live from the repo (layer 1 — cannot drift).
The manifests under views/ carry the roster, lanes, file lists, and playbook attachments (layer 2 —
can drift). This check makes layer-2 drift a failing gate:

  errors  — a manifest path that doesn't exist, a node whose SKILL.md is missing or has unparseable
            frontmatter, a lane reference to nowhere, a flow edge to an unknown node.
  warnings — a markdown file present in a node's source dir but not listed in the manifest
            (excluding evals/, THIRD_PARTY_LICENSES.md, and variants/).

Run from anywhere: python3 site/check.py   (exit 1 on errors, 0 with warnings)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEWS = Path(__file__).resolve().parent / "views"
IGNORE = {"THIRD_PARTY_LICENSES.md"}


def frontmatter_ok(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return bool(re.match(r"^---\n.*?\nname: ", text, re.S)) or text.startswith("---\nname:")


def check_view(view_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    view = json.loads(view_path.read_text(encoding="utf-8"))
    lane_ids = {l["id"] for l in view["lanes"]}
    node_ids = {n["id"] for n in view["nodes"]}

    for node in view["nodes"]:
        src = ROOT / node["source"]
        if node["lane"] not in lane_ids:
            errors.append(f"{node['id']}: unknown lane {node['lane']!r}")
        if not src.is_dir():
            errors.append(f"{node['id']}: source dir missing: {node['source']}")
            continue
        skill = src / "SKILL.md"
        if not skill.exists():
            errors.append(f"{node['id']}: SKILL.md missing")
        elif not frontmatter_ok(skill):
            errors.append(f"{node['id']}: SKILL.md frontmatter unparseable")
        listed = set()
        for f in node["files"]:
            listed.add(f["path"])
            if not (src / f["path"]).exists():
                errors.append(f"{node['id']}: listed file missing: {node['source']}/{f['path']}")
        for p in node.get("playbooks", []):
            if not (ROOT / p).exists():
                errors.append(f"{node['id']}: playbook missing: {p}")
        for md in src.rglob("*.md"):
            rel = md.relative_to(src).as_posix()
            if rel in listed or rel in IGNORE:
                continue
            if rel.startswith(("evals/", "variants/", "agents/")):
                continue
            warnings.append(f"{node['id']}: unlisted file {node['source']}/{rel}")

    for edge in view.get("flow", []):
        for end in (edge["from"], edge["to"]):
            if end not in node_ids:
                errors.append(f"flow edge references unknown node {end!r}")
    return errors, warnings


def main() -> int:
    all_errors, all_warnings = [], []
    for view_path in sorted(VIEWS.glob("*.json")):
        errors, warnings = check_view(view_path)
        all_errors += [f"{view_path.name}: {e}" for e in errors]
        all_warnings += [f"{view_path.name}: {w}" for w in warnings]
    for w in all_warnings:
        print(f"warning: {w}")
    for e in all_errors:
        print(f"ERROR: {e}")
    print(f"{'FAIL' if all_errors else 'OK'}: {len(all_errors)} errors, {len(all_warnings)} warnings")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
