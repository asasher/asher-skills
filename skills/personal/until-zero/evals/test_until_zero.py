#!/usr/bin/env python3
"""Behavior tests for Until Zero's local materialization and deterministic core."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SETUP = SKILL / "scripts" / "setup_instance.py"
CLI = SKILL / "scripts" / "until_zero.py"
MIGRATE = SKILL / "scripts" / "migrate_lakebed.py"
DRAIN = SKILL / "scripts" / "drain_capture_queue.py"
API_APP = SKILL / "assets" / "runway-api" / "src" / "app.js"
sys.path.insert(0, str(SKILL / "scripts"))
import until_zero as until_zero_module  # noqa: E402
import migrate_lakebed as migrate_lakebed_module  # noqa: E402
import drain_capture_queue as drain_capture_queue_module  # noqa: E402


def run_script(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class QueueHandler(BaseHTTPRequestHandler):
    server: "QueueServer"

    def log_message(self, _format: str, *_arguments: object) -> None:
        return

    def send_json(self, status: int, value: dict[str, object]) -> None:
        data = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:  # noqa: N802 - stdlib server interface
        if self.headers.get("Authorization") != "Bearer drain-token":
            self.send_json(401, {"error": "unauthorized"})
            return
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/v1/captures/lease":
            items = [] if self.server.acked else [self.server.item]
            self.send_json(200, {"ok": True, "lease_id": "lease-1", "items": items})
            return
        if self.path.endswith("/ack"):
            if body.get("lease_id") != "lease-1":
                self.send_json(409, {"error": "lease_mismatch"})
                return
            self.server.acked = True
            self.send_json(200, {"ok": True, "acknowledged": True})
            return
        if self.path.endswith("/release"):
            self.send_json(200, {"ok": True, "released": True})
            return
        self.send_json(404, {"error": "not_found"})


class QueueServer(ThreadingHTTPServer):
    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), QueueHandler)
        self.acked = False
        self.item = {
            "id": "queue-1",
            "received_at": "2026-07-14T08:00:00Z",
            "envelope": {
                "version": 1,
                "source": "ios-wallet",
                "captured_at": "2026-07-14T08:00:00Z",
                "transaction": {"amount_minor": "-2500", "currency": "AED", "description": "Coffee", "date_iso": "2026-07-14", "card": {"label": "Unknown"}},
            },
        }


class RedirectHandler(BaseHTTPRequestHandler):
    server: "RedirectServer"

    def log_message(self, _format: str, *_arguments: object) -> None:
        return

    def do_POST(self) -> None:  # noqa: N802
        self.send_response(307)
        self.send_header("location", self.server.destination)
        self.end_headers()


class RedirectServer(ThreadingHTTPServer):
    def __init__(self, destination: str) -> None:
        super().__init__(("127.0.0.1", 0), RedirectHandler)
        self.destination = destination


class SecretSinkHandler(BaseHTTPRequestHandler):
    server: "SecretSinkServer"

    def log_message(self, _format: str, *_arguments: object) -> None:
        return

    def do_POST(self) -> None:  # noqa: N802
        self.server.authorizations.append(str(self.headers.get("Authorization") or ""))
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')


class SecretSinkServer(ThreadingHTTPServer):
    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), SecretSinkHandler)
        self.authorizations: list[str] = []


class UntilZeroTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @property
    def instance(self) -> Path:
        return self.project / "control-plane" / "runway"

    def setup_instance(self) -> None:
        result = run_script(SETUP, "--project", str(self.project))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_setup_is_idempotent_private_and_consumer_owned(self) -> None:
        self.setup_instance()
        env_file = self.project / ".env"
        self.assertEqual(env_file.stat().st_mode & 0o777, 0o600)
        self.assertIn("RUNWAY_PRODUCER_TOKEN=", env_file.read_text(encoding="utf-8"))
        self.assertIn("RUNWAY_DRAIN_TOKEN=", env_file.read_text(encoding="utf-8"))
        self.assertIn("RUNWAY_API_ORIGIN=", env_file.read_text(encoding="utf-8"))
        self.assertTrue((self.instance / "api" / "src" / "app.js").is_file())
        self.assertTrue((self.instance / "state" / "accounts.json").is_file())
        self.assertTrue((self.instance / "state" / "approvals.jsonl").is_file())
        self.assertTrue((self.instance / "reports" / "current.html").is_file())
        self.assertEqual(list((self.instance / "shortcut").iterdir()), [])
        before = tree_bytes(self.project)
        rerun = run_script(SETUP, "--project", str(self.project))
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertEqual(tree_bytes(self.project), before)

    def test_setup_preserves_consumer_api_edits_and_emits_candidate(self) -> None:
        self.setup_instance()
        target = self.instance / "api" / "src" / "app.js"
        target.write_text(target.read_text(encoding="utf-8") + "\n// consumer edit\n", encoding="utf-8")
        edited = target.read_bytes()
        rerun = run_script(SETUP, "--project", str(self.project))
        self.assertEqual(rerun.returncode, 3)
        self.assertEqual(target.read_bytes(), edited)
        self.assertEqual(target.with_name("app.js.setup-candidate").read_bytes(), API_APP.read_bytes())

    def test_custom_instance_ignores_its_own_signed_shortcuts(self) -> None:
        result = run_script(SETUP, "--project", str(self.project), "--instance", "private/runway")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("private/runway/shortcut/*.shortcut", (self.project / ".gitignore").read_text(encoding="utf-8"))

    def test_projection_preserves_zero_bands_and_card_timing(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {
            "schema_version": 1,
            "items": [
                {"id": "cash", "name": "Cash", "kind": "cash", "currency": "AED", "balance_minor": "100000", "balance_as_of": "2026-06-01", "archived": False},
                {"id": "card", "name": "Card", "kind": "credit_card", "currency": "AED", "funding_account_id": "cash", "statement_day": "24", "due_day_offset": "9", "balance_minor": "0", "archived": False},
            ],
        })
        write_json(self.instance / "state" / "events.json", {
            "schema_version": 1,
            "items": [
                {"id": "rent", "account_id": "cash", "date_iso": "2026-06-11", "amount_minor": "-200000", "currency": "AED", "label": "Rent", "certainty": "committed", "active": True},
                {"id": "maybe", "account_id": "cash", "date_iso": "2026-06-10", "amount_minor": "500000", "currency": "AED", "label": "Maybe", "certainty": "speculative", "active": True},
            ],
        })
        write_json(self.instance / "state" / "transactions.json", {
            "schema_version": 1,
            "items": [{"id": "charge", "account_id": "card", "date_iso": "2026-06-20", "amount_minor": "-73500", "currency": "AED", "description": "Tools", "status": "uncleared", "source": "wallet"}],
        })
        result = run_script(CLI, "project", "--project", str(self.project), "--today", "2026-06-01", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        projection = json.loads(result.stdout)
        self.assertEqual(projection["zero_dates"]["expected"], "2026-06-11")
        self.assertIsNone(projection["zero_dates"]["optimistic"])
        self.assertEqual(projection["card_statements"][0]["due_date_iso"], "2026-07-03")
        self.assertEqual(projection["card_statements"][0]["total_base"], -73500)

    def test_unmapped_capture_is_excluded_until_assigned(self) -> None:
        self.setup_instance()
        capture = {"queue_id": "q-1", "amount_minor": "-5000", "currency": "AED", "description": "Unknown", "date_iso": "2026-06-02", "card_label": "Mystery"}
        capture_path = self.project / "capture.json"
        write_json(capture_path, capture)
        ingest = run_script(CLI, "ingest", "--project", str(self.project), "--capture", str(capture_path))
        self.assertEqual(ingest.returncode, 0, ingest.stderr)
        pending = json.loads((self.instance / "state" / "pending_captures.json").read_text(encoding="utf-8"))
        transactions = json.loads((self.instance / "state" / "transactions.json").read_text(encoding="utf-8"))
        self.assertEqual(len(pending["items"]), 1)
        self.assertEqual(transactions["items"], [])

    def test_ambiguous_account_match_stays_pending(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {"schema_version": 1, "items": [
            {"id": "one", "name": "One", "kind": "credit_card", "currency": "AED", "balance_minor": "0", "last4": "1234", "archived": False},
            {"id": "two", "name": "Two", "kind": "credit_card", "currency": "AED", "balance_minor": "0", "last4": "1234", "archived": False},
        ]})
        capture = self.project / "ambiguous.json"
        write_json(capture, {"queue_id": "q-ambiguous", "amount_minor": "-5000", "currency": "AED", "description": "Unknown", "date_iso": "2026-06-02", "last4": "1234"})
        result = run_script(CLI, "ingest", "--project", str(self.project), "--capture", str(capture))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["mapped"])

    def test_ingest_rejects_non_currency_codes_before_canonical_write(self) -> None:
        self.setup_instance()
        capture = self.project / "bad-currency.json"
        write_json(capture, {"queue_id": "q-bad", "amount_minor": "-5000", "currency": "123", "description": "Invalid", "date_iso": "2026-06-02"})
        result = run_script(CLI, "ingest", "--project", str(self.project), "--capture", str(capture))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads((self.instance / "state" / "pending_captures.json").read_text(encoding="utf-8"))["items"], [])

    def test_proposal_requires_matching_approval_before_atomic_apply(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {
            "schema_version": 1,
            "items": [{"id": "cash", "name": "Cash", "kind": "cash", "currency": "AED", "balance_minor": "1000", "balance_as_of": "2026-06-01", "archived": False}],
        })
        write_json(self.instance / "state" / "events.json", {
            "schema_version": 1,
            "items": [{"id": "rent", "account_id": "cash", "date_iso": "2026-06-02", "amount_minor": "-1000", "currency": "AED", "label": "Rent", "certainty": "committed", "active": True}],
        })
        change = self.project / "change.json"
        write_json(change, {"operations": [{"collection": "events", "id": "rent", "set": {"amount_minor": "-1400000"}}]})
        proposed = run_script(CLI, "propose", "--project", str(self.project), "--changes", str(change), "--actor", "test")
        self.assertEqual(proposed.returncode, 0, proposed.stderr)
        proposal = json.loads(proposed.stdout)
        denied = run_script(CLI, "apply", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "test")
        self.assertEqual(denied.returncode, 4)
        approved = run_script(CLI, "approve", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "asher")
        self.assertEqual(approved.returncode, 0, approved.stderr)
        applied = run_script(CLI, "apply", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "test")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        events = json.loads((self.instance / "state" / "events.json").read_text(encoding="utf-8"))
        self.assertEqual(events["items"][0]["amount_minor"], "-1400000")
        self.assertTrue((self.instance / "state" / "audit.jsonl").read_text(encoding="utf-8").strip())

    def test_tampered_proposal_is_rejected_after_approval(self) -> None:
        self.setup_instance()
        change = self.project / "change.json"
        write_json(change, {"operations": [{"collection": "config", "id": "settings", "set": {"horizon_days": 180}}]})
        proposal = json.loads(run_script(CLI, "propose", "--project", str(self.project), "--changes", str(change), "--actor", "test").stdout)
        self.assertEqual(run_script(CLI, "approve", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "asher").returncode, 0)
        proposal_path = self.instance / "proposals" / f"{proposal['id']}.json"
        proposal_path.write_text(proposal_path.read_text(encoding="utf-8") + " ", encoding="utf-8")
        result = run_script(CLI, "apply", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "test")
        self.assertEqual(result.returncode, 4)
        self.assertIn("hash", result.stderr.lower())

    def test_config_drift_invalidates_an_approved_proposal(self) -> None:
        self.setup_instance()
        change = self.project / "change.json"
        write_json(change, {"operations": [{"collection": "config", "id": "settings", "set": {"horizon_days": 180}}]})
        proposal = json.loads(run_script(CLI, "propose", "--project", str(self.project), "--changes", str(change), "--actor", "test").stdout)
        self.assertEqual(run_script(CLI, "approve", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "asher").returncode, 0)
        config = json.loads((self.instance / "config.json").read_text(encoding="utf-8"))
        config["buffer_minor"] = "100"
        write_json(self.instance / "config.json", config)
        result = run_script(CLI, "apply", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "test")
        self.assertEqual(result.returncode, 4)
        self.assertIn("changed", result.stderr)

    def test_interrupted_apply_recovery_is_bound_to_approved_targets(self) -> None:
        self.setup_instance()
        change = self.project / "change.json"
        write_json(change, {"operations": [{"collection": "config", "id": "settings", "set": {"horizon_days": 180}}]})
        proposal = json.loads(run_script(CLI, "propose", "--project", str(self.project), "--changes", str(change), "--actor", "test").stdout)
        self.assertEqual(run_script(CLI, "approve", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "asher").returncode, 0)
        original = until_zero_module.atomic_write_json
        failed = False

        def interrupt_config(path: Path, value: object, mode: int = 0o644) -> None:
            nonlocal failed
            if path == self.instance / "config.json" and not failed:
                failed = True
                raise OSError("injected failure")
            original(path, value, mode)

        with mock.patch.object(until_zero_module, "atomic_write_json", side_effect=interrupt_config):
            with self.assertRaises(OSError):
                until_zero_module.apply_proposal(self.instance, self.instance / "state", proposal["id"], "test")
        recovered = run_script(CLI, "recover", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "test")
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertFalse((self.instance / "state" / "apply-journal.json").exists())
        self.assertEqual(json.loads((self.instance / "config.json").read_text(encoding="utf-8"))["horizon_days"], 180)
        self.assertIn("recover_proposal", (self.instance / "state" / "audit.jsonl").read_text(encoding="utf-8"))

    def test_recovery_rejects_forged_approved_proposal_targets(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {"schema_version": 1, "items": [{"id": "cash", "name": "Cash", "kind": "cash", "currency": "AED", "balance_minor": "1000", "balance_as_of": "2026-07-14", "archived": False}]})
        change = self.project / "change.json"
        write_json(change, {"operations": [{"collection": "config", "id": "settings", "set": {"horizon_days": 180}}]})
        proposal = json.loads(run_script(CLI, "propose", "--project", str(self.project), "--changes", str(change), "--actor", "test").stdout)
        self.assertEqual(run_script(CLI, "approve", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "asher").returncode, 0)
        original = until_zero_module.atomic_write_json
        with mock.patch.object(until_zero_module, "atomic_write_json", side_effect=lambda path, value, mode=0o644: (_ for _ in ()).throw(OSError("injected failure")) if path == self.instance / "config.json" else original(path, value, mode)):
            with self.assertRaises(OSError):
                until_zero_module.apply_proposal(self.instance, self.instance / "state", proposal["id"], "test")
        journal_path = self.instance / "state" / "apply-journal.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        journal["targets"]["config"]["buffer_minor"] = "999999999"
        write_json(journal_path, journal)
        result = run_script(CLI, "recover", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "test")
        self.assertEqual(result.returncode, 4)
        self.assertEqual(json.loads((self.instance / "config.json").read_text(encoding="utf-8"))["buffer_minor"], "0")

    def test_incompatible_apply_cannot_overwrite_an_outstanding_journal(self) -> None:
        self.setup_instance()
        proposals = []
        for value in (180, 90):
            change = self.project / f"change-{value}.json"
            write_json(change, {"operations": [{"collection": "config", "id": "settings", "set": {"horizon_days": value}}]})
            proposal = json.loads(run_script(CLI, "propose", "--project", str(self.project), "--changes", str(change), "--actor", "test").stdout)
            self.assertEqual(run_script(CLI, "approve", "--project", str(self.project), "--proposal", proposal["id"], "--actor", "asher").returncode, 0)
            proposals.append(proposal)
        original = until_zero_module.atomic_write_json
        with mock.patch.object(until_zero_module, "atomic_write_json", side_effect=lambda path, value, mode=0o644: (_ for _ in ()).throw(OSError("injected failure")) if path == self.instance / "config.json" else original(path, value, mode)):
            with self.assertRaises(OSError):
                until_zero_module.apply_proposal(self.instance, self.instance / "state", proposals[0]["id"], "test")
        journal_path = self.instance / "state" / "apply-journal.json"
        journal_before = journal_path.read_bytes()
        blocked = run_script(CLI, "apply", "--project", str(self.project), "--proposal", proposals[1]["id"], "--actor", "test")
        self.assertEqual(blocked.returncode, 4)
        self.assertEqual(journal_path.read_bytes(), journal_before)
        self.assertIn("outstanding", blocked.stderr)

    def test_assignment_recovers_mid_commit_without_duplicate_or_missing_audit(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {"schema_version": 1, "items": [{"id": "cash", "name": "Cash", "kind": "cash", "currency": "AED", "balance_minor": "1000", "balance_as_of": "2026-07-14", "archived": False}]})
        write_json(self.instance / "state" / "pending_captures.json", {"schema_version": 1, "items": [{"queue_id": "q", "date_iso": "2026-07-14", "amount_minor": "-100", "currency": "AED", "description": "Coffee"}]})
        original = until_zero_module.atomic_write_json
        failed = False

        def flaky(path: Path, value: object, mode: int = 0o644) -> None:
            nonlocal failed
            if path.name == "pending_captures.json" and not failed:
                failed = True
                raise OSError("injected failure")
            original(path, value, mode)

        with mock.patch.object(until_zero_module, "atomic_write_json", side_effect=flaky):
            with self.assertRaises(OSError):
                until_zero_module.assign_capture(self.instance, self.instance / "state", "q", "cash", "test")
        recovered = until_zero_module.assign_capture(self.instance, self.instance / "state", "q", "cash", "test")
        self.assertEqual(recovered["id"], "wallet:q")
        transactions = json.loads((self.instance / "state" / "transactions.json").read_text(encoding="utf-8"))["items"]
        self.assertEqual([item["id"] for item in transactions], ["wallet:q"])
        self.assertEqual(json.loads((self.instance / "state" / "pending_captures.json").read_text(encoding="utf-8"))["items"], [])
        audits = [json.loads(line) for line in (self.instance / "state" / "audit.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([item["action"] for item in audits], ["assign_capture"])

    def test_report_is_self_contained_and_records_provenance(self) -> None:
        self.setup_instance()
        report = run_script(CLI, "report", "--project", str(self.project), "--today", "2026-06-01")
        self.assertEqual(report.returncode, 0, report.stderr)
        html = (self.instance / "reports" / "current.html").read_text(encoding="utf-8")
        self.assertIn("<!doctype html>", html.lower())
        self.assertIn("Until Zero", html)
        self.assertIn("2026-06-01", html)
        self.assertNotIn("<script src=", html)
        self.assertNotIn("<link rel=", html)
        self.assertIn(hashlib.sha256((self.instance / "state" / "accounts.json").read_bytes()).hexdigest(), html)

    def test_lakebed_inspection_and_import_never_copy_secrets(self) -> None:
        self.setup_instance()
        dump = self.project / "lakebed.json"
        secret = "do-not-copy-this-token"
        write_json(dump, {"tables": {
            "accounts": [{"id": "cash", "ownerId": "owner-a", "name": "Cash", "kind": "cash", "currency": "AED", "balanceMinor": "10000", "balanceAsOf": "2026-07-14", "archived": False, "apiToken": "SHOULD_NOT_COPY"}],
            "rules": [], "events": [], "fxRates": [], "transactions": [], "ingestLog": [],
            "settings": [{"id": "settings", "ownerId": "owner-a", "baseCurrency": "AED", "bufferMinor": "0", "horizonDays": "365", "ingestToken": secret, "agentToken": secret}],
        }})
        inspected = run_script(MIGRATE, "inspect", "--input", str(dump))
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        self.assertNotIn(secret, inspected.stdout)
        imported = run_script(MIGRATE, "import", "--input", str(dump), "--owner", "owner-a", "--project", str(self.project))
        self.assertEqual(imported.returncode, 0, imported.stderr)
        for path in self.instance.rglob("*"):
            if path.is_file():
                self.assertNotIn(secret.encode(), path.read_bytes(), str(path))
        manifest = json.loads((self.instance / "migration" / "lakebed-import.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["secrets"], "excluded")
        self.assertIn("apiToken", manifest["secret_fields_excluded"])
        self.assertNotIn(b"SHOULD_NOT_COPY", (self.instance / "state" / "accounts.json").read_bytes())

    def test_semantic_validation_rejects_fractional_minor_units_and_broken_dates(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {"schema_version": 1, "items": [{"id": "cash", "name": "Cash", "kind": "cash", "currency": "AED", "balance_minor": "1.9", "balance_as_of": "2026-99-99"}]})
        result = run_script(SKILL / "scripts" / "validate_instance.py", "--project", str(self.project))
        self.assertEqual(result.returncode, 1)
        self.assertIn("minor-unit", result.stdout)

    def test_semantic_validation_rejects_rule_configs_that_projection_cannot_execute(self) -> None:
        self.setup_instance()
        write_json(self.instance / "state" / "accounts.json", {"schema_version": 1, "items": [{"id": "cash", "name": "Cash", "kind": "cash", "currency": "AED", "balance_minor": "1000", "balance_as_of": "2026-07-14", "archived": False}]})
        write_json(self.instance / "state" / "rules.json", {"schema_version": 1, "items": [{"id": "rent", "account_id": "cash", "label": "Rent", "amount_minor": "-100", "currency": "AED", "cadence": "monthly", "anchor_date_iso": "2026-07-01", "certainty": "committed", "active": True, "config": {"day_of_month": "abc"}}]})
        result = run_script(SKILL / "scripts" / "validate_instance.py", "--project", str(self.project))
        self.assertEqual(result.returncode, 1)
        self.assertIn("day_of_month", result.stdout)

    def test_invalid_lakebed_owner_is_rejected_before_any_state_write(self) -> None:
        self.setup_instance()
        dump = self.project / "lakebed-invalid.json"
        write_json(dump, {"tables": {
            "accounts": [{"id": "cash", "ownerId": "owner-a", "name": "Cash"}],
            "settings": [],
        }})
        before = tree_bytes(self.instance / "state")
        result = run_script(MIGRATE, "import", "--input", str(dump), "--owner", "owner-a", "--project", str(self.project))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(tree_bytes(self.instance / "state"), before)

    def test_lakebed_import_recovers_after_a_mid_write_failure(self) -> None:
        self.setup_instance()
        dump = self.project / "lakebed-recovery.json"
        value = {"tables": {
            "accounts": [{"id": "cash", "ownerId": "owner-a", "name": "Cash", "kind": "cash", "currency": "AED", "balanceMinor": "10000", "balanceAsOf": "2026-07-14", "archived": False}],
            "rules": [], "events": [], "fxRates": [], "transactions": [],
            "settings": [{"ownerId": "owner-a", "baseCurrency": "AED", "bufferMinor": "0", "horizonDays": 365}],
        }}
        write_json(dump, value)
        tables = migrate_lakebed_module.tables_from_dump(value)
        original = migrate_lakebed_module.atomic_write_json
        failed = False

        def interrupt_rules(path: Path, content: object, mode: int = 0o644) -> None:
            nonlocal failed
            if path.name == "rules.json" and not failed:
                failed = True
                raise OSError("injected failure")
            original(path, content, mode)

        with mock.patch.object(migrate_lakebed_module, "atomic_write_json", side_effect=interrupt_rules):
            with self.assertRaises(OSError):
                migrate_lakebed_module.import_owner(self.project, "control-plane/runway", dump, tables, "owner-a")
        self.assertTrue((self.instance / "state" / "migration-journal.json").exists())
        manifest = migrate_lakebed_module.import_owner(self.project, "control-plane/runway", dump, tables, "owner-a")
        self.assertEqual(manifest["counts"]["accounts"], 1)
        self.assertFalse((self.instance / "state" / "migration-journal.json").exists())

    def test_refresh_rejects_project_selected_secret_names_before_network_access(self) -> None:
        self.setup_instance()
        config = json.loads((self.instance / "config.json").read_text(encoding="utf-8"))
        config["capture"]["drain_token_env"] = "AWS_SECRET_ACCESS_KEY"
        write_json(self.instance / "config.json", config)
        deployment = json.loads((self.instance / "deployment.json").read_text(encoding="utf-8"))
        deployment["api_url"] = "https://attacker.invalid"
        write_json(self.instance / "deployment.json", deployment)
        result = run_script(DRAIN, "--project", str(self.project))
        self.assertEqual(result.returncode, 2)
        self.assertIn("token binding", result.stderr)

    def test_http_redirect_never_forwards_the_drain_bearer_token(self) -> None:
        sink = SecretSinkServer()
        sink_thread = threading.Thread(target=sink.serve_forever, daemon=True)
        sink_thread.start()
        redirect = RedirectServer(f"http://127.0.0.1:{sink.server_address[1]}/steal")
        redirect_thread = threading.Thread(target=redirect.serve_forever, daemon=True)
        redirect_thread.start()
        try:
            with self.assertRaises(until_zero_module.StateError):
                drain_capture_queue_module.request_json(f"http://127.0.0.1:{redirect.server_address[1]}/start", "TOPSECRET", {"ok": True})
            self.assertEqual(sink.authorizations, [])
        finally:
            redirect.shutdown()
            redirect.server_close()
            sink.shutdown()
            sink.server_close()
            redirect_thread.join(timeout=2)
            sink_thread.join(timeout=2)

    def test_refresh_acknowledges_only_after_valid_local_commit(self) -> None:
        self.setup_instance()
        server = QueueServer()
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            deployment = json.loads((self.instance / "deployment.json").read_text(encoding="utf-8"))
            deployment["api_url"] = f"http://127.0.0.1:{server.server_address[1]}"
            write_json(self.instance / "deployment.json", deployment)
            origin = f"http://127.0.0.1:{server.server_address[1]}"
            (self.project / ".env").write_text(f"RUNWAY_PRODUCER_TOKEN=\nRUNWAY_DRAIN_TOKEN=drain-token\nRUNWAY_API_ORIGIN={origin}\n", encoding="utf-8")
            (self.project / ".env").chmod(0o600)
            transactions = self.instance / "state" / "transactions.json"
            transactions.write_text("{broken", encoding="utf-8")
            failed = run_script(DRAIN, "--project", str(self.project))
            self.assertEqual(failed.returncode, 1)
            self.assertFalse(server.acked)
            write_json(transactions, {"schema_version": 1, "items": []})
            completed = run_script(DRAIN, "--project", str(self.project))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(server.acked)
            pending = json.loads((self.instance / "state" / "pending_captures.json").read_text(encoding="utf-8"))
            self.assertEqual(pending["items"][0]["queue_id"], "queue-1")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
