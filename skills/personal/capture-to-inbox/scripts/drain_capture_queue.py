#!/usr/bin/env python3
"""Drain a configured Capture to Inbox queue into a consumer project's Inbox."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

QUEUE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
URL_PATTERN = re.compile(r'https?://[^\s<>"\')\]]+', re.IGNORECASE)
ENV_ASSIGNMENT = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")


class DrainError(RuntimeError):
    pass


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise DrainError(f"configuration file is missing: {path}; run capture-to-inbox setup") from error
    except json.JSONDecodeError as error:
        raise DrainError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise DrainError(f"expected a JSON object in {path}")
    return value


def dotenv_value(path: Path, key: str) -> str | None:
    if not path.exists():
        return None
    if path.stat().st_mode & 0o077:
        raise DrainError(f"local secret file is readable by group or others: {path}; run chmod 600 {path}")

    found: list[tuple[int, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise DrainError(f"local secret file is not valid UTF-8: {path}") from error

    for line_number, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = ENV_ASSIGNMENT.fullmatch(line)
        if not match or match.group(1) != key:
            continue
        value = match.group(2).strip()
        if value.startswith(("'", '"')):
            quote = value[0]
            if len(value) < 2 or value[-1] != quote:
                raise DrainError(f"unterminated quoted value for {key} in {path}:{line_number}")
            value = value[1:-1]
        found.append((line_number, value))

    if len(found) > 1:
        locations = ", ".join(str(line_number) for line_number, _value in found)
        raise DrainError(f"duplicate {key} assignments in {path} at lines {locations}")
    return found[0][1] if found else None


def project_path(project: Path, raw: str, label: str) -> Path:
    relative = Path(raw)
    if relative.is_absolute() or ".." in relative.parts:
        raise DrainError(f"{label} must be a project-relative path")
    resolved = (project / relative).resolve()
    if resolved != project and project not in resolved.parents:
        raise DrainError(f"{label} resolves outside the project")
    return resolved


class ApiClient:
    def __init__(self, api_url: str, token: str, timeout: float) -> None:
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    def request(self, pathname: str, method: str = "GET") -> bytes:
        request = urllib.request.Request(
            f"{self.api_url}{pathname}",
            method=method,
            headers={"Authorization": f"Bearer {self.token}", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            details = error.read(500).decode("utf-8", "replace").strip()
            raise DrainError(f"{method} {pathname} failed: HTTP {error.code} {details}") from error
        except urllib.error.URLError as error:
            raise DrainError(f"{method} {pathname} failed: {error.reason}") from error

    def json(self, pathname: str, method: str = "GET") -> dict[str, Any]:
        try:
            value = json.loads(self.request(pathname, method).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise DrainError(f"{method} {pathname} returned invalid JSON") from error
        if not isinstance(value, dict):
            raise DrainError(f"{method} {pathname} returned a non-object JSON value")
        return value


def normalize_inline(value: Any) -> str:
    return " ".join(str(value or "").split())


def truncate(value: str, length: int) -> str:
    return value if len(value) <= length else f"{value[: length - 3].rstrip()}..."


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def extract_urls(meta: dict[str, Any]) -> list[str]:
    fields = meta.get("fields") if isinstance(meta.get("fields"), dict) else {}
    values = [
        meta.get("shared_urls"),
        meta.get("shared_item"),
        meta.get("shared_input_text"),
        meta.get("context"),
        fields.get("shared_urls"),
        fields.get("shared_item"),
        fields.get("shared_input_text"),
    ]
    urls: list[str] = []
    for value in values:
        for match in URL_PATTERN.findall(str(value or "")):
            urls.append(match.rstrip(".,;:!?"))
    return unique(urls)


def shared_text(meta: dict[str, Any]) -> str:
    fields = meta.get("fields") if isinstance(meta.get("fields"), dict) else {}
    candidates = [
        meta.get("shared_item"),
        meta.get("shared_input_text"),
        fields.get("shared_item"),
        fields.get("shared_input_text"),
    ]
    return next((normalize_inline(value) for value in candidates if normalize_inline(value)), "")


def payload_meta(meta: dict[str, Any]) -> tuple[int, str | None]:
    payload = meta.get("payload") if isinstance(meta.get("payload"), dict) else {}
    try:
        size = int(payload.get("size") or 0)
    except (TypeError, ValueError) as error:
        raise DrainError(f"invalid payload size for {meta.get('id', '<unknown>')}") from error
    digest = payload.get("sha256")
    if size < 0 or (digest is not None and not re.fullmatch(r"[0-9a-fA-F]{64}", str(digest))):
        raise DrainError(f"invalid payload metadata for {meta.get('id', '<unknown>')}")
    return size, str(digest).lower() if digest else None


def sanitize_file_name(value: Any) -> str:
    name = Path(str(value or "payload.bin")).name
    clean = re.sub(r"[^A-Za-z0-9._-]", "_", name)[:180]
    return clean or "payload.bin"


def item_id(meta: dict[str, Any]) -> str:
    value = str(meta.get("id") or "")
    if not QUEUE_ID.fullmatch(value):
        raise DrainError(f"invalid queue item ID: {value!r}")
    return value


def title_for(meta: dict[str, Any], urls: list[str]) -> str:
    payload = meta.get("payload") if isinstance(meta.get("payload"), dict) else {}
    candidates = [
        normalize_inline(meta.get("context")),
        urls[0] if urls else "",
        shared_text(meta),
        normalize_inline(payload.get("original_name") or payload.get("filename")),
        f"Capture {item_id(meta)}",
    ]
    return truncate(next(value for value in candidates if value), 180)


def tags_for(meta: dict[str, Any], urls: list[str]) -> list[str]:
    payload = meta.get("payload") if isinstance(meta.get("payload"), dict) else {}
    mime_type = str(payload.get("mime_type") or "").lower()
    joined_urls = " ".join(urls).lower()
    tags = ["#capture", "#shortcut"]
    if "instagram.com" in joined_urls:
        tags.append("#instagram")
    for prefix, tag in (("image/", "#image"), ("audio/", "#audio"), ("video/", "#video")):
        if mime_type.startswith(prefix):
            tags.append(tag)
    if mime_type == "application/pdf":
        tags.append("#pdf")
    return unique(tags)


def detail_lines(label: str, value: Any) -> list[str]:
    text = str(value or "").replace("\r\n", "\n").strip()
    if not text:
        return []
    if "\n" not in text and len(text) <= 240:
        return [f"  - {label}: {text}"]
    return [f"  - {label}:", *(f"    > {line}" for line in text.split("\n"))]


def build_entry(meta: dict[str, Any], attachment: Path | None, project: Path) -> str:
    identifier = item_id(meta)
    urls = extract_urls(meta)
    text = shared_text(meta)
    context = str(meta.get("context") or "").strip()
    lines = [f"- [ ] {title_for(meta, urls)} {' '.join(tags_for(meta, urls))}"]
    sources = unique([normalize_inline(meta.get("source")), normalize_inline(meta.get("client"))])
    if sources:
        lines.append(f"  - Source: {' / '.join(sources)}")
    if meta.get("captured_at"):
        lines.append(f"  - Captured: {meta['captured_at']}")
    if meta.get("received_at"):
        lines.append(f"  - Received: {meta['received_at']}")
    lines.append(f"  - Queue ID: `{identifier}`")
    lines.extend(detail_lines("Context", context))
    lines.extend(f"  - Link: {url}" for url in urls)
    if text and text not in urls and normalize_inline(text) != normalize_inline(context):
        lines.extend(detail_lines("Shared text", text))
    if attachment:
        lines.append(f"  - Attachment: [[{attachment.relative_to(project).as_posix()}]]")
    elif payload_meta(meta)[0] == 0:
        lines.append("  - Payload: none")
    return "\n".join(lines) + "\n"


def marker(identifier: str) -> str:
    return f"Queue ID: `{identifier}`"


def atomic_payload_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def verify_payload(data: bytes, expected_size: int, expected_sha256: str | None, identifier: str) -> None:
    if len(data) != expected_size:
        raise DrainError(
            f"downloaded payload size mismatch for {identifier}: expected {expected_size}, got {len(data)}"
        )
    if expected_sha256 and hashlib.sha256(data).hexdigest() != expected_sha256:
        raise DrainError(f"downloaded payload checksum mismatch for {identifier}")


def date_folder(meta: dict[str, Any]) -> str:
    raw = str(meta.get("received_at") or meta.get("captured_at") or "")
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", raw)
    return match.group(1) if match else "undated"


def download_payload(
    client: ApiClient, meta: dict[str, Any], attachments_root: Path, project: Path
) -> Path | None:
    identifier = item_id(meta)
    size, expected_sha256 = payload_meta(meta)
    if not size:
        return None
    payload = meta.get("payload") if isinstance(meta.get("payload"), dict) else {}
    name = sanitize_file_name(payload.get("original_name") or payload.get("filename"))
    target = attachments_root / date_folder(meta) / f"{identifier}-{name}"
    if project != target and project not in target.resolve().parents:
        raise DrainError(f"attachment path resolves outside the project: {target}")
    if target.exists():
        data = target.read_bytes()
        verify_payload(data, size, expected_sha256, identifier)
        return target
    quoted_id = urllib.parse.quote(identifier, safe="")
    data = client.request(f"/queue/items/{quoted_id}/payload")
    verify_payload(data, size, expected_sha256, identifier)
    atomic_payload_write(target, data)
    return target


def append_entry(inbox: Path, current: str, entry: str) -> str:
    separator = "" if current.endswith("\n\n") else "\n" if current.endswith("\n") else "\n\n"
    addition = f"{separator}{entry}"
    with inbox.open("a", encoding="utf-8") as handle:
        handle.write(addition)
        handle.flush()
        os.fsync(handle.fileno())
    return current + addition


def describe(meta: dict[str, Any]) -> str:
    size, _digest = payload_meta(meta)
    payload = meta.get("payload") if isinstance(meta.get("payload"), dict) else {}
    description = (
        f"{size} bytes {payload.get('original_name') or payload.get('filename') or ''}".strip()
        if size
        else "no payload"
    )
    return f"{item_id(meta)} | {title_for(meta, extract_urls(meta))} | {description}"


def resolve_runtime(args: argparse.Namespace) -> tuple[Path, Path, Path, str, str]:
    project = args.project.resolve()
    if not project.is_dir():
        raise DrainError(f"project directory does not exist: {project}")
    config_path = args.config.resolve() if args.config else project / "control-plane" / "config.json"
    config = load_json_object(config_path)
    paths = config.get("paths") if isinstance(config.get("paths"), dict) else {}
    capture = config.get("capture_to_inbox") if isinstance(config.get("capture_to_inbox"), dict) else {}
    try:
        inbox = project_path(project, paths["inbox"], "paths.inbox")
        attachments = project_path(project, paths["attachments"], "paths.attachments")
        deployment_path = project_path(project, capture["deployment"], "capture_to_inbox.deployment")
        token_env = str(capture["token_env"])
    except (KeyError, TypeError) as error:
        raise DrainError(f"incomplete capture configuration in {config_path}") from error
    deployment = load_json_object(deployment_path)
    api_url = (args.api_url or deployment.get("api_url") or "").rstrip("/")
    if not api_url.startswith(("http://", "https://")):
        raise DrainError(f"deployment API URL is not configured in {deployment_path}")
    local_env = project_path(
        project,
        str(capture.get("token_file") or ".env"),
        "capture_to_inbox.token_file",
    )
    file_token = dotenv_value(local_env, token_env)
    token = file_token if file_token is not None else os.environ.get(token_env, "")
    if not token:
        raise DrainError(
            f"required bearer token is missing: set {token_env} in {local_env} "
            "or in the process environment"
        )
    if not inbox.is_file():
        raise DrainError(f"Inbox is missing: {inbox}; run capture-to-inbox setup")
    return project, inbox, attachments, api_url, token


def run(args: argparse.Namespace) -> int:
    project, inbox, attachments, api_url, token = resolve_runtime(args)
    client = ApiClient(api_url, token, args.timeout)
    listed = client.json("/queue/items")
    all_items = listed.get("items")
    if not isinstance(all_items, list) or not all(isinstance(item, dict) for item in all_items):
        raise DrainError("GET /queue/items returned an invalid items list")
    items = all_items[: args.limit] if args.limit else all_items
    if not items:
        print("Queue is empty.")
        return 0

    inbox_text = inbox.read_text(encoding="utf-8")
    if args.dry_run:
        print(f"Dry run: {len(items)} of {len(all_items)} queue item(s).")
        for item in items:
            identifier = item_id(item)
            state = "already in inbox" if marker(identifier) in inbox_text else "new"
            print(f"- {describe(item)} | {state}")
        return 0

    counts = {"appended": 0, "downloaded": 0, "deleted": 0, "seen": 0, "failed": 0}
    for item in items:
        try:
            identifier = item_id(item)
            quoted_id = urllib.parse.quote(identifier, safe="")
            if marker(identifier) in inbox_text:
                counts["seen"] += 1
                if not args.keep_remote:
                    client.json(f"/queue/items/{quoted_id}", "DELETE")
                    counts["deleted"] += 1
                print(f"[seen] {identifier}")
                continue

            attachment = download_payload(client, item, attachments, project)
            if attachment:
                counts["downloaded"] += 1
            inbox_text = append_entry(inbox, inbox_text, build_entry(item, attachment, project))
            counts["appended"] += 1
            if not args.keep_remote:
                client.json(f"/queue/items/{quoted_id}", "DELETE")
                counts["deleted"] += 1
            print(f"[drained] {identifier}")
        except (DrainError, OSError) as error:
            counts["failed"] += 1
            print(f"[failed] {item.get('id', '<unknown>')}: {error}", file=sys.stderr)

    print(
        "Done. "
        f"Appended {counts['appended']}, downloaded {counts['downloaded']}, "
        f"deleted {counts['deleted']}, seen {counts['seen']}, failed {counts['failed']}."
    )
    return 1 if counts["failed"] else 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="consumer project root")
    parser.add_argument("--config", type=Path, help="config path (default: <project>/control-plane/config.json)")
    parser.add_argument("--api-url", help="temporary API URL override")
    parser.add_argument("--dry-run", action="store_true", help="list without local writes or remote deletes")
    parser.add_argument("--keep-remote", action="store_true", help="write locally without deleting queue items")
    parser.add_argument("--limit", type=int, help="process only the first positive number of items")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    args = parser.parse_args(argv)
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be a positive integer")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    return args


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv))
    except DrainError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
