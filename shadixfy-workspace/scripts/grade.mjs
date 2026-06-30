#!/usr/bin/env node
// Mechanical grader for one eval cell.
// Reads the eval's assertions from evals.json, auto-grades the objectively
// checkable ones against outputs/index.html, and marks the rest manual:true
// for the human/LLM visual review pass. Writes grading.json into the cell dir.
//
// Usage: node grade.mjs <eval_id> <cell_dir>
//   cell_dir is .../iteration-N/<eval>/<agent>/<condition>

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(__dirname, "../..");
const EVALS = JSON.parse(fs.readFileSync(path.join(REPO, "skills/shadixfy/evals/evals.json"), "utf8"));

const [evalId, cellDir] = process.argv.slice(2);
if (!evalId || !cellDir) { console.error("usage: grade.mjs <eval_id> <cell_dir>"); process.exit(1); }

const ev = EVALS.evals.find((e) => e.id === evalId);
if (!ev) { console.error(`no eval '${evalId}'`); process.exit(1); }

const htmlPath = path.join(cellDir, "outputs", "index.html");
const html = fs.existsSync(htmlPath) ? fs.readFileSync(htmlPath, "utf8") : "";
const lc = html.toLowerCase();

// ---- detectors -------------------------------------------------------------
const TW_RADIUS = { "rounded-sm": 2, "rounded-md": 6, "rounded-lg": 8, "rounded-xl": 12, "rounded-2xl": 16, "rounded-3xl": 24, "rounded": 4 };

function maxRadiusPx() {
  let max = 0; const hits = [];
  // CSS border-radius values
  for (const m of html.matchAll(/border-radius\s*:\s*([0-9.]+)(px|rem)/gi)) {
    const px = m[2].toLowerCase() === "rem" ? parseFloat(m[1]) * 16 : parseFloat(m[1]);
    if (px > max) { max = px; }
    hits.push(`${m[1]}${m[2]}`);
  }
  // Tailwind rounded-* classes (exclude rounded-full = pills/avatars, handled separately)
  for (const [cls, px] of Object.entries(TW_RADIUS)) {
    const re = new RegExp(`(?:^|[\\s"'])${cls}(?:[\\s"'/]|$)`, "g");
    if (re.test(html) && px > max) { max = px; hits.push(cls); }
  }
  return { max, hits: [...new Set(hits)] };
}
function fullPills() { return (html.match(/rounded-full/g) || []).length; }

function find(re) { const m = [...html.matchAll(re)].map((x) => x[0]); return [...new Set(m)]; }

const D = {
  gradients: () => find(/(linear|radial|conic)-gradient|bg-gradient-to-/gi),
  glass: () => find(/backdrop-filter\s*:\s*blur|backdrop-blur/gi),
  badFonts: () => {
    const bad = [];
    for (const f of ["inter", "roboto", "segoe ui", "trebuchet", "arial"]) {
      if (lc.includes(`family=${f}`) || new RegExp(`font-family[^;}]*${f}`, "i").test(html) || lc.includes(`'${f}'`) || lc.includes(`"${f}"`)) bad.push(f);
    }
    return bad;
  },
  geist: () => /geist/i.test(html),
  blueAccent: () => find(/bg-(blue|indigo|sky|cyan|violet|fuchsia)-[0-9]{3}|#[0-9a-f]*(?:)/gi).filter((s) => /bg-(blue|indigo|sky|cyan|violet|fuchsia)-/i.test(s)),
  bigShadow: () => {
    const hits = find(/shadow-2xl/gi);
    for (const m of html.matchAll(/box-shadow\s*:\s*[^;}]+/gi)) {
      const lens = [...m[0].matchAll(/([0-9.]+)px/g)].map((x) => parseFloat(x[1]));
      if (lens.length >= 3 && lens[2] > 24) hits.push(m[0].slice(0, 60));
    }
    return [...new Set(hits)];
  },
  eyebrow: () => {
    // uppercase + letter-spacing/tracking co-occurring = classic eyebrow kicker
    const css = /text-transform\s*:\s*uppercase/i.test(html) && /letter-spacing/i.test(html);
    const tw = /uppercase/.test(html) && /tracking-(wide|wider|widest)/.test(html);
    return css || tw;
  },
};

