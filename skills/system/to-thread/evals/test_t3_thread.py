#!/usr/bin/env python3
"""Integration-style tests for the public T3 thread helper."""

from __future__ import annotations

import base64
import importlib.util
import json
import os
import subprocess
import tempfile
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "t3-thread.py"


def token_for(session_id: str) -> str:
    payload = json.dumps({"sid": session_id}, separators=(",", ":")).encode()
    encoded = base64.urlsafe_b64encode(payload).decode().rstrip("=")
    return f"{encoded}.signature"


class ApiState:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.posts: list[dict[str, object]] = []
        self.fail_turn = False
        self.fail_turn_status = 500
        self.include_other_project = False
        self.include_deleted_same_root = False
        self.snapshot_redirect: str | None = None
        self.bad_create_ack = False
        self.bad_turn_ack = False
        self.drop_turn_ack = False
        self.invalid_utf8_turn_ack = False
        self.truncated_turn_error = False
        self.reject_create_empty_400 = False
        self.reject_turn_empty_400 = False
        self.reject_delete_empty_400 = False
        self.fail_create = False
        self.fail_delete = False


class Handler(BaseHTTPRequestHandler):
    server: "ApiServer"

    def do_GET(self) -> None:
        if self.path != "/api/orchestration/shell":
            self.send_error(404)
            return
        if self.server.state.snapshot_redirect:
            self.send_response(302)
            self.send_header("Location", self.server.state.snapshot_redirect)
            self.end_headers()
            return
        projects = [
            {
                "id": "project-1",
                "title": "Project",
                "workspaceRoot": str(self.server.state.project_root),
            }
        ]
        if self.server.state.include_other_project:
            projects.append(
                {
                    "id": "project-2",
                    "title": "Other",
                    "workspaceRoot": str(self.server.state.project_root.parent / "other"),
                }
            )
        if self.server.state.include_deleted_same_root:
            # Defensive shape: the live shell payload carries no deletedAt today,
            # but an explicit tombstone must stay excluded if the field returns.
            projects.append(
                {
                    "id": "project-tombstone",
                    "title": "Deleted twin",
                    "workspaceRoot": str(self.server.state.project_root),
                    "deletedAt": "2026-07-01T00:00:00Z",
                }
            )
        self.respond(
            200,
            {
                "projects": projects,
                "threads": [],
                "snapshotSequence": 1,
                "updatedAt": "2026-07-30T00:00:00Z",
            },
        )

    def do_POST(self) -> None:
        if self.path != "/api/orchestration/dispatch":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length))
        self.server.state.posts.append(payload)
        if payload["type"] == "thread.create" and self.server.state.reject_create_empty_400:
            # Mirror the live app: a payload the schema refuses gets a bare 400.
            self.send_response(400)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if payload["type"] == "thread.turn.start" and self.server.state.reject_turn_empty_400:
            self.send_response(400)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if payload["type"] == "thread.delete" and self.server.state.reject_delete_empty_400:
            self.send_response(400)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if payload["type"] == "thread.create" and self.server.state.fail_create:
            self.respond_dispatch_failed()
            return
        if payload["type"] == "thread.delete" and self.server.state.fail_delete:
            self.respond_dispatch_failed()
            return
        if payload["type"] == "thread.create" and self.server.state.bad_create_ack:
            self.respond(200, {"error": "command was not acknowledged"})
            return
        if payload["type"] == "thread.turn.start" and self.server.state.drop_turn_ack:
            self.close_connection = True
            return
        if payload["type"] == "thread.turn.start" and self.server.state.invalid_utf8_turn_ack:
            self.send_response(200)
            self.send_header("Content-Length", "1")
            self.end_headers()
            self.wfile.write(b"\xff")
            return
        if payload["type"] == "thread.turn.start" and self.server.state.truncated_turn_error:
            self.send_response(400)
            self.send_header("Content-Length", "10")
            self.end_headers()
            self.wfile.write(b"x")
            self.close_connection = True
            return
        if payload["type"] == "thread.turn.start" and self.server.state.bad_turn_ack:
            self.respond(200, {"error": "command was not acknowledged"})
            return
        if payload["type"] == "thread.turn.start" and self.server.state.fail_turn:
            self.respond(self.server.state.fail_turn_status, {"error": "dispatch failed"})
            return
        self.respond(200, {"sequence": len(self.server.state.posts)})

    def respond_dispatch_failed(self) -> None:
        # Mirror the live app's engine failure envelope.
        self.respond(
            500,
            {
                "_tag": "EnvironmentInternalError",
                "code": "internal_error",
                "reason": "orchestration_dispatch_failed",
            },
        )

    def respond(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


class ApiServer(ThreadingHTTPServer):
    def __init__(self, state: ApiState) -> None:
        super().__init__(("127.0.0.1", 0), Handler)
        self.state = state


class T3ThreadHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sandbox = tempfile.TemporaryDirectory()
        self.root = Path(self.sandbox.name)
        self.project = self.root / "project"
        self.worktree = self.root / "project-worktrees" / "136-shape"
        self.project.mkdir()
        self.worktree.mkdir(parents=True)
        self.state = ApiState(self.project.resolve())
        self.server = ApiServer(self.state)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        self.origin = f"http://127.0.0.1:{self.server.server_port}"

        self.runtime_file = self.root / "server-runtime.json"
        self.runtime_file.write_text(json.dumps({"version": 1, "origin": self.origin}))
        self.base_dir = self.root / ".t3"
        self.base_dir.mkdir()
        self.revoke_log = self.root / "revoked.txt"
        self.server_entry = self.root / "bin.mjs"
        self.server_entry.write_text("// placeholder\n")
        self.fake_cli = self.root / "fake-t3-cli.py"
        self.fake_cli.write_text(
            """#!/usr/bin/env python3
import os
import pathlib
import sys
import json

args = sys.argv[2:]
if args[:3] == ["auth", "session", "issue"]:
    if "--json" in args:
        print(json.dumps({
            "token": os.environ["FAKE_T3_TOKEN"],
            "sessionId": os.environ["FAKE_T3_SESSION_ID"],
            "subject": "local to-thread dispatch",
        }))
    else:
        print(os.environ["FAKE_T3_TOKEN"])
    raise SystemExit(0)
if args[:3] == ["auth", "session", "revoke"]:
    pathlib.Path(os.environ["FAKE_T3_REVOKE_LOG"]).write_text(args[3] + "\\n")
    if os.environ.get("FAKE_T3_REVOKE_INVALID_BYTES") == "1":
        sys.stdout.buffer.write(bytes([255]))
    raise SystemExit(int(os.environ.get("FAKE_T3_REVOKE_FAIL", "0")))
raise SystemExit(2)
"""
        )
        self.fake_cli.chmod(0o755)
        self.fake_app_cli = self.root / "T3 Code.app" / "Contents" / "MacOS" / "T3 Code"
        self.fake_app_cli.parent.mkdir(parents=True)
        self.fake_app_cli.write_text(self.fake_cli.read_text())
        self.fake_app_cli.chmod(0o755)
        fake_archive = self.root / "T3 Code.app" / "Contents" / "Resources" / "app.asar"
        fake_archive.parent.mkdir(parents=True)
        fake_archive.write_text("archive placeholder\n")
        self.session_id = "session-123"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join(timeout=2)
        self.sandbox.cleanup()

    def run_helper(
        self,
        *,
        check: bool = True,
        revoke_fail: bool = False,
        revoke_invalid_bytes: bool = False,
        derive_server_entry: bool = False,
        token: str | None = None,
        effort: str = "high",
        provider: str | None = None,
        effort_option_id: str | None = None,
        prompt: str = "Shape ticket #136 and wait for the user.",
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["FAKE_T3_TOKEN"] = token or token_for(self.session_id)
        env["FAKE_T3_SESSION_ID"] = self.session_id
        env["FAKE_T3_REVOKE_LOG"] = str(self.revoke_log)
        env["FAKE_T3_REVOKE_FAIL"] = "1" if revoke_fail else "0"
        env["FAKE_T3_REVOKE_INVALID_BYTES"] = "1" if revoke_invalid_bytes else "0"
        command = [
                "python3",
                str(SCRIPT),
                "--name",
                "shape-driver-payouts",
                "--prompt",
                prompt,
                "--project-directory",
                str(self.project),
                "--directory",
                str(self.worktree),
                "--branch",
                "136-shape",
                "--model",
                "gpt-5.6-sol",
                "--effort",
                effort,
                "--runtime-mode",
                "approval-required",
                "--base-dir",
                str(self.base_dir),
                "--runtime-file",
                str(self.runtime_file),
                "--t3-executable",
                str(self.fake_app_cli if derive_server_entry else self.fake_cli),
            ]
        if provider is not None:
            command.extend(["--provider", provider])
        if effort_option_id is not None:
            command.extend(["--effort-option-id", effort_option_id])
        if not derive_server_entry:
            command.extend(["--server-entry", str(self.server_entry)])
        result = subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=True,
            env=env,
        )
        if check and result.returncode:
            self.fail(f"helper failed: {result.stderr}")
        return result

    def test_creates_and_starts_named_thread_with_external_worktree(self) -> None:
        result = self.run_helper()
        output = json.loads(result.stdout)

        self.assertEqual(0, result.returncode)
        self.assertEqual("shape-driver-payouts", output["name"])
        self.assertEqual("project-1", output["project_id"])
        self.assertEqual(str(self.worktree.resolve()), output["worktree_path"])
        self.assertEqual(2, len(self.state.posts))

        create, turn = self.state.posts
        self.assertEqual("thread.create", create["type"])
        self.assertEqual("project-1", create["projectId"])
        self.assertEqual("136-shape", create["branch"])
        self.assertEqual(str(self.worktree.resolve()), create["worktreePath"])
        self.assertEqual("gpt-5.6-sol", create["modelSelection"]["model"])
        self.assertEqual("thread.turn.start", turn["type"])
        self.assertEqual(create["threadId"], turn["threadId"])
        self.assertNotIn("titleSeed", turn)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_resolves_exact_workspace_when_snapshot_has_multiple_projects(self) -> None:
        self.state.include_other_project = True

        result = self.run_helper()
        output = json.loads(result.stdout)

        self.assertEqual("project-1", output["project_id"])
        self.assertEqual("project-1", self.state.posts[0]["projectId"])

    def test_accepts_server_entry_inside_present_asar_archive(self) -> None:
        result = self.run_helper(derive_server_entry=True)

        self.assertEqual(0, result.returncode)
        self.assertEqual(2, len(self.state.posts))

    def test_accepts_opaque_token_and_revokes_structured_session_id(self) -> None:
        result = self.run_helper(token="opaque-local-token")

        self.assertEqual(0, result.returncode)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def assert_unknown_turn(self, result) -> None:
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            ["thread.create", "thread.turn.start"],
            [post["type"] for post in self.state.posts],
        )
        output = json.loads(result.stdout)
        self.assertEqual(self.state.posts[0]["threadId"], output["thread_id"])
        self.assertEqual("unknown", output["turn_state"])
        self.assertEqual("retained", output["ownership"])
        self.assertEqual(str(self.worktree.resolve()), output["worktree_path"])
        self.assertIn(output["thread_id"], result.stderr)
        self.assertIn("liveness is unknown", result.stderr)
        self.assertNotIn("without a running turn", result.stderr)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_retains_identity_and_ownership_when_start_returns_500(self) -> None:
        self.state.fail_turn = True
        self.assert_unknown_turn(self.run_helper(check=False))

    def test_retains_identity_and_ownership_when_start_response_is_lost(self) -> None:
        self.state.drop_turn_ack = True
        self.assert_unknown_turn(self.run_helper(check=False))

    def test_http_timeout_is_ambiguous_even_with_a_4xx_status(self) -> None:
        self.state.fail_turn = True
        self.state.fail_turn_status = 408
        self.assert_unknown_turn(self.run_helper(check=False))

    def test_invalid_utf8_start_ack_preserves_identity_and_ownership(self) -> None:
        self.state.invalid_utf8_turn_ack = True
        self.assert_unknown_turn(self.run_helper(check=False))

    def test_truncated_error_body_is_ambiguous_even_with_http_400(self) -> None:
        self.state.truncated_turn_error = True
        result = self.run_helper(check=False)
        self.assert_unknown_turn(result)
        self.assertNotIn("schema decode", result.stderr)

    def test_success_identity_survives_revoke_failure(self) -> None:
        result = self.run_helper(check=False, revoke_fail=True)
        self.assertNotEqual(0, result.returncode)
        output = json.loads(result.stdout)
        self.assertEqual(self.state.posts[0]["threadId"], output["thread_id"])
        self.assertEqual("start_acknowledged", output["turn_state"])
        self.assertEqual("failed", output["session_revocation"])
        self.assertEqual(self.session_id, output["session_id"])
        self.assertEqual(2, len(self.state.posts))

    def test_success_identity_survives_invalid_auth_output_during_revoke(self) -> None:
        result = self.run_helper(check=False, revoke_invalid_bytes=True)
        self.assertNotEqual(0, result.returncode)
        output = json.loads(result.stdout)
        self.assertEqual(self.state.posts[0]["threadId"], output["thread_id"])
        self.assertEqual("start_acknowledged", output["turn_state"])
        self.assertEqual("failed", output["session_revocation"])
        self.assertEqual("retained", output["ownership"])
        self.assertEqual(2, len(self.state.posts))

    def test_deletes_ambiguous_creation_when_success_ack_is_invalid(self) -> None:
        self.state.bad_create_ack = True

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("acknowledge", result.stderr.lower())
        self.assertEqual(
            ["thread.create", "thread.delete"],
            [post["type"] for post in self.state.posts],
        )
        self.assertEqual(self.state.posts[0]["threadId"], self.state.posts[1]["threadId"])
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_retains_identity_and_ownership_when_start_ack_is_invalid(self) -> None:
        self.state.bad_turn_ack = True
        self.assert_unknown_turn(self.run_helper(check=False))

    def test_reports_shape_drift_without_cleanup_when_create_is_rejected(self) -> None:
        self.state.reject_create_empty_400 = True

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("drifted", result.stderr)
        self.assertIn("nothing was created", result.stderr)
        self.assertIn("full-access", result.stderr)
        # A schema rejection applies nothing, so no compensating delete is sent.
        self.assertEqual(["thread.create"], [post["type"] for post in self.state.posts])
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_turn_shape_drift_report_does_not_claim_nothing_was_created(self) -> None:
        self.state.reject_turn_empty_400 = True

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("drifted", result.stderr)
        # The thread was created before the turn was refused, so the report must
        # not claim nothing was created — and the compensating delete must run.
        self.assertNotIn("nothing was created", result.stderr)
        self.assertEqual(
            ["thread.create", "thread.turn.start", "thread.delete"],
            [post["type"] for post in self.state.posts],
        )
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_delete_drift_report_omits_enum_advice_for_fields_not_sent(self) -> None:
        # Correlated drift: create fails outright (5xx), and the compensating
        # thread.delete is itself rejected at schema decode. The delete's drift
        # report must not steer the operator at runtimeMode/interactionMode —
        # fields ThreadDeleteCommand never carries.
        self.state.fail_create = True
        self.state.reject_delete_empty_400 = True

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("thread.delete", result.stderr)
        self.assertIn("drifted", result.stderr)
        self.assertIn("non-empty after trimming", result.stderr)
        self.assertNotIn("runtimeMode", result.stderr)
        self.assertNotIn("interactionMode", result.stderr)
        self.assertEqual(
            ["thread.create", "thread.delete"],
            [post["type"] for post in self.state.posts],
        )
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_resolves_active_project_when_tombstoned_entry_shares_root(self) -> None:
        self.state.include_deleted_same_root = True

        result = self.run_helper()
        output = json.loads(result.stdout)

        self.assertEqual("project-1", output["project_id"])
        self.assertEqual("project-1", self.state.posts[0]["projectId"])

    def test_rejects_blank_prompt_before_dispatching(self) -> None:
        result = self.run_helper(check=False, prompt="   ")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("--prompt", result.stderr)
        self.assertNotIn("drifted", result.stderr)
        self.assertEqual([], self.state.posts)
        # Argument-local validation fails before any session is issued, so
        # there is nothing to revoke.
        self.assertFalse(self.revoke_log.exists())

    def test_names_orphaned_thread_when_partial_delete_fails(self) -> None:
        self.state.reject_turn_empty_400 = True
        self.state.fail_delete = True

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            ["thread.create", "thread.turn.start", "thread.delete"],
            [post["type"] for post in self.state.posts],
        )
        thread_id = str(self.state.posts[0]["threadId"])
        self.assertIn(thread_id, result.stderr)
        self.assertIn("shape-driver-payouts", result.stderr)
        self.assertIn("discard", result.stderr)
        # Creation is known, but a lost delete response cannot establish
        # whether the thread still exists.
        self.assertIn("was created", result.stderr)
        self.assertIn("deletion is unconfirmed", result.stderr)
        self.assertEqual("unknown", json.loads(result.stdout)["thread_state"])
        self.assertNotIn("if it appears there", result.stderr)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_names_orphaned_thread_when_ambiguous_create_cleanup_fails(self) -> None:
        self.state.fail_create = True
        self.state.fail_delete = True

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            ["thread.create", "thread.delete"],
            [post["type"] for post in self.state.posts],
        )
        thread_id = str(self.state.posts[0]["threadId"])
        self.assertIn(thread_id, result.stderr)
        self.assertIn("discard", result.stderr)
        # Creation is genuinely ambiguous on this path, so the notice keeps
        # its conditional phrasing.
        self.assertIn("may have been left", result.stderr)
        self.assertIn("if it appears there", result.stderr)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_sends_the_effort_option_id_each_driver_reads(self) -> None:
        # The drivers ignore option ids they do not read, so a mis-labeled
        # effort silently runs the thread at the default: the id must match
        # the driver, not be one constant for every provider.
        self.run_helper(provider="claudeAgent")
        self.assertEqual(
            [{"id": "effort", "value": "high"}],
            self.state.posts[0]["modelSelection"]["options"],
        )

        self.state.posts.clear()
        self.run_helper(provider="codex")
        self.assertEqual(
            [{"id": "reasoningEffort", "value": "high"}],
            self.state.posts[0]["modelSelection"]["options"],
        )

    def test_fails_before_dispatch_for_unmappable_provider_instance(self) -> None:
        result = self.run_helper(check=False, provider="codex-personal")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("--effort-option-id", result.stderr)
        self.assertEqual([], self.state.posts)
        # Argument-local validation fails before any session is issued, so
        # there is nothing to revoke.
        self.assertFalse(self.revoke_log.exists())

    def test_explicit_effort_option_id_covers_renamed_instances(self) -> None:
        self.run_helper(provider="codex-personal", effort_option_id="reasoningEffort")

        self.assertEqual(
            [{"id": "reasoningEffort", "value": "high"}],
            self.state.posts[0]["modelSelection"]["options"],
        )

    def test_rejects_blank_effort_before_dispatching(self) -> None:
        result = self.run_helper(check=False, effort="   ")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("--effort", result.stderr)
        self.assertNotIn("drifted", result.stderr)
        self.assertEqual([], self.state.posts)
        # Argument-local validation fails before any session is issued, so
        # there is nothing to revoke.
        self.assertFalse(self.revoke_log.exists())

    def test_fails_before_creation_when_project_is_not_registered(self) -> None:
        self.state.project_root = self.root / "different-project"

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("project", result.stderr.lower())
        self.assertEqual([], self.state.posts)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())

    def test_refuses_http_redirects_before_forwarding_bearer_credentials(self) -> None:
        self.state.snapshot_redirect = "http://127.0.0.1:9/credential-leak"

        result = self.run_helper(check=False)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("redirect", result.stderr.lower())
        self.assertEqual([], self.state.posts)
        self.assertEqual(self.session_id, self.revoke_log.read_text().strip())


