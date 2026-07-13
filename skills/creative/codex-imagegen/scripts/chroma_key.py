#!/usr/bin/env python3
"""Remove a flat chroma-key background (magenta or green) from a generated image:
key -> despill -> edge feather -> trim to content. Writes an RGBA PNG.

Usage:  chroma_key.py IN OUT [--key magenta|green] [--hi 90] [--lo 20] [--pad 4]

Requires numpy + Pillow (pip install numpy pillow). Codex ships an equivalent at
~/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py if deps are missing.
"""
import argparse, sys

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--key", choices=("magenta", "green"), default="magenta")
    ap.add_argument("--hi", type=float, default=90.0, help="keyness above this => fully transparent")
    ap.add_argument("--lo", type=float, default=20.0, help="keyness below this => fully opaque")
    ap.add_argument("--pad", type=int, default=4, help="transparent-margin padding kept on trim")
    a = ap.parse_args()

    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        sys.exit("needs numpy + Pillow: pip install numpy pillow "
                 "(or use ~/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py)")

    img = Image.open(a.inp).convert("RGBA")
    arr = np.asarray(img).astype(np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

    if a.key == "magenta":                 # magenta = high R & B, low G
        keyness = np.minimum(r, b) - g
    else:                                  # green = high G, low R & B
        keyness = g - np.maximum(r, b)

    # alpha ramp: 0 where keyness>=hi, 255 where keyness<=lo, linear between
    alpha = np.clip((a.hi - keyness) / max(a.hi - a.lo, 1e-6), 0.0, 1.0) * 255.0

    # despill the fringe: pull the key channels toward the neutral channel(s)
    frac = np.clip(keyness / max(a.hi, 1e-6), 0.0, 1.0)[..., None]  # how spilled
    if a.key == "magenta":
        r = r - (r - g) * frac[..., 0] * 0.9
        b = b - (b - g) * frac[..., 0] * 0.9
    else:
        g = g - (g - np.maximum(r, b)) * frac[..., 0] * 0.9

    out = np.dstack([r, g, b, alpha]).clip(0, 255).astype(np.uint8)

    # trim to content bounds (+pad)
    ys, xs = np.where(out[..., 3] > 10)
    if len(xs):
        x0, x1 = max(0, xs.min() - a.pad), min(out.shape[1], xs.max() + 1 + a.pad)
        y0, y1 = max(0, ys.min() - a.pad), min(out.shape[0], ys.max() + 1 + a.pad)
        out = out[y0:y1, x0:x1]

    Image.fromarray(out, "RGBA").save(a.out)
    print(f"wrote {a.out} ({out.shape[1]}x{out.shape[0]}, key={a.key})")


if __name__ == "__main__":
    main()
