#!/usr/bin/env python3
"""Allocate immutable sibling output paths for generated image artifacts."""

from contextlib import contextmanager
from pathlib import Path
import re


VERSION_SUFFIX = re.compile(r"^(?P<base>.+)-v(?P<version>[1-9][0-9]*)$")


def _family(path):
    match = VERSION_SUFFIX.match(path.stem)
    if match:
        return match.group("base"), int(match.group("version")), True
    return path.stem, 1, False


def _existing_versions(path):
    base, _, _ = _family(path)
    versions = {}
    unversioned = path.with_name(f"{base}{path.suffix}")
    if unversioned.exists():
        versions[1] = unversioned

    pattern = re.compile(rf"^{re.escape(base)}-v([1-9][0-9]*){re.escape(path.suffix)}$")
    if path.parent.exists():
        for sibling in path.parent.iterdir():
            match = pattern.match(sibling.name)
            if match and sibling.is_file():
                versions[int(match.group(1))] = sibling
    return base, versions


def latest_existing_path(requested):
    """Return the highest existing sibling version, or None for a new family."""
    path = Path(requested)
    _, versions = _existing_versions(path)
    return versions[max(versions)] if versions else None


def next_output_path(requested):
    """Return the requested path or the next monotonic ``-vN`` sibling."""
    path = Path(requested)
    base, requested_version, explicitly_versioned = _family(path)
    _, versions = _existing_versions(path)
    if explicitly_versioned and not path.exists():
        return path
    if not versions:
        return path
    version = max(max(versions) + 1, requested_version + 1)
    return path.with_name(f"{base}-v{version}{path.suffix}")


@contextmanager
def open_output(requested):
    """Open a new output atomically, retrying with a later version on races."""
    path = Path(requested)
    path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        candidate = next_output_path(path)
        try:
            handle = candidate.open("xb")
            break
        except FileExistsError:
            continue

    try:
        yield candidate, handle
    except BaseException:
        handle.close()
        try:
            candidate.unlink()
        except FileNotFoundError:
            pass
        raise
    else:
        handle.close()
