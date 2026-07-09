#!/usr/bin/env python3
"""Create the deterministic 4x4 isometric sprite-sheet fixture."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


SIZE = 1024
CELL = 256
KEY = (0, 255, 0)
COLORS = np.array(
    [
        (122, 84, 42),
        (174, 112, 53),
        (116, 116, 128),
        (222, 195, 120),
        (42, 119, 210),
        (74, 164, 190),
        (72, 72, 78),
        (145, 91, 54),
        (219, 63, 38),
        (236, 244, 250),
        (36, 117, 64),
        (96, 83, 138),
        (210, 162, 70),
        (157, 98, 178),
        (101, 71, 61),
        (136, 205, 232),
    ],
    dtype=np.uint8,
)


def build_fixture() -> Image.Image:
    image = Image.new("RGB", (SIZE, SIZE), KEY)
    draw = ImageDraw.Draw(image)
    for index, color in enumerate(COLORS):
        row = index // 4
        col = index % 4
        x = col * CELL
        y = row * CELL
        points = [
            (x + CELL // 2, y + 52),
            (x + 210, y + CELL // 2),
            (x + CELL // 2, y + 204),
            (x + 46, y + CELL // 2),
        ]
        draw.polygon(points, fill=tuple(int(v) for v in color))
    return image


def main() -> int:
    out = Path(__file__).resolve().parent / "fixtures/iso-4x4.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    build_fixture().save(out, "PNG", compress_level=9)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
