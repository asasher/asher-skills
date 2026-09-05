#!/usr/bin/env python3
"""Reconcile the backlog family's label colors and descriptions on GitHub.
Applies the fixed scheme in reference/labels.md. Touches only the family's
labels (by default only ones that already exist); every other label on the
repo is never modified.
Usage:
  reconcile-labels.py [--repo owner/name] [--dry-run] [--create]
                      [--label role=name ...] [--color role=hex ...]
                      [--description role=text ...]
"""
import argparse
import json
import subprocess
import sys

# label -> (color without '#', description). Canonical source: the Label
# colors table in reference/labels.md; keep in sync.
SCHEME = {
    # Readiness: saturated, temperature-coded parked -> flying.
    "needs-shaping": ("D93F0B", "Parked for shaping: unsettled product or scope decisions; never selected by backlog build"),
    "shaping": ("FBCA04", "Shaping or approved split publication owns this issue; builds skip it"),
    "needs-info": ("D876E3", "Parked, waiting on the reporter"),
    "ready-for-agent": ("0E8A16", "Released: an agent may work it; requires a work-type"),
    "ready-for-human": ("5319E7", "Human-only; agents skip. Also the handback target for blockers"),
    "building": ("1D76DB", "Claimed: a build thread owns it; the claim comment is the dispatch declaration with its deadline"),
    # Work-type: pastel; bug and spec are the saturated exceptions.
    "bug": ("D73A4A", "Something isn't working"),
    "enhancement": ("A2EEEF", "New feature or request"),
    "spec": ("8250DF", "Parent of a split: coverage check and promotion PR once every child is closed"),
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
    ap.add_argument("--color", action="append", metavar="ROLE=HEX", help="color override, no '#'")
    ap.add_argument("--description", action="append", metavar="ROLE=TEXT", help="description override")
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
