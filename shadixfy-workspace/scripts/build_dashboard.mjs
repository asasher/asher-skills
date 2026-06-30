#!/usr/bin/env node
// Build a self-contained review dashboard from the eval workspace.
// Scans iteration-*/ for benchmark/grading/timing/feedback + screenshots,
// inlines the data, and writes shadixfy-workspace/dashboard.html.
// Open it directly (file://) — no server needed; screenshots load by relative path.
//
// Usage: node scripts/build_dashboard.mjs

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.resolve(__dirname, "..");
const REPO = path.resolve(WORKSPACE, "..");
const EVALS = JSON.parse(fs.readFileSync(path.join(REPO, "skills/shadixfy/evals/evals.json"), "utf8"));

const readJSON = (p) => { try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; } };
const exists = (p) => { try { return fs.existsSync(p); } catch { return false; } };

const AGENTS = EVALS.agents || ["claude", "codex"];
const CONDITIONS = EVALS.conditions || ["no_skill", "uncodixfy", "shadixfy"];
const evalMeta = {};
for (const e of EVALS.evals) evalMeta[e.id] = { prompt: e.prompt, expected: e.expected_output, assertions: e.assertions };
const evalIds = EVALS.evals.map((e) => e.id);

// Discover iterations.
const iterations = fs.readdirSync(WORKSPACE)
  .filter((d) => /^iteration-\d+$/.test(d) && fs.statSync(path.join(WORKSPACE, d)).isDirectory())
  .map((d) => d.replace("iteration-", ""))
  .sort((a, b) => Number(a) - Number(b));

const data = {
  generatedAt: new Date().toISOString(),
  skill: EVALS.skill_name,
  agents: AGENTS, conditions: CONDITIONS, evals: evalIds, evalMeta,
  iterations, benchmark: {}, feedback: {}, cells: {},
};

for (const it of iterations) {
  const itDir = path.join(WORKSPACE, `iteration-${it}`);
  data.benchmark[it] = readJSON(path.join(itDir, "benchmark.json"));
  data.feedback[it] = readJSON(path.join(itDir, "feedback.json"));
  data.cells[it] = {};
  for (const ev of evalIds) for (const ag of AGENTS) for (const cd of CONDITIONS) {
    const cell = path.join(itDir, ev, ag, cd);
    if (!exists(cell)) continue;
    const shot = path.join(cell, "outputs", "screenshot.png");
    data.cells[it][`${ev}|${ag}|${cd}`] = {
      screenshot: exists(shot) ? path.relative(WORKSPACE, shot) : null,
      hasHtml: exists(path.join(cell, "outputs", "index.html")),
      htmlPath: path.relative(WORKSPACE, path.join(cell, "outputs", "index.html")),
      grading: readJSON(path.join(cell, "grading.json")),
      timing: readJSON(path.join(cell, "timing.json")),
    };
  }
}

