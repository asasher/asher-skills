#!/usr/bin/env python3
"""Create a named T3 Code thread through the local orchestration API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import NoReturn, Sequence


class T3ThreadError(RuntimeError):
    """A user-actionable T3 dispatch failure."""


class RefuseRedirects(urllib.request.HTTPRedirectHandler):
    """Keep short-lived bearer credentials on the validated origin."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> None:
        return None


def fail(message: str) -> NoReturn:
    raise T3ThreadError(message)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        fail(f"T3 runtime file was not found: {path}")
    except (OSError, json.JSONDecodeError) as error:
        fail(f"T3 runtime file is unreadable: {path}: {error}")
    if not isinstance(value, dict):
        fail(f"T3 runtime file is not a JSON object: {path}")
    return value


def discover_executable(explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        if not candidate.is_file():
            fail(f"T3 executable was not found: {candidate}")
        return candidate

    candidates = [
        Path("/Applications/T3 Code (Alpha).app/Contents/MacOS/T3 Code (Alpha)"),
        Path("/Applications/T3 Code.app/Contents/MacOS/T3 Code"),
    ]
    candidates.extend(sorted(Path("/Applications").glob("T3 Code*.app/Contents/MacOS/T3 Code*")))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    fail("no local T3 Code executable was found under /Applications")


def discover_server_entry(executable: Path, explicit: str | None) -> Path:
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
    else:
        try:
            app_root = executable.parents[2]
        except IndexError:
            fail(f"cannot derive the T3 application root from: {executable}")
        candidate = app_root / "Contents/Resources/app.asar/apps/server/dist/bin.mjs"
    if candidate.is_file():
        return candidate
    candidate_text = str(candidate)
    archive_marker = ".asar/"
    if archive_marker in candidate_text:
        archive = Path(candidate_text.split(archive_marker, 1)[0] + ".asar")
        if archive.is_file():
            return candidate
    fail(f"T3 server CLI entry was not found: {candidate}")


def local_origin(runtime: dict[str, object]) -> str:
    origin = runtime.get("origin")
    if not isinstance(origin, str) or not origin:
        fail("T3 runtime does not advertise an origin")
    parsed = urllib.parse.urlparse(origin)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "127.0.0.1",
        "localhost",
        "::1",
    }:
        fail(f"T3 runtime origin is not local: {origin}")
    return origin.rstrip("/")


def auth_command(
    executable: Path,
    server_entry: Path,
    base_dir: Path,
    *args: str,
) -> list[str]:
    return [
        str(executable),
        str(server_entry),
        "auth",
        "session",
        *args,
        "--base-dir",
        str(base_dir),
        "--log-level",
        "none",
    ]


def run_auth(command: list[str]) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["ELECTRON_RUN_AS_NODE"] = "1"
    return subprocess.run(
        command,
        check=False,
        text=True,
        capture_output=True,
        env=environment,
    )


