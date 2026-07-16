#!/usr/bin/env python3
"""Authorize, create, verify, and send one exact AgentMail draft; dry by default."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from relay_common import append_event, build_approval_manifest, canonical_json, dotenv_value, instance_root, load_json, now, read_jsonl, recipient_hash, sha256_bytes, sha256_file, workflow_event


class ManifestParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capture = False
        self.value = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("id") == "relay-approval-manifest":
            self.capture = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capture:
            self.capture = False

    def handle_data(self, data: str) -> None:
        if self.capture:
            self.value += data


def extract_id(value: Any, names: tuple[str, ...]) -> str | None:
    if isinstance(value, dict):
        for name in names:
            if isinstance(value.get(name), str) and value[name]:
                return value[name]
        for child in value.values():
            found = extract_id(child, names)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = extract_id(child, names)
            if found:
                return found
    return None


def invoke(command: list[str], env: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=60, check=False)
    if result.returncode:
        raise RuntimeError(f"AgentMail command failed with exit {result.returncode}")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("AgentMail returned non-JSON output") from error
    if not isinstance(value, dict):
        raise RuntimeError("AgentMail returned an unexpected response")
    return value


def verify_draft(value: dict[str, Any], manifest: dict[str, Any], run: Path) -> None:
    expected = {
        "subject": manifest["subject"], "sender": manifest["sender"],
        "to": manifest["recipients"]["to"], "cc": manifest["recipients"]["cc"],
        "html_sha256": manifest["content"]["html_sha256"], "text_sha256": manifest["content"]["text_sha256"],
    }
    candidate = value.get("draft", value)
    actual = {
        "subject": candidate.get("subject"), "sender": candidate.get("sender") or candidate.get("from"),
        "to": sorted(candidate.get("to", [])), "cc": sorted(candidate.get("cc", [])),
        "html_sha256": candidate.get("html_sha256") or (sha256_bytes(candidate["html"].encode()) if isinstance(candidate.get("html"), str) else None),
        "text_sha256": candidate.get("text_sha256") or (sha256_bytes(candidate["text"].encode()) if isinstance(candidate.get("text"), str) else None),
    }
    if actual != expected:
        raise RuntimeError("AgentMail draft fields do not match the approved manifest")


def approved_event(run: Path) -> dict[str, Any] | None:
    doc_hash = sha256_file(run / "review.html")[:16]
    events = read_jsonl(run / "review-state" / "events.jsonl")
    matches = [event for event in events if event.get("type") == "feedback_submitted" and event.get("verdict") in {"approve", "approve_with_nits"} and event.get("doc_hash") == doc_hash]
    return matches[-1] if matches else None


def reconcile(path: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    value = json.loads(path.read_text(encoding="utf-8"))
    matches = value if isinstance(value, list) else value.get("messages", [])
    matches = [item for item in matches if isinstance(item, dict) and (item.get("client_id") == manifest["client_id"] or item.get("communication_id") == manifest["communication_id"])]
    return matches[0] if len(matches) == 1 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--reconcile-file", type=Path)
    parser.add_argument("--fail-at", choices=["before-draft", "after-draft", "after-send-submit-before-call", "after-send-call"])
    args = parser.parse_args()
    try:
        repo, run = args.repository_root.resolve(), args.run.resolve()
        instance = instance_root(repo)
        recorded = load_json(run / "approval-manifest.json")
        current = build_approval_manifest(repo, run)
        parser_value = ManifestParser()
        parser_value.feed((run / "review.html").read_text(encoding="utf-8"))
        embedded = json.loads(parser_value.value)
        workflow = instance / "state" / "workflow.jsonl"
        if recorded != current or embedded != current or approved_event(run) is None:
            append_event(workflow, workflow_event(repo, current, "superseded", reason="approval-mismatch-or-missing"))
            raise ValueError("exact current review is not approved")
        approval = approved_event(run)
        append_event(workflow, workflow_event(repo, current, "reviewed", review_doc_hash=sha256_file(run / "review.html")[:16], verdict=approval.get("verdict"), review_event_id=approval.get("id")))
        capability = load_json(instance / "capabilities.json")["agentmail"]
        if capability.get("status") != "verified" or not capability.get("sender_verified") or capability.get("sender") != current["sender"]:
            raise ValueError("selected AgentMail capability or sender is not verified")
        events = [item for item in read_jsonl(workflow) if item.get("communication_id") == current["communication_id"] and item.get("manifest_sha256") == current["manifest_sha256"]]
        sent = next((item for item in reversed(events) if item.get("state") == "sent"), None)
        if sent:
            print(json.dumps({"status": "already_sent", "message_id": sent.get("message_id"), "client_id": current["client_id"]}, indent=2))
            return 0
        submitted = next((item for item in reversed(events) if item.get("state") == "send-submitted"), None)
        if submitted:
            match = reconcile(args.reconcile_file, current) if args.reconcile_file else None
            if not match:
                append_event(workflow, workflow_event(repo, current, "blocked-ambiguous", draft_id=submitted.get("draft_id"), reason="send-outcome-not-unique"))
                print(json.dumps({"status": "blocked_ambiguous", "client_id": current["client_id"]}))
                return 4
            sent_event = workflow_event(repo, current, "sent", draft_id=submitted.get("draft_id"), message_id=match.get("message_id"), thread_id=match.get("thread_id"), reconciliation="unique")
            append_event(workflow, sent_event)
            print(json.dumps({"status": "reconciled_sent", "message_id": match.get("message_id"), "client_id": current["client_id"]}, indent=2))
            return 0
        if not args.execute:
            print(json.dumps({"status": "dry_run", "authorized": True, "client_id": current["client_id"], "sender": current["sender"], "to": current["recipients"]["to"], "cc": current["recipients"]["cc"], "actions": ["draft-create", "draft-get-verify", "draft-send"]}, indent=2))
            return 0
        token = dotenv_value(repo / ".env", "AGENTMAIL_API_KEY")
        ignored = (repo / ".gitignore").is_file() and ".env" in {line.strip() for line in (repo / ".gitignore").read_text(encoding="utf-8").splitlines()}
        if not token or not ignored or (repo / ".env").stat().st_mode & 0o777 != 0o600:
            raise ValueError("protected repository-root AGENTMAIL_API_KEY is required")
        executable = shutil.which("agentmail")
        if not executable:
            raise ValueError("agentmail CLI is not installed")
        env = dict(os.environ)
        env["AGENTMAIL_API_KEY"] = token
        inbox = capability["inbox_id"]
        html_body = (run / "rendered-email.html").read_text(encoding="utf-8")
        text_body = (run / "rendered-email.txt").read_text(encoding="utf-8")
        draft_event = next((item for item in reversed(events) if item.get("state") == "draft-created"), None)
        if draft_event:
            draft_id = draft_event["draft_id"]
        else:
            if args.fail_at == "before-draft":
                return 75
            create = [executable, "--format", "json", "inboxes:drafts", "create", "--inbox-id", inbox, "--client-id", current["client_id"], "--from", current["sender"]]
            for address in current["recipients"]["to"]:
                create.extend(["--to", address])
            for address in current["recipients"]["cc"]:
                create.extend(["--cc", address])
            create.extend(["--subject", current["subject"], "--html", html_body, "--text", text_body])
            created = invoke(create, env)
            draft_id = extract_id(created, ("draft_id", "draftId", "id"))
            if not draft_id:
                raise RuntimeError("AgentMail create response omitted draft ID")
            fetched = invoke([executable, "--format", "json", "inboxes:drafts", "get", "--inbox-id", inbox, "--draft-id", draft_id], env)
            verify_draft(fetched, current, run)
            append_event(workflow, workflow_event(repo, current, "draft-created", draft_id=draft_id, client_id=current["client_id"], verified=True))
            if args.fail_at == "after-draft":
                return 75
        append_event(workflow, workflow_event(repo, current, "send-submitted", draft_id=draft_id, client_id=current["client_id"]))
        if args.fail_at == "after-send-submit-before-call":
            return 75
        response = invoke([executable, "--format", "json", "inboxes:drafts", "send", "--inbox-id", inbox, "--draft-id", draft_id], env)
        if args.fail_at == "after-send-call":
            return 75
        message_id = extract_id(response, ("message_id", "messageId", "id"))
        thread_id = extract_id(response, ("thread_id", "threadId"))
        append_event(workflow, workflow_event(repo, current, "sent", draft_id=draft_id, message_id=message_id, thread_id=thread_id, confirmation="send-response"))
        delivery = instance / "state" / "delivery.jsonl"
        for address in current["recipients"]["to"] + current["recipients"]["cc"]:
            hashed = recipient_hash(address)
            append_event(delivery, {"schema_version": 1, "timestamp": now(), "communication_id": current["communication_id"], "audience_id": current["audience_id"], "recipient_hash": hashed, "state": "pending", "idempotency_key": sha256_bytes(f"pending:{current['manifest_sha256']}:{hashed}".encode())})
        print(json.dumps({"status": "sent", "client_id": current["client_id"], "draft_id": draft_id, "message_id": message_id, "thread_id": thread_id}, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
