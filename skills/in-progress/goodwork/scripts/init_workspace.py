#!/usr/bin/env python3
"""Initialize a local Goodwork v2 workspace."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def is_git_repo(root: Path) -> bool:
    return run_git(root, ["rev-parse", "--is-inside-work-tree"]).returncode == 0


def is_tracked(root: Path, rel: str) -> bool:
    return run_git(root, ["ls-files", "--error-unmatch", rel]).returncode == 0


def is_ignored(root: Path, rel: str) -> bool:
    return run_git(root, ["check-ignore", "-q", rel]).returncode == 0


def ensure_env_ignored(root: Path, workspace_name: str) -> None:
    env_rel = f"{workspace_name}/.env"
    if is_git_repo(root) and is_tracked(root, env_rel):
        raise RuntimeError(f"{env_rel} is tracked by git; remove it from tracking before initializing Goodwork")
    gitignore = root / ".gitignore"
    if is_git_repo(root) and is_ignored(root, env_rel):
        return
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    lines = existing.splitlines()
    needed = [env_rel, f"{workspace_name}/chrome-profile/"]
    additions = []
    for pattern in needed:
        if pattern not in lines:
            additions.append(pattern)
    if additions:
        prefix = existing
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        gitignore.write_text(prefix + "\n".join(additions) + "\n", encoding="utf-8")


def json_defaults(workspace_name: str) -> dict[str, dict]:
    ts = now_iso()
    return {
        "pipeline.json": {"version": 1, "updated_at": ts, "cards": [], "unmatched_replies": []},
        "leads.json": {"version": 1, "updated_at": ts, "leads": []},
        "sources.json": {"version": 1, "updated_at": ts, "sources": []},
        "targets.json": {"version": 1, "updated_at": ts, "targets": []},
        "capabilities.json": {
            "version": 1,
            "updated_at": ts,
            "workspace_id": f"gw_{workspace_name}",
            "connectors": {"gmail": "unavailable", "calendar": "unavailable"},
            "chrome": {
                "profile_path": f"{workspace_name}/chrome-profile",
                "status": "missing",
                "sites": {"linkedin": "missing", "job_boards": "missing", "whatsapp": "not_configured"},
            },
            "tailscale": {"status": "missing", "magicdns_url": None},
            "ui": {"diffs_vendor": "missing", "status": "missing"},
            "reconcile": {"cadence": "manual", "last_run_at": None},
            "execution": {"rungs": ["manual"]},
            "presentation": {"rungs": ["markdown"]},
            "notifications": {"status": "missing"},
        },
        "metrics.json": {"version": 1, "updated_at": ts, "quotas": {"weekly_applications": 0}, "weeks": []},
        "evidence-inbox.json": {"version": 1, "updated_at": ts, "entries": []},
    }


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--workspace", default="goodwork")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    workspace = root / args.workspace
    try:
        ensure_env_ignored(root, args.workspace)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "chrome-profile").mkdir(exist_ok=True)
    (workspace / "artifacts").mkdir(exist_ok=True)
    created: list[str] = []
    for name, payload in json_defaults(args.workspace).items():
        if write_if_missing(workspace / name, json.dumps(payload, indent=2, ensure_ascii=False) + "\n"):
            created.append(name)
    for name in ["approvals.jsonl", "events.jsonl", ".await-cursor", ".env"]:
        if write_if_missing(workspace / name, ""):
            created.append(name)
    narratives = {
        "PROFILE.md": "# Good Work Profile\n\n",
        "ODYSSEYS.md": "# Odysseys\n\n",
        "EXPERIMENTS.md": "# Experiments\n\n",
        "NICHE.md": "# Niche\n\n",
        "JOURNAL.md": "# Journal\n\n",
    }
    for name, content in narratives.items():
        if write_if_missing(workspace / name, content):
            created.append(name)
    print(json.dumps({"workspace": str(workspace), "created": created}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
