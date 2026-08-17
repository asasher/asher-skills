#!/usr/bin/env python3
"""Reconcile role-label colors and descriptions on a color-capable tracker (GitHub).

Applies the backlog skill's shared label scheme — the Label colors table in
templates/common/backlog-policy.md; a repo's docs/agents/backlog-policy.md may
override it, and the agent running setup passes those overrides as flags.

Touches only role labels (by default only ones that already exist); every other
label on the tracker is neutral and never modified. Trackers without label
colors have nothing to reconcile.

Usage:
  reconcile-labels.py [--repo owner/name] [--dry-run] [--create]
                      [--label role=name ...] [--color role=hex ...]
                      [--description role=text ...]
"""

import argparse
import json
import subprocess
import sys

# role -> (color without '#', tracker description). Canonical source: the
# Label colors table in templates/common/backlog-policy.md — keep in sync.
SCHEME = {
    # Readiness / ownership — saturated, temperature-coded parked -> flying.
    "needs-shaping": ("D93F0B", "Parked for strategic shaping: unsettled product/scope decisions; never selectable by backlog build"),
    "shaping": ("FBCA04", "A shaping thread is attending this issue; set by backlog groom at dispatch"),
    "needs-info": ("D876E3", "Parked, waiting on the reporter"),
    "ready-for-agent": ("0E8A16", "Groomed and released: an agent may work it; requires a work-type and dispatch metadata"),
    "ready-for-human": ("5319E7", "Human-only; agents skip. Also the abort target for verify caps and environment blockers"),
    "building": ("1D76DB", "Claimed: a build thread owns it; the claim comment is the dispatch declaration with its deadline"),
    "delivered": ("008672", "Merged into its feature branch, awaiting promotion; closed natively by the promotion PR's Closes lines"),
    # Work-type — pastel attributes; bug and spec are the saturated exceptions.
    "bug": ("D73A4A", "Something isn't working"),
    "enhancement": ("A2EEEF", "New feature or request"),
    "refactor": ("C5DEF5", "Work-type: behavior-preserving structure or code improvement"),
    "research": ("D4C5F9", "Work-type: primary-source research with traceable claims"),
    "draft": ("FEF2C0", "Work-type: judgment-terminal produce-and-review; done at the human review verdict"),
    "spec": ("8250DF", "Work-type: parent of slices; coverage check once children are closed or delivered"),
    # Exclusions — grayscale, terminal.
    "duplicate": ("CFD3D7", "This issue or pull request already exists"),
    "superseded": ("BFBFBF", "Replaced by newer work; removed from grooming and the run queue"),
    "invalid": ("E4E669", "This doesn't seem right"),
    "wontfix": ("FFFFFF", "This will not be worked on"),
}


def run(cmd, check=True):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        sys.exit(f"error: {' '.join(cmd)}\n{proc.stderr.strip()}")
    return proc


def parse_overrides(pairs, what):
    out = {}
    for pair in pairs or []:
        role, sep, value = pair.partition("=")
        if not sep or role not in SCHEME:
            sys.exit(f"error: --{what} wants role=value with a known role, got {pair!r}")
        out[role] = value
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", help="owner/name; default: the repo gh resolves from the cwd")
    ap.add_argument("--dry-run", action="store_true", help="report what would change, change nothing")
    ap.add_argument("--create", action="store_true", help="also create missing role labels (with the user's consent)")
    ap.add_argument("--label", action="append", metavar="ROLE=NAME", help="this repo's label name for a role")
    ap.add_argument("--color", action="append", metavar="ROLE=HEX", help="repo playbook color override, no '#'")
    ap.add_argument("--description", action="append", metavar="ROLE=TEXT", help="repo playbook description override")
    args = ap.parse_args()

    repo = args.repo or json.loads(run(["gh", "repo", "view", "--json", "nameWithOwner"]).stdout)["nameWithOwner"]
    names = parse_overrides(args.label, "label")
    colors = parse_overrides(args.color, "color")
    descriptions = parse_overrides(args.description, "description")

    existing = {
        label["name"]: label
        for label in json.loads(run(["gh", "label", "list", "-R", repo, "--limit", "300", "--json", "name,color,description"]).stdout)
    }

    edited, created, missing, ok = [], [], [], []
    for role, (color, description) in SCHEME.items():
        name = names.get(role, role)
        color = colors.get(role, color).lstrip("#")
        description = descriptions.get(role, description)
        current = existing.get(name)
        if current is None:
            if args.create:
                if not args.dry_run:
                    run(["gh", "label", "create", name, "-R", repo, "--color", color, "--description", description])
                created.append(name)
            else:
                missing.append(name)
            continue
        if current["color"].upper() == color.upper() and current["description"] == description:
            ok.append(name)
            continue
        if not args.dry_run:
            run(["gh", "label", "edit", name, "-R", repo, "--color", color, "--description", description])
        edited.append(f"{name} (#{current['color'].upper()} -> #{color.upper()})" if current["color"].upper() != color.upper() else f"{name} (description)")

    verb = "would edit" if args.dry_run else "edited"
    print(f"{repo}: {len(ok)} in scheme, {verb} {len(edited)}" + (f", created {len(created)}" if created else ""))
    for line in edited:
        print(f"  {verb}: {line}")
    for name in created:
        print(f"  created: {name}")
    if missing:
        print(f"  absent, untouched (use --create to mint): {', '.join(missing)}")


if __name__ == "__main__":
    main()