def issue_session(
    executable: Path,
    server_entry: Path,
    base_dir: Path,
    label: str,
) -> tuple[str, str]:
    command = auth_command(
        executable,
        server_entry,
        base_dir,
        "issue",
        "--ttl",
        "5m",
        "--label",
        label,
        "--subject",
        "local to-thread dispatch",
        "--json",
    )
    result = run_auth(command)
    if result.returncode:
        detail = result.stderr.strip() or "T3 did not issue a bearer session"
        fail(f"could not issue a short-lived T3 session: {detail}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        fail(f"T3 issued unreadable session metadata: {error}")
    token = payload.get("token") if isinstance(payload, dict) else None
    session_id = payload.get("sessionId") if isinstance(payload, dict) else None
    if not isinstance(token, str) or not token:
        fail("T3 session metadata contains no bearer token")
    if not isinstance(session_id, str) or not session_id:
        fail("T3 session metadata contains no revocable session id")
    return token, session_id


def revoke_session(
    executable: Path,
    server_entry: Path,
    base_dir: Path,
    session_id: str,
) -> None:
    command = auth_command(
        executable,
        server_entry,
        base_dir,
        "revoke",
        session_id,
    )
    result = run_auth(command)
    if result.returncode:
        detail = result.stderr.strip() or "T3 session revoke failed"
        fail(f"temporary T3 session {session_id} was not revoked: {detail}")


def http_json(
    origin: str,
    token: str,
    method: str,
    path: str,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        f"{origin}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        opener = urllib.request.build_opener(RefuseRedirects)
        with opener.open(request, timeout=10) as response:
            value = json.load(response)
    except urllib.error.HTTPError as error:
        if 300 <= error.code < 400:
            fail(f"T3 refused an HTTP redirect at {path}")
        body = error.read().decode(errors="replace").strip()
        fail(f"{payload.get('type') if payload else path} failed with HTTP {error.code}: {body}")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        fail(f"T3 request failed at {path}: {error}")
    if not isinstance(value, dict):
        fail(f"T3 returned a non-object response at {path}")
    return value


def resolve_project(snapshot: dict[str, object], project_directory: Path) -> str:
    projects = snapshot.get("projects")
    if not isinstance(projects, list):
        fail("T3 orchestration snapshot has no projects list")
    target = project_directory.resolve()
    matches = [
        project
        for project in projects
        if isinstance(project, dict)
        and project.get("deletedAt") is None
        and isinstance(project.get("workspaceRoot"), str)
        and Path(str(project["workspaceRoot"])).expanduser().resolve() == target
    ]
    if len(matches) != 1:
        fail(f"expected one active T3 project for {target}, found {len(matches)}")
    project_id = matches[0].get("id")
    if not isinstance(project_id, str) or not project_id:
        fail(f"T3 project for {target} has no id")
    return project_id


def command_sequence(response: dict[str, object], command_type: str) -> int:
    sequence = response.get("sequence")
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
        fail(f"T3 did not acknowledge {command_type} with a valid sequence")
    return sequence


def delete_thread(origin: str, token: str, thread_id: str) -> int:
    payload: dict[str, object] = {
        "type": "thread.delete",
        "commandId": str(uuid.uuid4()),
        "threadId": thread_id,
    }
    response = http_json(
        origin,
        token,
        "POST",
        "/api/orchestration/dispatch",
        payload,
    )
    return command_sequence(response, "thread.delete")


def model_selection(args: argparse.Namespace) -> dict[str, object]:
    options: list[dict[str, str]] = [{"id": "reasoningEffort", "value": args.effort}]
    if args.service_tier:
        options.append({"id": "serviceTier", "value": args.service_tier})
    return {
        "instanceId": args.provider,
        "model": args.model,
        "options": options,
    }


def infer_worktree_path(project_directory: Path, directory: Path) -> str | None:
    project = project_directory.resolve()
    working = directory.resolve()
    return None if project == working else str(working)


def create_thread(args: argparse.Namespace, origin: str, token: str) -> dict[str, object]:
    project_directory = Path(args.project_directory).expanduser().resolve()
    directory = Path(args.directory).expanduser().resolve()
    if not project_directory.is_dir():
        fail(f"project directory does not exist: {project_directory}")
    if not directory.is_dir():
        fail(f"thread directory does not exist: {directory}")

    snapshot = http_json(origin, token, "GET", "/api/orchestration/snapshot")
    project_id = resolve_project(snapshot, project_directory)
    thread_id = str(uuid.uuid4())
    created_at = utc_now()
    selection = model_selection(args)
    worktree_path = infer_worktree_path(project_directory, directory)

    create_payload: dict[str, object] = {
        "type": "thread.create",
        "commandId": str(uuid.uuid4()),
        "threadId": thread_id,
        "projectId": project_id,
        "title": args.name,
        "modelSelection": selection,
        "runtimeMode": args.runtime_mode,
        "interactionMode": args.interaction_mode,
        "branch": args.branch,
        "worktreePath": worktree_path,
        "createdAt": created_at,
    }
    try:
        create_response = http_json(
            origin,
            token,
            "POST",
            "/api/orchestration/dispatch",
            create_payload,
        )
        create_sequence = command_sequence(create_response, "thread.create")
    except T3ThreadError as create_error:
        try:
            delete_thread(origin, token, thread_id)
        except T3ThreadError as delete_error:
            fail(f"{create_error}; ambiguous thread {thread_id} cleanup failed: {delete_error}")
        raise create_error

    turn_payload: dict[str, object] = {
        "type": "thread.turn.start",
        "commandId": str(uuid.uuid4()),
        "threadId": thread_id,
        "message": {
            "messageId": str(uuid.uuid4()),
            "role": "user",
            "text": args.prompt,
            "attachments": [],
        },
        "modelSelection": selection,
        "runtimeMode": args.runtime_mode,
        "interactionMode": args.interaction_mode,
        "createdAt": created_at,
    }
    try:
        turn_response = http_json(
            origin,
            token,
            "POST",
            "/api/orchestration/dispatch",
            turn_payload,
        )
        turn_sequence = command_sequence(turn_response, "thread.turn.start")
    except T3ThreadError as turn_error:
        try:
            delete_thread(origin, token, thread_id)
        except T3ThreadError as delete_error:
            fail(f"{turn_error}; partial thread {thread_id} cleanup failed: {delete_error}")
        raise turn_error
    return {
        "branch": args.branch,
        "create_sequence": create_sequence,
        "name": args.name,
        "project_id": project_id,
        "thread_id": thread_id,
        "turn_sequence": turn_sequence,
        "worktree_path": worktree_path,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Create a named thread in the running local T3 Code supervisor."
    )
    result.add_argument("--name", required=True)
    result.add_argument("--prompt", required=True)
    result.add_argument("--project-directory", required=True)
    result.add_argument("--directory", required=True)
    result.add_argument("--branch", required=True)
    result.add_argument("--provider", default="codex")
    result.add_argument("--model", required=True)
    result.add_argument("--effort", required=True)
    result.add_argument("--service-tier")
    result.add_argument("--runtime-mode", required=True)
    result.add_argument("--interaction-mode", default="default")
    result.add_argument("--base-dir", default=str(Path.home() / ".t3"))
    result.add_argument("--runtime-file")
    result.add_argument("--t3-executable")
    result.add_argument("--server-entry")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    base_dir = Path(args.base_dir).expanduser().resolve()
    runtime_file = (
        Path(args.runtime_file).expanduser().resolve()
        if args.runtime_file
        else base_dir / "userdata/server-runtime.json"
    )
    session_id: str | None = None
    result_payload: dict[str, object] | None = None
    failure: T3ThreadError | None = None
    try:
        executable = discover_executable(args.t3_executable)
        server_entry = discover_server_entry(executable, args.server_entry)
        origin = local_origin(load_json(runtime_file))
        token, session_id = issue_session(
            executable,
            server_entry,
            base_dir,
            f"to-thread: {args.name}",
        )
        result_payload = create_thread(args, origin, token)
    except T3ThreadError as error:
        failure = error
    finally:
        if session_id:
            try:
                revoke_session(executable, server_entry, base_dir, session_id)
            except T3ThreadError as revoke_error:
                failure = (
                    T3ThreadError(f"{failure}; {revoke_error}")
                    if failure
                    else revoke_error
                )

    if failure:
        print(f"t3-thread: {failure}", file=sys.stderr)
        return 2
    print(json.dumps(result_payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
