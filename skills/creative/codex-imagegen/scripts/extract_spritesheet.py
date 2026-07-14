#!/usr/bin/env python3
"""Extract keyed sprite sheets into transparent assets and spritesheet.json.

The module exposes extract(...) for tests and automation, and a documented
argparse CLI for direct use.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from image_key import key_image
from output_paths import next_output_path, reserve_output_dir


DEFAULT_GENERATOR_CMD = (
    "python3 {imagegen} --subject {subject} --key magenta --out {out}"
)
ALPHA_THRESHOLD = 10


class SpriteExtractionError(RuntimeError):
    """Base error for extraction failures."""


class OutputExistsError(SpriteExtractionError):
    """Raised when an internal write would collide inside a reserved artifact."""


class GenerationError(SpriteExtractionError):
    """Raised when --generate cannot produce a source sheet."""


class ValidationError(SpriteExtractionError):
    """Raised when --validate checks fail."""

    def __init__(self, report: dict):
        self.report = report
        failures = [check["name"] for check in report["checks"] if not check["ok"]]
        super().__init__("validation failed: " + ", ".join(failures))


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    w: int
    h: int

    @property
    def right(self) -> int:
        return self.x + self.w

    @property
    def bottom(self) -> int:
        return self.y + self.h

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "w": self.w, "h": self.h}


@dataclass
class Element:
    index: int
    row: int
    col: int
    base_name: str
    sheet_rect: Rect
    trimmed_bounds: Rect
    image: Image.Image
    asset_rel: str = ""


def _as_path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    return Path(value).expanduser()


def _parse_pair(text: str | Sequence[int], flag: str) -> tuple[int, int]:
    if isinstance(text, (tuple, list)):
        if len(text) != 2:
            raise ValueError(f"{flag} expects two integers")
        return int(text[0]), int(text[1])
    parts = str(text).split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"{flag} must be X,Y")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{flag} must be X,Y integers") from exc


def _parse_size(text: str | Sequence[int] | None) -> tuple[int, int] | None:
    if text is None:
        return None
    if isinstance(text, (tuple, list)):
        if len(text) != 2:
            raise ValueError("--tile expects two integers")
        return int(text[0]), int(text[1])
    match = re.fullmatch(r"\s*(\d+)x(\d+)\s*", str(text), re.IGNORECASE)
    if not match:
        raise argparse.ArgumentTypeError("--tile must be WxH, for example 256x256")
    return int(match.group(1)), int(match.group(2))


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip()).strip("-")
    return cleaned or "sprite"


def _load_names(names: str | Sequence[str] | None) -> list[str]:
    if names is None:
        return []
    if isinstance(names, (list, tuple)):
        return [_slug(str(item)) for item in names if str(item).strip()]
    value = str(names)
    path = Path(value).expanduser()
    if path.exists() and path.is_file():
        return [_slug(line.strip()) for line in path.read_text().splitlines() if line.strip()]
    return [_slug(part.strip()) for part in value.split(",") if part.strip()]


def _content_bounds(arr: np.ndarray, origin_x: int, origin_y: int) -> Rect | None:
    ys, xs = np.where(arr[..., 3] > ALPHA_THRESHOLD)
    if len(xs) == 0:
        return None
    x0 = int(xs.min())
    x1 = int(xs.max()) + 1
    y0 = int(ys.min())
    y1 = int(ys.max()) + 1
    return Rect(origin_x + x0, origin_y + y0, x1 - x0, y1 - y0)


def _expand_rect(rect: Rect, pad: int, limit: Rect) -> Rect:
    x0 = max(limit.x, rect.x - pad)
    y0 = max(limit.y, rect.y - pad)
    x1 = min(limit.right, rect.right + pad)
    y1 = min(limit.bottom, rect.bottom + pad)
    return Rect(x0, y0, max(0, x1 - x0), max(0, y1 - y0))


def _grid_rects(
    width: int,
    height: int,
    cols: int | None,
    rows: int | None,
    tile: tuple[int, int] | None,
    margin: tuple[int, int],
    spacing: tuple[int, int],
) -> tuple[list[tuple[int, int, Rect]], int, int, tuple[int, int]]:
    margin_x, margin_y = margin
    spacing_x, spacing_y = spacing
    if min(margin_x, margin_y, spacing_x, spacing_y) < 0:
        raise SpriteExtractionError("--margin and --spacing must be non-negative")

    if tile is None:
        if cols is None or rows is None:
            raise SpriteExtractionError("grid slicing requires --cols and --rows, or --tile")
        usable_w = width - margin_x - spacing_x * (cols - 1)
        usable_h = height - margin_y - spacing_y * (rows - 1)
        tile = (usable_w // cols, usable_h // rows)
    else:
        tile_w, tile_h = tile
        if cols is None:
            cols = max(0, (width - margin_x + spacing_x) // (tile_w + spacing_x))
        if rows is None:
            rows = max(0, (height - margin_y + spacing_y) // (tile_h + spacing_y))

    if cols <= 0 or rows <= 0 or tile[0] <= 0 or tile[1] <= 0:
        raise SpriteExtractionError("grid dimensions must be positive")

    rects: list[tuple[int, int, Rect]] = []
    tile_w, tile_h = tile
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * (tile_w + spacing_x)
            y = margin_y + row * (tile_h + spacing_y)
            if x >= width or y >= height:
                continue
            rects.append((row, col, Rect(x, y, min(tile_w, width - x), min(tile_h, height - y))))
    return rects, cols, rows, tile


class _UnionFind:
    def __init__(self) -> None:
        self.parent = [0]

    def make(self) -> int:
        label = len(self.parent)
        self.parent.append(label)
        return label

    def find(self, label: int) -> int:
        root = label
        while self.parent[root] != root:
            root = self.parent[root]

        while self.parent[label] != label:
            parent = self.parent[label]
            self.parent[label] = root
            label = parent
        return root

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            if ra < rb:
                self.parent[rb] = ra
            else:
                self.parent[ra] = rb


def _connected_component_bboxes(mask: np.ndarray) -> list[Rect]:
    opaque = np.asarray(mask, dtype=bool)
    height, _ = opaque.shape
    uf = _UnionFind()
    prev_runs: list[tuple[int, int, int]] = []
    runs: list[tuple[int, int, int, int]] = []

    for y in range(height):
        edges = np.diff(opaque[y].astype(np.int8), prepend=0, append=0)
        starts = np.flatnonzero(edges == 1).tolist()
        ends = np.flatnonzero(edges == -1).tolist()
        current_runs: list[tuple[int, int, int]] = []
        prev_index = 0

        for start, end in zip(starts, ends):
            label = uf.make()
            current_runs.append((start, end, label))
            runs.append((y, start, end, label))

            while prev_index < len(prev_runs) and prev_runs[prev_index][1] <= start:
                prev_index += 1
            overlap_index = prev_index
            while overlap_index < len(prev_runs) and prev_runs[overlap_index][0] < end:
                _, prev_end, prev_label = prev_runs[overlap_index]
                if prev_end > start:
                    uf.union(label, prev_label)
                overlap_index += 1
        prev_runs = current_runs

    boxes: dict[int, list[int]] = {}
    for y, start, end, label in runs:
        root = uf.find(label)
        if root not in boxes:
            boxes[root] = [start, y, end, y + 1]
        else:
            box = boxes[root]
            box[0] = min(box[0], start)
            box[1] = min(box[1], y)
            box[2] = max(box[2], end)
            box[3] = max(box[3], y + 1)
    return [Rect(x0, y0, x1 - x0, y1 - y0) for x0, y0, x1, y1 in boxes.values()]


def _order_component_rects(rects: list[Rect]) -> list[tuple[int, int, Rect]]:
    if not rects:
        return []
    sorted_rects = sorted(rects, key=lambda rect: (rect.y + rect.h / 2.0, rect.x))
    median_h = float(np.median([rect.h for rect in sorted_rects]))
    threshold = max(8.0, median_h * 0.65)
    rows: list[dict] = []
    for rect in sorted_rects:
        center = rect.y + rect.h / 2.0
        target = None
        for row in rows:
            if abs(center - row["center"]) <= threshold:
                target = row
                break
        if target is None:
            rows.append({"center": center, "rects": [rect]})
        else:
            target["rects"].append(rect)
            target["center"] = sum(r.y + r.h / 2.0 for r in target["rects"]) / len(target["rects"])

    ordered: list[tuple[int, int, Rect]] = []
    for row_index, row in enumerate(sorted(rows, key=lambda item: item["center"])):
        for col_index, rect in enumerate(sorted(row["rects"], key=lambda item: item.x)):
            ordered.append((row_index, col_index, rect))
    return ordered


def _asset_base_name(index: int, total: int, names: Sequence[str]) -> str:
    width = max(2, len(str(total)))
    prefix = f"tile_{index + 1:0{width}d}"
    if index < len(names) and names[index]:
        return f"{prefix}_{names[index]}"
    return prefix


def _slice_grid(
    keyed: Image.Image,
    cols: int | None,
    rows: int | None,
    tile: tuple[int, int] | None,
    margin: tuple[int, int],
    spacing: tuple[int, int],
    pad: int,
    names: Sequence[str],
) -> tuple[list[Element], dict, list[dict]]:
    width, height = keyed.size
    rects, cols, rows, tile = _grid_rects(width, height, cols, rows, tile, margin, spacing)
    elements: list[Element] = []
    empty_cells: list[dict] = []
    total = len(rects)

    for row, col, cell in rects:
        crop = keyed.crop((cell.x, cell.y, cell.right, cell.bottom))
        arr = np.asarray(crop, dtype=np.uint8)
        bounds = _content_bounds(arr, cell.x, cell.y)
        if bounds is None:
            empty_cells.append({"row": row, "col": col, "sheet_rect": cell.to_dict()})
            continue
        sheet_rect = _expand_rect(bounds, pad, cell)
        image = keyed.crop((sheet_rect.x, sheet_rect.y, sheet_rect.right, sheet_rect.bottom))
        index = len(elements)
        elements.append(
            Element(
                index=index,
                row=row,
                col=col,
                base_name=_asset_base_name(index, total, names),
                sheet_rect=sheet_rect,
                trimmed_bounds=bounds,
                image=image,
            )
        )

    slicing = {
        "mode": "grid",
        "cols": cols,
        "rows": rows,
        "tile": [tile[0], tile[1]],
        "margin": [margin[0], margin[1]],
        "spacing": [spacing[0], spacing[1]],
    }
    return elements, slicing, empty_cells


def _slice_components(
    keyed: Image.Image,
    pad: int,
    names: Sequence[str],
) -> tuple[list[Element], dict, list[dict]]:
    arr = np.asarray(keyed, dtype=np.uint8)
    rects = _connected_component_bboxes(arr[..., 3] > ALPHA_THRESHOLD)
    ordered = _order_component_rects(rects)
    sheet_limit = Rect(0, 0, keyed.size[0], keyed.size[1])
    elements: list[Element] = []
    total = len(ordered)

    for index, (row, col, bounds) in enumerate(ordered):
        sheet_rect = _expand_rect(bounds, pad, sheet_limit)
        image = keyed.crop((sheet_rect.x, sheet_rect.y, sheet_rect.right, sheet_rect.bottom))
        elements.append(
            Element(
                index=index,
                row=row,
                col=col,
                base_name=_asset_base_name(index, total, names),
                sheet_rect=sheet_rect,
                trimmed_bounds=bounds,
                image=image,
            )
        )

    slicing = {
        "mode": "components",
        "cols": max((element.col for element in elements), default=-1) + 1,
        "rows": max((element.row for element in elements), default=-1) + 1,
        "tile": None,
        "margin": [0, 0],
        "spacing": [0, 0],
    }
    return elements, slicing, []


def _anchor(size: tuple[int, int], mode: str) -> tuple[list[int], list[float]]:
    width, height = size
    if mode == "bottom-center":
        return [width // 2, height], [0.5, 1.0]
    if mode == "center":
        return [width // 2, height // 2], [0.5, 0.5]
    if mode == "top-left":
        return [0, 0], [0.0, 0.0]
    raise SpriteExtractionError("--anchor must be bottom-center, center, or top-left")


def _planned_output_paths(
    out_dir: Path,
    elements: Sequence[Element],
    export_format: str,
    contact_sheet: Path | None,
) -> list[Path]:
    paths = [out_dir / "spritesheet.json"]
    assets_dir = out_dir / "assets"
    for element in elements:
        if export_format in ("png", "both"):
            paths.append(assets_dir / f"{element.base_name}.png")
        if export_format in ("webp", "both"):
            paths.append(assets_dir / f"{element.base_name}.webp")
    if contact_sheet is not None:
        paths.append(contact_sheet)
    return paths


def _ensure_writable_outputs(paths: Iterable[Path], source_path: Path, force: bool) -> None:
    source_resolved = source_path.resolve()
    existing: list[str] = []
    for path in paths:
        resolved = path.resolve() if path.exists() else path.absolute()
        if resolved == source_resolved:
            raise OutputExistsError(f"refusing to write output over source: {path}")
        if path.exists() and not force:
            existing.append(str(path))
    if existing:
        raise OutputExistsError(
            "refusing to overwrite existing output files inside the reserved artifact: "
            + ", ".join(existing[:8])
            + (" ..." if len(existing) > 8 else "")
        )


def _write_assets(out_dir: Path, elements: Sequence[Element], export_format: str) -> None:
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    for element in elements:
        if export_format in ("png", "both"):
            path = assets_dir / f"{element.base_name}.png"
            element.image.save(path, "PNG")
            if not element.asset_rel:
                element.asset_rel = path.relative_to(out_dir).as_posix()
        if export_format in ("webp", "both"):
            path = assets_dir / f"{element.base_name}.webp"
            element.image.save(path, "WEBP", lossless=True)
            if not element.asset_rel:
                element.asset_rel = path.relative_to(out_dir).as_posix()


def _element_manifest(element: Element, anchor_mode: str) -> dict:
    width, height = element.image.size
    anchor, pivot = _anchor((width, height), anchor_mode)
    sheet_rect = element.sheet_rect.to_dict()
    return {
        "name": element.base_name,
        "index": element.index,
        "row": element.row,
        "col": element.col,
        "sheet_rect": sheet_rect,
        "trimmed_bounds": element.trimmed_bounds.to_dict(),
        "asset": element.asset_rel,
        "size": [width, height],
        "anchor": anchor,
        "pivot": pivot,
        "css": {
            "background-position": f"-{element.sheet_rect.x}px -{element.sheet_rect.y}px",
            "width": width,
            "height": height,
        },
        "frame": sheet_rect,
    }


def _checkerboard(size: tuple[int, int], block: int = 12) -> Image.Image:
    width, height = size
    base = Image.new("RGBA", size, (236, 236, 236, 255))
    draw = ImageDraw.Draw(base)
    for y in range(0, height, block):
        for x in range(0, width, block):
            if (x // block + y // block) % 2:
                draw.rectangle((x, y, x + block - 1, y + block - 1), fill=(204, 204, 204, 255))
    return base


def _write_contact_sheet(path: Path, elements: Sequence[Element]) -> None:
    if not elements:
        Image.new("RGBA", (128, 64), (255, 255, 255, 0)).save(path, "PNG")
        return
    font = ImageFont.load_default()
    max_w = max(element.image.size[0] for element in elements)
    max_h = max(element.image.size[1] for element in elements)
    label_h = 18
    padding = 12
    cols = max(1, math.ceil(math.sqrt(len(elements))))
    rows = math.ceil(len(elements) / cols)
    cell_w = max_w + padding * 2
    cell_h = max_h + label_h + padding * 2
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(sheet)

    for i, element in enumerate(elements):
        col = i % cols
        row = i // cols
        x0 = col * cell_w
        y0 = row * cell_h
        board = _checkerboard((cell_w, cell_h - label_h))
        sheet.alpha_composite(board, (x0, y0))
        ix = x0 + (cell_w - element.image.size[0]) // 2
        iy = y0 + padding
        sheet.alpha_composite(element.image, (ix, iy))
        draw.rectangle((x0, y0 + cell_h - label_h, x0 + cell_w, y0 + cell_h), fill=(32, 32, 32, 255))
        label = element.base_name
        draw.text((x0 + 4, y0 + cell_h - label_h + 3), label, fill=(255, 255, 255, 255), font=font)

    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(path, "PNG")


def _validate(
    manifest: dict,
    out_dir: Path,
    expect: int | None,
    empty_cells: Sequence[dict],
    key_rgb: tuple[int, int, int] | None,
    key_lo: float,
) -> dict:
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    elements = manifest["elements"]
    if expect is None:
        add("asset-count", len(elements) > 0, f"{len(elements)} element(s) extracted")
    else:
        add("asset-count", len(elements) == expect, f"expected {expect}, got {len(elements)}")

    add("empty-cells", len(empty_cells) == 0, f"{len(empty_cells)} empty cell(s)")

    alpha_failures: list[str] = []
    remnant_failures: list[str] = []
    for element in elements:
        asset_path = out_dir / element["asset"]
        with Image.open(asset_path) as image:
            rgba = image.convert("RGBA")
            width, height = rgba.size
            corners = [
                rgba.getpixel((0, 0))[3],
                rgba.getpixel((width - 1, 0))[3],
                rgba.getpixel((0, height - 1))[3],
                rgba.getpixel((width - 1, height - 1))[3],
            ]
            if any(alpha != 0 for alpha in corners):
                alpha_failures.append(element["name"])
            if key_rgb is not None:
                arr = np.asarray(rgba, dtype=np.float32)
                opaque = arr[..., 3] > ALPHA_THRESHOLD
                if np.any(opaque):
                    dist = np.linalg.norm(arr[..., :3] - np.asarray(key_rgb, dtype=np.float32), axis=2)
                    remnants = np.count_nonzero(opaque & (dist <= max(key_lo, 1.0)))
                    if remnants:
                        remnant_failures.append(f"{element['name']}:{remnants}")

    add("alpha-corners", not alpha_failures, "all corners transparent" if not alpha_failures else ", ".join(alpha_failures))
    add("key-remnants", not remnant_failures, "no keyed remnants" if not remnant_failures else ", ".join(remnant_failures[:8]))

    return {"ok": all(check["ok"] for check in checks), "checks": checks}


def _print_validation_report(report: dict) -> None:
    for check in report["checks"]:
        status = "PASS" if check["ok"] else "FAIL"
        print(f"{status} {check['name']}: {check['detail']}")


def _imagegen_script() -> Path:
    return Path(__file__).resolve().with_name("codex_imagegen.py")


def _run_generator(subject: str, out_path: Path, generator_cmd: str) -> None:
    imagegen_script = _imagegen_script()
    if generator_cmd == DEFAULT_GENERATOR_CMD and not imagegen_script.exists():
        raise GenerationError(
            "--generate needs codex-imagegen's bundled generator "
            f"(looked for {imagegen_script}). "
            "Repair the skill, pass --in instead, or provide --generator-cmd for a stub/CI generator."
        )

    try:
        command = generator_cmd.format(
            subject=shlex.quote(subject),
            out=shlex.quote(str(out_path)),
            imagegen=shlex.quote(str(imagegen_script)),
        )
    except KeyError as exc:
        raise GenerationError(f"--generator-cmd placeholder not recognized: {exc}") from exc

    out_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        stderr = (proc.stderr or proc.stdout or "").strip()
        raise GenerationError(
            "generator command failed. Repair codex-imagegen, pass --in, "
            f"or provide a working --generator-cmd. Exit {proc.returncode}: {stderr[:500]}"
        )
    if not out_path.exists():
        raise GenerationError(
            f"generator command finished but did not write {out_path}. "
            "Ensure --generator-cmd contains the {out} placeholder."
        )


def extract(
    source_path: str | Path | None = None,
    *,
    generate: str | None = None,
    out_dir: str | Path | None = None,
    slice_mode: str = "grid",
    cols: int | None = None,
    rows: int | None = None,
    tile: str | Sequence[int] | None = None,
    margin: str | Sequence[int] = (0, 0),
    spacing: str | Sequence[int] = (0, 0),
    key: str = "auto",
    key_hi: float = 90.0,
    key_lo: float = 20.0,
    names: str | Sequence[str] | None = None,
    pad: int = 0,
    export_format: str = "png",
    anchor: str = "bottom-center",
    validate: bool = False,
    expect: int | None = None,
    contact_sheet: str | Path | None = None,
    generator_cmd: str = DEFAULT_GENERATOR_CMD,
    print_validation: bool = False,
) -> dict:
    """Extract sprites and return the manifest dict.

    Exactly one of source_path or generate is required. Validation failures and
    internal write collisions raise SpriteExtractionError subclasses.
    """
    if bool(source_path) == bool(generate):
        raise SpriteExtractionError("provide exactly one of source_path/--in or generate/--generate")
    if pad < 0:
        raise SpriteExtractionError("--pad must be non-negative")
    if export_format not in {"png", "webp", "both"}:
        raise SpriteExtractionError("--format must be png, webp, or both")
    if slice_mode not in {"grid", "components"}:
        raise SpriteExtractionError("--slice must be grid or components")

    names_list = _load_names(names)
    tile_pair = _parse_size(tile)
    margin_pair = _parse_pair(margin, "--margin")
    spacing_pair = _parse_pair(spacing, "--spacing")
    requested_contact_path = _as_path(contact_sheet)
    generated_source = False
    subject = None
    if generate:
        subject = generate
        generated_source = True
        if out_dir is None:
            out_dir = Path.cwd() / f"{_slug(subject)}-sprites"
    else:
        source = _as_path(source_path)
        if source is None:
            raise SpriteExtractionError("missing source path")
        if out_dir is None:
            out_dir = source.with_name(f"{source.stem}-sprites")

    requested_out = _as_path(out_dir)
    if requested_out is None:
        raise SpriteExtractionError("missing output directory")
    try:
        out_path = reserve_output_dir(requested_out)
    except ValueError as exc:
        raise SpriteExtractionError(str(exc)) from exc

    if generate:
        source = out_path / "source" / "generated-source.png"
        _run_generator(subject, source, generator_cmd)
    else:
        source = _as_path(source_path)
        if source is None:
            raise SpriteExtractionError("missing source path")

    source = source.expanduser()
    if not source.exists():
        raise SpriteExtractionError(f"source not found: {source}")
    contact_path = next_output_path(requested_contact_path) if requested_contact_path else None

    with Image.open(source) as opened:
        original = opened.copy()
    try:
        keyed, key_info, key_rgb = key_image(original, key, float(key_hi), float(key_lo))
    except ValueError as exc:
        raise SpriteExtractionError(str(exc)) from exc

    if slice_mode == "grid":
        elements, slicing, empty_cells = _slice_grid(
            keyed, cols, rows, tile_pair, margin_pair, spacing_pair, pad, names_list
        )
    else:
        elements, slicing, empty_cells = _slice_components(keyed, pad, names_list)

    planned = _planned_output_paths(out_path, elements, export_format, contact_path)
    _ensure_writable_outputs(planned, source, False)
    _write_assets(out_path, elements, export_format)

    source_entry: str | dict
    if generated_source:
        source_entry = {
            "path": str(source.relative_to(out_path)),
            "generated": True,
            "subject": subject,
        }
    else:
        source_entry = str(source.resolve())

    manifest = {
        "mode": "spritesheet",
        "artifact": str(out_path),
        "source": source_entry,
        "sheet": {"width": original.size[0], "height": original.size[1]},
        "slicing": slicing,
        "key": key_info,
        "elements": [_element_manifest(element, anchor) for element in elements],
    }

    manifest_path = out_path / "spritesheet.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    if contact_path is not None:
        _write_contact_sheet(contact_path, elements)

    if validate:
        report = _validate(manifest, out_path, expect, empty_cells, key_rgb, float(key_lo))
        if print_validation:
            _print_validation_report(report)
        if not report["ok"]:
            raise ValidationError(report)

    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract a keyed sprite sheet into transparent assets and spritesheet.json.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--in", dest="in_path", help="source sprite sheet path")
    source.add_argument("--generate", metavar="SUBJECT", help="generate source sheet first via codex-imagegen")
    parser.add_argument("--out", dest="out_dir", help="output directory; defaults beside the source")
    parser.add_argument("--slice", choices=("grid", "components"), default="grid", help="slicing mode")
    parser.add_argument("--cols", type=int, help="grid column count")
    parser.add_argument("--rows", type=int, help="grid row count")
    parser.add_argument("--tile", type=_parse_size, metavar="WxH", help="grid tile size, such as 256x256")
    parser.add_argument("--margin", type=lambda value: _parse_pair(value, "--margin"), default=(0, 0), metavar="L,T", help="outer grid offset")
    parser.add_argument("--spacing", type=lambda value: _parse_pair(value, "--spacing"), default=(0, 0), metavar="X,Y", help="gutter between grid cells")
    parser.add_argument("--key", default="auto", help="background key: auto, none, or #RRGGBB")
    parser.add_argument("--key-hi", type=float, default=90.0, help="distance at/above which pixels are fully opaque")
    parser.add_argument("--key-lo", type=float, default=20.0, help="distance at/below which pixels are fully transparent")
    parser.add_argument("--names", help="comma-separated names or a file with one name per line")
    parser.add_argument("--pad", type=int, default=0, help="transparent padding to keep around trimmed content")
    parser.add_argument("--format", dest="export_format", choices=("png", "webp", "both"), default="png", help="asset export format")
    parser.add_argument("--anchor", choices=("bottom-center", "center", "top-left"), default="bottom-center", help="anchor/pivot mode")
    parser.add_argument("--validate", action="store_true", help="run validation checks and fail on any error")
    parser.add_argument("--expect", type=int, help="expected element count for validation")
    parser.add_argument("--contact-sheet", help="optional QA preview PNG path")
    parser.add_argument(
        "--generator-cmd",
        default=DEFAULT_GENERATOR_CMD,
        help="shell command template for --generate with {subject} and {out} placeholders",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        manifest = extract(
            source_path=args.in_path,
            generate=args.generate,
            out_dir=args.out_dir,
            slice_mode=args.slice,
            cols=args.cols,
            rows=args.rows,
            tile=args.tile,
            margin=args.margin,
            spacing=args.spacing,
            key=args.key,
            key_hi=args.key_hi,
            key_lo=args.key_lo,
            names=args.names,
            pad=args.pad,
            export_format=args.export_format,
            anchor=args.anchor,
            validate=args.validate,
            expect=args.expect,
            contact_sheet=args.contact_sheet,
            generator_cmd=args.generator_cmd,
            print_validation=args.validate,
        )
    except ValidationError as exc:
        if not args.validate:
            _print_validation_report(exc.report)
        print(str(exc), file=sys.stderr)
        return 2
    except SpriteExtractionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"wrote {len(manifest['elements'])} element(s) to {manifest['artifact']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
