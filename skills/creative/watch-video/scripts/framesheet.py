#!/usr/bin/env python3
"""Build a timestamped contact sheet from a video.

Samples N frames uniformly from a video (or a window of it), stamps each
tile with its source timestamp, and tiles them into a single image sized
to a vision model's pixel budget (default ~1.15 MP, max 1568 px wide).

Requires: ffmpeg/ffprobe on PATH, Pillow.

Usage:
  framesheet.py VIDEO OUT.png [--frames N] [--start SEC] [--duration SEC]
                              [--cols C] [--budget MEGAPIXELS]
"""

import argparse
import glob
import math
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def die(msg):
    sys.exit(f"framesheet: {msg}")


def probe(video):
    if not shutil.which("ffprobe"):
        die("ffprobe not found on PATH (install ffmpeg)")
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-show_entries",
         "format=duration", "-of", "csv=p=0", video],
        capture_output=True, text=True)
    if out.returncode != 0:
        die(f"ffprobe failed on {video}: {out.stderr.strip()}")
    lines = out.stdout.strip().splitlines()
    w, h = (int(x) for x in lines[0].split(",")[:2])
    duration = float(lines[-1])
    return w, h, duration


def pick_grid(n, aspect, budget_px, max_w):
    """Choose cols/rows and tile size maximizing tile area within budget."""
    best = None
    for cols in range(1, n + 1):
        rows = math.ceil(n / cols)
        tw = min(max_w / cols, math.sqrt(budget_px * aspect / (cols * rows)))
        th = tw / aspect
        if tw < 32:
            continue
        # prefer bigger tiles; tiebreak toward squarer sheets
        squareness = -abs(math.log((cols * tw) / (rows * th)))
        key = (int(tw), squareness)
        if best is None or key > best[0]:
            best = (key, cols, rows, int(tw) // 2 * 2, int(th) // 2 * 2)
    if best is None:
        die(f"{n} frames cannot fit legible tiles in budget; lower --frames")
    return best[1], best[2], best[3], best[4]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fmt_ts(t):
    t = int(t)
    if t >= 3600:
        return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"
    return f"{t // 60}:{t % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--frames", type=int, default=30)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--duration", type=float, default=None,
                    help="window length in seconds (default: to end of video)")
    ap.add_argument("--cols", type=int, default=None)
    ap.add_argument("--budget", type=float, default=1.15,
                    help="sheet pixel budget in megapixels")
    args = ap.parse_args()

    if not os.path.exists(args.video):
        die(f"no such file: {args.video}")
    src_w, src_h, video_dur = probe(args.video)
    duration = args.duration or (video_dur - args.start)
    if duration <= 0 or args.start >= video_dur:
        die(f"window [{args.start}, +{args.duration}] outside video "
            f"(duration {video_dur:.1f}s)")
    n = args.frames
    aspect = src_w / src_h

    if args.cols:
        cols = args.cols
        rows = math.ceil(n / cols)
        tw = min(1568 / cols, math.sqrt(args.budget * 1e6 * aspect / (cols * rows)))
        tw, th = int(tw) // 2 * 2, int(tw / aspect) // 2 * 2
    else:
        cols, rows, tw, th = pick_grid(n, aspect, args.budget * 1e6, 1568)

    interval = duration / n
    tmp = tempfile.mkdtemp(prefix="framesheet_")
    try:
        cmd = ["ffmpeg", "-v", "error", "-y"]
        if args.start:
            cmd += ["-ss", str(args.start)]
        cmd += ["-t", str(duration), "-i", args.video,
                "-vf", f"fps={n}/{duration},scale={tw}:{th}",
                "-frames:v", str(n), f"{tmp}/f%04d.png"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            die(f"ffmpeg failed: {r.stderr.strip()}")
        files = sorted(glob.glob(f"{tmp}/f*.png"))
        if not files:
            die("ffmpeg produced no frames")

        fontsize = max(10, th // 11)
        font = load_font(fontsize)
        rows = math.ceil(len(files) / cols)
        sheet = Image.new("RGB", (cols * tw, rows * th), "black")
        for i, f in enumerate(files):
            img = Image.open(f).convert("RGB")
            ts = fmt_ts(args.start + i * interval)
            d = ImageDraw.Draw(img)
            xy = (3, th - fontsize - 5)
            bbox = d.textbbox(xy, ts, font=font)
            d.rectangle([bbox[0] - 2, bbox[1] - 1, bbox[2] + 2, bbox[3] + 1],
                        fill=(0, 0, 0))
            d.text(xy, ts, font=font, fill=(255, 230, 0))
            sheet.paste(img, ((i % cols) * tw, (i // cols) * th))
        sheet.save(args.out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"{args.out}: {len(files)} frames, grid {cols}x{rows}, "
          f"tile {tw}x{th}, sheet {sheet.size[0]}x{sheet.size[1]}, "
          f"one tile every {interval:.1f}s "
          f"({fmt_ts(args.start)} to {fmt_ts(args.start + duration)})")


if __name__ == "__main__":
    main()
