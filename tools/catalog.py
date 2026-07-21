#!/usr/bin/env python3
"""Compile and validate asher-skills' canonical skill graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
GITHUB_HTTPS = re.compile(
    r"^https://github\.com/"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/"
    r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?(?:\.git)?$"
)
META_KEYS = {
    "invocation", "execution", "requires", "optional", "external", "setup", "internal", "variants"
}
EXTERNAL_REQUIRED_KEYS = {"name", "kind", "source", "capability"}
EXTERNAL_KEYS = EXTERNAL_REQUIRED_KEYS | {"version"}
PROVIDERS = {"claude", "codex"}
PROTECTED_VARIANT_PATHS = {"SKILL.md", "agents/openai.yaml", "reference/setup.md"}


class CatalogError(ValueError):
    pass


@dataclass(frozen=True)
class ExternalRequirement:
    name: str
    kind: str
    source: str
    capability: str
    version: str | None = None

    def record(self) -> dict[str, str]:
        result = {
            "name": self.name,
            "kind": self.kind,
            "source": self.source,
            "capability": self.capability,
        }
        if self.version is not None:
            result["version"] = self.version
        return result


@dataclass(frozen=True)
class Skill:
    name: str
    source: str
    category: str | None
    invocation: str
    execution: str
    requires: tuple[str, ...]
    optional: tuple[str, ...]
    external: tuple[ExternalRequirement, ...]
    setup: str | None
    internal: bool
    variants: tuple[tuple[str, str], ...]

    def record(self) -> dict[str, object]:
        result: dict[str, object] = {
            "source": self.source,
            "category": self.category,
            "invocation": self.invocation,
            "execution": self.execution,
            "requires": list(self.requires),
            "optional": list(self.optional),
            "external": [requirement.record() for requirement in self.external],
            "internal": self.internal,
            "variants": dict(self.variants),
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


def _external(value: str, path: Path) -> tuple[ExternalRequirement, ...]:
    try:
        raw = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CatalogError(f"{path}: metadata.external must be a one-line JSON array") from exc
    if not isinstance(raw, list):
        raise CatalogError(f"{path}: metadata.external must be a one-line JSON array")

    requirements: list[ExternalRequirement] = []
    for index, item in enumerate(raw):
        label = f"{path}: metadata.external[{index}]"
        if not isinstance(item, dict):
            raise CatalogError(f"{label} must be an object")
        keys = set(item)
        missing = EXTERNAL_REQUIRED_KEYS - keys
        unknown = keys - EXTERNAL_KEYS
        if missing or unknown:
            raise CatalogError(f"{label} unknown={sorted(unknown)} missing={sorted(missing)}")
        if any(not isinstance(item[key], str) or not item[key].strip() for key in keys):
            raise CatalogError(f"{label} values must be non-empty strings")
        if any(item[key] != item[key].strip() or "\n" in item[key] for key in keys):
            raise CatalogError(f"{label} values must be trimmed one-line strings")
        if not NAME.fullmatch(item["name"]):
            raise CatalogError(f"{label}.name is invalid")
        if item["kind"] not in {"skill", "codex-plugin"}:
            raise CatalogError(f"{label}.kind must be skill or codex-plugin")
        if not GITHUB_HTTPS.fullmatch(item["source"]):
            raise CatalogError(f"{label}.source must be a GitHub HTTPS repository URL")
        requirements.append(
            ExternalRequirement(
                name=item["name"],
                kind=item["kind"],
                source=item["source"],
                capability=item["capability"],
                version=item.get("version"),
            )
        )

    names = tuple(requirement.name for requirement in requirements)
    if len(names) != len(set(names)):
        raise CatalogError(f"{path}: metadata.external contains duplicate names")
    if names != tuple(sorted(names)):
        raise CatalogError(f"{path}: metadata.external must be sorted by name")
    return tuple(requirements)


def _variants(value: str, path: Path) -> tuple[tuple[str, str], ...]:
    try:
        raw = json.loads(value)
    except json.JSONDecodeError as exc:
        raise CatalogError(f"{path}: metadata.variants must be a one-line JSON object") from exc
    if not isinstance(raw, dict) or not raw:
        raise CatalogError(f"{path}: metadata.variants must be a non-empty one-line JSON object")
    if list(raw) != sorted(raw):
        raise CatalogError(f"{path}: metadata.variants keys must be sorted")
    if set(raw) - PROVIDERS:
        raise CatalogError(
            f"{path}: metadata.variants has unsupported provider(s): "
            + ", ".join(sorted(set(raw) - PROVIDERS))
        )
    result: list[tuple[str, str]] = []
    source_root = path.parent.resolve()
    for provider, relative in raw.items():
        if not isinstance(relative, str) or relative != f"variants/{provider}":
            raise CatalogError(
                f"{path}: metadata.variants.{provider} must be variants/{provider}"
            )
        overlay = (path.parent / relative).resolve()
        if source_root not in overlay.parents or not overlay.is_dir():
            raise CatalogError(f"{path}: missing variant overlay: {relative}")
        for candidate in sorted(overlay.rglob("*")):
            if candidate.is_symlink():
                raise CatalogError(f"{path}: variant overlays cannot contain symlinks: {candidate}")
            if candidate.is_file():
                rel = candidate.relative_to(overlay).as_posix()
                if rel in PROTECTED_VARIANT_PATHS:
                    raise CatalogError(
                        f"{path}: variant overlay changes shared contract path {rel}"
                    )
        result.append((provider, relative))
    return tuple(result)


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
    description = top.get("description", "").strip()
    if not description:
        raise CatalogError(f"{path}: frontmatter description is required")
    if ": " in description and not (
        len(description) >= 2 and description[0] == description[-1] and description[0] in "\"'"
    ):
        raise CatalogError(f"{path}: description containing ': ' must be quoted for YAML compatibility")
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
    external = _external(metadata.get("external", "[]"), path)
    collisions = set(requires + optional) & {requirement.name for requirement in external}
    if collisions:
        raise CatalogError(
            f"{path}: external requirements collide with sibling edges: {', '.join(sorted(collisions))}"
        )
    setup = _scalar(metadata["setup"]) if "setup" in metadata else None
    internal = _scalar(metadata.get("internal", "false")).lower() == "true"
    variants = _variants(metadata["variants"], path) if "variants" in metadata else ()
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
        external=external,
        setup=setup,
        internal=internal,
        variants=variants,
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
    merged_external: dict[str, ExternalRequirement] = {}
    declared_by: dict[str, str] = {}
    for skill_name in sorted(active):
        for requirement in skills[skill_name].external:
            existing = merged_external.get(requirement.name)
            if existing is not None and existing != requirement:
                raise CatalogError(
                    f"conflicting external requirement {requirement.name}: "
                    f"{declared_by[requirement.name]} != {skill_name}"
                )
            merged_external[requirement.name] = requirement
            declared_by.setdefault(requirement.name, skill_name)
    return {
        "selected": sorted(selected),
        "closure": sorted(active),
        "setup_order": _required_order(skills, active),
        "external": [merged_external[name].record() for name in sorted(merged_external)],
    }


def compile_catalog(root: Path) -> dict[str, object]:
    skills = discover(root)
    return {
        "schema_version": 3,
        "skills": {name: skill.record() for name, skill in skills.items()},
    }


def _tree_files(root: Path, *, omit_variants: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if omit_variants and path.relative_to(root).parts[:1] == ("variants",):
            continue
        if path.is_symlink():
            raise CatalogError(f"skill trees cannot contain symlinks: {path}")
        if path.is_file():
            files.append(path)
    return files


def tree_hash(root: Path, *, omit_variants: bool = False) -> str:
    digest = hashlib.sha256()
    for path in _tree_files(root, omit_variants=omit_variants):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return "sha256:" + digest.hexdigest()


def materialize_variant(skill: Skill, root: Path, provider: str, output: Path) -> dict[str, str]:
    variants = dict(skill.variants)
    if provider not in variants:
        raise CatalogError(f"{skill.name}: provider is not declared: {provider}")
    source = root.resolve() / skill.source
    output = output.resolve()
    if source == output or source in output.parents:
        raise CatalogError(f"materialization output cannot be inside the skill source: {output}")
    if output.exists() or output.is_symlink():
        raise CatalogError(f"refusing existing materialization output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        for child in sorted(source.iterdir()):
            if child.name in {"variants", "evals"}:
                continue
            target = temporary / child.name
            if child.is_symlink():
                raise CatalogError(f"skill trees cannot contain symlinks: {child}")
            if child.is_dir():
                shutil.copytree(child, target)
            else:
                shutil.copy2(child, target)
        overlay = source / variants[provider]
        shutil.copytree(overlay, temporary, dirs_exist_ok=True)
        if (temporary / "variants").exists():
            raise CatalogError("compiled provider tree unexpectedly contains variants/")
        effective_hash = tree_hash(temporary)
        temporary.replace(output)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return {
        "skill": skill.name,
        "provider": provider,
        "source_revision": tree_hash(source),
        "effective_hash": effective_hash,
        "output": str(output),
    }


def _write(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("compile", "validate", "closure", "materialize"))
    parser.add_argument("skills", nargs="*")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--present", action="append", default=[])
    parser.add_argument("--provider", choices=sorted(PROVIDERS))
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
        elif args.command == "closure":
            graph = discover(args.root)
            print(json.dumps(resolve(graph, set(args.skills), set(args.present)), indent=2, sort_keys=True))
        else:
            if len(args.skills) != 1 or not args.provider or not args.output:
                parser.error("materialize requires one skill, --provider, and --output")
            graph = discover(args.root)
            name = args.skills[0]
            if name not in graph:
                raise CatalogError(f"unknown skill: {name}")
            print(
                json.dumps(
                    materialize_variant(graph[name], args.root, args.provider, args.output),
                    indent=2,
                    sort_keys=True,
                )
            )
    except (CatalogError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
