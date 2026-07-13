#!/usr/bin/env python3
"""Compile and validate asher-skills' canonical skill graph."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
META_KEYS = {"invocation", "execution", "requires", "optional", "setup", "internal"}


class CatalogError(ValueError):
    pass


@dataclass(frozen=True)
class Skill:
    name: str
    source: str
    category: str | None
    invocation: str
    execution: str
    requires: tuple[str, ...]
    optional: tuple[str, ...]
    setup: str | None
    internal: bool

    def record(self) -> dict[str, object]:
        result: dict[str, object] = {
            "source": self.source,
            "category": self.category,
            "invocation": self.invocation,
            "execution": self.execution,
            "requires": list(self.requires),
            "optional": list(self.optional),
            "internal": self.internal,
        }
        if self.setup:
            result["setup"] = self.setup
        return result


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _names(value: str, field: str, path: Path) -> tuple[str, ...]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        raise CatalogError(f"{path}: metadata.{field} must be an inline list")
    inner = value[1:-1].strip()
    names = tuple(_scalar(item) for item in inner.split(",") if item.strip())
    if any(not NAME.fullmatch(name) for name in names):
        raise CatalogError(f"{path}: metadata.{field} contains an invalid skill name")
    if len(names) != len(set(names)):
        raise CatalogError(f"{path}: metadata.{field} contains duplicates")
    if names != tuple(sorted(names)):
        raise CatalogError(f"{path}: metadata.{field} must be sorted")
    return names


def _frontmatter(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise CatalogError(f"{path}: missing frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise CatalogError(f"{path}: unterminated frontmatter") from exc
    top: dict[str, str] = {}
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line == "metadata:":
            in_metadata = True
            continue
        if line.startswith("  "):
            if not in_metadata or line.startswith("    ") or ":" not in line:
                raise CatalogError(f"{path}: unsupported nested frontmatter: {line}")
            key, value = line.strip().split(":", 1)
            if key in metadata:
                raise CatalogError(f"{path}: duplicate metadata.{key}")
            metadata[key] = value.strip()
            continue
        in_metadata = False
        if ":" not in line:
            raise CatalogError(f"{path}: malformed frontmatter: {line}")
        key, value = line.split(":", 1)
        if key in top:
            raise CatalogError(f"{path}: duplicate frontmatter key {key}")
        top[key] = value.strip()
    return top, metadata


def _parse(path: Path, root: Path, category: str | None) -> Skill:
    top, metadata = _frontmatter(path)
    unknown = set(metadata) - META_KEYS
    missing = {"invocation", "execution", "requires", "optional"} - set(metadata)
    if unknown or missing:
        raise CatalogError(f"{path}: metadata unknown={sorted(unknown)} missing={sorted(missing)}")
    name = _scalar(top.get("name", ""))
    if not NAME.fullmatch(name) or path.parent.name != name:
        raise CatalogError(f"{path}: frontmatter name must match its directory")
    invocation = _scalar(metadata["invocation"])
    execution = _scalar(metadata["execution"])
    if invocation not in {"user", "model"} or execution not in {"orchestrator", "thread"}:
        raise CatalogError(f"{path}: invalid invocation/execution metadata")
    disabled = _scalar(top.get("disable-model-invocation", "false")).lower() == "true"
    if (invocation == "user") != disabled:
        raise CatalogError(f"{path}: invocation disagrees with disable-model-invocation")
    openai = path.parent / "agents" / "openai.yaml"
    if openai.is_file():
        match = re.search(
            r"^\s*allow_implicit_invocation:\s*(true|false)\s*$",
            openai.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if not match or (invocation == "model") != (match.group(1) == "true"):
            raise CatalogError(f"{path}: invocation disagrees with agents/openai.yaml")
    requires = _names(metadata["requires"], "requires", path)
    optional = _names(metadata["optional"], "optional", path)
    if name in requires + optional or set(requires) & set(optional):
        raise CatalogError(f"{path}: sibling edges must be disjoint and non-self-referential")
    setup = _scalar(metadata["setup"]) if "setup" in metadata else None
    internal = _scalar(metadata.get("internal", "false")).lower() == "true"
    if setup:
        if setup != "reference/setup.md" or not (path.parent / setup).is_file():
            raise CatalogError(f"{path}: setup must point to a shipped reference/setup.md")
        body = path.read_text(encoding="utf-8").split("---", 2)[-1]
        if setup not in body:
            raise CatalogError(f"{path}: command surface does not route setup to {setup}")
    return Skill(
        name=name,
        source=path.parent.relative_to(root).as_posix(),
        category=category,
        invocation=invocation,
        execution=execution,
        requires=requires,
        optional=optional,
        setup=setup,
        internal=internal,
    )


def discover(root: Path) -> dict[str, Skill]:
    root = root.resolve()
    skills_dir = root / "skills"
    paths = sorted(skills_dir.rglob("SKILL.md"))
    if not paths:
        raise CatalogError(f"{skills_dir}: no skills found")
    skills: dict[str, Skill] = {}
    for path in paths:
        parts = path.relative_to(skills_dir).parts
        if len(parts) == 2:
            category = None
        elif len(parts) == 3 and not (skills_dir / parts[0] / "SKILL.md").exists():
            category = parts[0]
        else:
            raise CatalogError(f"{path}: skills must be flat or exactly one category deep")
        skill = _parse(path, root, category)
        if skill.name in skills:
            raise CatalogError(f"duplicate skill name: {skill.name}")
        skills[skill.name] = skill
    names = set(skills)
    for skill in skills.values():
        missing = (set(skill.requires) | set(skill.optional)) - names
        if missing:
            raise CatalogError(f"{skill.name}: missing sibling(s): {', '.join(sorted(missing))}")
        held = [name for name in skill.requires if skills[name].internal and not skill.internal]
        if held:
            raise CatalogError(f"{skill.name}: public skill requires internal sibling(s): {', '.join(held)}")
    _required_order(skills, set(skills))
    return dict(sorted(skills.items()))


def _required_order(skills: dict[str, Skill], active: set[str]) -> list[str]:
    order: list[str] = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(name: str) -> None:
        if state.get(name) == 2:
            return
        if state.get(name) == 1:
            start = stack.index(name)
            raise CatalogError("required sibling cycle: " + " -> ".join(stack[start:] + [name]))
        state[name] = 1
        stack.append(name)
        for dependency in skills[name].requires:
            if dependency in active:
                visit(dependency)
        stack.pop()
        state[name] = 2
        order.append(name)

    for name in sorted(active):
        visit(name)
    return order


def resolve(
    skills: dict[str, Skill], selected: set[str], present: set[str] | None = None
) -> dict[str, object]:
    present = present or set()
    unknown = (selected | present) - set(skills)
    if unknown:
        raise CatalogError("unknown skill(s): " + ", ".join(sorted(unknown)))
    held = sorted(name for name in selected if skills[name].internal)
    if held:
        raise CatalogError("internal skill(s) are not installable: " + ", ".join(held))
    active = set(selected)
    queue = sorted(selected)
    while queue:
        skill = skills[queue.pop(0)]
        additions = set(skill.requires)
        additions.update(
            name for name in skill.optional
            if (name in selected or name in present) and not skills[name].internal
        )
        for name in sorted(additions - active):
            active.add(name)
            queue.append(name)
        queue.sort()
    return {"selected": sorted(selected), "closure": sorted(active), "setup_order": _required_order(skills, active)}


def compile_catalog(root: Path) -> dict[str, object]:
    skills = discover(root)
    return {
        "schema_version": 1,
        "skills": {name: skill.record() for name, skill in skills.items()},
    }


def _write(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("compile", "validate", "closure"))
    parser.add_argument("skills", nargs="*")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--present", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        if args.command == "compile":
            data = compile_catalog(args.root)
            if not args.output:
                print(json.dumps(data, indent=2, sort_keys=True))
            else:
                _write(args.output, data)
        elif args.command == "validate":
            if not args.snapshot:
                parser.error("validate requires --snapshot")
            actual = compile_catalog(args.root)
            expected = json.loads(args.snapshot.read_text(encoding="utf-8"))
            if actual != expected:
                raise CatalogError(f"{args.snapshot}: snapshot differs from source declarations")
            print(f"valid: {len(actual['skills'])} skills")
        else:
            graph = discover(args.root)
            print(json.dumps(resolve(graph, set(args.skills), set(args.present)), indent=2, sort_keys=True))
    except (CatalogError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
