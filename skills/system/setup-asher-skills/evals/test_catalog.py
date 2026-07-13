#!/usr/bin/env python3
"""Focused tests for the canonical skill catalog compiler."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/catalog.py"
SPEC = importlib.util.spec_from_file_location("skill_catalog", SCRIPT)
assert SPEC and SPEC.loader
catalog = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = catalog
SPEC.loader.exec_module(catalog)


def write_skill(
    root: Path,
    source: str,
    *,
    name: str | None = None,
    requires: tuple[str, ...] = (),
    optional: tuple[str, ...] = (),
    setup: bool = False,
) -> None:
    directory = root / "skills" / source
    directory.mkdir(parents=True, exist_ok=True)
    name = name or directory.name
    setup_line = "  setup: reference/setup.md\n" if setup else ""
    (directory / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        "description: fixture\n"
        "metadata:\n"
        "  invocation: model\n"
        "  execution: thread\n"
        f"  requires: [{', '.join(requires)}]\n"
        f"  optional: [{', '.join(optional)}]\n"
        f"{setup_line}"
        "---\n"
        + ("setup loads reference/setup.md\n" if setup else ""),
        encoding="utf-8",
    )
    if setup:
        (directory / "reference").mkdir()
        (directory / "reference/setup.md").write_text("# Setup\n", encoding="utf-8")


class CatalogTests(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        return temp, Path(temp.name)

    def test_live_snapshot_matches_sources(self) -> None:
        root = Path(__file__).parents[4]
        actual = catalog.compile_catalog(root)
        snapshot = root / "skills/system/setup-asher-skills/reference/catalog.json"
        self.assertEqual(actual, json.loads(snapshot.read_text()))

    def test_live_migration_map_and_root_catalog_match_sources(self) -> None:
        root = Path(__file__).parents[4]
        graph = catalog.discover(root)
        migration = json.loads((root / "skills/source-migration.json").read_text())["moves"]
        self.assertEqual(set(migration.values()), {skill.source for skill in graph.values()})
        self.assertEqual(set(migration), {f"skills/{name}" for name in graph})
        readme = (root / "README.md").read_text()
        for skill in graph.values():
            execution = skill.execution + (" (internal provenance hold)" if skill.internal else "")
            row = f"| {skill.category} | `{skill.name}` | {skill.invocation} | {execution} |"
            self.assertEqual(readme.count(row), 1, row)

    def test_no_stale_flat_source_paths_in_authoritative_surfaces(self) -> None:
        root = Path(__file__).parents[4]
        old_paths = json.loads((root / "skills/source-migration.json").read_text())["moves"]
        stale = []
        for path in root.rglob("*"):
            relative = path.relative_to(root)
            top = relative.parts[0]
            if (
                not path.is_file()
                or {".git", ".agents", ".claude"} & set(path.parts)
                or top in {"plans", "evidence"}
                or top.endswith("-workspace")
                or path.name == "source-migration.json"
            ):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for old in old_paths:
                if old + "/" in text:
                    stale.append(f"{path.relative_to(root)}: {old}/")
        self.assertEqual(stale, [])

    def test_discovers_flat_and_one_category_layer(self) -> None:
        temp, root = self.fixture()
        self.addCleanup(temp.cleanup)
        write_skill(root, "flat")
        write_skill(root, "delivery/nested")
        found = catalog.discover(root)
        self.assertIsNone(found["flat"].category)
        self.assertEqual(found["nested"].category, "delivery")

    def test_rejects_deeper_and_nested_public_identities(self) -> None:
        for sources in (("one/two/three",), ("parent", "parent/child")):
            with self.subTest(sources=sources):
                temp, root = self.fixture()
                try:
                    for source in sources:
                        write_skill(root, source)
                    with self.assertRaisesRegex(catalog.CatalogError, "flat or exactly one category"):
                        catalog.discover(root)
                finally:
                    temp.cleanup()

    def test_rejects_duplicate_names_and_missing_siblings(self) -> None:
        temp, root = self.fixture()
        self.addCleanup(temp.cleanup)
        write_skill(root, "a/same")
        write_skill(root, "b/same")
        with self.assertRaisesRegex(catalog.CatalogError, "duplicate skill name"):
            catalog.discover(root)

        temp2, root2 = self.fixture()
        self.addCleanup(temp2.cleanup)
        write_skill(root2, "only", requires=("missing",))
        with self.assertRaisesRegex(catalog.CatalogError, "missing sibling"):
            catalog.discover(root2)

    def test_rejects_required_cycle_and_broken_setup_pointer(self) -> None:
        temp, root = self.fixture()
        self.addCleanup(temp.cleanup)
        write_skill(root, "a", requires=("b",))
        write_skill(root, "b", requires=("a",))
        with self.assertRaisesRegex(catalog.CatalogError, r"a -> b -> a"):
            catalog.discover(root)

        temp2, root2 = self.fixture()
        self.addCleanup(temp2.cleanup)
        write_skill(root2, "owner", setup=True)
        (root2 / "skills/owner/reference/setup.md").unlink()
        with self.assertRaisesRegex(catalog.CatalogError, "shipped reference/setup.md"):
            catalog.discover(root2)

        temp3, root3 = self.fixture()
        self.addCleanup(temp3.cleanup)
        write_skill(root3, "owner", setup=True)
        skill = root3 / "skills/owner/SKILL.md"
        skill.write_text(skill.read_text().replace("setup loads reference/setup.md\n", ""))
        with self.assertRaisesRegex(catalog.CatalogError, "command surface does not route setup"):
            catalog.discover(root3)

    def test_required_closure_is_dependency_first_and_optional_is_explicit(self) -> None:
        temp, root = self.fixture()
        self.addCleanup(temp.cleanup)
        write_skill(root, "app", requires=("base",), optional=("extra",))
        write_skill(root, "base")
        write_skill(root, "extra", requires=("helper",))
        write_skill(root, "helper")
        graph = catalog.discover(root)
        without = catalog.resolve(graph, {"app"})
        self.assertEqual(without["closure"], ["app", "base"])
        self.assertEqual(without["setup_order"], ["base", "app"])
        with_present = catalog.resolve(graph, {"app"}, {"extra"})
        self.assertEqual(with_present["closure"], ["app", "base", "extra", "helper"])
        order = with_present["setup_order"]
        self.assertLess(order.index("base"), order.index("app"))
        self.assertLess(order.index("helper"), order.index("extra"))

    def test_rejects_cross_harness_invocation_mismatch(self) -> None:
        temp, root = self.fixture()
        self.addCleanup(temp.cleanup)
        write_skill(root, "alpha")
        agents = root / "skills/alpha/agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(
            "policy:\n  allow_implicit_invocation: false\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(catalog.CatalogError, "agents/openai.yaml"):
            catalog.discover(root)

    def test_internal_skill_is_cataloged_but_not_selectable(self) -> None:
        temp, root = self.fixture()
        self.addCleanup(temp.cleanup)
        write_skill(root, "held")
        skill = root / "skills/held/SKILL.md"
        skill.write_text(skill.read_text().replace("metadata:\n", "metadata:\n  internal: true\n"))
        graph = catalog.discover(root)
        self.assertTrue(graph["held"].internal)
        with self.assertRaisesRegex(catalog.CatalogError, "not installable"):
            catalog.resolve(graph, {"held"})

        write_skill(root, "public", optional=("held",))
        graph = catalog.discover(root)
        self.assertEqual(catalog.resolve(graph, {"public"}, {"held"})["closure"], ["public"])


if __name__ == "__main__":
    unittest.main()