class AuthTimeoutTests(unittest.TestCase):
    def test_silent_auth_child_is_killed_and_reaped(self) -> None:
        spec = importlib.util.spec_from_file_location("t3_thread", SCRIPT)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        children = []
        popen = subprocess.Popen

        def launch(*args, **kwargs):
            child = popen(*args, **kwargs)
            children.append(child)
            return child

        with mock.patch.object(helper, "AUTH_TIMEOUT_SECONDS", 0.1, create=True), mock.patch.object(
            helper.subprocess, "Popen", side_effect=launch
        ):
            with self.assertRaisesRegex(helper.T3ThreadError, "timed out"):
                helper.run_auth([sys.executable, "-c", "import time; time.sleep(1)"])
        self.assertEqual(1, len(children))
        self.assertIsNotNone(children[0].returncode)
        self.assertNotEqual(0, children[0].returncode)

    def test_revoke_timeout_preserves_success_identity(self) -> None:
        spec = importlib.util.spec_from_file_location("t3_thread", SCRIPT)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        import contextlib
        import io
        stdout = io.StringIO()
        with mock.patch.object(helper, "validate_dispatch_arguments"), mock.patch.object(
            helper, "discover_executable", return_value=Path("fake")
        ), mock.patch.object(helper, "discover_server_entry", return_value=Path("fake")), mock.patch.object(
            helper, "load_json", return_value={"origin": "http://localhost:1"}
        ), mock.patch.object(helper, "issue_session", return_value=("token", "sid")), mock.patch.object(
            helper, "create_thread", return_value={"thread_id": "known-uuid", "turn_state": "start_acknowledged"}
        ), mock.patch.object(helper, "run_auth", side_effect=helper.T3ThreadError("auth timed out")), contextlib.redirect_stdout(
            stdout
        ), contextlib.redirect_stderr(io.StringIO()):
            status = helper.main([
                "--name", "worker", "--prompt", "work", "--project-directory", ".",
                "--directory", ".", "--branch", "branch", "--model", "model",
                "--effort", "high", "--runtime-mode", "approval-required",
            ])
        self.assertEqual(2, status)
        self.assertEqual("known-uuid", json.loads(stdout.getvalue())["thread_id"])


if __name__ == "__main__":
    unittest.main()
