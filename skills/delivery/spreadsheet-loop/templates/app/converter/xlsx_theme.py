#!/usr/bin/env python3
"""xlsx_theme.py — resolve Excel THEME and INDEXED colours to concrete #RRGGBB.

openpyxl exposes a cell colour as one of: an explicit rgb ARGB, a theme index + tint, or a palette index.
It does NOT resolve theme/indexed colours to RGB — so a converter that reads only `.rgb` silently drops the
colour of most real-workbook cells (theme colours are the Excel default). This module reads the workbook's
theme palette once and resolves any openpyxl Color to a concrete hex, so styling round-trips visually.

Note: theme tint is applied with the standard linear-RGB approximation of Excel's HSL-luminance model —
visually near-identical for the tints Excel emits; exact HSL round-trip is a later refinement.
"""
import zipfile
from xml.etree import ElementTree as ET
from openpyxl.styles.colors import COLOR_INDEX

_NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
_SYS = {"windowText": "000000", "window": "FFFFFF"}

def read_theme(xlsx_path):
    """Return the 12 theme base colours in Excel theme-index order, or None if unavailable.
    Index order (Excel): 0 lt1, 1 dk1, 2 lt2, 3 dk2, 4-9 accent1-6, 10 hlink, 11 folHlink.
    (Note the lt/dk swap versus the clrScheme XML order dk1,lt1,dk2,lt2.)"""
    try:
        with zipfile.ZipFile(xlsx_path) as z:
            xml = z.read("xl/theme/theme1.xml")
    except (KeyError, zipfile.BadZipFile, FileNotFoundError, OSError):
        return None
    scheme = ET.fromstring(xml).find(".//a:clrScheme", _NS)
    if scheme is None:
        return None
    d = {}
    for child in scheme:
        name = child.tag.split("}")[-1]
        srgb = child.find("a:srgbClr", _NS)
        sysc = child.find("a:sysClr", _NS)
        if srgb is not None:
            d[name] = srgb.get("val", "000000").upper()
        elif sysc is not None:
            d[name] = (sysc.get("lastClr") or _SYS.get(sysc.get("val"), "000000")).upper()
    return [d.get("lt1", "FFFFFF"), d.get("dk1", "000000"), d.get("lt2", "FFFFFF"), d.get("dk2", "000000"),
            d.get("accent1"), d.get("accent2"), d.get("accent3"), d.get("accent4"), d.get("accent5"),
            d.get("accent6"), d.get("hlink"), d.get("folHlink")]

def _apply_tint(rgb, tint):
    if not tint:
        return rgb
    def f(c):
        c = c * (1 + tint) if tint < 0 else c * (1 - tint) + 255 * tint
        return max(0, min(255, round(c)))
    return f"{f(int(rgb[0:2],16)):02X}{f(int(rgb[2:4],16)):02X}{f(int(rgb[4:6],16)):02X}"

def resolve(color, theme_idx):
    """openpyxl Color -> '#RRGGBB' or None. Handles explicit rgb, theme+tint, and indexed palette."""
    if color is None:
        return None
    ctype = getattr(color, "type", None)
    if ctype == "rgb":
        rgb = getattr(color, "rgb", None)
        if isinstance(rgb, str) and len(rgb) >= 6:
            return "#" + rgb[-6:].upper()
    if ctype == "theme" and theme_idx is not None:
        ti = getattr(color, "theme", None)
        if isinstance(ti, int) and 0 <= ti < len(theme_idx) and theme_idx[ti]:
            return "#" + _apply_tint(theme_idx[ti], getattr(color, "tint", 0.0) or 0.0)
    if ctype == "indexed":
        i = getattr(color, "indexed", None)
        if isinstance(i, int) and 0 <= i < len(COLOR_INDEX):
            argb = COLOR_INDEX[i]
            if isinstance(argb, str) and len(argb) >= 6:
                return "#" + argb[-6:].upper()
    # Fallback: a bare rgb string even when type isn't 'rgb'
    rgb = getattr(color, "rgb", None)
    if isinstance(rgb, str) and len(rgb) >= 6:
        return "#" + rgb[-6:].upper()
    return None
