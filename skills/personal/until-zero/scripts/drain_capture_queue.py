#!/usr/bin/env python3
"""Lease Runway API captures, commit locally, then acknowledge exact successes."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from runway_core import StateError, canonical_bytes, load_json, sha256_bytes
from until_zero import ingest_capture, instance_paths


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def read_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise StateError(f"secret file {path} is overexposed; run chmod 600 {path}")
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def request_json(url: str, token: str, body: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=canonical_bytes(body),
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
            value = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:500]
        raise StateError(f"Runway API {error.code}: {detail}") from error
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise StateError(f"Runway API request failed: {error}") from error
    if not isinstance(value, dict) or value.get("ok") is not True:
        raise StateError("Runway API returned an invalid response")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--instance", default="control-plane/runway")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--lease-seconds", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--actor", default="until-zero-refresh")
    arguments = parser.parse_args(argv)
    try:
        instance, state_dir, config = instance_paths(arguments.project, arguments.instance)
        deployment = load_json(instance / "deployment.json")
        api_url = str(deployment.get("api_url") or "").rstrip("/")
        parsed = urlsplit(api_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        is_loopback = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}
        if (parsed.scheme != "https" and not is_loopback) or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
            raise StateError("deployment api_url must be HTTPS (or loopback for local testing)")
        capture_config = config.get("capture") if isinstance(config.get("capture"), dict) else {}
        if capture_config.get("drain_token_env", "RUNWAY_DRAIN_TOKEN") != "RUNWAY_DRAIN_TOKEN" or capture_config.get("token_file", ".env") != ".env":
            raise StateError("capture token binding must use project .env and RUNWAY_DRAIN_TOKEN")
        token_file = arguments.project.resolve() / ".env"
        file_values = read_dotenv(token_file)
        if file_values.get("RUNWAY_DRAIN_TOKEN"):
            token = file_values["RUNWAY_DRAIN_TOKEN"]
            bound_origin = file_values.get("RUNWAY_API_ORIGIN", "")
        else:
            token = os.environ.get("RUNWAY_DRAIN_TOKEN", "")
            bound_origin = os.environ.get("RUNWAY_API_ORIGIN", "")
        if not token:
            raise StateError("missing RUNWAY_DRAIN_TOKEN in private token file or environment")
        if bound_origin.rstrip("/") != origin:
            raise StateError("RUNWAY_API_ORIGIN does not match deployment api_url; verify and bind the deployment before refresh")
        if not is_loopback and (deployment.get("verification_status") != "verified" or str(deployment.get("verified_origin") or "").rstrip("/") != origin):
            raise StateError("deployment origin is not verified in deployment.json")
        worker_id = str(capture_config.get("worker_id") or "until-zero-local")
        leased = request_json(f"{api_url}/v1/captures/lease", token, {
            "worker_id": worker_id,
            "limit": max(1, min(100, arguments.limit)),
            "lease_seconds": max(30, min(3600, arguments.lease_seconds)),
        })
        lease_id = str(leased.get("lease_id") or "")
        items = leased.get("items") if isinstance(leased.get("items"), list) else []
        if not items:
            print("Runway capture queue is empty.")
            return 0
        failures = 0
        for item in items:
            if not isinstance(item, dict):
                failures += 1
                continue
            identifier = str(item.get("id") or "")
            if arguments.dry_run:
                request_json(f"{api_url}/v1/captures/{identifier}/release", token, {"lease_id": lease_id})
                print(f"preview: {identifier}")
                continue
            try:
                result = ingest_capture(instance, state_dir, item, arguments.actor)
            except (OSError, StateError, ValueError) as error:
                failures += 1
                print(f"failed: {identifier}: {error}", file=sys.stderr)
                continue
            result_hash = sha256_bytes(canonical_bytes(result))
            request_json(f"{api_url}/v1/captures/{identifier}/ack", token, {"lease_id": lease_id, "result_hash": result_hash})
            print(f"committed-and-acknowledged: {identifier}")
        if failures:
            print(f"refresh incomplete: {failures} capture(s) remain unacknowledged", file=sys.stderr)
            return 1
        return 0
    except (OSError, StateError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