const html = `<!doctype html>
<html lang="en" class="">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>shadixfy · eval review</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --background:0 0% 100%;--foreground:240 10% 3.9%;--card:0 0% 100%;--card-foreground:240 10% 3.9%;
  --popover:0 0% 100%;--popover-foreground:240 10% 3.9%;--primary:240 5.9% 10%;--primary-foreground:0 0% 98%;
  --secondary:240 4.8% 95.9%;--secondary-foreground:240 5.9% 10%;--muted:240 4.8% 95.9%;--muted-foreground:240 3.8% 46.1%;
  --accent:240 4.8% 95.9%;--accent-foreground:240 5.9% 10%;--destructive:0 72% 51%;--destructive-foreground:0 0% 98%;
  --success:142 71% 45%;--border:240 5.9% 90%;--input:240 5.9% 90%;--ring:240 10% 3.9%;--radius:.5rem;
}
.dark{
  --background:240 10% 3.9%;--foreground:0 0% 98%;--card:240 10% 3.9%;--card-foreground:0 0% 98%;
  --popover:240 10% 3.9%;--popover-foreground:0 0% 98%;--primary:0 0% 98%;--primary-foreground:240 5.9% 10%;
  --secondary:240 3.7% 15.9%;--secondary-foreground:0 0% 98%;--muted:240 3.7% 15.9%;--muted-foreground:240 5% 64.9%;
  --accent:240 3.7% 15.9%;--accent-foreground:0 0% 98%;--destructive:0 62.8% 45%;--destructive-foreground:0 0% 98%;
  --success:142 65% 47%;--border:240 3.7% 15.9%;--input:240 3.7% 15.9%;--ring:240 4.9% 83.9%;
}
*{box-sizing:border-box;border-color:hsl(var(--border))}
html,body{margin:0}
body{background:hsl(var(--background));color:hsl(var(--foreground));font-family:Geist,ui-sans-serif,system-ui,sans-serif;font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
.mono{font-family:"Geist Mono",ui-monospace,monospace}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
header{position:sticky;top:0;z-index:30;background:hsl(var(--background)/.8);backdrop-filter:blur(8px);border-bottom:1px solid hsl(var(--border))}
.hrow{display:flex;align-items:center;gap:16px;height:56px}
.brand{display:flex;align-items:center;gap:10px;font-weight:600}
.logo{width:26px;height:26px;border-radius:7px;background:hsl(var(--primary));color:hsl(var(--primary-foreground));display:grid;place-items:center;font-weight:700;font-size:13px}
.sub{color:hsl(var(--muted-foreground));font-weight:400;font-size:12.5px}
.spacer{flex:1}
.btn{height:34px;padding:0 12px;border-radius:calc(var(--radius) - 2px);border:1px solid hsl(var(--border));background:hsl(var(--background));color:inherit;font:inherit;font-size:13px;font-weight:500;display:inline-flex;align-items:center;gap:7px;cursor:pointer}
.btn:hover{background:hsl(var(--accent))}
.btn.icon{width:34px;padding:0;justify-content:center}
select.btn{padding-right:8px}
h2{font-size:15px;font-weight:600;margin:0}
.muted{color:hsl(var(--muted-foreground))}
section{padding:28px 0;border-bottom:1px solid hsl(var(--border))}
.sec-head{display:flex;align-items:baseline;gap:10px;margin-bottom:16px}
.sec-head .muted{font-size:12.5px}
/* table */
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:10px 12px;border-bottom:1px solid hsl(var(--border));white-space:nowrap}
th{font-weight:500;color:hsl(var(--muted-foreground));font-size:12px}
tbody tr:hover{background:hsl(var(--muted)/.5)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.bar{position:relative;height:6px;width:120px;background:hsl(var(--muted));border-radius:99px;overflow:hidden;display:inline-block;vertical-align:middle;margin-right:8px}
.bar>i{position:absolute;left:0;top:0;bottom:0;background:hsl(var(--primary));border-radius:99px}
.cond-pill{font-size:11px;font-weight:500;padding:2px 8px;border-radius:99px;border:1px solid hsl(var(--border));color:hsl(var(--muted-foreground))}
.cond-shadixfy{border-color:transparent;background:hsl(var(--primary));color:hsl(var(--primary-foreground))}
.cond-uncodixfy{background:hsl(var(--secondary));color:hsl(var(--secondary-foreground))}
.badge{font-size:11px;font-weight:500;padding:2px 8px;border-radius:99px;border:1px solid hsl(var(--border));display:inline-flex;gap:5px;align-items:center}
.badge.ok{border-color:transparent;background:hsl(var(--success)/.14);color:hsl(var(--success))}
.badge.bad{border-color:transparent;background:hsl(var(--destructive)/.14);color:hsl(var(--destructive))}
.badge.warn{border-color:transparent;background:hsl(45 90% 50%/.16);color:hsl(38 80% 38%)}
.dark .badge.warn{color:hsl(45 90% 62%)}
.dot{width:6px;height:6px;border-radius:99px;background:currentColor}
.delta-pos{color:hsl(var(--success))}.delta-neg{color:hsl(var(--destructive))}
/* tabs/filters */
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tab{height:32px;padding:0 12px;border-radius:calc(var(--radius) - 2px);border:1px solid transparent;background:transparent;color:hsl(var(--muted-foreground));font:inherit;font-size:13px;font-weight:500;cursor:pointer}
.tab:hover{background:hsl(var(--accent));color:hsl(var(--foreground))}
.tab[aria-selected=true]{background:hsl(var(--secondary));color:hsl(var(--foreground))}
.filterbar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px}
.chiprow{display:flex;gap:6px;align-items:center}
.label-xs{font-size:11px;text-transform:none;color:hsl(var(--muted-foreground))}
/* gallery */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:880px){.grid{grid-template-columns:1fr}}
.cardx{border:1px solid hsl(var(--border));border-radius:var(--radius);background:hsl(var(--card));overflow:hidden;display:flex;flex-direction:column}
.thumb{position:relative;aspect-ratio:16/11;background:hsl(var(--muted));overflow:hidden;cursor:pointer;border-bottom:1px solid hsl(var(--border))}
.thumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .25s ease}
.thumb:hover img{transform:scale(1.015)}
.thumb .empty{position:absolute;inset:0;display:grid;place-items:center;color:hsl(var(--muted-foreground));font-size:12px}
.cardx .meta{padding:11px 13px;display:flex;flex-direction:column;gap:9px}
.metarow{display:flex;align-items:center;justify-content:space-between;gap:8px}
.agent{font-weight:600;font-size:13px;text-transform:capitalize}
.foot{display:flex;gap:12px;color:hsl(var(--muted-foreground));font-size:12px}
.foot .mono{font-size:11.5px}
/* modal */
.ov{position:fixed;inset:0;z-index:50;background:hsl(240 10% 3.9%/.55);backdrop-filter:blur(3px);display:none;align-items:stretch;justify-content:center;padding:28px}
.ov.open{display:flex}
.modal{background:hsl(var(--background));border:1px solid hsl(var(--border));border-radius:var(--radius);width:min(1080px,100%);max-height:100%;display:grid;grid-template-columns:1.35fr 1fr;overflow:hidden}
@media(max-width:820px){.modal{grid-template-columns:1fr;overflow:auto}}
.mshot{background:hsl(var(--muted));overflow:auto;border-right:1px solid hsl(var(--border))}
.mshot img{width:100%;display:block}
.mside{display:flex;flex-direction:column;min-height:0}
.mhead{padding:16px 18px;border-bottom:1px solid hsl(var(--border));display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.mttl{font-weight:600;font-size:15px}
.mbody{padding:16px 18px;overflow:auto;display:flex;flex-direction:column;gap:18px}
.kv{display:flex;gap:10px;flex-wrap:wrap}
.asrt{display:flex;gap:9px;padding:9px 0;border-bottom:1px solid hsl(var(--border));font-size:12.5px;align-items:flex-start}
.asrt:last-child{border-bottom:0}
.ic{flex:0 0 16px;width:16px;height:16px;border-radius:99px;display:grid;place-items:center;font-size:11px;margin-top:1px;font-weight:700}
.ic.ok{background:hsl(var(--success)/.16);color:hsl(var(--success))}
.ic.bad{background:hsl(var(--destructive)/.16);color:hsl(var(--destructive))}
.ic.man{background:hsl(var(--muted));color:hsl(var(--muted-foreground))}
.asrt .ev{color:hsl(var(--muted-foreground));font-size:11.5px;margin-top:2px}
details{font-size:12.5px}details summary{cursor:pointer;color:hsl(var(--muted-foreground))}
pre{white-space:pre-wrap;background:hsl(var(--muted));padding:11px;border-radius:8px;font-size:11.5px;margin:8px 0 0}
.fb{border:1px solid hsl(var(--border));border-radius:var(--radius);padding:14px 16px;background:hsl(var(--card));font-size:13px;color:hsl(var(--muted-foreground))}
.fb b{color:hsl(var(--foreground));font-weight:600}
.fb ul{margin:8px 0 0;padding-left:18px}.fb li{margin:5px 0}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:hsl(var(--muted-foreground));margin-top:6px}
.x{border:0;background:transparent;color:hsl(var(--muted-foreground));cursor:pointer;font-size:18px;line-height:1}
</style>
</head>
<body>
<header><div class="wrap hrow">
  <div class="brand"><span class="logo">sx</span>shadixfy <span class="sub">eval review</span></div>
  <div class="spacer"></div>
  <label class="sub" style="display:flex;align-items:center;gap:7px">iteration
    <select id="iter" class="btn"></select>
  </label>
  <button class="btn icon" id="theme" title="Toggle theme">◐</button>
</div></header>

<div class="wrap">
  <section id="summary">
    <div class="sec-head"><h2>Benchmark</h2><span class="muted" id="bench-note"></span></div>
    <div id="bench"></div>
    <div class="legend">
      <span>auto_pass_rate = mechanical assertions only (anti-Codex hygiene + shadcn checks).</span>
      <span>Δ vs no-skill per agent.</span>
    </div>
  </section>

  <section id="gallery">
    <div class="sec-head"><h2>Outputs</h2><span class="muted">click any frame to inspect grading, timing &amp; prompt</span></div>
    <div class="filterbar">
      <div class="tabs" id="evaltabs"></div>
      <div class="spacer"></div>
      <div class="chiprow"><span class="label-xs">agent</span><div class="tabs" id="agentfilter"></div></div>
    </div>
    <div class="grid" id="cards"></div>
  </section>

  <section id="feedback-sec" style="border-bottom:0">
    <div class="sec-head"><h2>Review notes</h2><span class="muted">human / agent pass — iteration <span id="fb-it"></span></span></div>
    <div id="feedback"></div>
  </section>
</div>

<div class="ov" id="ov"><div class="modal">
  <div class="mshot"><img id="m-img" alt=""/></div>
  <div class="mside">
    <div class="mhead">
      <div><div class="mttl" id="m-ttl"></div><div class="muted" id="m-sub" style="font-size:12.5px;margin-top:2px"></div></div>
      <button class="x" id="m-x">✕</button>
    </div>
    <div class="mbody">
      <div class="kv" id="m-badges"></div>
      <div><div class="label-xs" style="margin-bottom:8px">Assertions</div><div id="m-asserts"></div></div>
      <details id="m-promptwrap"><summary>Prompt &amp; expected output</summary><div id="m-prompt"></div></details>
    </div>
  </div>
</div></div>

<script>
const D = ${JSON.stringify(data)};
const $ = (s,r=document)=>r.querySelector(s);
const el = (t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
const condClass = c=>c==='shadixfy'?'cond-pill cond-shadixfy':c==='uncodixfy'?'cond-pill cond-uncodixfy':'cond-pill';
const condLabel = {no_skill:'no skill',uncodixfy:'uncodixfy',shadixfy:'shadixfy'};
const fmtTok = n=>n==null?'—':(n>=1000?(n/1000).toFixed(1)+'k':n);
const fmtSec = ms=>ms==null?'—':(ms/1000).toFixed(0)+'s';
const pct = v=>v==null?'—':Math.round(v*100)+'%';

let state={iter:D.iterations[D.iterations.length-1]||'1',evalId:D.evals[0],agent:'all'};

// theme
const setTheme=t=>{document.documentElement.classList.toggle('dark',t==='dark');localStorage.shadixfyTheme=t};
setTheme(localStorage.shadixfyTheme||'light');
$('#theme').onclick=()=>setTheme(document.documentElement.classList.contains('dark')?'light':'dark');

// iteration select
const iterSel=$('#iter');
D.iterations.forEach(it=>{const o=el('option');o.value=it;o.textContent='#'+it;iterSel.append(o)});
iterSel.value=state.iter;
iterSel.onchange=()=>{state.iter=iterSel.value;renderAll()};

function renderBench(){
  const b=D.benchmark[state.iter];
  const host=$('#bench');host.innerHTML='';
  $('#bench-note').textContent='iteration #'+state.iter+(b?'':' — no benchmark.json');
  if(!b){return}
  const t=el('table');
  t.innerHTML='<thead><tr><th>Agent</th><th>Condition</th><th>Pass</th><th class="num">Δ pass</th><th class="num">Tokens</th><th class="num">Time</th></tr></thead>';
  const tb=el('tbody');
  D.agents.forEach(ag=>{
    const ad=b.by_agent&&b.by_agent[ag];if(!ad)return;
    D.conditions.forEach((cd,i)=>{
      const c=ad.conditions[cd]||{};const d=ad.delta_vs_no_skill&&ad.delta_vs_no_skill[cd];
      const tr=el('tr');
      tr.append(el('td',null,i===0?'<b>'+ag+'</b>':''));
      tr.append(el('td',null,'<span class="'+condClass(cd)+'">'+condLabel[cd]+'</span>'));
      const pr=c.auto_pass_rate;
      tr.append(el('td',null,'<span class="bar"><i style="width:'+Math.round((pr||0)*100)+'%"></i></span>'+pct(pr)));
      let dd='—';if(d&&d.auto_pass_rate!=null){const v=d.auto_pass_rate;dd='<span class="'+(v>=0?'delta-pos':'delta-neg')+'">'+(v>=0?'+':'')+Math.round(v*100)+'%</span>'}
      tr.append(el('td','num',dd));
      tr.append(el('td','num mono',fmtTok(c.total_tokens)));
      tr.append(el('td','num mono',fmtSec(c.duration_ms)));
      tb.append(tr);
    });
  });
  t.append(tb);host.append(t);
}

function gradeBadge(g){
  if(!g)return '<span class="badge">no html</span>';
  const s=g.summary||{};const ok=s.auto_passed||0,tot=s.auto_total||0;
  const cls=tot&&ok===tot?'ok':ok>=Math.ceil(tot*0.7)?'warn':'bad';
  return '<span class="badge '+cls+'"><span class="dot"></span>'+ok+'/'+tot+(s.manual_pending?' · '+s.manual_pending+' man':'')+'</span>';
}

function renderTabs(){
  const et=$('#evaltabs');et.innerHTML='';
  D.evals.forEach(ev=>{const b=el('button','tab',ev);b.setAttribute('aria-selected',ev===state.evalId);b.onclick=()=>{state.evalId=ev;renderCards();renderTabs()};et.append(b)});
  const af=$('#agentfilter');af.innerHTML='';
  ['all',...D.agents].forEach(a=>{const b=el('button','tab',a);b.setAttribute('aria-selected',a===state.agent);b.onclick=()=>{state.agent=a;renderCards();renderTabs()};af.append(b)});
}

function renderCards(){
  const host=$('#cards');host.innerHTML='';
  const cells=D.cells[state.iter]||{};
  const agents=state.agent==='all'?D.agents:[state.agent];
  agents.forEach(ag=>{
    D.conditions.forEach(cd=>{
      const key=state.evalId+'|'+ag+'|'+cd;const cell=cells[key];
      const card=el('div','cardx');
      const thumb=el('div','thumb');
      if(cell&&cell.screenshot){const img=el('img');img.src=cell.screenshot;img.loading='lazy';img.alt=key;thumb.append(img)}
      else thumb.append(el('div','empty',cell?'no screenshot':'no run'));
      thumb.onclick=()=>openModal(key,cell);
      card.append(thumb);
      const meta=el('div','meta');
      const r1=el('div','metarow');
      r1.append(el('span',condClass(cd),condLabel[cd]));
      r1.innerHTML+=gradeBadge(cell&&cell.grading);
      meta.append(r1);
      const r2=el('div','metarow');
      r2.append(el('span','agent',ag));
      const t=cell&&cell.timing||{};
      r2.append(el('div','foot','<span class="mono">'+fmtTok(t.total_tokens)+'</span><span class="mono">'+fmtSec(t.duration_ms)+'</span>'));
      meta.append(r2);
      card.append(meta);host.append(card);
    });
  });
}

function openModal(key,cell){
  const [ev,ag,cd]=key.split('|');
  $('#m-ttl').textContent=ev+' · '+ag;
  $('#m-sub').innerHTML='<span class="'+condClass(cd)+'">'+condLabel[cd]+'</span>';
  const img=$('#m-img');if(cell&&cell.screenshot){img.src=cell.screenshot;img.style.display='block'}else{img.removeAttribute('src');img.style.display='none'}
  const g=cell&&cell.grading,t=cell&&cell.timing||{};
  $('#m-badges').innerHTML=gradeBadge(g)+
    '<span class="badge"><span class="mono">'+fmtTok(t.total_tokens)+'</span> tokens</span>'+
    '<span class="badge"><span class="mono">'+fmtSec(t.duration_ms)+'</span></span>'+
    (cell&&cell.hasHtml?'<a class="badge" href="'+cell.htmlPath+'" target="_blank">open html ↗</a>':'');
  const ah=$('#m-asserts');ah.innerHTML='';
  ((g&&g.assertion_results)||[]).forEach(a=>{
    const row=el('div','asrt');
    const icon=a.manual?'<span class="ic man">~</span>':a.passed?'<span class="ic ok">✓</span>':'<span class="ic bad">✕</span>';
    row.innerHTML=icon+'<div><div>'+a.text+'</div><div class="ev">'+(a.evidence||'')+'</div></div>';
    ah.append(row);
  });
  if(!g||!g.assertion_results)ah.innerHTML='<div class="muted" style="font-size:12.5px">No grading recorded.</div>';
  const m=D.evalMeta[ev]||{};
  $('#m-prompt').innerHTML='<pre>'+(m.prompt||'').replace(/</g,'&lt;')+'</pre><div class="label-xs" style="margin-top:10px">Expected</div><pre>'+(m.expected||'').replace(/</g,'&lt;')+'</pre>';
  $('#ov').classList.add('open');
}
$('#m-x').onclick=()=>$('#ov').classList.remove('open');
$('#ov').onclick=e=>{if(e.target.id==='ov')$('#ov').classList.remove('open')};
document.addEventListener('keydown',e=>{if(e.key==='Escape')$('#ov').classList.remove('open')});

function renderFeedback(){
  $('#fb-it').textContent='#'+state.iter;
  const fb=D.feedback[state.iter];const host=$('#feedback');host.innerHTML='';
  if(!fb){host.innerHTML='<div class="muted">No feedback.json for this iteration.</div>';return}
  const notes=Object.entries(fb).filter(([k,v])=>!k.startsWith('_')&&typeof v==='string'&&v.trim());
  const box=el('div','fb');
  if(notes.length){box.innerHTML=notes.map(([k,v])=>'<div style="margin:6px 0"><b>'+k+'</b> — '+v+'</div>').join('')}
  const cands=fb._iteration_candidates;
  if(cands&&cands.length){box.innerHTML+='<div style="margin-top:12px"><b>Iteration candidates</b><ul>'+cands.map(c=>'<li>'+c+'</li>').join('')+'</ul></div>'}
  host.append(box);
}

function renderAll(){renderBench();renderTabs();renderCards();renderFeedback()}
renderAll();
</script>
</body></html>`;

const out = path.join(WORKSPACE, "dashboard.html");
fs.writeFileSync(out, html);
console.log(`wrote ${path.relative(REPO, out)} (${(html.length/1024).toFixed(0)}kb) — open it in a browser`);
console.log(`iterations: ${iterations.join(", ") || "none"} · cells: ${Object.values(data.cells).reduce((a,c)=>a+Object.keys(c).length,0)}`);
