from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SETUP = SKILL / "scripts" / "setup_instance.py"
VALIDATE = SKILL / "scripts" / "validate_instance.py"
VALIDATE_BAG = SKILL / "scripts" / "validate_comms_bag.py"
HANDOFF = SKILL / "scripts" / "agentmail_handoff.py"
PROVISION = SKILL / "scripts" / "provision_agentmail_key.py"


def run(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


class ManageCommunicationsTests(unittest.TestCase):
    def make_workspace(self, root: Path, token: str = "sentinel-secret") -> None:
        (root / ".gitignore").write_text(".env\nnode_modules/\n", encoding="utf-8")
        (root / ".env").write_text(
            f"CAPTURE_TOKEN=preserve-me\nAGENTMAIL_API_KEY={token}\n", encoding="utf-8"
        )
        (root / ".env").chmod(0o600)

    def configure_instance(self, root: Path) -> None:
        instance = root / "control-plane" / "communications"
        capabilities = json.loads((instance / "capabilities.json").read_text(encoding="utf-8"))
        capabilities["rich_email_delivery"].update(
            {
                "status": "verified",
                "inbox_id": "inbox_test",
                "review_recipient": "reviewer@example.com",
                "allowed_recipients": ["reviewer@example.com"],
                "credential_scope": "inbox",
                "permissions": ["draft_read", "draft_create", "draft_send"],
            }
        )
        capabilities["delegated_mailbox_management"]["status"] = "verified"
        (instance / "capabilities.json").write_text(
            json.dumps(capabilities, indent=2) + "\n", encoding="utf-8"
        )

        people = root / "People"
        people.mkdir()
        (people / "Reviewer.md").write_text(
            "---\nperson: Reviewer\nemail: reviewer@example.com\n---\n", encoding="utf-8"
        )
        (people / "Client.md").write_text(
            "---\nperson: Client\nemail: client@example.com\n---\n", encoding="utf-8"
        )
        profiles = instance / "profiles"
        profiles.mkdir(exist_ok=True)
        profile = profiles / "fixture.md"
        profile.write_text(
            "# Fixture communications\n\nCanonical recipient and interest preferences.\n",
            encoding="utf-8",
        )
        profile_digest = hashlib.sha256(profile.read_bytes()).hexdigest()
        (instance / "audiences" / "fixture.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "id": "fixture",
                    "kind": "external",
                    "project_id": "fixture-project",
                    "profile_file": "profiles/fixture.md",
                    "profile_sha256": profile_digest,
                    "recipients": [
                        {"person_note": "People/Client.md", "role": "external"},
                        {"person_note": "People/Reviewer.md", "role": "internal"},
                    ],
                    "interest_file": "interests/fixture.json",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (instance / "interests" / "fixture.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "id": "fixture",
                    "project_id": "fixture-project",
                    "profile_file": "profiles/fixture.md",
                    "profile_sha256": profile_digest,
                    "include": ["rfq-management"],
                    "exclude": ["*"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_setup_is_idempotent_and_preserves_shared_env(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_workspace(root)
            before_env = (root / ".env").read_bytes()

            first = run(str(SETUP), str(root))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((root / "control-plane" / "communications" / "policy.json").is_file())
            self.assertTrue((root / "docs" / "agents" / "communications.md").is_file())
            policy = json.loads(
                (root / "control-plane" / "communications" / "policy.json").read_text(encoding="utf-8")
            )
            self.assertEqual(policy["delivery"]["review_gate"], "browser_explicit_approval")
            self.assertEqual(policy["delivery"]["outlook_sender_recipient"], "exclude")
            states = json.loads(
                (root / "control-plane" / "communications" / "state" / "schema.json").read_text(
                    encoding="utf-8"
                )
            )["ledger_states"]
            self.assertIn("reviewed", states)
            self.assertEqual((root / ".env").read_bytes(), before_env)

            files_before = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            second = run(str(SETUP), str(root))
            self.assertEqual(second.returncode, 0, second.stderr)
            files_after = {
                path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(files_before, files_after)

    def test_validator_reports_structure_without_exposing_token(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_workspace(root)
            self.assertEqual(run(str(SETUP), str(root)).returncode, 0)
            self.configure_instance(root)

            result = run(str(VALIDATE), str(root), "--require-token")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("sentinel-secret", result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "valid")
            self.assertEqual(report["checks"]["profile_count"], 1)

    def test_validator_rejects_a_stale_profile_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_workspace(root)
            self.assertEqual(run(str(SETUP), str(root)).returncode, 0)
            self.configure_instance(root)
            profile = root / "control-plane" / "communications" / "profiles" / "fixture.md"
            profile.write_text(profile.read_text(encoding="utf-8") + "Changed.\n", encoding="utf-8")

            result = run(str(VALIDATE), str(root), "--require-token")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stale profile_sha256", result.stdout)

    def test_comms_bag_accepts_both_internal_digest_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = {
                "id": "user:fixture",
                "source": "user confirmation",
                "observed_at": "2026-07-13T09:00:00+04:00",
                "status": "pending",
                "feature": "fixture",
            }
            item = {
                "status": "pending",
                "title": "Fixture",
                "detail": "Pending review.",
                "evidence_ids": ["user:fixture"],
            }
            base = {
                "schema_version": 1,
                "id": "fixture-digest",
                "kind": "internal_digest",
                "generated_at": "2026-07-13T09:00:00+04:00",
                "subject": "Fixture digest",
                "preheader": "Fixture preheader",
                "audience_id": "internal-digest",
                "project_ids": ["fixture"],
                "summary": "Fixture summary.",
                "evidence": [evidence],
            }
            layouts = [
                [
                    {"title": "Delivery", "items": []},
                    {"title": "Pending", "items": [item]},
                    {"title": "Cash", "items": []},
                    {"title": "Growth", "items": []},
                ],
                [
                    {"title": "Fixture", "subtitle": "Fixture Client", "items": [item]},
                    {"title": "Cash", "items": []},
                    {"title": "Growth", "items": []},
                ],
            ]
            for index, sections in enumerate(layouts):
                bag = root / f"bag-{index}.json"
                bag.write_text(json.dumps({**base, "sections": sections}), encoding="utf-8")
                result = run(str(VALIDATE_BAG), str(bag))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_agentmail_adapter_is_dry_by_default_and_uses_exact_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "must-not-exist"
            token = f"$(touch {marker})-sentinel"
            self.make_workspace(root, token=token)
            self.assertEqual(run(str(SETUP), str(root)).returncode, 0)
            self.configure_instance(root)

            html = root / "message.html"
            text = root / "message.txt"
            html.write_text("<p>Hello</p>", encoding="utf-8")
            text.write_text("Hello", encoding="utf-8")

            dry = run(
                str(HANDOFF),
                str(root),
                "--subject",
                "Fixture update",
                "--html-file",
                str(html),
                "--text-file",
                str(text),
                "--client-id",
                "fixture-001",
            )
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse(marker.exists())
            self.assertNotIn(token, dry.stdout + dry.stderr)

            bin_dir = root / "bin"
            bin_dir.mkdir()
            log = root / "agentmail-argv.jsonl"
            fake = bin_dir / "agentmail"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "with open(os.environ['FAKE_AGENTMAIL_LOG'], 'a', encoding='utf-8') as h:\n"
                "    h.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if 'create' in sys.argv:\n"
                "    print(json.dumps({'draft_id': 'draft_fixture'}))\n"
                "else:\n"
                "    print(json.dumps({'message_id': 'message_fixture'}))\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            env = dict(os.environ)
            env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
            env["FAKE_AGENTMAIL_LOG"] = str(log)
            env.pop("AGENTMAIL_API_KEY", None)

            live = run(
                str(HANDOFF),
                str(root),
                "--subject",
                "Fixture update",
                "--html-file",
                str(html),
                "--text-file",
                str(text),
                "--client-id",
                "fixture-001",
                "--execute",
                env=env,
            )
            self.assertEqual(live.returncode, 0, live.stdout + live.stderr)
            self.assertFalse(marker.exists())
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
            self.assertIn("inboxes:drafts", calls[0])
            self.assertIn("create", calls[0])
            self.assertIn("inboxes:drafts", calls[1])
            self.assertIn("send", calls[1])
            self.assertNotIn(token, json.dumps(calls))
            self.assertNotIn(token, live.stdout + live.stderr)

    def test_scoped_key_rotation_preserves_shared_env_and_hides_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_workspace(root, token="parent-key")
            self.assertEqual(run(str(SETUP), str(root)).returncode, 0)
            self.configure_instance(root)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            fake = bin_dir / "agentmail"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'api_key_id': 'key_fixture', 'api_key': 'scoped-secret', 'prefix': 'am_test'}))\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            env = dict(os.environ)
            env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
            env.pop("AGENTMAIL_API_KEY", None)
            result = run(str(PROVISION), str(root), "--execute", env=env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            contents = (root / ".env").read_text(encoding="utf-8")
            self.assertIn("CAPTURE_TOKEN=preserve-me", contents)
            self.assertIn("AGENTMAIL_API_KEY=scoped-secret", contents)
            self.assertNotIn("parent-key", contents)
            self.assertNotIn("scoped-secret", result.stdout + result.stderr)
            self.assertEqual((root / ".env").stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
