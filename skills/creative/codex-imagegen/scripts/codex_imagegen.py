#!/usr/bin/env python3
"""Generate immutable flat, layered, or batch image artifacts.

Backends: configured CLIProxyAPI, native Codex, or explicitly authorized OpenAI API.
Run --help for options; backend configuration is documented in reference/backends.md.
Native requests use the bundled Codex/transcript adapter; API requests use stdlib HTTP.
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path

from image_backends import Backend, BackendError, add_backend_arguments, decode_image, request_image, resolve_backend
from image_key import key_image, parse_key, trim_transparent
from output_paths import latest_existing_path, open_output, reserve_output_dir

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
    color = "#{:02X}{:02X}{:02X}".format(*parse_key(key))
    keyname = KEYS[key][1] if key in KEYS else color
    return PROMPT_TMPL.format(subject=subject, size=size, keyname=keyname)


def build_background_prompt(subject, size):
    return BACKGROUND_PROMPT_TMPL.format(subject=subject, size=size)


def generate(prompt, out, match=None, timeout=420, effort="low", backend=None, size=1024):
    """Run one generation and save its attributable image to `out`.
    Returns (ok: bool, note: str, actual_path: Path | None). Sequential use only."""
    backend = backend or Backend("native")
    if backend.name != "native":
        try:
            raw, dimensions = request_image(backend, prompt, size, timeout)
            with open_output(out) as (actual_out, handle):
                handle.write(raw)
        except BackendError as exc:
            return False, str(exc), None
        mismatch = dimensions != (size, size)
        return True, (
            f"wrote {actual_out} ({len(raw)}B); backend={backend.name}; model={backend.model}; "
            f"requested={size}x{size}; actual={dimensions[0]}x{dimensions[1]}; "
            f"dimension_mismatch={str(mismatch).lower()}; dimensions preserved"
        ), actual_out
    try:
        return _generate_native(prompt, out, timeout, effort, size, backend.codex_home)
    except subprocess.TimeoutExpired:
        return False, "Native generation timed out; it may have completed. Inspect the session before retrying; no provider switch attempted.", None
    except OSError:
        return False, "Native Codex execution unavailable; check the CLI and current session. No provider switch attempted.", None


def _generate_native(prompt, out, timeout, effort, size, codex_home=None):
    native_env = dict(os.environ)
    if codex_home:
        native_env["CODEX_HOME"] = codex_home
    sessions_root = Path(native_env.get("CODEX_HOME", "~/.codex")).expanduser() / "sessions"
    proc = subprocess.run(
        ["codex", "exec", "--json", "--dangerously-bypass-approvals-and-sandbox",
         "--skip-git-repo-check", "-c", f"model_reasoning_effort={effort}", "-"],
        input=prompt, text=True, capture_output=True, timeout=timeout, env=native_env,
    )
    if proc.returncode != 0:
        return False, f"Native Codex failed (exit {proc.returncode}); session evidence preserved. No provider switch attempted.", None
    try:
        events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
        ids = [event["thread_id"] for event in events if event.get("type") == "thread.started"]
        if len(ids) != 1 or not re.fullmatch(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", ids[0]):
            raise ValueError("missing or ambiguous session identity")
        session_id = ids[0]
        if any(event.get("type") in ("error", "turn.failed") for event in events) or sum(event.get("type") == "turn.completed" for event in events) != 1:
            raise ValueError("native turn did not complete successfully")
        # Only the exact launched thread can supply results. Never rank other
        # sessions by timestamps, prompt words, or image size.
        transcripts = list(sessions_root.glob(f"**/rollout-*-{session_id}.jsonl"))
        if len(transcripts) != 1:
            raise ValueError("missing or ambiguous transcript for launched session")
        records = [json.loads(line) for line in transcripts[0].read_text(encoding="utf-8").splitlines() if line.strip()]
        identities = [record.get("payload", {}).get("id") for record in records if record.get("type") == "session_meta"]
        if identities != [session_id]:
            raise ValueError("transcript identity does not match launched session")
        results = [record["payload"] for record in records if record.get("type") == "response_item" and record.get("payload", {}).get("type") == "image_generation_call"]
        if len(results) != 1 or results[0].get("status") != "completed":
            raise ValueError("expected one completed image-generation result")
        result = results[0]
        if not isinstance(result.get("id"), str) or not result["id"]:
            raise ValueError("image-generation result has no identity")
        raw, dimensions = decode_image(result.get("result"))
    except (ValueError, KeyError, TypeError, AttributeError, OSError, BackendError):
        return False, "Native image result is missing, failed, ambiguous, or unattributable; inspect the launched session. Session evidence preserved; no provider switch attempted.", None
    with open_output(out) as (actual_out, handle):
        handle.write(raw)
    return True, f"wrote {actual_out} ({len(raw)}B); backend=native; session={session_id}; result={result['id']}; requested={size}x{size}; actual={dimensions[0]}x{dimensions[1]}; dimension_mismatch={str(dimensions != (size, size)).lower()}; dimensions preserved", actual_out


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


def generate_layered(scene_file, requested_out, timeout=420, effort="low", backend=None):
    """Generate an asset-first scene as a versioned directory artifact."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("layered mode needs Pillow and numpy; install requirements.txt") from exc

    backend = backend or Backend("native")
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
        "backend": backend.name,
        "requested_model": backend.model if backend.name != "native" else None,
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
                timeout=timeout,
                effort=effort,
                backend=backend,
                size=size,
            )
            print(f"{'OK  ' if good else 'FAIL'} {name}: {note}", flush=True)
            if not good or actual_raw is None:
                manifest["status"] = "failed"
                manifest["error"] = note
                _write_manifest(manifest_path, manifest)
                return False, f"layered generation stopped at {name}; partial artifact preserved at {artifact}", artifact

            with Image.open(actual_raw) as opened:
                raw_size = list(opened.size)

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
                "requested_size": [size, size],
                "raw_size": raw_size,
                "dimension_mismatch": raw_size != [size, size],
                "resize_policy": "stretch-to-canvas" if role == "background" else "preserve-scale; trim-transparent-padding",
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
    ap.add_argument("--key", type=lambda value: "#{:02X}{:02X}{:02X}".format(*parse_key(value)), default="magenta", help="background key: magenta, green, or #RRGGBB")
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--match", help="legacy option, ignored; native results are bound to the launched session")
    ap.add_argument("--timeout", type=int, default=420)
    ap.add_argument("--effort", default="low")
    add_backend_arguments(ap)
    a = ap.parse_args()

    selected_modes = sum(bool(value) for value in (a.batch, a.layers, a.subject, a.prompt_file))
    if selected_modes != 1:
        ap.error("choose exactly one of --subject, --prompt-file, --batch, or --layers")

    if a.size <= 0 or a.timeout <= 0:
        ap.error("--size and --timeout must be positive")
    try:
        backend = resolve_backend(a)
    except BackendError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if a.layers:
        if not a.out:
            ap.error("--out directory is required for layered generation")
        try:
            good, note, _ = generate_layered(a.layers, a.out, a.timeout, a.effort, backend=backend)
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(note)
        return 0 if good else 2

    if a.batch:
        items = json.loads(Path(a.batch).read_text(encoding="utf-8"))
        os.makedirs(a.outdir, exist_ok=True)
        ok = 0
        for it in items:
            name = it["name"]
            out = os.path.join(a.outdir, f"{name}.png")
            latest = latest_existing_path(out)
            if not a.new_version and latest and latest.stat().st_size > 50_000:
                print(f"SKIP {name} (exists: {latest})", flush=True); ok += 1; continue
            prompt = it.get("prompt") or build_prompt(it["subject"], a.key, a.size)
            print(f"GEN  {name} …", flush=True)
            good, note, _ = generate(prompt, out, timeout=a.timeout, effort=a.effort, backend=backend, size=a.size)
            print(f"{'OK  ' if good else 'FAIL'} {name}: {note}", flush=True)
            if not good:
                print("BATCH STOPPED; completed artifacts preserved. No retry or provider switch attempted.", flush=True)
                return 1
            ok += good
        print(f"BATCH DONE {ok}/{len(items)}", flush=True)
        return 0 if ok == len(items) else 1

    if not a.out:
        ap.error("--out is required for single generation")
    if a.prompt_file:
        prompt = Path(a.prompt_file).read_text(encoding="utf-8")
    elif a.subject:
        prompt = build_prompt(a.subject, a.key, a.size)
    else:
        ap.error("provide --subject or --prompt-file (or --batch)")
    good, note, _ = generate(prompt, a.out, timeout=a.timeout, effort=a.effort, backend=backend, size=a.size)
    print(note)
    return 0 if good else 2


if __name__ == "__main__":
    sys.exit(main())
