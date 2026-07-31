#!/usr/bin/env python3
"""Check machine-fact records under docs/agents/ against the current machine.

Scans every Markdown file under <root>/docs/agents/ (the gitignored local/
overlays included, when present) for the two markers the machine-facts
convention defines (reference/machine-facts.md):

    <!-- machine-record: machine=<hostname> probed=<YYYY-MM-DD> -->
    <!-- machine-local: docs/agents/local/<name>.md setup="<skill> setup" -->

Findings — a machine-record naming another machine, a declared machine-local
overlay whose file is absent, or a marker matching the comment prefix but not
the grammar — print one per line on stdout. Exit 1 when any finding exists,
0 when none. No stored state: the scan is the whole verdict.

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
    for path in sorted(agents_dir.rglob("*.md")):
        rel = path.relative_to(root)
        for lineno, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            stripped = line.strip()
            if not PREFIX_RE.search(stripped):
                continue
            record = RECORD_RE.match(stripped)
            if record:
                recorded, probed = record.groups()
                if normalize(recorded) != normalize(machine):
                    findings.append(
                        f"stale {rel}: recorded machine '{recorded}' is not "
                        f"this machine '{machine}' (probed {probed})"
                    )
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
    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Check docs/agents/ machine-fact records against the current machine."
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
