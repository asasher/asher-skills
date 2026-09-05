#!/usr/bin/env python3
"""Commit files to a branch without checking it out; print the new commit hash.

Usage: to-branch.py <branch> <file[:dest]>... -m <message> [--push] [--remote origin]

Forks from HEAD when the branch does not exist yet. Never force-moves a ref.
"""

import argparse
import os
import subprocess
import sys
import tempfile


def git(*args, env=None, capture=True):
    result = subprocess.run(["git", *args], env=env, text=True, capture_output=capture)
    if result.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {(result.stderr or '').strip()}")
    return (result.stdout or "").strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("branch")
    parser.add_argument("files", nargs="+", help="source path, or source:dest-path-in-branch")
    parser.add_argument("-m", "--message", required=True)
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--remote", default="origin")
    args = parser.parse_args()

    ref = f"refs/heads/{args.branch}"
    parent = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", ref], text=True, capture_output=True
    ).stdout.strip()
    base = parent or git("rev-parse", "HEAD")

    fd, index = tempfile.mkstemp(prefix="to-branch-index-")
    os.close(fd)
    os.unlink(index)
    env = dict(os.environ, GIT_INDEX_FILE=index)
    try:
        git("read-tree", base, env=env)
        for spec in args.files:
            src, _, dest = spec.partition(":")
            dest = dest or os.path.basename(src)
            if not os.path.isfile(src):
                sys.exit(f"not a file: {src}")
            blob = git("hash-object", "-w", "--", src)
            git("update-index", "--add", "--cacheinfo", f"100644,{blob},{dest}", env=env)
        tree = git("write-tree", env=env)
        cmd = ["commit-tree", tree, "-m", args.message]
        if parent:
            cmd += ["-p", parent]
        else:
            cmd += ["-p", base]
        commit = git(*cmd, env=env)
        # refuse non-fast-forward: update only if the ref still points where we read it
        git("update-ref", ref, commit, parent or "")
    finally:
        if os.path.exists(index):
            os.unlink(index)

    if args.push:
        git("push", args.remote, f"{ref}:{ref}")
    print(commit)


if __name__ == "__main__":
    main()
