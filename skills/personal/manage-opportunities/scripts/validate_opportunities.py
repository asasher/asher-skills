#!/usr/bin/env python3
"""Validate structural Opportunity invariants in a markdown workspace."""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

STAGES = {
    "lead",
    "qualified",
    "discovery",
    "proposal",
    "negotiation",
    "closed-won",
    "closed-lost",
    "dormant",
}
ACTIVE_STAGES = {"lead", "qualified", "discovery", "proposal", "negotiation"}
REQUIRED_FIELDS = ("opportunity", "type", "company", "customer", "owner", "stage", "opened")
REQUIRED_SECTIONS = (
    "Backlog",
    "Done",
    "Commercial",
    "Decision Log",
    "Events Log",
    "Projects",
    "Links",
)
TASK_RE = re.compile(
    r"^\s*-\s+\[([ /xX><!\-])\]\s+.*?🆔\s+([A-Za-z0-9_-]+)(?=\s|$)"
)
BLOCKER_RE = re.compile(r"⛔\s+([A-Za-z0-9_-]+)")
TASK_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True, order=True)
class Issue:
    path: str
    line: int
    code: str
    message: str

    def as_dict(self) -> dict[str, object]:
        return {"path": self.path, "line": self.line, "code": self.code, "message": self.message}


@dataclass(frozen=True)
class Document:
    path: Path
    metadata: dict[str, Any]
    body_lines: list[str]
    body_start: int


@dataclass(frozen=True)
class Task:
    task_id: str
    status: str
    blockers: tuple[str, ...]
    path: Path
    line: int
    h2: str | None
    origin_heading: str | None


