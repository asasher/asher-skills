#!/usr/bin/env python3
"""Mechanical leak scan for an upstream feedback draft — part of the retro skill's upstream gate.

The draft is written generatively in skill vocabulary; this script is the net underneath. It flags
denylist terms, email addresses, absolute filesystem paths, and URLs outside the allowed prefixes.
A clean exit is necessary for submission, never sufficient: the human approval of the verbatim
draft is the gate.

Usage:
    python3 scrub.py DRAFT DENYLIST [--allow URL_PREFIX]...

DENYLIST is one term per line; blank lines and #-comments are ignored; matching is
case-insensitive substring. --allow is repeatable and defaults to the upstream repo's own URL
space being absent — pass e.g. --allow https://github.com/asasher/asher-skills to permit links
into the target repo.

Exit 0: no findings. Exit 1: findings, one per line:  <line>:<kind>: <excerpt>
"""

import argparse
import re
import sys
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL = re.compile(r"https?://[^\s)\"'`>\]]+")
ABS_PATH = re.compile(
    r"(?:^|(?<=[\s\"'`(=\[]))"
    r"(/(?:Users|home|Volumes|private|var|opt|srv|tmp|etc|root)/[^\s\"'`)\]]+"
    r"|[A-Za-z]:\\[^\s\"'`)\]]+"
    r"|~/[^\s\"'`)\]]+)"
)


def load_denylist(path: Path) -> list[str]:
    terms = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        term = raw.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return terms


def scan(text: str, denylist: list[str], allow: list[str]) -> list[tuple[int, str, str]]:
    findings = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for term in denylist:
            if term.lower() in lowered:
                findings.append((lineno, "denylist", term))
        for match in EMAIL.finditer(line):
            findings.append((lineno, "email", match.group(0)))
        for match in ABS_PATH.finditer(line):
            findings.append((lineno, "path", match.group(0)))
        for match in URL.finditer(line):
            url = match.group(0)
            if not any(url.startswith(prefix) for prefix in allow):
                findings.append((lineno, "url", url))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("draft", type=Path)
    parser.add_argument("denylist", type=Path)
    parser.add_argument("--allow", action="append", default=[], metavar="URL_PREFIX")
    args = parser.parse_args()

    findings = scan(
        args.draft.read_text(encoding="utf-8"),
        load_denylist(args.denylist),
        args.allow,
    )
    for lineno, kind, excerpt in findings:
        print(f"{lineno}:{kind}: {excerpt}")
    if findings:
        print(f"FAIL: {len(findings)} finding(s) — rewrite and re-run", file=sys.stderr)
        return 1
    print("clean", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
