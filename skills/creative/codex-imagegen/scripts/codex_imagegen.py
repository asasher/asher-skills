#!/usr/bin/env python3
"""Headless raster image generation via the Codex CLI's built-in image_gen tool.

Recovered recipe (see SKILL.md for the why):
  - MUST bypass the sandbox: `codex exec --dangerously-bypass-approvals-and-sandbox`,
    else the image tool no-ops and codex reuses a stale image.
  - The image is base64 inside ~/.codex/sessions/**/*.jsonl (payload
    type "image_generation_call"), NOT a file and NOT in --json stdout.
  - Sequential only; parallel runs corrupt fresh-session detection.
  - Disambiguate by matching subject keywords against `revised_prompt`, not recency.
  - Ask for a solid flat key-color background; key it out afterwards (chroma_key.py).

Flat:    codex_imagegen.py --subject "..." --out path.png [--key magenta|green] [--size 1024] [--match "kw kw"]
Custom:  codex_imagegen.py --prompt-file p.txt --out path.png [--match "kw"]
Batch:   codex_imagegen.py --batch batch.json --outdir DIR [--new-version] [--key ...] [--size ...]
Layers:  codex_imagegen.py --layers scene.json --out scene
         batch.json = [{"name":"oak-tree","subject":"..."}, ...]  (or "prompt" for a raw prompt)
"""
import argparse, base64, glob, json, os, re, subprocess, sys, time
from pathlib import Path

from image_key import key_image, trim_transparent
from output_paths import latest_existing_path, open_output, reserve_output_dir

SESS = os.path.expanduser("~/.codex/sessions")
PNG_SIG, JPG_SIG = "iVBORw0KGgo", "/9j/"

KEYS = {
    "magenta": ("#FF00FF", "pure magenta (#FF00FF)"),
    "green":   ("#00FF00", "pure green (#00FF00)"),
}

PROMPT_TMPL = """Use your image generation tool to actually generate a raster image (do NOT draw SVG or code, do NOT fake transparency with a checkerboard).

Subject: {subject}.

Dimensions: {size}x{size}.

Background: a SOLID {keyname} flat fill covering the ENTIRE image behind the subject — no checkerboard, no gradient, no other background elements, no text, no ground shadow. The fill must be uniform and unbroken so it can be cleanly keyed out. The subject itself must contain NO {keyname} pixels anywhere."""

BACKGROUND_PROMPT_TMPL = """Use your image generation tool to actually generate a raster image (do NOT draw SVG or code).

Create only this full-bleed background layer: {subject}.

Dimensions: {size}x{size}. Fill the entire canvas. Do not include any foreground subjects, isolated props, text, checkerboard, transparent areas, borders, or watermark."""


def build_prompt(subject, key, size):
    _, keyname = KEYS[key]
    return PROMPT_TMPL.format(subject=subject, size=size, keyname=keyname)


def build_background_prompt(subject, size):
    return BACKGROUND_PROMPT_TMPL.format(subject=subject, size=size)


def walk_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from walk_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk_strings(v)


def generate(prompt, out, match, timeout=420, effort="low"):
    """Run one codex generation and extract the matching image to `out`.
    Returns (ok: bool, note: str, actual_path: Path | None). Sequential use only."""
    mark = time.time() - 2  # small clock-skew guard
    proc = subprocess.run(
        ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox",
         "--skip-git-repo-check", "-c", f"model_reasoning_effort={effort}", "-"],
        input=prompt, text=True, capture_output=True, timeout=timeout,
    )
    tail = (proc.stdout or "")[-200:].strip()
    sessions = sorted(
        (p for p in glob.glob(os.path.join(SESS, "**", "*.jsonl"), recursive=True)
         if os.path.getmtime(p) >= mark),
        key=os.path.getmtime, reverse=True,
    )
    cands = []  # (b64, revised_prompt)
    for s in sessions:
        try:
            lines = open(s, encoding="utf-8").read().splitlines()
        except OSError:
            continue
        for ln in lines:
            if PNG_SIG not in ln and JPG_SIG not in ln:
                continue
            try:
                obj = json.loads(ln)
            except ValueError:
                continue
            m = re.search(r'"revised_prompt"\s*:\s*"([^"]{0,400})', ln)
            rev = m.group(1) if m else ""
            for st in walk_strings(obj):
                core = st.split(",", 1)[1] if st.startswith("data:") else st
                if (core.startswith(PNG_SIG) or core.startswith(JPG_SIG)) and len(core) > 8000:
                    cands.append((core, rev))
    if not cands:
        return False, f"NO_IMAGE (codex exit {proc.returncode}; tail: {tail})", None

    kw = [w for w in re.split(r"[^a-z0-9]+", match.lower()) if len(w) > 2]
    def score(c):
        return (sum(k in c[1].lower() for k in kw), len(c[0]))
    cands.sort(key=score, reverse=True)
    best, matched = cands[0][0], score(cands[0])[0]
    raw = base64.b64decode(best + "=" * (-len(best) % 4))
    with open_output(out) as (actual_out, f):
        f.write(raw)
    return True, f"wrote {actual_out} ({len(raw)}B); matched_kw={matched}; candidates={len(cands)}", actual_out


