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

Single:  codex_imagegen.py --subject "..." --out path.png [--key magenta|green] [--size 1024] [--match "kw kw"]
Custom:  codex_imagegen.py --prompt-file p.txt --out path.png [--match "kw"]
Batch:   codex_imagegen.py --batch batch.json --outdir DIR [--key ...] [--size ...]
         batch.json = [{"name":"oak-tree","subject":"..."}, ...]  (or "prompt" for a raw prompt)
"""
import argparse, base64, glob, json, os, re, subprocess, sys, time

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


def build_prompt(subject, key, size):
    _, keyname = KEYS[key]
    return PROMPT_TMPL.format(subject=subject, size=size, keyname=keyname)


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
    Returns (ok: bool, note: str). Sequential use only."""
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
        return False, f"NO_IMAGE (codex exit {proc.returncode}; tail: {tail})"

    kw = [w for w in re.split(r"[^a-z0-9]+", match.lower()) if len(w) > 2]
    def score(c):
        return (sum(k in c[1].lower() for k in kw), len(c[0]))
    cands.sort(key=score, reverse=True)
    best, matched = cands[0][0], score(cands[0])[0]
    raw = base64.b64decode(best + "=" * (-len(best) % 4))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(raw)
    return True, f"wrote {out} ({len(raw)}B); matched_kw={matched}; candidates={len(cands)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subject")
    ap.add_argument("--prompt-file")
    ap.add_argument("--out")
    ap.add_argument("--batch", help="JSON list of {name, subject|prompt}")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--key", choices=list(KEYS), default="magenta")
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--match", help="keywords to disambiguate the image (default: from subject/out)")
    ap.add_argument("--timeout", type=int, default=420)
    ap.add_argument("--effort", default="low")
    a = ap.parse_args()

    if a.batch:
        items = json.load(open(a.batch))
        os.makedirs(a.outdir, exist_ok=True)
        ok = 0
        for it in items:
            name = it["name"]
            out = os.path.join(a.outdir, f"{name}.png")
            if os.path.exists(out) and os.path.getsize(out) > 50_000:
                print(f"SKIP {name} (exists)", flush=True); ok += 1; continue
            prompt = it.get("prompt") or build_prompt(it["subject"], a.key, a.size)
            match = it.get("match") or it.get("subject") or name
            print(f"GEN  {name} …", flush=True)
            good, note = generate(prompt, out, match, a.timeout, a.effort)
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
    good, note = generate(prompt, a.out, match, a.timeout, a.effort)
    print(note)
    return 0 if good else 2


if __name__ == "__main__":
    sys.exit(main())
