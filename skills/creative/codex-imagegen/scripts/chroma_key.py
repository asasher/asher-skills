#!/usr/bin/env python3
"""Remove a flat background from a generated image:
key -> despill -> edge feather -> trim to content. Writes an RGBA PNG.

Usage:  chroma_key.py IN OUT [--key auto|magenta|green|#RRGGBB] [--hi 90] [--lo 20] [--pad 4]

Requires numpy + Pillow (pip install numpy pillow). Codex ships an equivalent at
~/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py if deps are missing.
"""
import argparse, sys

from image_key import key_image, trim_transparent
from output_paths import open_output

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--key", default="magenta", help="auto, magenta, green, or #RRGGBB")
    ap.add_argument("--hi", type=float, default=90.0, help="distance at/above which pixels are fully opaque")
    ap.add_argument("--lo", type=float, default=20.0, help="distance at/below which pixels are fully transparent")
    ap.add_argument("--pad", type=int, default=4, help="transparent-margin padding kept on trim")
    a = ap.parse_args()

    try:
        from PIL import Image
    except ImportError:
        sys.exit("needs numpy + Pillow: pip install numpy pillow "
                 "(or use ~/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py)")

    try:
        keyed, _, _ = key_image(Image.open(a.inp), a.key, a.hi, a.lo)
    except ValueError as exc:
        sys.exit(str(exc))
    out, _ = trim_transparent(keyed, pad=a.pad)

    with open_output(a.out) as (actual_out, handle):
        out.save(handle, format="PNG")
    print(f"wrote {actual_out} ({out.width}x{out.height}, key={a.key})")


if __name__ == "__main__":
    main()
