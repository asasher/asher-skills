#!/usr/bin/env python3
"""Per-owner global apply and whole-tree staffing-variant integration checks."""

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


def apply_owner(script: Path, module: Path, global_file: Path, *extra: object, **kw):
    return run(script, "apply", "--module", module, "--global-file", global_file, *extra, **kw)


def apply_presentation(provider: str, module: Path, global_file: Path, *extra: object, **kw):
    return apply_owner(PRESENTATION, module, global_file, "--provider", provider, *extra, **kw)


def section(data: bytes, heading: str) -> bytes:
    match = re.search(rf"(?m)^## {re.escape(heading)}\n", data.decode())
    if not match:
        return b""
    text = data.decode()
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
                    f"## Presentation\nold-presentation-{provider}\n\n"
                    f"## Tail\nkeep-tail-{provider}\n"
                )

            # Injected failure before any write leaves the global untouched.
            env = dict(os.environ)
            env["ASHER_SKILLS_FAIL_MODULE"] = "staffing:claude"
            before = globals_["claude"].read_bytes()
            failed = apply_owner(
                compiled["claude"] / "scripts" / "render-global.py",
                root / "modules" / "staffing" / "claude" / "module.md",
                globals_["claude"], ok=False, env=env,
            )
            self.assertIn("injected module apply failure", failed.stderr)
            self.assertEqual(globals_["claude"].read_bytes(), before)

            for provider in ("codex", "claude"):
                old_user = section(globals_[provider].read_bytes(), "User")
                old_staffing = section(globals_[provider].read_bytes(), "Staffing")
                apply_presentation(
                    provider, root / "modules" / "presentation" / provider / "module.md",
                    globals_[provider],
                )
                data = globals_[provider].read_bytes()
                self.assertEqual(section(data, "User"), old_user)
                self.assertEqual(section(data, "Staffing"), old_staffing)
                self.assertEqual(section(data, "Tail"), f"## Tail\nkeep-tail-{provider}\n".encode())

                presentation = section(globals_[provider].read_bytes(), "Presentation")
                apply_owner(
                    compiled[provider] / "scripts" / "render-global.py",
                    root / "modules" / "staffing" / provider / "module.md",
                    globals_[provider],
                )
                data = globals_[provider].read_bytes()
                self.assertEqual(section(data, "Presentation"), presentation)
                self.assertEqual(section(data, "User"), old_user)

            # Idempotent rerun: bytes and module inodes stable.
            first = {provider: path.read_bytes() for provider, path in globals_.items()}
            module_inodes = {
                path: path.stat().st_ino for path in (root / "modules").rglob("module.md")
            }
            for provider in ("codex", "claude"):
                apply_presentation(
                    provider, root / "modules" / "presentation" / provider / "module.md",
                    globals_[provider],
                )
                apply_owner(
                    compiled[provider] / "scripts" / "render-global.py",
                    root / "modules" / "staffing" / provider / "module.md",
                    globals_[provider],
                )
            self.assertEqual(
                {provider: path.read_bytes() for provider, path in globals_.items()}, first
            )
            self.assertEqual(
                {path: path.stat().st_ino for path in module_inodes}, module_inodes
            )

    def test_legacy_seeded_conventions_migrate_to_exact_compact_globals(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            compiled = {
                provider: materialize(provider, root / f"staffing-{provider}")
                for provider in ("codex", "claude")
            }
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
                apply_presentation(
                    provider, root / "modules" / "presentation" / provider / "module.md",
                    global_file,
                )
                apply_owner(
                    compiled[provider] / "scripts" / "render-global.py",
                    root / "modules" / "staffing" / provider / "module.md",
                    global_file,
                )

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

    def test_unowned_conventions_refuse_migration_and_empty_order_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            compiled = {
                provider: materialize(provider, root / f"staffing-{provider}")
                for provider in ("codex", "claude")
            }
            unowned = root / "unowned.md"
            unowned.write_text("# Personal rules\n\n## Conventions\nkeep me\n")
            before = unowned.read_bytes()
            denied = apply_presentation(
                "codex", root / "modules" / "presentation" / "codex" / "module.md",
                unowned, ok=False,
            )
            self.assertIn("unrecognized ## Conventions owner", denied.stderr)
            self.assertEqual(unowned.read_bytes(), before)

            # Empty file: whichever owner applies first, Presentation lands before Staffing.
            empty = root / "empty-codex.md"
            apply_owner(
                compiled["codex"] / "scripts" / "render-global.py",
                root / "modules" / "staffing" / "codex" / "module.md", empty,
            )
            apply_presentation(
                "codex", root / "modules" / "presentation" / "codex" / "module.md", empty,
            )
            text = empty.read_text()
            self.assertLess(text.index("## Presentation"), text.index("## Staffing"))

    def test_audited_module_content_lands_byte_for_byte(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            seed_module = root / "seed.md"
            seed_pointer = root / "pointer.md"
            run(PRESENTATION, "render", "--provider", "claude",
                "--module", seed_module, "--pointer", seed_pointer)
            audited = root / "audited.md"
            audited.write_bytes(
                seed_module.read_bytes()
                .replace(b"<owner>", b"Tester")
                .replace(b"<tailnet-root>", b"https://example.test")
            )
            global_file = root / "global.md"
            apply_presentation(
                "claude", root / "module-dest.md", global_file, "--audited", audited,
            )
            self.assertEqual((root / "module-dest.md").read_bytes(), audited.read_bytes())
            run(PRESENTATION, "check", "--provider", "claude",
                "--module", root / "module-dest.md", "--pointer", seed_pointer,
                "--audited", audited)
            drift = run(PRESENTATION, "check", "--provider", "claude",
                        "--module", root / "module-dest.md", "--pointer", seed_pointer,
                        ok=False)
            self.assertIn("mismatch: module", drift.stderr)


if __name__ == "__main__":
    unittest.main()
