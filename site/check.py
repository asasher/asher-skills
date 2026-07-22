#!/usr/bin/env python3
"""Drift check for the site's view manifests.

The app renders skill content and dependency edges live from the repo (layer 1 — cannot drift).
The manifests under views/ carry rosters, lanes/phases, file lists, and open targets (layer 2 —
can drift). This check makes layer-2 drift a failing gate:

  errors   — a referenced path that doesn't exist, a node whose SKILL.md is missing or has
             unparseable frontmatter, a lane/phase reference to nowhere, an edge or open target
             pointing at an unknown node or view.
  warnings — a markdown file present in a skill node's source dir but not listed in the manifest
             (excluding evals/, variants/, agents/, and license files).

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
    return text.startswith("---\n") and "\nname: " in text.split("\n---", 1)[0]


def load_views() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(VIEWS.glob("*.json"))}


def check_view(name: str, view: dict, all_views: dict[str, dict]) -> tuple[list[str], list[str]]:
    if view.get("type") == "simulation":
        errors: list[str] = []
        root = VIEWS.parents[1]
        for sc in view.get("scenarios", []):
            if not sc.get("steps"):
                errors.append(f"scenario {sc.get('id', '?')!r} has no steps")
            for i, step in enumerate(sc.get("steps", [])):
                if not step.get("caption"):
                    errors.append(f"scenario {sc.get('id', '?')!r} step {i + 1} missing caption")
                cite = step.get("cite")
                if cite and not (root / cite).exists():
                    errors.append(f"scenario {sc.get('id', '?')!r} step {i + 1} cites missing file {cite}")
        return errors, []
    if view.get("type") == "sequence":
        errors: list[str] = []
        actor_ids = {a["id"] for a in view.get("actors", [])}
        for msg in view.get("messages", []):
            if "phase" in msg:
                continue
            for end in ("from", "to"):
                if msg.get(end) not in actor_ids:
                    errors.append(f"sequence message {msg.get('label', '?')!r}: unknown actor {msg.get(end)!r}")
        return errors, []
    errors: list[str] = []
    warnings: list[str] = []
    lane_ids = {l["id"] for l in view.get("lanes", [])}
    phase_ids = {p["id"] for p in view.get("phases", [])}
    node_ids = {n["id"] for n in view["nodes"]}
    swim = view.get("type") == "swimlane"

    for node in view["nodes"]:
        nid = node["id"]
        if node["lane"] not in lane_ids:
            errors.append(f"{nid}: unknown lane {node['lane']!r}")
        if swim and node.get("phase") not in phase_ids:
            errors.append(f"{nid}: unknown phase {node.get('phase')!r}")

        if "source" in node:
            src = ROOT / node["source"]
            if not src.is_dir():
                errors.append(f"{nid}: source dir missing: {node['source']}")
                continue
            skill = src / "SKILL.md"
            if not skill.exists():
                errors.append(f"{nid}: SKILL.md missing")
            elif not frontmatter_ok(skill):
                errors.append(f"{nid}: SKILL.md frontmatter unparseable")
            listed = set()
            for f in node.get("files", []):
                listed.add(f["path"])
                if not (src / f["path"]).exists():
                    errors.append(f"{nid}: listed file missing: {node['source']}/{f['path']}")
            for p in node.get("playbooks", []):
                if not (ROOT / p).exists():
                    errors.append(f"{nid}: playbook missing: {p}")
            for mdf in src.rglob("*.md"):
                rel = mdf.relative_to(src).as_posix()
                if rel in listed or rel in IGNORE or rel.startswith(("evals/", "variants/", "agents/")):
                    continue
                warnings.append(f"{nid}: unlisted file {node['source']}/{rel}")

        for b in node.get("bindings", []):
            path = b.get("default")
            if path and not (ROOT / path).exists():
                errors.append(f"{nid}: bindings[{b.get('port')}].default missing: {path}")

        open_t = node.get("open") or {}
        if "file" in open_t and not (ROOT / open_t["file"]).exists():
            errors.append(f"{nid}: open.file missing: {open_t['file']}")
        if "jump" in open_t:
            target_view = all_views.get(open_t["jump"])
            if target_view is None:
                errors.append(f"{nid}: open.jump to unknown view {open_t['jump']!r}")
            elif open_t.get("node") and open_t["node"] not in {n["id"] for n in target_view["nodes"]}:
                errors.append(f"{nid}: open.jump node {open_t['node']!r} not in view {open_t['jump']!r}")
        elif "node" in open_t:
            sdlc = all_views.get("sdlc", {"nodes": []})
            if open_t["node"] not in {n["id"] for n in sdlc["nodes"]}:
                errors.append(f"{nid}: open.node {open_t['node']!r} not in the sdlc view")

    for edge in (view.get("flow", []) + view.get("edges", [])):
        for end in (edge["from"], edge["to"]):
            if end not in node_ids:
                errors.append(f"edge references unknown node {end!r}")
    return errors, warnings


def main() -> int:
    views = load_views()
    all_errors, all_warnings = [], []
    for name, view in views.items():
        errors, warnings = check_view(name, view, views)
        all_errors += [f"{name}.json: {e}" for e in errors]
        all_warnings += [f"{name}.json: {w}" for w in warnings]
    for w in all_warnings:
        print(f"warning: {w}")
    for e in all_errors:
        print(f"ERROR: {e}")
    print(f"{'FAIL' if all_errors else 'OK'}: {len(all_errors)} errors, {len(all_warnings)} warnings")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
