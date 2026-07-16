#!/usr/bin/env python3
"""Build Relay's self-contained exact-content review sheet."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from relay_common import append_event, build_approval_manifest, canonical_json, instance_root, pretty_json, workflow_event


def sheet(manifest: dict, run: Path) -> str:
    delivery_html = (run / "rendered-email.html").read_text(encoding="utf-8")
    plain = (run / "rendered-email.txt").read_text(encoding="utf-8")
    light = (run / "rendered-email-light.html").read_text(encoding="utf-8")
    dark = (run / "rendered-email-dark.html").read_text(encoding="utf-8")
    embedded = canonical_json(manifest).replace("<", "\\u003c")
    evidence_rows = "".join(
        f"<tr><td>{html.escape(str(item.get('id','')))}</td><td>{html.escape(str(item.get('status','')))}</td><td>{html.escape(str(item.get('source','')))}</td></tr>"
        for item in manifest["evidence"]
    ) or '<tr><td colspan="3">No evidence items</td></tr>'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Relay review — {html.escape(str(manifest["communication_id"]))}</title><style>
:root{{color-scheme:light dark;--bg:#f6f6f8;--card:#fff;--fg:#18181b;--muted:#71717a;--line:#dedee5;--accent:#4f46e5}}@media(prefers-color-scheme:dark){{:root{{--bg:#111115;--card:#1b1b21;--fg:#ededf2;--muted:#a1a1aa;--line:#34343d;--accent:#9b95ff}}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}main{{max-width:1120px;margin:auto;padding:28px 18px 70px}}h1{{font-size:24px;margin:0}}h2{{font-size:15px;margin:0 0 12px}}.muted{{color:var(--muted)}}.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:16px 0}}.headers{{display:grid;grid-template-columns:90px 1fr;gap:7px 12px}}code,pre{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--bg);padding:14px;border-radius:8px}}.previews{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}iframe{{width:100%;height:620px;border:1px solid var(--line);border-radius:8px;background:white}}table{{width:100%;border-collapse:collapse}}th,td{{padding:7px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}.hashes td:first-child{{width:180px;color:var(--muted)}}@media(max-width:800px){{.previews{{grid-template-columns:1fr}}}}
</style></head><body><main>
<header id="relay-review-header"><h1>Relay delivery review</h1><p class="muted">Approval authorizes only the exact content, sender, recipients, template, and hashes embedded in this document.</p></header>
<section class="card" id="message-{html.escape(str(manifest['communication_id']))}"><h2>{html.escape(str(manifest['subject']))}</h2><div class="headers">
<strong>Sender</strong><span>{html.escape(str(manifest['sender']))}</span><strong>To</strong><span>{html.escape(', '.join(manifest['recipients']['to']))}</span><strong>CC</strong><span>{html.escape(', '.join(manifest['recipients']['cc']) or '—')}</span><strong>Audience</strong><span>{html.escape(str(manifest['audience_id']))}</span></div></section>
<section class="card" id="email-previews"><h2>Authored light and dark previews</h2><div class="previews"><div id="light-preview"><p class="muted">Forced light</p><iframe title="Forced light email preview" srcdoc="{html.escape(light, quote=True)}"></iframe></div><div id="dark-preview"><p class="muted">Forced dark</p><iframe title="Forced dark email preview" srcdoc="{html.escape(dark, quote=True)}"></iframe></div></div></section>
<section class="card" id="delivery-html"><h2>Actual delivery HTML</h2><iframe title="Actual delivery HTML" srcdoc="{html.escape(delivery_html, quote=True)}"></iframe></section>
<section class="card" id="delivery-text"><h2>Actual plain text</h2><pre>{html.escape(plain)}</pre></section>
<section class="card" id="evidence-summary"><h2>Evidence summary</h2><table><thead><tr><th>ID</th><th>Status</th><th>Source</th></tr></thead><tbody>{evidence_rows}</tbody></table></section>
<section class="card" id="canonical-hashes"><h2>Canonical approval hashes</h2><table class="hashes"><tbody><tr><td>Manifest</td><td><code>{manifest['manifest_sha256']}</code></td></tr><tr><td>HTML</td><td><code>{manifest['content']['html_sha256']}</code></td></tr><tr><td>Text</td><td><code>{manifest['content']['text_sha256']}</code></td></tr><tr><td>Recipients</td><td><code>{manifest['recipient_hash']}</code></td></tr><tr><td>Template</td><td><code>{html.escape(str(manifest['template']['id']))}@{html.escape(str(manifest['template']['version']))}</code></td></tr></tbody></table></section>
<script type="application/json" id="relay-approval-manifest">{embedded}</script>
</main></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    try:
        repo, run = args.repository_root.resolve(), args.run.resolve()
        manifest = build_approval_manifest(repo, run)
        (run / "approval-manifest.json").write_bytes(pretty_json(manifest))
        (run / "review.html").write_text(sheet(manifest, run), encoding="utf-8")
        append_event(instance_root(repo) / "state" / "workflow.jsonl", workflow_event(repo, manifest, "rendered", run=str(run.relative_to(repo))))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2
    print(json.dumps({"status": "ok", "review": str(run / "review.html"), "manifest_sha256": manifest["manifest_sha256"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
