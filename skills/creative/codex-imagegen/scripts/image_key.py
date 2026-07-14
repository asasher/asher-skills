#!/usr/bin/env python3
"""Shared flat-background keying for transparent image assets."""

from __future__ import annotations

import re

import numpy as np
from PIL import Image


ALPHA_THRESHOLD = 10


def _hex_color(rgb):
    if rgb is None:
        return None
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def parse_key(value):
    aliases = {"magenta": (255, 0, 255), "green": (0, 255, 0)}
    if value in aliases:
        return aliases[value]
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", str(value).strip())
    if not match:
        raise ValueError("key must be auto, none, magenta, green, or #RRGGBB")
    raw = match.group(1)
    return int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)


def dominant_border_color(image):
    rgb = np.asarray(image.convert("RGB"), dtype=np.uint8)
    border = np.concatenate(
        [
            rgb[0:1, :, :].reshape(-1, 3),
            rgb[-1:, :, :].reshape(-1, 3),
            rgb[:, 0:1, :].reshape(-1, 3),
            rgb[:, -1:, :].reshape(-1, 3),
        ],
        axis=0,
    )
    colors, counts = np.unique(border, axis=0, return_counts=True)
    return tuple(int(value) for value in colors[int(np.argmax(counts))])


def key_image(image, key="auto", key_hi=90.0, key_lo=20.0):
    """Return ``(rgba, key metadata, rgb key)`` using a soft distance matte."""
    if key_hi <= key_lo:
        raise ValueError("key_hi must be greater than key_lo")
    if key == "none":
        return image.convert("RGBA"), {"color": None, "method": "none"}, None
    if key == "auto":
        key_rgb = dominant_border_color(image)
        method = "border-sample"
    else:
        key_rgb = parse_key(key)
        method = "supplied"

    rgba = np.asarray(image.convert("RGBA"), dtype=np.float32)
    rgb = rgba[..., :3]
    input_alpha = rgba[..., 3]
    key_vec = np.asarray(key_rgb, dtype=np.float32)
    distance = np.linalg.norm(rgb - key_vec, axis=2)

    ramp = np.clip((distance - key_lo) / max(key_hi - key_lo, 1e-6), 0.0, 1.0)
    alpha = input_alpha * ramp
    alpha_frac = np.clip(alpha / 255.0, 0.0, 1.0)

    corrected = rgb.copy()
    fringe = (alpha_frac > 0.05) & (alpha_frac < 0.999)
    if np.any(fringe):
        fraction = alpha_frac[fringe][..., None]
        corrected[fringe] = (
            rgb[fringe] - (1.0 - fraction) * key_vec
        ) / np.maximum(fraction, 1e-6)

    out = np.dstack([corrected, alpha]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA"), {"color": _hex_color(key_rgb), "method": method}, key_rgb


def trim_transparent(image, pad=0, threshold=ALPHA_THRESHOLD):
    """Trim transparent borders while retaining optional transparent padding."""
    array = np.asarray(image.convert("RGBA"), dtype=np.uint8)
    ys, xs = np.where(array[..., 3] > threshold)
    if not len(xs):
        return image.convert("RGBA"), {"x": 0, "y": 0, "w": image.width, "h": image.height}
    x0 = max(0, int(xs.min()) - pad)
    x1 = min(image.width, int(xs.max()) + 1 + pad)
    y0 = max(0, int(ys.min()) - pad)
    y1 = min(image.height, int(ys.max()) + 1 + pad)
    return image.crop((x0, y0, x1, y1)), {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}