// ---- assertion router ------------------------------------------------------
// Returns {passed, evidence} for auto-gradable assertions, or null for manual.
function autoGrade(a) {
  const t = a.toLowerCase();

  if (t.includes("renders without errors")) return null; // needs the screenshot

  if (t.includes("gradient") && t.startsWith("no")) {
    const g = D.gradients(); return { passed: g.length === 0, evidence: g.length ? `found: ${g.slice(0,5).join(", ")}` : "no gradient backgrounds detected" };
  }
  if (t.includes("gradient text") || (t.includes("gradient") && t.includes("hero"))) {
    const g = D.gradients(); return { passed: g.length === 0, evidence: g.length ? `gradient usage: ${g.slice(0,5).join(", ")}` : "no gradient/hero gradient detected" };
  }
  if (t.includes("glassmorphism") || t.includes("backdrop-filter") || (t.includes("blur") && !t.includes("blur radius"))) {
    const g = D.glass(); return { passed: g.length === 0, evidence: g.length ? `found: ${g.join(", ")}` : "no backdrop blur detected" };
  }
  if (t.includes("border-radius") || t.includes("radius")) {
    const r = maxRadiusPx(); const pills = fullPills();
    return { passed: r.max <= 16, evidence: `max non-full radius ~${r.max}px (${r.hits.join(", ") || "n/a"}); rounded-full uses: ${pills}` };
  }
  if (t.includes("box-shadow") || (t.includes("shadow") && (t.includes("blur radius") || t.includes("colored")))) {
    const s = D.bigShadow(); return { passed: s.length === 0, evidence: s.length ? `heuristic: ${s.slice(0,4).join(" | ")}` : "no oversized shadow detected (heuristic)" };
  }
  if (t.includes("font is geist") || (t.includes("font") && t.includes("not inter"))) {
    const bad = D.badFonts(); return { passed: bad.length === 0, evidence: bad.length ? `banned font(s): ${bad.join(", ")}` : (D.geist() ? "Geist referenced" : "no banned font; (Geist not explicitly found — verify system stack)") };
  }
  if (t.includes("not blue") || t.includes("restrained hue") || (t.includes("accent") && t.includes("neutral"))) {
    const b = D.blueAccent(); return { passed: b.length === 0, evidence: b.length ? `heuristic: saturated cool utilities ${[...new Set(b)].slice(0,6).join(", ")}` : "no obvious blue/indigo/cyan accent utilities (heuristic — confirm visually)" };
  }
  if (t.includes("eyebrow") || t.includes("kicker") || (t.includes("uppercase") && t.includes("letter-spacing"))) {
    const e = D.eyebrow(); return { passed: !e, evidence: e ? "uppercase + letter-spacing/tracking co-occur (likely eyebrow)" : "no eyebrow kicker pattern detected (heuristic)" };
  }
  if (t.includes("glows") || t.includes("conic-gradient")) {
    const g = D.gradients().filter((x) => /conic/i.test(x)); return { passed: g.length === 0, evidence: g.length ? `conic gradient(s): ${g.join(", ")}` : "no conic-gradient glow detected" };
  }
  if (t.includes("not full-width pills") || t.includes("pill")) {
    const pills = fullPills(); return { passed: true, evidence: `rounded-full uses: ${pills} (manual: confirm these are avatars/toggles, not buttons/cards)` };
  }
  return null; // visual / structural → human review
}

const assertion_results = ev.assertions.map((text) => {
  const r = autoGrade(text);
  return r === null
    ? { text, manual: true, passed: null, evidence: "manual review (visual/structural)" }
    : { text, manual: false, passed: r.passed, evidence: r.evidence };
});

const auto = assertion_results.filter((a) => !a.manual);
const passed = auto.filter((a) => a.passed).length;
const failed = auto.filter((a) => !a.passed).length;
const manual = assertion_results.filter((a) => a.manual).length;

const grading = {
  eval_id: evalId,
  html_present: html.length > 0,
  assertion_results,
  summary: {
    auto_passed: passed,
    auto_failed: failed,
    auto_total: auto.length,
    auto_pass_rate: auto.length ? +(passed / auto.length).toFixed(3) : null,
    manual_pending: manual,
  },
};

fs.writeFileSync(path.join(cellDir, "grading.json"), JSON.stringify(grading, null, 2) + "\n");
console.log(`   graded ${evalId} @ ${path.relative(REPO, cellDir)}: auto ${passed}/${auto.length} pass, ${manual} manual`);
