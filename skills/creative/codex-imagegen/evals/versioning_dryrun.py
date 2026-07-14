#!/usr/bin/env python3
"""Exercise codex-imagegen's non-destructive output contract without a live generation."""

import base64
from io import BytesIO
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile


SKILL_DIR = Path(__file__).resolve().parents[1]
IMAGEGEN = SKILL_DIR / "scripts" / "codex_imagegen.py"
CHROMA_KEY = SKILL_DIR / "scripts" / "chroma_key.py"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def run(command, *, env=None):
    proc = subprocess.run(command, capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise AssertionError(
            f"command failed ({proc.returncode}): {' '.join(map(str, command))}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def install_codex_stub(bin_dir, home):
    try:
        from PIL import Image
    except ImportError as exc:
        raise AssertionError("Pillow is required to build the image-generation stub") from exc

    stub = bin_dir / "codex"
    session = home / ".codex" / "sessions" / "stub" / "session.jsonl"
    image = Image.new("RGB", (256, 256), "#ff00ff")
    rng = random.Random(42)
    pixels = image.load()
    for y in range(48, 208):
        for x in range(48, 208):
            pixels[x, y] = (rng.randrange(20, 235), rng.randrange(20, 235), rng.randrange(20, 235))
    buffer = BytesIO()
    image.save(buffer, "PNG")
    png = buffer.getvalue()
    check(len(png) > 8_000, "stub PNG is too small for transcript candidate detection")
    payload = json.dumps(
        {
            "type": "image_generation_call",
            "revised_prompt": "oak tree generated image",
            "result": base64.b64encode(png).decode("ascii"),
        }
    )
    stub.write_text(
        f"#!{sys.executable}\n"
        "import os\n"
        "from pathlib import Path\n"
        "if os.environ.get('CODEX_STUB_NO_IMAGE'):\n    raise SystemExit(1)\n"
        f"session = Path({str(session)!r})\n"
        "session.parent.mkdir(parents=True, exist_ok=True)\n"
        f"with session.open('a', encoding='utf-8') as handle:\n    handle.write({payload!r} + '\\n')\n",
        encoding="utf-8",
    )
    stub.chmod(0o755)


def exercise_generation(root):
    home = root / "home"
    bin_dir = root / "bin"
    bin_dir.mkdir()
    install_codex_stub(bin_dir, home)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"

    asset_dir = root / "assets"
    asset_dir.mkdir()
    fresh = asset_dir / "fresh-oak-tree.png"
    fresh_run = run(
        [sys.executable, str(IMAGEGEN), "--subject", "oak tree", "--out", str(fresh)],
        env=env,
    )
    check(fresh.exists(), "first generation did not use the requested path")
    check("fresh-oak-tree.png" in fresh_run.stdout, "first generation did not report its path")

    output = asset_dir / "oak-tree.png"
    original = b"original-expensive-image"
    output.write_bytes(original)

    first = run(
        [sys.executable, str(IMAGEGEN), "--subject", "oak tree", "--out", str(output)],
        env=env,
    )
    check(output.read_bytes() == original, "single generation overwrote the requested output")
    check((output.parent / "oak-tree-v2.png").exists(), "single generation did not create v2")
    check("oak-tree-v2.png" in first.stdout, "single generation did not report its actual path")

    second = run(
        [sys.executable, str(IMAGEGEN), "--subject", "oak tree", "--out", str(output)],
        env=env,
    )
    check(output.read_bytes() == original, "second generation overwrote the original")
    check((output.parent / "oak-tree-v2.png").exists(), "second generation lost v2")
    check((output.parent / "oak-tree-v3.png").exists(), "second generation did not create v3")
    check("oak-tree-v3.png" in second.stdout, "second generation did not report its actual path")

    batch_dir = root / "batch"
    batch_dir.mkdir()
    batch_original = batch_dir / "oak-tree.png"
    batch_original.write_bytes(b"incomplete-but-preserved")
    batch_file = root / "batch.json"
    batch_file.write_text(
        json.dumps([{"name": "oak-tree", "subject": "oak tree"}]),
        encoding="utf-8",
    )
    batch_run = [
        sys.executable,
        str(IMAGEGEN),
        "--batch",
        str(batch_file),
        "--outdir",
        str(batch_dir),
    ]
    run(batch_run, env=env)
    check(batch_original.read_bytes() == b"incomplete-but-preserved", "batch overwrote an existing file")
    check((batch_dir / "oak-tree-v2.png").exists(), "batch did not preserve regeneration as v2")

    resumed = run(batch_run, env=env)
    check("SKIP oak-tree" in resumed.stdout, "batch did not resume from the latest completed version")
    check(not (batch_dir / "oak-tree-v3.png").exists(), "batch resume generated an unnecessary version")

    run(
        [
            *batch_run,
            "--new-version",
        ],
        env=env,
    )
    check((batch_dir / "oak-tree-v3.png").exists(), "batch iteration did not create v3")

    scene_flat = asset_dir / "scene.png"
    scene_flat.write_bytes(b"original-flat-scene")
    scene_file = root / "scene.json"
    scene_file.write_text(
        json.dumps(
            {
                "size": 256,
                "art_direction": "storybook game art",
                "layers": [
                    {"name": "background", "role": "background", "subject": "forest clearing"},
                    {"name": "oak tree", "role": "subject", "subject": "large oak tree"},
                ],
            }
        ),
        encoding="utf-8",
    )
    layered = run(
        [sys.executable, str(IMAGEGEN), "--layers", str(scene_file), "--out", str(asset_dir / "scene")],
        env=env,
    )
    scene_dir = asset_dir / "scene-v2"
    check(scene_dir.is_dir(), "layered mode did not share the flat scene version family")
    manifest = json.loads((scene_dir / "manifest.json").read_text())
    check(manifest["status"] == "complete", "layered manifest is not complete")
    check(len(manifest["layers"]) == 2, "layered artifact did not record both layers")
    check((scene_dir / "composite.png").exists(), "layered artifact has no derived composite")
    check("scene-v2" in layered.stdout, "layered mode did not report the actual artifact directory")

    failed_scene = root / "failed-scene.json"
    failed_scene.write_text(scene_file.read_text(), encoding="utf-8")
    session = home / ".codex/sessions/stub/session.jsonl"
    os.utime(session, (1, 1))
    failed_env = env.copy()
    failed_env["CODEX_STUB_NO_IMAGE"] = "1"
    failed = subprocess.run(
        [sys.executable, str(IMAGEGEN), "--layers", str(failed_scene), "--out", str(asset_dir / "failed-scene")],
        capture_output=True,
        text=True,
        env=failed_env,
    )
    check(failed.returncode != 0, "layered generation failure exited successfully")
    failed_manifest = json.loads((asset_dir / "failed-scene/manifest.json").read_text())
    check(failed_manifest["status"] == "failed", "layered failure did not mark its manifest failed")
    check(not (asset_dir / "failed-scene/composite.png").exists(), "failed layered run wrote a composite")

    invalid_scene = root / "invalid-scene.json"
    invalid_scene.write_text(
        json.dumps({"layers": [{"name": "bad", "subject": "bad", "anchor": "unsupported"}]}),
        encoding="utf-8",
    )
    invalid = subprocess.run(
        [sys.executable, str(IMAGEGEN), "--layers", str(invalid_scene), "--out", str(asset_dir / "invalid-scene")],
        capture_output=True,
        text=True,
        env=env,
    )
    check(invalid.returncode != 0, "invalid layered plan exited successfully")
    check(not (asset_dir / "invalid-scene").exists(), "invalid layered plan reserved an artifact")

    third = run(
        [sys.executable, str(IMAGEGEN), "--subject", "new scene", "--out", str(scene_flat)],
        env=env,
    )
    check((asset_dir / "scene-v3.png").exists(), "flat mode ignored a layered sibling version")
    check("scene-v3.png" in third.stdout, "flat mode did not report the shared-family version")


def exercise_chroma_key(root):
    try:
        from PIL import Image
    except ImportError as exc:
        raise AssertionError("Pillow is required to drive chroma_key.py") from exc

    source = root / "keyed.png"
    Image.new("RGB", (8, 8), "#ff00ff").save(source)
    output = root / "transparent.png"
    original = b"original-transparent-image"
    output.write_bytes(original)

    proc = run([sys.executable, str(CHROMA_KEY), str(source), str(output), "--key", "magenta"])
    check(output.read_bytes() == original, "chroma-key conversion overwrote the requested output")
    versioned = root / "transparent-v2.png"
    check(versioned.exists(), "chroma-key conversion did not create v2")
    check("transparent-v2.png" in proc.stdout, "chroma-key conversion did not report its actual path")
    with Image.open(versioned) as image:
        check(image.mode == "RGBA", "versioned chroma-key output is not RGBA")


def main():
    with tempfile.TemporaryDirectory(prefix="codex-imagegen-versioning-") as tmp:
        root = Path(tmp)
        exercise_generation(root)
        exercise_chroma_key(root)
    print("PASS versioned outputs preserve every earlier image")


if __name__ == "__main__":
    main()
