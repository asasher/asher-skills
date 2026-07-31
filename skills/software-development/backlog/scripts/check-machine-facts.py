#!/usr/bin/env python3
"""Check the machine-fact rule under docs/agents/ against the current machine.

The rule (reference/machine-facts.md): a tracked file never records a machine
fact; recorded machine facts live only in the gitignored docs/agents/local/
overlays, each opening with a machine-record stamp. Two markers exist:

    <!-- machine-record: machine=<hostname> probed=<YYYY-MM-DD> -->
    <!-- machine-local: docs/agents/local/<name>.md setup="<skill> setup" -->

Findings, one per line on stdout:
  - a machine-record stamp in a tracked (non-overlay) file — machine facts
    belong in the overlay
  - a declared machine-local overlay whose file is absent
  - an overlay whose first marker is missing or names another machine
  - a marker matching the comment prefix but not the grammar

Exit 1 when any finding exists, 0 when none. No stored state: the scan is the
whole verdict.

A marker counts only when the comment opens the line (leading whitespace
aside): prose quoting a marker mid-sentence is ignored rather than reported
malformed.
"""

import argparse
import re
import socket
import subprocess
import sys
from pathlib import Path

RECORD_RE = re.compile(
    r"^<!--\s*machine-record:\s*machine=(\S+)\s+probed=(\d{4}-\d{2}-\d{2})\s*-->$"
)
LOCAL_RE = re.compile(
    r'^<!--\s*machine-local:\s*(\S+)\s+setup="([^"]+)"\s*-->$'
)
PREFIX_RE = re.compile(r"^<!--\s*machine-(record|local)\b")


def normalize(name):
    """Short hostname, case-insensitive: 'Some-Host.local' -> 'some-host'."""
    return name.split(".", 1)[0].lower()


def current_machine():
    """The machine's stable short name.

    On macOS the network hostname is transient (DHCP can rename it), so prefer
    the local host name; fall back to socket.gethostname() everywhere else.
    """
    if sys.platform == "darwin":
        try:
            result = subprocess.run(
                ["scutil", "--get", "LocalHostName"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            name = result.stdout.strip()
            if result.returncode == 0 and name:
                return name
        except (OSError, subprocess.SubprocessError):
            pass
    return socket.gethostname()


def scan(root, machine):
    findings = []
    agents_dir = root / "docs" / "agents"
    if not agents_dir.is_dir():
        return findings
    local_dir = agents_dir / "local"
    for path in sorted(agents_dir.rglob("*.md")):
        rel = path.relative_to(root)
        is_overlay = local_dir in path.parents
        saw_stamp = False
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            stripped = line.strip()
            if not PREFIX_RE.search(stripped):
                continue
            record = RECORD_RE.match(stripped)
            if record:
                recorded, probed = record.groups()
                if not is_overlay:
                    findings.append(
                        f"tracked {rel}:{lineno}: machine-record stamp in a "
                        f"tracked file — machine facts live in the "
                        f"docs/agents/local/ overlay"
                    )
                elif normalize(recorded) != normalize(machine):
                    findings.append(
                        f"stale {rel}: recorded machine '{recorded}' is not "
                        f"this machine '{machine}' (probed {probed})"
                    )
                saw_stamp = True
                continue
            local = LOCAL_RE.match(stripped)
            if local:
                overlay, setup = local.groups()
                if not (root / overlay).is_file():
                    findings.append(
                        f"missing {overlay}: machine-local overlay absent "
                        f"— run '{setup}'"
                    )
                continue
            findings.append(f"malformed {rel}:{lineno}: {stripped}")
        if is_overlay and not saw_stamp:
            findings.append(
                f"unstamped {rel}: overlay carries no machine-record stamp "
                f"— re-run the owning setup"
            )
    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Check the docs/agents/ machine-fact rule against the current machine."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="repo root whose docs/agents/ is scanned (default: .)",
    )
    parser.add_argument(
        "--machine",
        default=None,
        help="override the current machine name (default: this host's stable short name)",
    )
    args = parser.parse_args()
    machine = args.machine if args.machine is not None else current_machine()
    findings = scan(Path(args.root), machine)
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
