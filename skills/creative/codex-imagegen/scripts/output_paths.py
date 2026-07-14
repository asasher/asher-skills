#!/usr/bin/env python3
"""Allocate immutable sibling paths for flat files and directory artifacts."""

from contextlib import contextmanager
from pathlib import Path
import re


VERSION_SUFFIX = re.compile(r"^(?P<base>.+)-v(?P<version>[1-9][0-9]*)$")


def _artifact_name(path):
    return path.stem if path.suffix else path.name


def _family(path):
    match = VERSION_SUFFIX.match(_artifact_name(path))
    if match:
        return match.group("base"), int(match.group("version")), True
    return _artifact_name(path), 1, False


def _existing_versions(path):
    base, _, _ = _family(path)
    versions = {}
    pattern = re.compile(rf"^{re.escape(base)}(?:-v([1-9][0-9]*))?$")
    if path.parent.exists():
        for sibling in path.parent.iterdir():
            if sibling.is_dir():
                sibling_name = sibling.name
            elif sibling.is_file() and (not path.suffix or sibling.suffix == path.suffix):
                sibling_name = sibling.stem
            else:
                continue
            match = pattern.fullmatch(sibling_name)
            if match:
                version = int(match.group(1) or 1)
                versions[version] = sibling
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
    if explicitly_versioned and requested_version not in versions:
        return path
    if not versions:
        return path
    version = max(max(versions) + 1, requested_version + 1)
    return path.with_name(f"{base}-v{version}{path.suffix}")


def reserve_output_dir(requested):
    """Create and return a new versioned directory without overwriting siblings."""
    path = Path(requested)
    if path.suffix:
        raise ValueError(f"directory artifact must not have a suffix: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        candidate = next_output_path(path)
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue


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
