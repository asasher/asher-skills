#!/usr/bin/env python3
"""Offline acceptance selfcheck for codex-imagegen's spritesheet mode."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts/extract_spritesheet.py"
FIXTURE = SKILL_DIR / "evals/spritesheet-fixtures/iso-4x4.png"
MAKE_FIXTURE = SKILL_DIR / "evals/spritesheet_make_fixture.py"
NAMES = [
    "grass",
    "dirt",
    "stone",
    "sand",
    "water",
    "shoreline",
    "roads",
    "wood",
    "lava",
    "snow",
    "forest",
    "mountain",
    "farmland",
    "bridge",
    "cliff",
    "ice",
]


def import_extractor():
    sys.path.insert(0, str(SCRIPT.parent))
    spec = importlib.util.spec_from_file_location("extract_spritesheet", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ensure_fixture() -> None:
    if not FIXTURE.exists():
        subprocess.run([sys.executable, str(MAKE_FIXTURE)], check=True)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def asset_paths(manifest: dict, out_dir: Path) -> list[Path]:
    return [out_dir / element["asset"] for element in manifest["elements"]]


def run_extract(extractor, out_dir: Path, **kwargs) -> dict:
    params = {
        "source_path": FIXTURE,
        "out_dir": out_dir,
        "cols": 4,
        "rows": 4,
        "key": "auto",
        "names": NAMES,
    }
    params.update(kwargs)
    return extractor.extract(**params)


def check_ac4_cli_help() -> None:
    proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
    assert_true(proc.returncode == 0, proc.stderr)
    help_text = proc.stdout
    flags = [
        "--in",
        "--generate",
        "--out",
        "--slice",
        "--cols",
        "--rows",
        "--tile",
        "--margin",
        "--spacing",
        "--key",
        "--key-hi",
        "--key-lo",
        "--names",
        "--pad",
        "--format",
        "--anchor",
        "--validate",
        "--expect",
        "--contact-sheet",
        "--generator-cmd",
    ]
    missing = [flag for flag in flags if flag not in help_text]
    assert_true(not missing, "missing help flags: " + ", ".join(missing))


def check_ac2_grid(manifest: dict, out_dir: Path) -> None:
    paths = asset_paths(manifest, out_dir)
    assert_true(len(paths) == 16, f"expected 16 assets, got {len(paths)}")
    assert_true(all(path.exists() for path in paths), "not every manifest asset exists")
    assert_true(len(manifest["elements"]) == 16, "manifest element count is not 16")
    for index, element in enumerate(manifest["elements"]):
        assert_true(element["row"] == index // 4, f"row-major row mismatch at {index}")
        assert_true(element["col"] == index % 4, f"row-major col mismatch at {index}")
        assert_true(0 <= element["row"] <= 3 and 0 <= element["col"] <= 3, "row/col out of range")


def check_ac1_alpha_corners(manifest: dict, out_dir: Path) -> None:
    for path in asset_paths(manifest, out_dir):
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            width, height = rgba.size
            corners = [
                rgba.getpixel((0, 0))[3],
                rgba.getpixel((width - 1, 0))[3],
                rgba.getpixel((0, height - 1))[3],
                rgba.getpixel((width - 1, height - 1))[3],
            ]
            assert_true(corners == [0, 0, 0, 0], f"{path.name} corners are {corners}")


def check_ac5_manifest_schema(manifest: dict) -> None:
    top = {"mode", "artifact", "source", "sheet", "slicing", "key", "elements"}
    assert_true(top.issubset(manifest), "manifest missing top-level keys")
    assert_true(manifest["mode"] == "spritesheet", "manifest mode is not spritesheet")
    required = {
        "name",
        "index",
        "row",
        "col",
        "sheet_rect",
        "trimmed_bounds",
        "asset",
        "size",
        "anchor",
        "pivot",
        "css",
        "frame",
    }
    rect_keys = {"x", "y", "w", "h"}
    for element in manifest["elements"]:
        assert_true(required.issubset(element), f"{element.get('name')} missing element keys")
        assert_true("background-position" in element["css"], "missing css.background-position")
        assert_true(rect_keys.issubset(element["frame"]), "frame missing rect keys")
        assert_true(rect_keys.issubset(element["sheet_rect"]), "sheet_rect missing rect keys")
        assert_true(rect_keys.issubset(element["trimmed_bounds"]), "trimmed_bounds missing rect keys")


def check_trimmed_within_sheet_rect(manifest: dict) -> None:
    for element in manifest["elements"]:
        sheet = element["sheet_rect"]
        trim = element["trimmed_bounds"]
        assert_true(trim["x"] >= sheet["x"], f"{element['name']} trim x before sheet")
        assert_true(trim["y"] >= sheet["y"], f"{element['name']} trim y before sheet")
        assert_true(trim["x"] + trim["w"] <= sheet["x"] + sheet["w"], f"{element['name']} trim x overflows")
        assert_true(trim["y"] + trim["h"] <= sheet["y"] + sheet["h"], f"{element['name']} trim y overflows")


def check_ac3_non_destructive(extractor, out_dir: Path) -> None:
    before = file_hash(FIXTURE)
    rerun = run_extract(extractor, out_dir)
    assert_true(Path(rerun["artifact"]).name == f"{out_dir.name}-v2", "re-run did not create v2 artifact")
    after = file_hash(FIXTURE)
    assert_true(before == after, "source hash changed")


def check_ac7_key_modes(extractor, root: Path) -> None:
    explicit = run_extract(extractor, root / "explicit-key", key="#00FF00")
    assert_true(explicit["key"]["color"] == "#00FF00", "explicit key not recorded")
    assert_true(len(explicit["elements"]) == 16, "explicit key did not extract 16")
    none = run_extract(extractor, root / "no-key", key="none")
    assert_true(none["key"]["method"] == "none", "key none not recorded")
    assert_true(len(none["elements"]) == 16, "key none did not slice 16 cells")


def check_ac8_components(extractor, root: Path) -> None:
    manifest = extractor.extract(source_path=FIXTURE, out_dir=root / "components", slice_mode="components", key="auto")
    assert_true(len(manifest["elements"]) > 1, "components mode extracted <=1 element")


def check_ac9_naming_determinism(extractor, root: Path, first_manifest: dict, first_out: Path) -> None:
    assert_true((first_out / "assets/tile_01_grass.png").exists(), "tile_01_grass.png missing")
    second = run_extract(extractor, root / "determinism")
    left = [(e["name"], e["row"], e["col"], e["sheet_rect"], e["trimmed_bounds"]) for e in first_manifest["elements"]]
    right = [(e["name"], e["row"], e["col"], e["sheet_rect"], e["trimmed_bounds"]) for e in second["elements"]]
    assert_true(left == right, "element order or geometry changed across runs")


def check_ac10_webp(extractor, root: Path) -> None:
    webp = run_extract(extractor, root / "webp", export_format="webp")
    webp_paths = asset_paths(webp, root / "webp")
    assert_true(len(webp_paths) == 16 and all(path.suffix == ".webp" for path in webp_paths), "webp assets missing")
    with Image.open(webp_paths[0]) as image:
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A").getextrema()
        assert_true(alpha[0] == 0 and alpha[1] > 0, "webp alpha channel not preserved")
    both = run_extract(extractor, root / "both", export_format="both")
    pngs = sorted((root / "both/assets").glob("*.png"))
    webps = sorted((root / "both/assets").glob("*.webp"))
    assert_true(len(pngs) == 16 and len(webps) == 16, "format both did not write PNG and WebP")
    assert_true(all((root / "both" / element["asset"]).suffix == ".png" for element in both["elements"]), "both manifest should point to PNG")


def check_ac12_contact_sheet(extractor, root: Path) -> None:
    contact = root / "contact.png"
    run_extract(extractor, root / "contact-run", contact_sheet=contact)
    with Image.open(contact) as image:
        assert_true(image.size[0] > 0 and image.size[1] > 0, "contact sheet has invalid dimensions")


def check_ac14_generate_source(extractor, root: Path) -> None:
    stub = f"cp {shlex.quote(str(FIXTURE))} {{out}}"
    subject = "stubbed 4x4 isometric terrain sheet"
    manifest = extractor.extract(
        generate=subject,
        out_dir=root / "generated",
        cols=4,
        rows=4,
        key="auto",
        names=NAMES,
        generator_cmd=stub,
    )
    source = manifest["source"]
    assert_true(isinstance(source, dict), "generated source should be an object")
    assert_true(source.get("generated") is True, "source.generated not true")
    assert_true(source.get("subject") == subject, "generated subject not recorded")
    assert_true(len(manifest["elements"]) == 16, "generated pipeline did not extract 16")

    relative = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--generate",
            subject,
            "--out",
            "relative-generated",
            "--cols",
            "4",
            "--rows",
            "4",
            "--key",
            "auto",
            "--generator-cmd",
            stub,
        ],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert_true(relative.returncode == 0, relative.stderr + relative.stdout)
    assert_true(
        (root / "relative-generated/source/generated-source.png").exists(),
        "relative --generate output escaped the caller working directory",
    )
    try:
        extractor.extract(
            generate="this should fail",
            out_dir=root / "generated-fail",
            cols=4,
            rows=4,
            key="auto",
            generator_cmd="missing_to_sprites_generator {subject} {out}",
        )
    except extractor.GenerationError as exc:
        assert_true("generator command failed" in str(exc), "bogus generator failed unclearly")
    else:
        raise AssertionError("bogus generator command did not fail")


def check_ac6_validate(extractor, root: Path) -> None:
    extractor.extract(source_path=FIXTURE, out_dir=root / "validate-api", cols=4, rows=4, key="auto", validate=True, expect=16)
    try:
        extractor.extract(source_path=FIXTURE, out_dir=root / "validate-api-bad", cols=4, rows=4, key="auto", validate=True, expect=99)
    except extractor.ValidationError:
        pass
    else:
        raise AssertionError("bad expected count did not raise ValidationError")

    good = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--in",
            str(FIXTURE),
            "--out",
            str(root / "validate-cli"),
            "--cols",
            "4",
            "--rows",
            "4",
            "--key",
            "auto",
            "--validate",
            "--expect",
            "16",
        ],
        capture_output=True,
        text=True,
    )
    assert_true(good.returncode == 0, good.stderr + good.stdout)
    bad = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--in",
            str(FIXTURE),
            "--out",
            str(root / "validate-cli-bad"),
            "--cols",
            "4",
            "--rows",
            "4",
            "--key",
            "auto",
            "--validate",
            "--expect",
            "99",
        ],
        capture_output=True,
        text=True,
    )
    assert_true(bad.returncode != 0, "bad CLI validation exited 0")


def check_ac11_prompts_doc() -> None:
    text = (SKILL_DIR / "reference/spritesheet-prompts.md").read_text()
    for phrase in ["flat key background", "consistent scale", "isolated non-touching"]:
        assert_true(phrase in text, f"prompts doc missing {phrase!r}")


def check_ac13_codex_surface() -> None:
    text = (SKILL_DIR / "agents/openai.yaml").read_text()
    assert_true('display_name: "Codex Imagegen"' in text, "display_name missing")
    assert_true("allow_implicit_invocation: true" in text, "implicit invocation policy wrong")


def main() -> int:
    ensure_fixture()
    extractor = import_extractor()
    failures: list[str] = []

    def run(label: str, func) -> None:
        try:
            func()
        except Exception as exc:  # noqa: BLE001 - this script reports every failed acceptance check.
            failures.append(label)
            print(f"FAIL {label}: {exc}")
        else:
            print(f"PASS {label}")

    with tempfile.TemporaryDirectory(prefix="codex-imagegen-spritesheet-") as tmp:
        root = Path(tmp)
        base_out = root / "base"
        base_manifest = run_extract(extractor, base_out)

        run("ac-1 keyed source exports transparent-corner PNG assets", lambda: check_ac1_alpha_corners(base_manifest, base_out))
        run("ac-2 regular 4x4 grid exports 16 row-major assets", lambda: check_ac2_grid(base_manifest, base_out))
        run("ac-3 re-run versions the artifact and preserves source bytes", lambda: check_ac3_non_destructive(extractor, base_out))
        run("ac-4 CLI help documents every flag", check_ac4_cli_help)
        run("ac-5 manifest schema is complete", lambda: check_ac5_manifest_schema(base_manifest))
        run("ac-5 sanity trimmed_bounds stay within sheet_rect", lambda: check_trimmed_within_sheet_rect(base_manifest))
        run("ac-6 validation passes expected count and fails wrong count", lambda: check_ac6_validate(extractor, root))
        run("ac-7 auto explicit hex and none key modes work", lambda: check_ac7_key_modes(extractor, root))
        run("ac-8 components mode extracts multiple blobs", lambda: check_ac8_components(extractor, root))
        run("ac-9 naming and ordering are deterministic", lambda: check_ac9_naming_determinism(extractor, root, base_manifest, base_out))
        run("ac-10 webp and both formats preserve alpha", lambda: check_ac10_webp(extractor, root))
        run("ac-11 prompt guidance is documented", check_ac11_prompts_doc)
        run("ac-12 contact sheet writes a valid PNG", lambda: check_ac12_contact_sheet(extractor, root))
        run("ac-13 Codex openai.yaml surface is present", check_ac13_codex_surface)
        run("ac-14 generate-source handoff records provenance and fails cleanly", lambda: check_ac14_generate_source(extractor, root))

        manifest_path = base_out / "spritesheet.json"
        assert_true(json.loads(manifest_path.read_text()) == base_manifest, "manifest file differs from returned dict")

    if failures:
        print(f"FAILURES: {len(failures)}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
