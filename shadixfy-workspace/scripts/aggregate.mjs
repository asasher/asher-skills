#!/usr/bin/env node
// Aggregate one iteration into benchmark.json.
// Computes, per (agent, condition): mean auto_pass_rate, mean duration_ms,
// mean total_tokens. Adds deltas of each skill condition vs the no_skill
// baseline, per agent. Also prints a compact table.
//
// Usage: node aggregate.mjs [iteration=1]

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.resolve(__dirname, "..");
const REPO = path.resolve(WORKSPACE, "..");
const EVALS = JSON.parse(fs.readFileSync(path.join(REPO, "skills/shadixfy/evals/evals.json"), "utf8"));

const iter = process.argv[2] || "1";
const iterDir = path.join(WORKSPACE, `iteration-${iter}`);
const AGENTS = EVALS.agents || ["claude", "codex"];
const CONDITIONS = EVALS.conditions || ["no_skill", "uncodixfy", "shadixfy"];
const evalIds = EVALS.evals.map((e) => e.id);

const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
const round = (x, n = 3) => (x == null ? null : +x.toFixed(n));

function readJSON(p) { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } }

const cells = {}; // agent -> condition -> {pass[], dur[], tok[], n}
for (const agent of AGENTS) {
  cells[agent] = {};
  for (const cond of CONDITIONS) {
    const pass = [], dur = [], tok = [];
    for (const id of evalIds) {
      const dir = path.join(iterDir, id, agent, cond);
      const g = readJSON(path.join(dir, "grading.json"));
      const t = readJSON(path.join(dir, "timing.json"));
      if (g?.summary?.auto_pass_rate != null) pass.push(g.summary.auto_pass_rate);
      if (t?.duration_ms != null) dur.push(t.duration_ms);
      if (t?.total_tokens != null) tok.push(t.total_tokens);
    }
    cells[agent][cond] = {
      auto_pass_rate: round(mean(pass)),
      duration_ms: round(mean(dur), 0),
      total_tokens: round(mean(tok), 0),
      n_graded: pass.length,
    };
  }
}

const benchmark = { iteration: iter, agents: AGENTS, conditions: CONDITIONS, by_agent: {} };
for (const agent of AGENTS) {
  const base = cells[agent].no_skill;
  const deltas = {};
  for (const cond of CONDITIONS) {
    if (cond === "no_skill") continue;
    const c = cells[agent][cond];
    deltas[cond] = {
      auto_pass_rate: c.auto_pass_rate != null && base.auto_pass_rate != null ? round(c.auto_pass_rate - base.auto_pass_rate) : null,
      duration_ms: c.duration_ms != null && base.duration_ms != null ? c.duration_ms - base.duration_ms : null,
      total_tokens: c.total_tokens != null && base.total_tokens != null ? c.total_tokens - base.total_tokens : null,
    };
  }
  benchmark.by_agent[agent] = { conditions: cells[agent], delta_vs_no_skill: deltas };
}

fs.writeFileSync(path.join(iterDir, "benchmark.json"), JSON.stringify(benchmark, null, 2) + "\n");

// Pretty print.
console.log(`\nbenchmark — iteration ${iter} (auto_pass_rate / dur_ms / tokens)`);
for (const agent of AGENTS) {
  console.log(`\n  ${agent}`);
  for (const cond of CONDITIONS) {
    const c = cells[agent][cond];
    const d = benchmark.by_agent[agent].delta_vs_no_skill[cond];
    const dStr = d && d.auto_pass_rate != null ? `   Δpass ${d.auto_pass_rate >= 0 ? "+" : ""}${d.auto_pass_rate}` : "";
    console.log(`    ${cond.padEnd(10)} pass=${c.auto_pass_rate ?? "—"}  dur=${c.duration_ms ?? "—"}  tok=${c.total_tokens ?? "—"}  (n=${c.n_graded})${dStr}`);
  }
}
console.log(`\nwrote ${path.relative(REPO, path.join(iterDir, "benchmark.json"))}`);
console.log("Note: auto_pass_rate covers mechanical assertions only. Fill manual/visual grades, then re-run.\n");
