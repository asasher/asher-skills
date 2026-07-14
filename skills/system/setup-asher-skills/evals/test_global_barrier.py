#!/usr/bin/env python3
"""Cross-owner barrier and whole-tree staffing-variant integration checks."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SETUP = Path(__file__).resolve().parent.parent
REPO = SETUP.parents[2]
CATALOG = SETUP / "scripts" / "catalog.py"
PRESENTATION = SETUP / "scripts" / "render-global.py"
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


def stage_all(root: Path, compiled: dict[str, Path], barrier: Path) -> None:
    run(PRESENTATION, "begin", "--barrier", barrier)
    for provider in ("codex", "claude"):
        run(
            PRESENTATION, "stage", "--provider", provider,
            "--module", root / "modules" / "presentation" / provider / "module.md",
            "--barrier", barrier,
        )
        run(
            compiled[provider] / "scripts" / "render-global.py", "stage",
            "--module", root / "modules" / "staffing" / provider / "module.md",
            "--barrier", barrier,
        )


def preflight_all(globals_: dict[str, Path], barrier: Path) -> None:
    for provider in ("codex", "claude"):
        run(
            PRESENTATION, "preflight", "--provider", provider,
            "--global-file", globals_[provider], "--barrier", barrier,
        )


def apply_all(compiled: dict[str, Path], globals_: dict[str, Path], barrier: Path) -> None:
    preflight_all(globals_, barrier)
    for provider in ("codex", "claude"):
        run(
            PRESENTATION, "apply", "--provider", provider,
            "--global-file", globals_[provider], "--barrier", barrier,
        )
    for provider in ("codex", "claude"):
        run(
            compiled[provider] / "scripts" / "render-global.py", "apply",
            "--global-file", globals_[provider], "--barrier", barrier,
        )
    run(PRESENTATION, "finalize", "--barrier", barrier)


def section(data: bytes, heading: str) -> bytes:
    match = re.search(rf"(?m)^## {re.escape(heading)}\n", data.decode())
    if not match:
        return b""
    text = data.decode()
    next_heading = re.search(r"(?m)^## ", text[match.end():])
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.start():end].encode()


class GlobalBarrierTests(unittest.TestCase):
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

    def test_all_four_modules_precede_cross_owner_pointer_application(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            compiled = {
                provider: materialize(provider, root / f"staffing-{provider}")
                for provider in ("codex", "claude")
            }
            barrier = root / "barrier.json"
            globals_ = {
                provider: root / f"{provider}-global.md" for provider in ("codex", "claude")
            }
            for provider, path in globals_.items():
                path.write_text(
                    f"# Global {provider}\n\n"
                    f"## User\nkeep-user-{provider}\n\n"
                    f"## Staffing\nold-staffing-{provider}\n\n"
                    f"## Presentation\nold-presentation-{provider}\n\n"
                    f"## Tail\nkeep-tail-{provider}\n"
                )
            original = {provider: path.read_bytes() for provider, path in globals_.items()}
            modules = {
                (owner, provider): root / "modules" / owner / provider / "module.md"
                for owner in ("presentation", "staffing") for provider in ("codex", "claude")
            }

            # A prior completed transaction must not satisfy a later partial one.
            stage_all(root, compiled, barrier)
            run(PRESENTATION, "begin", "--barrier", barrier)
            for provider in ("codex", "claude"):
                run(
                    PRESENTATION, "stage", "--provider", provider,
                    "--module", modules[("presentation", provider)], "--barrier", barrier,
                )
            run(
                compiled["codex"] / "scripts" / "render-global.py", "stage",
                "--module", modules[("staffing", "codex")], "--barrier", barrier,
            )
            env = dict(os.environ)
            env["ASHER_SKILLS_FAIL_MODULE"] = "staffing:claude"
            failed = run(
                compiled["claude"] / "scripts" / "render-global.py", "stage",
                "--module", modules[("staffing", "claude")], "--barrier", barrier,
                ok=False, env=env,
            )
            self.assertIn("injected module staging failure", failed.stderr)
            denied = run(
                PRESENTATION, "apply", "--provider", "codex",
                "--global-file", globals_["codex"], "--barrier", barrier, ok=False,
            )
            self.assertIn("all four deferred modules", denied.stderr)
            self.assertEqual(
                {provider: path.read_bytes() for provider, path in globals_.items()}, original
            )

            run(
                compiled["claude"] / "scripts" / "render-global.py", "stage",
                "--module", modules[("staffing", "claude")], "--barrier", barrier,
            )
            preflight_all(globals_, barrier)
            old_staffing = {
                provider: section(path.read_bytes(), "Staffing")
                for provider, path in globals_.items()
            }
            old_user = {
                provider: section(path.read_bytes(), "User")
                for provider, path in globals_.items()
            }
            for provider in ("codex", "claude"):
                run(
                    PRESENTATION, "apply", "--provider", provider,
                    "--global-file", globals_[provider], "--barrier", barrier,
                )
                self.assertEqual(section(globals_[provider].read_bytes(), "Staffing"), old_staffing[provider])
                self.assertEqual(section(globals_[provider].read_bytes(), "User"), old_user[provider])

            presentation = {
                provider: section(path.read_bytes(), "Presentation")
                for provider, path in globals_.items()
            }
            for provider in ("codex", "claude"):
                run(
                    compiled[provider] / "scripts" / "render-global.py", "apply",
                    "--global-file", globals_[provider], "--barrier", barrier,
                )
                self.assertEqual(
                    section(globals_[provider].read_bytes(), "Presentation"), presentation[provider]
                )
                self.assertEqual(section(globals_[provider].read_bytes(), "User"), old_user[provider])

            run(PRESENTATION, "finalize", "--barrier", barrier)
            self.assertFalse(barrier.exists())

    def test_legacy_seeded_conventions_migrate_to_exact_compact_globals(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            compiled = {
                provider: materialize(provider, root / f"staffing-{provider}")
                for provider in ("codex", "claude")
            }
            barrier = root / "barrier.json"
            globals_ = {
                provider: root / f"{provider}-global.md" for provider in ("codex", "claude")
            }
            for provider, global_file in globals_.items():
                native = "AGENTS" if provider == "codex" else "CLAUDE"
                global_file.write_text(
                    f"# Global {native}.md — machine-level conventions\n\n"
                    "Seeded by `setup-asher-skills` (`templates/global-conventions.md`), "
                    "2026-07-10, with Asher's consent.\n\n"
                    "## Conventions\n\n### Presenting HTML to the human\nlegacy presentation\n\n"
                    "## Staffing\nlegacy staffing\n"
                )

            stage_all(root, compiled, barrier)
            apply_all(compiled, globals_, barrier)
            first = {provider: path.read_bytes() for provider, path in globals_.items()}
            module_inodes = {
                path: path.stat().st_ino
                for path in (root / "modules").rglob("module.md")
            }
            self.assertFalse(barrier.exists())

            for provider, global_file in globals_.items():
                with self.subTest(provider=provider):
                    native = "AGENTS" if provider == "codex" else "CLAUDE"
                    presentation = (
                        SETUP / "templates" / "global" / f"presentation-pointer.{provider}.md"
                    ).read_text().rstrip()
                    staffing = (
                        compiled[provider] / "templates" / "global" / "staffing-pointer.md"
                    ).read_text()
                    expected = f"# Global {native}.md\n\n{presentation}\n\n{staffing}"
                    self.assertEqual(global_file.read_text(), expected)
                    self.assertNotIn("## Conventions", global_file.read_text())

            stage_all(root, compiled, barrier)
            apply_all(compiled, globals_, barrier)
            self.assertEqual(
                {provider: path.read_bytes() for provider, path in globals_.items()}, first
            )
            self.assertEqual(
                {path: path.stat().st_ino for path in module_inodes}, module_inodes
            )
            self.assertFalse(barrier.exists())

    def test_unowned_conventions_refuse_migration_and_empty_order_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            compiled = {
                provider: materialize(provider, root / f"staffing-{provider}")
                for provider in ("codex", "claude")
            }
            barrier = root / "barrier.json"
            stage_all(root, compiled, barrier)

            globals_ = {
                "codex": root / "unowned.md",
                "claude": root / "claude.md",
            }
            globals_["codex"].write_text("# Personal rules\n\n## Conventions\nkeep me\n")
            globals_["claude"].write_text("# Global CLAUDE.md\n")
            before = globals_["codex"].read_bytes()
            staffing_denied = run(
                compiled["codex"] / "scripts" / "render-global.py", "apply",
                "--global-file", globals_["codex"], "--barrier", barrier, ok=False,
            )
            self.assertIn("Presentation preflight", staffing_denied.stderr)
            denied = run(
                PRESENTATION, "preflight", "--provider", "codex",
                "--global-file", globals_["codex"], "--barrier", barrier, ok=False,
            )
            self.assertIn("unrecognized ## Conventions owner", denied.stderr)
            self.assertEqual(globals_["codex"].read_bytes(), before)

            empty_globals = {
                "codex": root / "empty-codex.md",
                "claude": root / "empty-claude.md",
            }
            stage_all(root, compiled, barrier)
            preflight_all(empty_globals, barrier)
            empty_before = {provider: path.read_bytes() if path.exists() else b"" for provider, path in empty_globals.items()}
            denied = run(
                compiled["codex"] / "scripts" / "render-global.py", "apply",
                "--global-file", empty_globals["codex"], "--barrier", barrier, ok=False,
            )
            self.assertIn("Presentation must apply before Staffing", denied.stderr)
            self.assertEqual(
                {provider: path.read_bytes() if path.exists() else b"" for provider, path in empty_globals.items()},
                empty_before,
            )
            for provider in ("codex", "claude"):
                run(
                    PRESENTATION, "apply", "--provider", provider,
                    "--global-file", empty_globals[provider], "--barrier", barrier,
                )
            for provider in ("codex", "claude"):
                run(
                    compiled[provider] / "scripts" / "render-global.py", "apply",
                    "--global-file", empty_globals[provider], "--barrier", barrier,
                )
            run(PRESENTATION, "finalize", "--barrier", barrier)
            text = empty_globals["codex"].read_text()
            self.assertLess(text.index("## Presentation"), text.index("## Staffing"))


if __name__ == "__main__":
    unittest.main()