class ParseError(ValueError):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _strip_comment(value: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote == '"':
            escaped = True
            continue
        if char in "\"'":
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        elif char == "#" and quote is None and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.strip()


def _scalar(value: str, line: int) -> Any:
    value = _strip_comment(value)
    if value == "":
        return ""
    if value[0:1] in {"\"", "'"}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ParseError(line, f"invalid quoted scalar: {exc}") from exc
        if not isinstance(parsed, str):
            raise ParseError(line, "quoted scalar must be a string")
        return parsed
    lowered = value.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered in {"true", "false"}:
        return lowered == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def _inline_list(value: str, line: int) -> list[Any]:
    inner = value[1:-1].strip()
    if not inner:
        return []
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return [_scalar(item.strip(), line) for item in inner.split(",")]
    if not isinstance(parsed, (list, tuple)):
        raise ParseError(line, "inline collection must be a list")
    return list(parsed)


def parse_document(path: Path) -> Document:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ParseError(1, "missing opening frontmatter delimiter")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ParseError(1, "unterminated frontmatter") from exc

    metadata: dict[str, Any] = {}
    active_list: str | None = None
    for index in range(1, end):
        line_no = index + 1
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            if active_list is None:
                raise ParseError(line_no, "list item has no top-level key")
            metadata[active_list].append(_scalar(raw[4:].strip(), line_no))
            continue
        if raw.startswith((" ", "\t")):
            raise ParseError(line_no, "nested mappings are not supported")
        if ":" not in raw:
            raise ParseError(line_no, "frontmatter entry must contain ':'")
        key, value = raw.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", key):
            raise ParseError(line_no, f"invalid frontmatter key {key!r}")
        if key in metadata:
            raise ParseError(line_no, f"duplicate frontmatter key {key}")
        value = _strip_comment(value.strip())
        if value == "":
            metadata[key] = []
            active_list = key
        elif value.startswith("[") and value.endswith("]"):
            metadata[key] = _inline_list(value, line_no)
            active_list = None
        else:
            metadata[key] = _scalar(value, line_no)
            active_list = None
    return Document(path=path, metadata=metadata, body_lines=lines[end + 1 :], body_start=end + 2)


def _heading_name(raw: str) -> str:
    value = raw.strip()
    match = re.fullmatch(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]", value)
    if match:
        return (match.group(2) or match.group(1)).strip()
    return re.sub(r"\s+#+\s*$", "", value).strip()


def scan_tasks(paths: list[Path]) -> dict[str, list[Task]]:
    tasks: dict[str, list[Task]] = {}
    for path in paths:
        if not path.is_file():
            continue
        h2: str | None = None
        origin_heading: str | None = None
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            heading = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
            if heading:
                level = len(heading.group(1))
                name = _heading_name(heading.group(2))
                if level == 2:
                    h2 = name
                    origin_heading = None
                elif level == 3:
                    origin_heading = name
            match = TASK_RE.match(line)
            if not match:
                continue
            task = Task(
                task_id=match.group(2),
                status=match.group(1).lower(),
                blockers=tuple(BLOCKER_RE.findall(line)),
                path=path,
                line=line_no,
                h2=h2,
                origin_heading=origin_heading,
            )
            tasks.setdefault(task.task_id, []).append(task)
    return tasks


def _date(value: Any) -> dt.date | None:
    if not isinstance(value, str):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def _wikilink_target(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", value.strip())
    return match.group(1).strip() if match else None


def _section_lines(document: Document, title: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    in_section = False
    for offset, line in enumerate(document.body_lines):
        line_no = document.body_start + offset
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading and len(heading.group(1)) <= 2:
            in_section = len(heading.group(1)) == 2 and _heading_name(heading.group(2)) == title
            continue
        if in_section:
            result.append((line_no, line))
    return result


def _project_links(document: Document) -> list[str]:
    links: list[str] = []
    for _, line in _section_lines(document, "Projects"):
        links.extend(match.group(1).strip() for match in WIKILINK_RE.finditer(line))
    return links


def _validate_document(
    root: Path,
    document: Document,
    tasks: dict[str, list[Task]],
    designated: dict[str, list[Path]],
) -> list[Issue]:
    issues: list[Issue] = []
    path_text = _relative(document.path, root)
    data = document.metadata

    def add(code: str, message: str, line: int = 1) -> None:
        issues.append(Issue(path_text, line, code, message))

    for field in REQUIRED_FIELDS:
        if field not in data or data[field] in (None, "", []):
            add("missing-field", f"required field {field!r} is missing")

    name = data.get("opportunity")
    if data.get("type") != "opportunity":
        add("invalid-type", "type must be 'opportunity'")
    stage = data.get("stage")
    if stage not in STAGES:
        add("invalid-stage", f"stage must be one of: {', '.join(sorted(STAGES))}")

    for field in ("company", "customer", "owner"):
        if field in data and data[field] not in (None, "") and _wikilink_target(data[field]) is None:
            add("invalid-link", f"{field} must be one wikilink string")
    contacts = data.get("contacts")
    if contacts is not None:
        if not isinstance(contacts, list) or any(_wikilink_target(item) is None for item in contacts):
            add("invalid-contacts", "contacts must be a list of wikilink strings")

    opened = _date(data.get("opened"))
    if "opened" in data and opened is None:
        add("invalid-date", "opened must be an ISO date")
    for field in ("outcomeDate", "reviewDate"):
        if field in data and _date(data[field]) is None:
            add("invalid-date", f"{field} must be an ISO date")
    outcome = _date(data.get("outcomeDate"))
    if opened and outcome and outcome < opened:
        add("invalid-date-order", "outcomeDate cannot precede opened")

    for field in ("value", "recurringValue"):
        if field in data and (isinstance(data[field], bool) or not isinstance(data[field], (int, float)) or data[field] < 0):
            add("invalid-number", f"{field} must be a non-negative number")
    if "probability" in data and (
        isinstance(data["probability"], bool)
        or not isinstance(data["probability"], int)
        or not 0 <= data["probability"] <= 100
    ):
        add("invalid-probability", "probability must be an integer from 0 through 100")
    if "currency" in data and (not isinstance(data["currency"], str) or not re.fullmatch(r"[A-Z]{3}", data["currency"])):
        add("invalid-currency", "currency must be a three-letter uppercase code")
    if any(field in data for field in ("value", "recurringValue")) and "currency" not in data:
        add("missing-currency", "currency is required when value or recurringValue is present")

    h1 = next((line[2:].strip() for line in document.body_lines if line.startswith("# ")), None)
    if isinstance(name, str) and h1 != name:
        add("invalid-heading", "first H1 must match opportunity")
    sections = {
        _heading_name(match.group(1))
        for line in document.body_lines
        if (match := re.match(r"^##\s+(.+?)\s*$", line))
    }
    for section in REQUIRED_SECTIONS:
        if section not in sections:
            add("missing-section", f"required section '## {section}' is missing")

    workspace_path = data.get("workspacePath")
    if workspace_path is not None:
        if not isinstance(workspace_path, str) or not Path(workspace_path).is_absolute():
            add("invalid-workspace-path", "workspacePath must be an absolute path")
        elif not Path(workspace_path).exists():
            add("missing-workspace-path", f"workspacePath does not resolve: {workspace_path}")

    next_action = data.get("nextAction")
    if stage in ACTIVE_STAGES and next_action in (None, ""):
        add("missing-next-action", "active stages require nextAction")
    if stage not in ACTIVE_STAGES and next_action not in (None, ""):
        add("unexpected-next-action", "closed and dormant stages must omit nextAction")
    if next_action not in (None, ""):
        if not isinstance(next_action, str) or not TASK_ID_RE.fullmatch(next_action):
            add("invalid-next-action", "nextAction must contain only one task ID")
        else:
            designated.setdefault(next_action, []).append(document.path)
            found = tasks.get(next_action, [])
            if len(found) != 1:
                add("next-action-count", f"nextAction {next_action!r} resolves to {len(found)} task occurrences; expected 1")
            else:
                task = found[0]
                in_own_backlog = task.path == document.path and task.h2 == "Backlog"
                in_todo = task.path == root / "TODO.md" and task.origin_heading in {name, document.path.stem}
                if not (in_own_backlog or in_todo):
                    add("next-action-origin", f"nextAction {next_action!r} is not in this Opportunity backlog or TODO heading")
                if task.status in {"!", "x", "-", ">"}:
                    add("next-action-status", f"nextAction {next_action!r} has invalid status [{task.status}]")
                unresolved = [blocker for blocker in task.blockers if len(tasks.get(blocker, [])) != 1 or tasks[blocker][0].status != "x"]
                if unresolved:
                    add("next-action-blocked", f"nextAction {next_action!r} has unresolved blockers: {', '.join(unresolved)}")

    if stage == "closed-lost":
        for field in ("outcomeDate", "closeReason"):
            if data.get(field) in (None, ""):
                add("missing-close-field", f"closed-lost requires {field}")
    if stage == "dormant":
        for field in ("dormantReason", "reviewDate"):
            if data.get(field) in (None, ""):
                add("missing-dormant-field", f"dormant requires {field}")
        review_date = _date(data.get("reviewDate"))
        if review_date and review_date <= dt.date.today():
            add("past-review-date", "dormant reviewDate must be in the future")
    if stage == "closed-won":
        if data.get("outcomeDate") in (None, ""):
            add("missing-win-field", "closed-won requires outcomeDate")
        project_links = _project_links(document)
        no_delivery = data.get("noDeliveryReason")
        if not project_links and no_delivery in (None, ""):
            add("missing-win-delivery", "closed-won requires linked Project(s) or noDeliveryReason")
        if project_links and no_delivery not in (None, ""):
            add("ambiguous-win-delivery", "closed-won cannot have both linked Projects and noDeliveryReason")
        for project_name in project_links:
            project_path = root / "Projects" / f"{project_name}.md"
            if not project_path.is_file():
                add("missing-project", f"linked Project does not exist: {project_name}")
                continue
            try:
                project = parse_document(project_path)
            except (OSError, UnicodeError, ParseError) as exc:
                add("invalid-project", f"cannot parse linked Project {project_name}: {exc}")
                continue
            source = _wikilink_target(project.metadata.get("sourceOpportunity"))
            if source not in {name, document.path.stem}:
                add("missing-project-reciprocity", f"Project {project_name} does not link back through sourceOpportunity")
            local_path = project.metadata.get("localPath")
            if not isinstance(local_path, str) or not Path(local_path).is_absolute():
                add("invalid-project-path", f"Project {project_name} requires an absolute localPath")
            elif not Path(local_path).exists():
                add("missing-project-path", f"Project {project_name} localPath does not resolve: {local_path}")
    return issues


def validate_workspace(root: Path) -> list[Issue]:
    root = root.resolve()
    if root.is_dir() and root.name == "Opportunities":
        root = root.parent
    opportunities_root = root / "Opportunities"
    if not opportunities_root.is_dir():
        return [Issue("Opportunities", 1, "missing-root", "Opportunities directory does not exist")]

    opportunity_paths = sorted(opportunities_root.glob("*.md"))
    task_paths = [root / "TODO.md", *opportunity_paths, *sorted((root / "Projects").glob("*.md"))]
    tasks = scan_tasks(task_paths)
    issues: list[Issue] = []
    documents: list[Document] = []
    for path in opportunity_paths:
        try:
            documents.append(parse_document(path))
        except (OSError, UnicodeError, ParseError) as exc:
            line = exc.line if isinstance(exc, ParseError) else 1
            issues.append(Issue(_relative(path, root), line, "parse-error", str(exc)))

    designated: dict[str, list[Path]] = {}
    for document in documents:
        issues.extend(_validate_document(root, document, tasks, designated))
    for task_id, paths in designated.items():
        if len(paths) > 1:
            for path in paths:
                issues.append(
                    Issue(
                        _relative(path, root),
                        1,
                        "shared-next-action",
                        f"nextAction {task_id!r} is designated by multiple Opportunities",
                    )
                )
    return sorted(set(issues))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="workspace root or its Opportunities directory (default: current directory)",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    args = parser.parse_args(argv)
    issues = validate_workspace(args.workspace)
    if args.json:
        print(json.dumps({"valid": not issues, "issues": [issue.as_dict() for issue in issues]}, indent=2))
    elif issues:
        for issue in issues:
            print(f"{issue.path}:{issue.line}: {issue.code}: {issue.message}")
        print(f"invalid: {len(issues)} issue(s)")
    else:
        print("valid: Opportunity structure")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
