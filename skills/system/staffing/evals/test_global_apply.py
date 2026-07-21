#!/usr/bin/env python3
"""Staffing global-module apply and whole-tree variant integration checks.

Ported from tools/global-modules/evals/test_global_barrier.py when the
Presentation module retired; the surviving owner keeps its guarantees:
variant-tree integrity, atomic apply (injected failure leaves the global
untouched), foreign-byte preservation, and idempotence.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


STAFFING = Path(__file__).resolve().parent.parent
REPO = STAFFING.parents[2]
CATALOG = REPO / "tools" / "catalog.py"
BASELINE_BYTES = 10_391


def run(*args: object, ok: bool = True, env: dict[str, str] | None = None):
    result = subprocess.run(
        [sys.executable, *map(str, args)], capture_output=True, text=True, env=env
    )
    if ok and result.returncode:
        raise AssertionError(result.stderr + result.stdout)
    return result


def materialize(provider: str, output: Path) -> Path:
    run(
        CATALOG, "materialize", "staffing", "--root", REPO,
        "--provider", provider, "--output", output,
    )
    return output


def apply_staffing(compiled: Path, module: Path, global_file: Path, *extra: object, **kw):
    return run(
        compiled / "scripts" / "render-global.py", "apply",
        "--module", module, "--global-file", global_file, *extra, **kw
    )


def section(data: bytes, heading: str) -> bytes:
    text = data.decode()
    match = re.search(rf"(?m)^## {re.escape(heading)}\n", text)
    if not match:
        return b""
    next_heading = re.search(r"(?m)^## ", text[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.start():end].encode()


class GlobalApplyTests(unittest.TestCase):
    def test_materialized_provider_tree_has_only_its_runtime_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for provider, opposite in (("codex", "claude"), ("claude", "codex")):
                with self.subTest(provider=provider):
                    compiled = materialize(provider, root / provider)
                    self.assertFalse((compiled / "variants").exists())
                    self.assertFalse((compiled / "evals").exists())
                    names = {
                        path.relative_to(compiled).as_posix()
                        for path in (compiled / "templates" / "global").iterdir()
                    }
                    self.assertEqual(
                        names,
                        {
                            "templates/global/global-header.txt",
                            "templates/global/provider.txt",
                            "templates/global/staffing-pointer.md",
                            "templates/global/staffing.common.md",
                            "templates/global/staffing.module.md",
                        },
                    )
                    all_paths = "\n".join(
                        path.relative_to(compiled).as_posix() for path in compiled.rglob("*")
                    )
                    self.assertNotIn(f"staffing.{opposite}.md", all_paths)
                    runtime = "\n".join(
                        path.read_text(errors="ignore")
                        for path in compiled.rglob("*") if path.is_file()
                    )
                    forbidden = (
                        ("~/.claude/", "Claude→Codex")
                        if provider == "codex"
                        else ("~/.codex/", "Codex→Claude")
                    )
                    for marker in forbidden:
                        self.assertNotIn(marker, runtime)
                    loaded = sum(
                        (compiled / relative).stat().st_size
                        for relative in (
                            "SKILL.md",
                            "reference/install-and-reconcile.md",
                            "reference/harness.md",
                        )
                    )
                    self.assertLessEqual(loaded, BASELINE_BYTES * 0.8)

    def test_apply_preserves_foreign_sections_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            compiled = {
                provider: materialize(provider, root / f"staffing-{provider}")
                for provider in ("codex", "claude")
            }
            globals_ = {
                provider: root / f"{provider}-global.md" for provider in ("codex", "claude")
            }
            for provider, path in globals_.items():
                path.write_text(
                    f"# Global {provider}\n\n"
                    f"## User\nkeep-user-{provider}\n\n"
                    f"## Staffing\nold-staffing-{provider}\n\n"
                    f"## Tail\nkeep-tail-{provider}\n"
                )

            # Injected failure before any write leaves the global untouched.
            env = dict(os.environ)
            env["ASHER_SKILLS_FAIL_MODULE"] = "staffing:claude"
            before = globals_["claude"].read_bytes()
            failed = apply_staffing(
                compiled["claude"],
                root / "modules" / "staffing" / "claude" / "module.md",
                globals_["claude"], ok=False, env=env,
            )
            self.assertIn("injected module apply failure", failed.stderr)
            self.assertEqual(globals_["claude"].read_bytes(), before)

            for provider in ("codex", "claude"):
                old_user = section(globals_[provider].read_bytes(), "User")
                old_tail = section(globals_[provider].read_bytes(), "Tail")
                apply_staffing(
                    compiled[provider],
                    root / "modules" / "staffing" / provider / "module.md",
                    globals_[provider],
                )
                data = globals_[provider].read_bytes()
                self.assertEqual(section(data, "User"), old_user)
                self.assertEqual(section(data, "Tail"), old_tail)
                self.assertNotEqual(
                    section(data, "Staffing"),
                    f"## Staffing\nold-staffing-{provider}\n\n".encode(),
                )

            # Idempotent rerun: global bytes and module inodes stable.
            first = {provider: path.read_bytes() for provider, path in globals_.items()}
            module_inodes = {
                path: path.stat().st_ino for path in (root / "modules").rglob("module.md")
            }
            for provider in ("codex", "claude"):
                apply_staffing(
                    compiled[provider],
                    root / "modules" / "staffing" / provider / "module.md",
                    globals_[provider],
                )
            self.assertEqual(
                {provider: path.read_bytes() for provider, path in globals_.items()}, first
            )
            self.assertEqual(
                {path: path.stat().st_ino for path in module_inodes}, module_inodes
            )


if __name__ == "__main__":
    unittest.main()
