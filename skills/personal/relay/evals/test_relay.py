#!/usr/bin/env python3
"""Deterministic Relay protocol tests; no network or live provider resources."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
SETUP = SCRIPTS / "setup_instance.py"
VALIDATE = SCRIPTS / "validate_instance.py"
SELECT = SCRIPTS / "select_bags.py"
VALIDATE_BAG = SCRIPTS / "validate_relay_bag.py"
BUILD_REVIEW = SCRIPTS / "build_review_sheet.py"
DELIVER = SCRIPTS / "agentmail_delivery.py"
INGEST = SCRIPTS / "ingest_agentmail_events.py"
STATUS = SCRIPTS / "relay_status.py"
PROVISION = SCRIPTS / "provision_agentmail_key.py"
FIXTURE = SKILL / "templates" / "instance" / "templates" / "fixtures" / "project-update.json"


def run(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python3", *args], capture_output=True, text=True, env=env, check=False)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class RelayTests(unittest.TestCase):
    maxDiff = None

    def binding(self, layout: str = "node") -> dict[str, Any]:
        location = "package.json" if layout == "node" else "src/project.py"
        return {
            "schema_version": 2,
            "projects": [{"id": "project-a", "root": "."}, {"id": "project-b", "root": "services/b"}],
            "evidence_providers": [
                {"id": "repo", "type": "path", "location": location, "classes": ["shipped", "pending"]},
                {"id": "commercial", "type": "path", "location": "records/commercial.json", "classes": ["cash", "growth"]},
            ],
            "section_recipes": {"project_update": ["Shipped", "Next"], "internal_digest": ["Delivery", "Pending", "Cash", "Growth"]},
            "audiences": ["external-a", "external-b", "internal"],
            "editorial": {"playbook": "docs/agents/relay.md"},
            "template": {"id": "relay-compact-default", "version": "2.0.0", "root": "relay/templates"},
            "reconciliation_mode": "manual",
        }

    def audience(self, audience_id: str, *, kind: str, project: str, address: str, feature: str, section: str) -> tuple[dict[str, Any], dict[str, Any]]:
        message_kind = "internal_digest" if kind == "internal" else "project_update"
        audience = {
            "schema_version": 2, "id": audience_id, "kind": kind, "message_kind": message_kind,
            "project_ids": [project], "interest_file": f"interests/{audience_id}.json",
            "allowed_disclosure": ["internal"] if kind == "internal" else ["external"],
            "recipients": [{"address": address, "header": "to"}], "operator_cc": "default",
            "sender": "relay@fixture.invalid", "subject": f"{audience_id} update", "preheader": "Verified update",
            "summary": f"Summary for {audience_id}.",
        }
        interest = {"schema_version": 2, "audience_id": audience_id, "features": [feature], "sections": [section]}
        return audience, interest

    def make_repo(self, root: Path, layout: str = "node", *, token: str = "fixture-secret") -> None:
        (root / ".git").mkdir()
        if layout == "node":
            write_json(root / "package.json", {"name": "fixture"})
        else:
            (root / "src").mkdir()
            (root / "src" / "project.py").write_text("VALUE = 1\n", encoding="utf-8")
        (root / "services" / "b").mkdir(parents=True)
        (root / "records").mkdir()
        write_json(root / "records" / "commercial.json", {})
        binding_file = root / "binding.json"
        write_json(binding_file, self.binding(layout))
        result = run(str(SETUP), str(root), "--binding", str(binding_file))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        env_path = root / ".env"
        env_path.write_text(f"UNRELATED=preserve\nAGENTMAIL_API_KEY={token}\n", encoding="utf-8")
        env_path.chmod(0o600)
        instance = root / "relay"
        for args in (
            ("external-a", "external", "project-a", "client-a@fixture.invalid", "feature-a", "Shipped"),
            ("external-b", "external", "project-b", "client-b@fixture.invalid", "feature-b", "Next"),
            ("internal", "internal", "project-a", "team@fixture.invalid", "feature-internal", "Delivery"),
        ):
            audience, interest = self.audience(args[0], kind=args[1], project=args[2], address=args[3], feature=args[4], section=args[5])
            write_json(instance / "audiences" / f"{args[0]}.json", audience)
            write_json(instance / "interests" / f"{args[0]}.json", interest)
        capabilities = json.loads((instance / "capabilities.json").read_text())
        capabilities["agentmail"].update({
            "credential_scope": "inbox", "permissions": ["draft_read", "draft_create", "draft_send"],
            "inbox_id": "inbox_fixture", "sender": "relay@fixture.invalid", "sender_verified": True,
            "domain": "fixture.invalid", "domain_verified": True, "event_mode": "manual", "status": "verified",
        })
        write_json(instance / "capabilities.json", capabilities)

    def make_run(self, root: Path, run_name: str = "run-001") -> Path:
        run_dir = root / "relay" / "runs" / run_name
        run_dir.mkdir(parents=True)
        shutil.copy2(FIXTURE, run_dir / "bag.json")
        bag = json.loads((run_dir / "bag.json").read_text())
        bag["id"] = run_name
        bag["audience_id"] = "external-a"
        bag["project_ids"] = ["project-a"]
        bag["recipients"] = {"to": ["client-a@fixture.invalid"], "cc": ["operator@fixture.invalid"]}
        write_json(run_dir / "bag.json", bag)
        html = "<!doctype html><html><body><h1>Project — delivery update</h1><p>A concise summary of verified client-relevant progress.</p><h2>Shipped</h2><p>Example capability</p><p>The capability is available and verified.</p><h2>Next</h2><p>Next verification</p><p>The team is validating the next workflow.</p><footer>Prepared with AI and reviewed before sending.</footer></body></html>"
        text = "Project — delivery update\n\nA concise summary of verified client-relevant progress.\n\nShipped\nExample capability\nThe capability is available and verified.\n\nNext\nNext verification\nThe team is validating the next workflow.\n\nPrepared with AI and reviewed before sending.\n"
        (run_dir / "rendered-email.html").write_text(html, encoding="utf-8")
        (run_dir / "rendered-email.txt").write_text(text, encoding="utf-8")
        (run_dir / "rendered-email-light.html").write_text(html.replace("<html>", '<html class="light-preview">'), encoding="utf-8")
        (run_dir / "rendered-email-dark.html").write_text(html.replace("<html>", '<html class="dark-preview">'), encoding="utf-8")
        result = run(str(BUILD_REVIEW), str(root), "--run", str(run_dir), env={**os.environ, "RELAY_NOW": "2026-07-16T09:00:00Z"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        review = run_dir / "review.html"
        event = {"type": "feedback_submitted", "verdict": "approve", "doc_hash": hashlib.sha256(review.read_bytes()).hexdigest()[:16], "annotations": [], "timestamp": "2026-07-16T09:10:00Z"}
        (run_dir / "review-state").mkdir()
        (run_dir / "review-state" / "events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
        return run_dir

    def fake_agentmail(self, root: Path, run_dir: Path) -> tuple[dict[str, str], Path]:
        bin_dir = root / "bin"
        bin_dir.mkdir(exist_ok=True)
        log = root / "agentmail-argv.jsonl"
        fake = bin_dir / "agentmail"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import hashlib,json,os,sys\n"
            "args=sys.argv[1:]\n"
            "with open(os.environ['FAKE_AGENTMAIL_LOG'],'a',encoding='utf-8') as h:h.write(json.dumps(args)+'\\n')\n"
            "run=os.environ['FAKE_RUN']; bag=json.load(open(run+'/bag.json'))\n"
            "if 'create' in args: print(json.dumps({'draft_id':'draft_fixture'}))\n"
            "elif 'get' in args:\n"
            " html=open(run+'/rendered-email.html','rb').read(); text=open(run+'/rendered-email.txt','rb').read()\n"
            " print(json.dumps({'draft':{'id':'draft_fixture','subject':bag['subject'],'from':bag['sender'],'to':bag['recipients']['to'],'cc':bag['recipients']['cc'],'html_sha256':hashlib.sha256(html).hexdigest(),'text_sha256':hashlib.sha256(text).hexdigest()}}))\n"
            "elif 'send' in args:\n"
            " marker=os.environ['FAKE_SENT_MARKER']\n"
            " if os.path.exists(marker): print(json.dumps({'error':'draft already consumed'})); sys.exit(9)\n"
            " open(marker,'w').write('sent')\n"
            " print(json.dumps({'message_id':'message_fixture','thread_id':'thread_fixture'}))\n"
            "else: print('agentmail 0.7.12')\n",
            encoding="utf-8",
        )
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        env = dict(os.environ)
        env.update({"PATH": f"{bin_dir}{os.pathsep}{env.get('PATH','')}", "FAKE_AGENTMAIL_LOG": str(log), "FAKE_RUN": str(run_dir), "FAKE_SENT_MARKER": str(root / "sent.marker"), "RELAY_NOW": "2026-07-16T09:20:00Z"})
        env.pop("AGENTMAIL_API_KEY", None)
        return env, log

    def test_published_surface_is_relay_and_agentmail_only(self) -> None:
        product_roots = [SKILL / "SKILL.md", SKILL / "README.md", SKILL / "agents", SKILL / "reference", SKILL / "scripts", SKILL / "templates"]
        paths = [root for root in product_roots if root.is_file()]
        paths.extend(path for root in product_roots if root.is_dir() for path in root.rglob("*") if path.is_file() and path.suffix != ".pyc")
        text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in paths)
        self.assertIn("name: relay", (SKILL / "SKILL.md").read_text())
        self.assertIn("requires: [review-loop]", (SKILL / "SKILL.md").read_text())
        self.assertNotIn("control-plane/communications", text)
        self.assertNotIn("control-plane/relay", text)
        self.assertNotIn("docs/agents/communications", text)
        self.assertNotIn("outlook-email", text.lower())
        self.assertNotIn("create_forward_draft", text)
        executable_and_templates = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for root in (SKILL / "scripts", SKILL / "templates" / "instance") for path in root.rglob("*") if path.is_file())
        self.assertNotIn("Dunn Harland", executable_and_templates)

    def test_setup_discovers_two_layouts_protects_env_and_reconciles(self) -> None:
        for layout in ("node", "python"):
            with self.subTest(layout=layout), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.make_repo(root, layout, token="$(touch never)-secret")
                (root / "CHANGELOG.md").write_text("# Releases\n", encoding="utf-8")
                (root / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
                (root / "docs" / "editorial.md").parent.mkdir(parents=True, exist_ok=True)
                (root / "docs" / "editorial.md").write_text("# Editorial\n", encoding="utf-8")
                (root / "records" / "inbox-export.json").write_text("{}\n", encoding="utf-8")
                discovered = run(str(SETUP), str(root), "--discover")
                self.assertEqual(discovered.returncode, 0)
                value = json.loads(discovered.stdout)["discovery"]
                self.assertIn("package.json" if layout == "node" else "", value["runtime_manifests"] if layout == "node" else [""])
                self.assertIn("CHANGELOG.md", value["release_evidence_candidates"])
                self.assertIn("tasks.md", value["tracker_candidates"])
                self.assertIn("docs/editorial.md", value["editorial_candidates"])
                self.assertIn("records/inbox-export.json", value["mailbox_candidates"])
                self.assertTrue(value["node"]["available"])
                self.assertTrue(value["npm"]["available"])
                self.assertNotIn("$(touch never)-secret", discovered.stdout + discovered.stderr)
                self.assertEqual((root / ".env").stat().st_mode & 0o777, 0o600)
                self.assertIn(".env", (root / ".gitignore").read_text().splitlines())
                self.assertIn("UNRELATED=preserve", (root / ".env").read_text())
                instance = root / "relay"
                local = instance / "template-config.json"
                changed = json.loads(local.read_text()); changed["accent"] = "#123456"; write_json(local, changed)
                binding = root / "binding.json"
                rerun = run(str(SETUP), str(root), "--binding", str(binding))
                self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
                self.assertEqual(json.loads(local.read_text())["accent"], "#123456")
                self.assertTrue((instance / "template-config.json.setup-candidate").exists())
                self.assertEqual((root / ".env").read_text().count("AGENTMAIL_API_KEY="), 1)

    def test_binding_applies_over_default_scaffold_and_rerun_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            write_json(root / "package.json", {"name": "fixture"})
            scaffold = run(str(SETUP), str(root))
            self.assertEqual(scaffold.returncode, 0, scaffold.stdout + scaffold.stderr)
            binding_file = root / "binding.json"
            write_json(binding_file, self.binding())
            bound = run(str(SETUP), str(root), "--binding", str(binding_file))
            self.assertEqual(bound.returncode, 0, bound.stdout + bound.stderr)
            bindings = json.loads((root / "relay" / "bindings.json").read_text())
            self.assertEqual(bindings["audiences"], ["external-a", "external-b", "internal"])
            self.assertFalse((root / "relay" / "bindings.json.setup-candidate").exists())
            before = (root / "relay" / "bindings.json").read_bytes()
            rerun = run(str(SETUP), str(root), "--binding", str(binding_file))
            self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
            self.assertEqual((root / "relay" / "bindings.json").read_bytes(), before)
            self.assertFalse((root / "relay" / "bindings.json.setup-candidate").exists())

    def test_complete_instance_validates_and_unverified_sender_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root)
            valid = run(str(VALIDATE), str(root), "--require-token", "--require-ready")
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
            path = root / "relay" / "capabilities.json"
            value = json.loads(path.read_text()); value["agentmail"]["sender_verified"] = False; write_json(path, value)
            invalid = run(str(VALIDATE), str(root), "--require-token", "--require-ready")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("sender is not verified", invalid.stdout)

    def test_selection_isolates_three_audiences_and_appends_operator_cc(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root)
            evidence = [
                {"id": "a", "source": "repo-a", "observed_at": "2026-07-16T08:00:00Z", "project_id": "project-a", "feature": "feature-a", "status": "production_verified", "disclosure": "external", "section": "Shipped", "title": "A only", "detail": "Visible only to A."},
                {"id": "b", "source": "repo-b", "observed_at": "2026-07-16T08:01:00Z", "project_id": "project-b", "feature": "feature-b", "status": "in_progress", "disclosure": "external", "section": "Next", "title": "B only", "detail": "Visible only to B."},
                {"id": "i", "source": "internal", "observed_at": "2026-07-16T08:02:00Z", "project_id": "project-a", "feature": "feature-internal", "status": "pending", "disclosure": "internal", "section": "Delivery", "title": "Internal only", "detail": "Private detail.", "visibility": "internal"},
            ]
            source = root / "evidence.json"; write_json(source, evidence)
            out = root / "selected"
            result = run(str(SELECT), str(root), "--evidence", str(source), "--out", str(out), env={**os.environ, "RELAY_NOW": "2026-07-16T09:00:00Z"})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            bags = {name: json.loads((out / name / "bag.json").read_text()) for name in ("external-a", "external-b", "internal")}
            self.assertEqual({item["id"] for item in bags["external-a"]["evidence"]}, {"a"})
            self.assertEqual({item["id"] for item in bags["external-b"]["evidence"]}, {"b"})
            self.assertEqual({item["id"] for item in bags["internal"]["evidence"]}, {"i"})
            self.assertEqual(bags["external-a"]["recipients"]["cc"], ["operator@fixture.invalid"])
            self.assertEqual(bags["internal"]["recipients"]["cc"], [])
            for bag in bags.values():
                path = root / "check.json"; write_json(path, bag)
                self.assertEqual(run(str(VALIDATE_BAG), str(path)).returncode, 0)

    def test_default_renderer_is_unbranded_compact_and_authors_themes(self) -> None:
        base = (SKILL / "templates" / "instance" / "templates" / "src" / "base.tsx").read_text()
        renderer = (SKILL / "templates" / "instance" / "scripts" / "render-email.tsx").read_text()
        config = json.loads((SKILL / "templates" / "instance" / "template-config.json").read_text())
        self.assertEqual(config["name"], "")
        self.assertIn("dark-preview", base); self.assertIn("light-preview", base)
        self.assertIn("rendered-email-dark.html", renderer); self.assertIn("rendered-email-light.html", renderer)
        self.assertNotIn("Dunn Harland", base + renderer + json.dumps(config))
        self.assertIn('fontSize: "13px"', base)

    def test_review_sheet_is_self_contained_and_hash_binds_every_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root); run_dir = self.make_run(root)
            sheet = (run_dir / "review.html").read_text()
            self.assertNotIn("src=\"rendered-email", sheet)
            for value in ("Actual delivery HTML", "Actual plain text", "Forced light", "Forced dark", "relay@fixture.invalid", "client-a@fixture.invalid", "operator@fixture.invalid", "relay-approval-manifest"):
                self.assertIn(value, sheet)
            authorized = run(str(DELIVER), str(root), "--run", str(run_dir))
            self.assertEqual(authorized.returncode, 0, authorized.stdout + authorized.stderr)
            self.assertTrue(json.loads(authorized.stdout)["authorized"])

    def test_each_approved_input_mutation_causes_zero_provider_calls(self) -> None:
        mutations = {
            "html": lambda run_dir: (run_dir / "rendered-email.html").write_text("changed", encoding="utf-8"),
            "text": lambda run_dir: (run_dir / "rendered-email.txt").write_text("changed", encoding="utf-8"),
            "sender": lambda run_dir: self.mutate_bag(run_dir, "sender", "other@fixture.invalid"),
            "to": lambda run_dir: self.mutate_recipient(run_dir, "to", ["other@fixture.invalid"]),
            "cc": lambda run_dir: self.mutate_recipient(run_dir, "cc", []),
            "manifest": lambda run_dir: (run_dir / "approval-manifest.json").write_text("{}\n", encoding="utf-8"),
            "sheet": lambda run_dir: (run_dir / "review.html").write_text((run_dir / "review.html").read_text() + "<!--changed-->", encoding="utf-8"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); self.make_repo(root); run_dir = self.make_run(root); env, log = self.fake_agentmail(root, run_dir)
                mutate(run_dir)
                result = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", env=env)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(log.exists() and log.read_text().strip())

    def mutate_bag(self, run_dir: Path, key: str, value: Any) -> None:
        bag = json.loads((run_dir / "bag.json").read_text()); bag[key] = value; write_json(run_dir / "bag.json", bag)

    def mutate_recipient(self, run_dir: Path, header: str, value: list[str]) -> None:
        bag = json.loads((run_dir / "bag.json").read_text()); bag["recipients"][header] = value; write_json(run_dir / "bag.json", bag)

    def test_draft_first_delivery_records_before_send_and_hides_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); secret = "$(touch never)-secret"; self.make_repo(root, token=secret); run_dir = self.make_run(root); env, log = self.fake_agentmail(root, run_dir)
            result = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual([next(word for word in ("create", "get", "send") if word in call) for call in calls], ["create", "get", "send"])
            self.assertNotIn(secret, json.dumps(calls) + result.stdout + result.stderr)
            create = calls[0]
            self.assertIn("--client-id", create); self.assertIn("--to", create); self.assertIn("--cc", create)
            workflow = read_jsonl(root / "relay" / "state" / "workflow.jsonl")
            states = [item["state"] for item in workflow]
            self.assertLess(states.index("draft-created"), states.index("send-submitted")); self.assertLess(states.index("send-submitted"), states.index("sent"))
            delivery = read_jsonl(root / "relay" / "state" / "delivery.jsonl")
            self.assertEqual(len(delivery), 2); self.assertTrue(all(item["state"] == "pending" for item in delivery))
            state_text = "".join(path.read_text() for path in (root / "relay" / "state").glob("*.jsonl"))
            self.assertNotIn("client-a@fixture.invalid", state_text); self.assertNotIn(secret, state_text)

    def test_key_provisioning_preserves_env_and_never_prints_or_argv_leaks_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root, token="parent-secret")
            bin_dir = root / "bin"; bin_dir.mkdir(); log = root / "key-argv.json"
            fake = bin_dir / "agentmail"
            fake.write_text("#!/usr/bin/env python3\nimport json,os,sys\nopen(os.environ['KEY_LOG'],'w').write(json.dumps(sys.argv[1:]))\nprint(json.dumps({'api_key_id':'key_fixture','api_key':'runtime-secret','prefix':'am_test'}))\n", encoding="utf-8")
            fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
            env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH','')}", "KEY_LOG": str(log)}
            env.pop("AGENTMAIL_API_KEY", None)
            result = run(str(PROVISION), str(root), "--execute", env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dotenv = (root / ".env").read_text()
            self.assertIn("UNRELATED=preserve", dotenv); self.assertIn("AGENTMAIL_API_KEY=runtime-secret", dotenv)
            self.assertNotIn("runtime-secret", result.stdout + result.stderr + log.read_text())
            self.assertNotIn("parent-secret", result.stdout + result.stderr + log.read_text())
            self.assertEqual((root / ".env").stat().st_mode & 0o777, 0o600)

            (root / ".gitignore").write_text("", encoding="utf-8")
            blocked = run(str(PROVISION), str(root))
            self.assertEqual(blocked.returncode, 2)
            self.assertIn("must be Git-ignored", blocked.stdout)

    def test_retry_seams_reuse_identity_and_ambiguous_send_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root); run_dir = self.make_run(root); env, log = self.fake_agentmail(root, run_dir)
            first = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", "--fail-at", "after-draft", env=env)
            self.assertEqual(first.returncode, 75)
            second = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", env=env)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(sum("create" in call for call in calls), 1); self.assertEqual(sum("send" in call for call in calls), 1)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root); run_dir = self.make_run(root); env, log = self.fake_agentmail(root, run_dir)
            lost = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", "--fail-at", "after-send-call", env=env)
            self.assertEqual(lost.returncode, 75)
            manifest = json.loads((run_dir / "approval-manifest.json").read_text())
            reconciliation = root / "reconcile.json"; write_json(reconciliation, [{"client_id": manifest["client_id"], "message_id": "message_fixture", "thread_id": "thread_fixture"}])
            recovered = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", "--reconcile-file", str(reconciliation), env=env)
            self.assertEqual(recovered.returncode, 0, recovered.stdout + recovered.stderr)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(sum("send" in call for call in calls), 1)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root); run_dir = self.make_run(root); env, log = self.fake_agentmail(root, run_dir)
            uncertain = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", "--fail-at", "after-send-submit-before-call", env=env)
            self.assertEqual(uncertain.returncode, 75)
            blocked = run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", env=env)
            self.assertEqual(blocked.returncode, 4)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(sum("send" in call for call in calls), 0)

    def test_duplicate_out_of_order_mixed_events_reply_and_watermark(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root); run_dir = self.make_run(root); env, _ = self.fake_agentmail(root, run_dir)
            self.assertEqual(run(str(DELIVER), str(root), "--run", str(run_dir), "--execute", env=env).returncode, 0)
            events = [
                {"id": "evt-deliver-a", "type": "message.delivered", "message_id": "message_fixture", "thread_id": "thread_fixture", "recipients": ["client-a@fixture.invalid"], "timestamp": "2026-07-16T10:03:00Z"},
                {"id": "evt-bounce-operator", "type": "message.bounced", "message_id": "message_fixture", "thread_id": "thread_fixture", "recipient": "operator@fixture.invalid", "timestamp": "2026-07-16T10:04:00Z"},
                {"id": "evt-reply", "type": "message.received", "thread_id": "thread_fixture", "message_id": "reply_fixture", "source_message_id": "message_fixture", "timestamp": "2026-07-16T10:05:00Z"},
                {"id": "evt-sent", "type": "message.sent", "message_id": "message_fixture", "thread_id": "thread_fixture", "observed_through": "2026-07-16T09:00:00Z", "timestamp": "2026-07-16T10:01:00Z"},
                {"id": "evt-deliver-a", "type": "message.delivered", "message_id": "message_fixture", "recipients": ["client-a@fixture.invalid"]},
            ]
            source = root / "events.json"; write_json(source, events)
            result = run(str(INGEST), str(root), "--events", str(source), "--mode", "manual")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            state = root / "relay" / "state"
            outcomes = {item["state"] for item in read_jsonl(state / "delivery.jsonl")}
            self.assertIn("receiving-server-delivered", outcomes); self.assertIn("bounced", outcomes)
            self.assertEqual(len(read_jsonl(state / "replies.jsonl")), 1)
            self.assertFalse(read_jsonl(state / "replies.jsonl")[0]["automatic_reply"])
            self.assertEqual(len(read_jsonl(state / "watermarks.jsonl")), 1)
            again = run(str(INGEST), str(root), "--events", str(source), "--mode", "manual")
            self.assertEqual(again.returncode, 0)
            self.assertEqual(len(read_jsonl(state / "watermarks.jsonl")), 1)
            self.assertFalse(json.loads(result.stdout)["real_time"])
            status = run(str(STATUS), str(root))
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            report = json.loads(status.stdout)["communications"][0]
            self.assertFalse(report["all_delivered"]); self.assertEqual(report["reply_count"], 1); self.assertTrue(report["watermark_confirmed"])

    def test_webhook_claim_requires_signature_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); self.make_repo(root); source = root / "events.json"; write_json(source, [])
            blocked = run(str(INGEST), str(root), "--events", str(source), "--mode", "webhook")
            self.assertNotEqual(blocked.returncode, 0)
            allowed = run(str(INGEST), str(root), "--events", str(source), "--mode", "webhook", "--signature-verified")
            self.assertEqual(allowed.returncode, 0)
            self.assertTrue(json.loads(allowed.stdout)["real_time"])


if __name__ == "__main__":
    unittest.main()