def _slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "layer"


def _write_manifest(path, manifest):
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _layer_position(layer, canvas, asset_size):
    anchor = layer.get("anchor", "bottom-center")
    default_x = canvas[0] // 2
    default_y = canvas[1] if anchor == "bottom-center" else canvas[1] // 2
    x = int(layer.get("x", default_x))
    y = int(layer.get("y", default_y))
    width, height = asset_size
    if anchor == "bottom-center":
        return x - width // 2, y - height, [x, y]
    if anchor == "center":
        return x - width // 2, y - height // 2, [x, y]
    if anchor == "top-left":
        return x, y, [x, y]
    raise ValueError(f"unsupported anchor {anchor!r}")


def generate_layered(scene_file, requested_out, timeout=420, effort="low"):
    """Generate an asset-first scene as a versioned directory artifact."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("layered mode needs Pillow and numpy; install requirements.txt") from exc

    spec = json.loads(Path(scene_file).read_text(encoding="utf-8"))
    layers = spec.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("layered scene needs a non-empty layers list")
    size = int(spec.get("size", 1024))
    if size <= 0:
        raise ValueError("layered scene size must be positive")
    if any(not isinstance(layer, dict) for layer in layers):
        raise ValueError("every layered scene entry must be an object")
    backgrounds = [layer for layer in layers if layer.get("role") == "background"]
    if len(backgrounds) > 1:
        raise ValueError("layered scene supports at most one background layer")
    for index, layer in enumerate(layers):
        if not layer.get("name") or not layer.get("subject"):
            raise ValueError(f"layer {index} needs name and subject")
        if layer.get("role", "subject") != "background":
            key = layer.get("key", spec.get("key", "magenta"))
            if key not in KEYS:
                raise ValueError(f"layer {layer['name']} key must be magenta or green")
            _layer_position(layer, (size, size), (1, 1))
        if int(layer.get("pad", 4)) < 0:
            raise ValueError(f"layer {layer['name']} pad must be non-negative")
        int(layer.get("z", index))

    artifact = reserve_output_dir(requested_out)
    raw_dir = artifact / "raw"
    layer_dir = artifact / "layers"
    raw_dir.mkdir()
    layer_dir.mkdir()
    manifest = {
        "mode": "layered",
        "status": "in_progress",
        "artifact": str(artifact),
        "canvas": {"width": size, "height": size},
        "composite": "composite.png",
        "layers": [],
    }
    manifest_path = artifact / "manifest.json"
    _write_manifest(manifest_path, manifest)
    art_direction = str(spec.get("art_direction", "")).strip()

    try:
        for index, layer in enumerate(layers):
            name = _slug(str(layer["name"]))
            role = layer.get("role", "subject")
            subject = str(layer["subject"])
            if art_direction:
                subject = f"{subject}. Shared art direction: {art_direction}"
            if role == "background":
                prompt = layer.get("prompt") or build_background_prompt(subject, size)
                requested_raw = raw_dir / f"{index:02d}-{name}.png"
            else:
                key = layer.get("key", spec.get("key", "magenta"))
                prompt = layer.get("prompt") or build_prompt(subject, key, size)
                requested_raw = raw_dir / f"{index:02d}-{name}-keyed.png"

            good, note, actual_raw = generate(
                prompt,
                requested_raw,
                layer.get("match") or subject,
                timeout,
                effort,
            )
            print(f"{'OK  ' if good else 'FAIL'} {name}: {note}", flush=True)
            if not good or actual_raw is None:
                manifest["status"] = "failed"
                manifest["error"] = note
                _write_manifest(manifest_path, manifest)
                return False, f"layered generation stopped at {name}; partial artifact preserved at {artifact}", artifact

            if role == "background":
                with Image.open(actual_raw) as opened:
                    asset = opened.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
                asset_path = layer_dir / f"{index:02d}-{name}.png"
                asset.save(asset_path, "PNG")
                position = [0, 0]
                anchor = "top-left"
                bounds = {"x": 0, "y": 0, "w": size, "h": size}
                raw_rel = actual_raw.relative_to(artifact).as_posix()
            else:
                key = layer.get("key", spec.get("key", "magenta"))
                with Image.open(actual_raw) as opened:
                    keyed, key_info, _ = key_image(opened, key)
                asset, bounds = trim_transparent(keyed, pad=int(layer.get("pad", 4)))
                asset_path = layer_dir / f"{index:02d}-{name}.png"
                asset.save(asset_path, "PNG")
                anchor = layer.get("anchor", "bottom-center")
                left, top, position = _layer_position(layer, (size, size), asset.size)
                bounds = {**bounds, "canvas_x": left, "canvas_y": top}
                raw_rel = actual_raw.relative_to(artifact).as_posix()

            entry = {
                "name": name,
                "role": role,
                "z": int(layer.get("z", index)),
                "file": asset_path.relative_to(artifact).as_posix(),
                "raw": raw_rel,
                "prompt": prompt,
                "size": [asset.width, asset.height],
                "anchor": anchor,
                "position": position,
                "bounds": bounds,
            }
            if role != "background":
                entry["key"] = key_info
            manifest["layers"].append(entry)
            _write_manifest(manifest_path, manifest)

        composite = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        for entry in sorted(manifest["layers"], key=lambda item: item["z"]):
            with Image.open(artifact / entry["file"]) as opened:
                layer_image = opened.convert("RGBA")
            if entry["role"] == "background":
                composite.alpha_composite(layer_image, (0, 0))
            else:
                composite.alpha_composite(
                    layer_image,
                    (entry["bounds"]["canvas_x"], entry["bounds"]["canvas_y"]),
                )
        composite.save(artifact / "composite.png", "PNG")
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = str(exc)
        _write_manifest(manifest_path, manifest)
        raise

    manifest["status"] = "complete"
    _write_manifest(manifest_path, manifest)
    return True, f"wrote layered artifact {artifact} ({len(layers)} layers)", artifact


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subject")
    ap.add_argument("--prompt-file")
    ap.add_argument("--out")
    ap.add_argument("--batch", help="JSON list of {name, subject|prompt}")
    ap.add_argument("--layers", help="JSON scene plan for asset-first layered generation")
    ap.add_argument("--outdir", default=".")
    ap.add_argument(
        "--new-version",
        action="store_true",
        help="in batch mode, generate the next version instead of skipping completed names",
    )
    ap.add_argument("--key", choices=list(KEYS), default="magenta")
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--match", help="keywords to disambiguate the image (default: from subject/out)")
    ap.add_argument("--timeout", type=int, default=420)
    ap.add_argument("--effort", default="low")
    a = ap.parse_args()

    selected_modes = sum(bool(value) for value in (a.batch, a.layers, a.subject, a.prompt_file))
    if selected_modes != 1:
        ap.error("choose exactly one of --subject, --prompt-file, --batch, or --layers")

    if a.layers:
        if not a.out:
            ap.error("--out directory is required for layered generation")
        try:
            good, note, _ = generate_layered(a.layers, a.out, a.timeout, a.effort)
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(note)
        return 0 if good else 2

    if a.batch:
        items = json.load(open(a.batch))
        os.makedirs(a.outdir, exist_ok=True)
        ok = 0
        for it in items:
            name = it["name"]
            out = os.path.join(a.outdir, f"{name}.png")
            latest = latest_existing_path(out)
            if not a.new_version and latest and latest.stat().st_size > 50_000:
                print(f"SKIP {name} (exists: {latest})", flush=True); ok += 1; continue
            prompt = it.get("prompt") or build_prompt(it["subject"], a.key, a.size)
            match = it.get("match") or it.get("subject") or name
            print(f"GEN  {name} …", flush=True)
            good, note, _ = generate(prompt, out, match, a.timeout, a.effort)
            print(f"{'OK  ' if good else 'FAIL'} {name}: {note}", flush=True)
            ok += good
        print(f"BATCH DONE {ok}/{len(items)}", flush=True)
        return 0 if ok == len(items) else 1

    if not a.out:
        ap.error("--out is required for single generation")
    if a.prompt_file:
        prompt = open(a.prompt_file).read()
    elif a.subject:
        prompt = build_prompt(a.subject, a.key, a.size)
    else:
        ap.error("provide --subject or --prompt-file (or --batch)")
    match = a.match or a.subject or os.path.splitext(os.path.basename(a.out))[0].replace("-", " ")
    good, note, _ = generate(prompt, a.out, match, a.timeout, a.effort)
    print(note)
    return 0 if good else 2


if __name__ == "__main__":
    sys.exit(main())
