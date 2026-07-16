#!/usr/bin/env python3
"""Discover and reconcile a consumer-owned Relay instance."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from relay_common import atomic_write, dotenv_value, instance_root, load_json, pretty_json, sha256_bytes

TEMPLATE_VERSION = "2.0.0"
DISCOVERY_EXCLUDED_DIRS = {".git", ".agents", ".claude", "node_modules", "dist", "build", "control-plane", "relay"}


def candidate_path(target: Path, data: bytes) -> Path:
    candidate = target.with_name(target.name + ".setup-candidate")
    index = 1
    while candidate.exists() and candidate.read_bytes() != data:
        candidate = target.with_name(f"{target.name}.setup-candidate.{index}")
        index += 1
    if not candidate.exists():
        atomic_write(candidate, data)
    return candidate


def template_files(root: Path) -> list[Path]:
    return [path.relative_to(root) for path in sorted(root.rglob("*")) if path.is_file() and path.name != ".DS_Store"]


def repository_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for directory, names, filenames in os.walk(repo, topdown=True):
        names[:] = [name for name in names if name not in DISCOVERY_EXCLUDED_DIRS and not Path(directory, name).is_symlink()]
        root = Path(directory)
        if len(root.relative_to(repo).parts) > 5:
            names[:] = []
            continue
        for filename in filenames:
            path = root / filename
            if not path.is_symlink():
                files.append(path.relative_to(repo))
    return sorted(files)[:2000]


def matching_candidates(files: list[Path], terms: tuple[str, ...]) -> list[str]:
    return [path.as_posix() for path in files if any(term in path.as_posix().lower() for term in terms)][:100]


def command_version(name: str) -> str | None:
    executable = shutil.which(name)
    if not executable:
        return None
    try:
        result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    line = (result.stdout or result.stderr).strip().splitlines()
    return line[0] if result.returncode == 0 and line else None


def release_tags(repo: Path) -> list[str]:
    if not (repo / ".git").exists() or not shutil.which("git"):
        return []
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "tag", "--list"], capture_output=True, text=True, timeout=5, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    return sorted(result.stdout.splitlines())[-50:] if result.returncode == 0 else []


def discover(repo: Path) -> dict[str, Any]:
    files = repository_files(repo)
    manifests = [name for name in ("package.json", "pyproject.toml", "Cargo.toml", "go.mod") if (repo / name).is_file()]
    repositories = ["."] if (repo / ".git").exists() else []
    repositories.extend(path.parent.relative_to(repo).as_posix() for path in sorted(repo.glob("*/.git")))
    optional_skills = [name for name in ("manage-tasks", "manage-opportunities") if (repo / ".agents" / "skills" / name).exists()]
    return {
        "schema_version": 1,
        "repository_root": str(repo),
        "repositories": sorted(set(repositories)),
        "runtime_manifests": manifests,
        "project_registry_candidates": matching_candidates(files, ("project", "customer", "people", "client")),
        "tracker_candidates": matching_candidates(files, ("task", "issue", "backlog", "roadmap")),
        "release_evidence_candidates": matching_candidates(files, ("changelog", "release", "deployment", "deploy")),
        "git_release_tags": release_tags(repo),
        "mailbox_candidates": matching_candidates(files, ("mailbox", "email", "inbox", "mail/")),
        "profile_candidates": matching_candidates(files, ("profile", "contact", "customer", "people")),
        "template_candidates": matching_candidates(files, ("template", "renderer", "render-email", "email.ts", "email.tsx")),
        "editorial_candidates": matching_candidates(files, ("editorial", "style-guide", "voice", "brand")),
        "docs_present": (repo / "docs").is_dir(),
        "optional_source_skills": optional_skills,
        "root_env": {
            "exists": (repo / ".env").is_file(),
            "agentmail_key": "present" if dotenv_value(repo / ".env", "AGENTMAIL_API_KEY") else "missing",
        },
        "agentmail_cli": shutil.which("agentmail") is not None,
        "node": {"available": shutil.which("node") is not None, "version": command_version("node")},
        "npm": {"available": shutil.which("npm") is not None, "version": command_version("npm")},
    }


def ensure_env(repo: Path) -> dict[str, Any]:
    env = repo / ".env"
    if not env.exists():
        atomic_write(env, b"AGENTMAIL_API_KEY=\n", 0o600)
    else:
        os.chmod(env, 0o600)
        has_assignment = any(
            raw.strip().removeprefix("export ").lstrip().partition("=")[0].strip() == "AGENTMAIL_API_KEY"
            and "=" in raw
            for raw in env.read_text(encoding="utf-8").splitlines()
            if raw.strip() and not raw.strip().startswith("#")
        )
        if not has_assignment:
            with env.open("a", encoding="utf-8") as handle:
                if env.stat().st_size and not env.read_bytes().endswith(b"\n"):
                    handle.write("\n")
                handle.write("AGENTMAIL_API_KEY=\n")
            os.chmod(env, 0o600)
    gitignore = repo / ".gitignore"
    lines = gitignore.read_text(encoding="utf-8").splitlines() if gitignore.is_file() else []
    if ".env" not in {line.strip() for line in lines}:
        lines.append(".env")
        atomic_write(gitignore, ("\n".join(lines) + "\n").encode())
    return {"file": ".env", "gitignored": True, "mode_0600": True, "AGENTMAIL_API_KEY": "present" if dotenv_value(env, "AGENTMAIL_API_KEY") else "missing"}


def setup(repo: Path, binding_path: Path | None) -> dict[str, Any]:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f"repository does not exist: {repo}")
    skill = Path(__file__).resolve().parents[1]
    source = skill / "templates" / "instance"
    instance = instance_root(repo)
    report: dict[str, Any] = {"created": [], "preserved": [], "candidates": [], "discovery": discover(repo)}
    records: dict[str, Any] = {}
    default_binding = (source / "bindings.json").read_bytes()
    supplied = pretty_json(load_json(binding_path.resolve())) if binding_path else None

    for relative in template_files(source):
        target = instance / relative
        data = (source / relative).read_bytes()
        supplied_binding = relative.as_posix() == "bindings.json" and supplied is not None
        if supplied_binding:
            data = supplied
        if not target.exists():
            atomic_write(target, data, (source / relative).stat().st_mode & 0o777)
            report["created"].append(str(target))
            status = "current"
        elif target.read_bytes() == data:
            report["preserved"].append(str(target))
            status = "current"
        elif supplied_binding and target.read_bytes() == default_binding:
            atomic_write(target, data, (source / relative).stat().st_mode & 0o777)
            report["created"].append(str(target))
            status = "current"
        else:
            report["preserved"].append(str(target))
            report["candidates"].append(str(candidate_path(target, data)))
            status = "consumer_modified"
        records[relative.as_posix()] = {"package_sha256": sha256_bytes((source / relative).read_bytes()), "status": status}

    for directory in ("profiles", "audiences", "interests", "runs", "state"):
        (instance / directory).mkdir(parents=True, exist_ok=True)
    playbook = repo / "docs" / "agents" / "relay.md"
    playbook_data = (skill / "templates" / "relay.md").read_bytes()
    if not playbook.exists():
        atomic_write(playbook, playbook_data)
        report["created"].append(str(playbook))
    elif playbook.read_bytes() != playbook_data:
        report["preserved"].append(str(playbook))
        report["candidates"].append(str(candidate_path(playbook, playbook_data)))
    else:
        report["preserved"].append(str(playbook))

    package_manifest = instance / "package-defaults.json"
    package_data = pretty_json({"schema_version": 1, "template_version": TEMPLATE_VERSION, "files": records})
    atomic_write(package_manifest, package_data)
    discovery_path = instance / "discovery.json"
    discovery_data = pretty_json(report["discovery"])
    if not discovery_path.exists() or discovery_path.read_bytes() == discovery_data:
        atomic_write(discovery_path, discovery_data)
    else:
        report["candidates"].append(str(candidate_path(discovery_path, discovery_data)))
    report["credential"] = ensure_env(repo)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--binding", type=Path)
    args = parser.parse_args()
    try:
        repo = args.repository_root.resolve()
        if args.discover and not args.binding:
            print(json.dumps({"status": "ok", "discovery": discover(repo)}, indent=2, sort_keys=True))
            return 0
        report = setup(repo, args.binding)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2
    print(json.dumps({"status": "ok", **report}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
