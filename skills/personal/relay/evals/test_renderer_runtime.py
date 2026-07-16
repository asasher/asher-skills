#!/usr/bin/env python3
"""Run the pinned consumer-local React Email renderer in an isolated repository."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SETUP = SKILL / "scripts" / "setup_instance.py"


class RendererRuntimeTests(unittest.TestCase):
    def test_project_and_digest_render_html_text_and_forced_themes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath(".git").mkdir()
            setup = subprocess.run(["python3", str(SETUP), str(root)], capture_output=True, text=True, check=False)
            self.assertEqual(setup.returncode, 0, setup.stdout + setup.stderr)
            instance = root / "relay"
            modules = os.environ.get("RELAY_NODE_MODULES")
            if modules:
                instance.joinpath("node_modules").symlink_to(Path(modules).resolve(), target_is_directory=True)
            else:
                install = subprocess.run(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"], cwd=instance, capture_output=True, text=True, timeout=180, check=False)
                self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            for fixture in ("project-update", "internal-digest"):
                out = instance / "runs" / f"fixture-{fixture}"
                command = [str(instance / "node_modules" / ".bin" / "tsx"), str(instance / "scripts" / "render-email.tsx"), "--bag", str(instance / "templates" / "fixtures" / f"{fixture}.json"), "--out", str(out)]
                result = subprocess.run(command, cwd=instance, capture_output=True, text=True, timeout=60, check=False)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                files = {name: (out / name).read_text(encoding="utf-8") for name in ("rendered-email.html", "rendered-email.txt", "rendered-email-light.html", "rendered-email-dark.html")}
                self.assertIn('class="light-preview"', files["rendered-email-light.html"])
                self.assertIn('class="dark-preview"', files["rendered-email-dark.html"])
                self.assertIn("color-scheme", files["rendered-email.html"])
                self.assertNotIn("Dunn Harland", "".join(files.values()))
                bag = json.loads((instance / "templates" / "fixtures" / f"{fixture}.json").read_text())
                for visible in [bag["subject"], bag["summary"], *[section["title"] for section in bag["sections"]], *[item["title"] for section in bag["sections"] for item in section["items"]], *[item["detail"] for section in bag["sections"] for item in section["items"]]]:
                    self.assertIn(visible, files["rendered-email.html"])
                    self.assertIn(visible.casefold(), files["rendered-email.txt"].casefold())


if __name__ == "__main__":
    unittest.main()
