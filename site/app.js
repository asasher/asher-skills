/* asher-skills documentation app — v2 (full-screen graphs, sheet reader, multi-view).
 * Drift design: node content and dependency edges come from the real files (SKILL.md fetched live,
 * frontmatter parsed from the same bytes the reader sees). Only rosters/lanes/blurbs live in views/*.json,
 * gated by site/check.py. See site/MAINTENANCE.md. */
(() => {
  const params = new URLSearchParams(location.search);
  const BASE = (params.get('base') || '..').replace(/\/$/, '');
  const VIEW_IDS = ['sdlc', 'flow', 'backlog'];
  const md = window.markdownit({ html: false, linkify: true });

  const state = { views: {}, fm: {}, current: 'sdlc', active: null };

  const $ = (s) => document.querySelector(s);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'class') n.className = v; else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v);
    }
    for (const k of kids) n.append(k);
    return n;
  };
  const svgEl = (tag, attrs = {}) => {
    const n = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    return n;
  };

  async function fetchText(path) {
    const r = await fetch(`${BASE}/${path}`);
    if (!r.ok) throw new Error(`${r.status} — ${path}`);
    return r.text();
  }

  function parseFrontmatter(text) {
    const m = text.match(/^---\n([\s\S]*?)\n---\n?/);
    if (!m) return { fm: {}, body: text };
    const fm = {};
    for (const line of m[1].split('\n')) {
      const kv = line.match(/^\s{0,2}([a-zA-Z-]+):\s*(.*)$/);
      if (!kv) continue;
      const [, key, raw] = kv;
      if (raw.startsWith('[{')) { try { fm[key] = JSON.parse(raw); } catch { fm[key] = raw; } }
      else if (raw.startsWith('[')) fm[key] = raw.replace(/^\[|\]$/g, '').split(',').map(s => s.trim()).filter(Boolean);
      else if (raw !== '') fm[key] = raw.replace(/^"|"$/g, '');
    }
    return { fm, body: text.slice(m[0].length) };
  }

  /* ---------- shared geometry ---------- */
  const NW = 172, NH = 54;
  const hashOff = (s) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return ((Math.abs(h) % 5) - 2) * 13; };

  function roundedElbow(x1, y1, x2, y2, r = 9) {
    if (Math.abs(x1 - x2) < 2) return `M ${x1} ${y1} L ${x2} ${y2}`;
    const my = (y1 + y2) / 2;
    const dirY = y2 > y1 ? 1 : -1, dirX = x2 > x1 ? 1 : -1;
    const rr = Math.min(r, Math.abs(x2 - x1) / 2, Math.abs(y2 - y1) / 2);
    return [
      `M ${x1} ${y1}`, `L ${x1} ${my - dirY * rr}`,
      `Q ${x1} ${my} ${x1 + dirX * rr} ${my}`, `L ${x2 - dirX * rr} ${my}`,
      `Q ${x2} ${my} ${x2} ${my + dirY * rr}`, `L ${x2} ${y2}`,
    ].join(' ');
  }
  function sideElbow(x1, y1, x2, y2, r = 9) {
    const mx = (x1 + x2) / 2;
    const dirX = x2 > x1 ? 1 : -1, dirY = y2 > y1 ? 1 : -1;
    if (Math.abs(y1 - y2) < 2) return `M ${x1} ${y1} L ${x2} ${y2}`;
    const rr = Math.min(r, Math.abs(x2 - x1) / 2, Math.abs(y2 - y1) / 2);
    return [
      `M ${x1} ${y1}`, `L ${mx - dirX * rr} ${y1}`,
      `Q ${mx} ${y1} ${mx} ${y1 + dirY * rr}`, `L ${mx} ${y2 - dirY * rr}`,
      `Q ${mx} ${y2} ${mx + dirX * rr} ${y2}`, `L ${x2} ${y2}`,
    ].join(' ');
  }

  function routeBetween(a, b, key) {
    const off = hashOff(key);
    const aC = { x: a.x + NW / 2 + off, y: a.y }, bC = { x: b.x + NW / 2 + off, y: b.y };
    const sameRow = Math.abs(a.y - b.y) < NH;
    if (sameRow) {
      const [l, r] = a.x < b.x ? [a, b] : [b, a];
      const y = a.y + NH / 2 + off / 2;
      const p = `M ${a.x < b.x ? a.x + NW : a.x} ${y} L ${a.x < b.x ? b.x : b.x + NW} ${y}`;
      return { d: p, mid: { x: (l.x + NW + r.x) / 2, y: y - 5 } };
    }
    if (b.y > a.y) {
      const d = roundedElbow(aC.x, a.y + NH, bC.x, b.y);
      return { d, mid: { x: (aC.x + bC.x) / 2, y: (a.y + NH + b.y) / 2 - 5 } };
    }
    const d = roundedElbow(aC.x, a.y, bC.x, b.y + NH);
    return { d, mid: { x: (aC.x + bC.x) / 2, y: (a.y + b.y + NH) / 2 - 5 } };
  }

  function nodeGroup(n, p, kind, extraClass = '') {
    const g = svgEl('g');
    g.setAttribute('class', `node k-${kind} ${extraClass}${state.active === n.id ? ' active' : ''}`);
    g.dataset.id = n.id;
    const rect = svgEl('rect', { x: p.x, y: p.y, width: NW, height: NH, rx: 8 });
    g.append(rect);
    const t = svgEl('text', { x: p.x + 10, y: p.y + 19, class: 't' });
    t.textContent = n.title; g.append(t);
    const words = (n.blurb || '').split(' '); const lines = ['', ''];
    for (const w of words) { if (lines[0].length + w.length < 30 && !lines[1]) lines[0] += w + ' '; else lines[1] += w + ' '; }
    lines.forEach((ln, i) => {
      if (!ln.trim()) return;
      const b = svgEl('text', { x: p.x + 10, y: p.y + 33 + i * 11, class: 'b' });
      b.textContent = ln.trim().slice(0, 33); g.append(b);
    });
    return g;
  }

  function attachHover(svg, adjacency) {
    svg.querySelectorAll('.node').forEach(g => {
      g.addEventListener('mouseenter', () => {
        svg.classList.add('dimming');
        const hot = adjacency[g.dataset.id] || new Set([g.dataset.id]);
        svg.querySelectorAll('.node').forEach(x => x.classList.toggle('hot', hot.has(x.dataset.id)));
        svg.querySelectorAll('.edge').forEach(e => e.classList.toggle('hot', e.dataset.from === g.dataset.id || e.dataset.to === g.dataset.id));
      });
      g.addEventListener('mouseleave', () => {
        svg.classList.remove('dimming');
        svg.querySelectorAll('.hot').forEach(x => x.classList.remove('hot'));
      });
    });
  }

  const arrowDefs = () => {
    const defs = svgEl('defs');
    defs.innerHTML = `<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor" opacity=".6"/></marker>`;
    return defs;
  };

  /* ---------- renderer: dependency graph (sdlc, backlog) ---------- */
  function renderGraph(view) {
    const pane = $('#graph-pane');
    const W = Math.max(980, Math.min(pane.clientWidth - 40, 1500));
    const GX = 18, GY = 16, LPAD = 12, LHEAD = 34, LGAP = 14;
    const perLane = {};
    for (const n of view.nodes) (perLane[n.lane] = perLane[n.lane] || []).push(n);
    if (view.id === 'sdlc') {
      for (const n of view.nodes) {
        const ext = (state.fm[n.id] && state.fm[n.id].external) || [];
        for (const e of (Array.isArray(ext) ? ext : [])) {
          if (typeof e !== 'object' || perLane[n.lane].some(x => x.id === e.name)) continue;
          perLane[n.lane].push({ id: e.name, title: e.name, blurb: `external · ${e.kind} · consent-gated`, external: e, lane: n.lane });
        }
      }
    }
    const pos = {}; let y = 0; const lanes = [];
    for (const lane of view.lanes) {
      const nodes = perLane[lane.id] || [];
      const cols = Math.max(1, Math.floor((W - 2 * LPAD + GX) / (NW + GX)));
      const rows = Math.ceil(nodes.length / cols) || 1;
      const h = LHEAD + rows * (NH + GY) + LPAD - GY + 6;
      lanes.push({ ...lane, y, h });
      nodes.forEach((n, i) => { pos[n.id] = { x: LPAD + (i % cols) * (NW + GX), y: y + LHEAD + Math.floor(i / cols) * (NH + GY), node: n }; });
      y += h + LGAP;
    }

    const svg = svgEl('svg', { viewBox: `0 0 ${W} ${y}`, width: W });
    svg.append(arrowDefs());
    for (const lane of lanes) {
      svg.append(svgEl('rect', { x: 2, y: lane.y, width: W - 4, height: lane.h, rx: 10, class: 'lane-bg' }));
      const t = svgEl('text', { x: LPAD + 2, y: lane.y + 16, class: 'lane-title' }); t.textContent = lane.title; svg.append(t);
      const b = svgEl('text', { x: LPAD + 4 + lane.title.length * 8.6, y: lane.y + 16, class: 'lane-blurb' }); b.textContent = '— ' + lane.blurb; svg.append(b);
    }

    const adjacency = {}; const touch = (a, b) => { (adjacency[a] = adjacency[a] || new Set([a])).add(b); (adjacency[b] = adjacency[b] || new Set([b])).add(a); };
    const edges = [];
    const addEdge = (from, to, cls, label) => {
      if (!pos[from] || !pos[to]) return;
      edges.push({ from, to, cls, label }); touch(from, to);
    };
    for (const f of view.flow || []) addEdge(f.from, f.to, 'flow', f.label);
    for (const e of view.edges || []) addEdge(e.from, e.to, e.style || '', e.label);
    if (view.id === 'sdlc') for (const n of view.nodes) {
      const fm = state.fm[n.id] || {};
      for (const r of fm.requires || []) addEdge(n.id, r, '');
      for (const o of fm.optional || []) addEdge(n.id, o, 'optional');
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) addEdge(n.id, e.name, 'external');
    }
    for (const e of edges) {
      const { d, mid } = routeBetween(pos[e.from], pos[e.to], e.from + e.to);
      const p = svgEl('path', { d, class: `edge ${e.cls}`, 'marker-end': 'url(#arr)' });
      p.dataset.from = e.from; p.dataset.to = e.to; svg.append(p);
      if (e.label) { const t = svgEl('text', { x: mid.x, y: mid.y, class: 'edge-label', 'text-anchor': 'middle' }); t.textContent = e.label; svg.append(t); }
    }

    for (const [id, p] of Object.entries(pos)) {
      const n = p.node;
      const kind = n.external ? n.lane : n.lane;
      const g = nodeGroup(n, p, kind, `${n.external ? 'external ' : ''}${id === 'merge-changes' ? 'gate' : ''}`);
      g.addEventListener('click', () => n.external ? window.open(n.external.source, '_blank') : openNode(view.id, id));
      svg.append(g);
    }
    pane.innerHTML = ''; pane.append(svg);
    attachHover(svg, adjacency);
  }

  /* ---------- renderer: swimlane (flow) ---------- */
  function renderSwimlane(view) {
    const pane = $('#graph-pane');
    const GUTTER = 128, PHEAD = 30, GX = 22, GY = 16, LPAD = 8;
    const cell = {}; // lane -> phase -> nodes
    for (const n of view.nodes) ((cell[n.lane] = cell[n.lane] || {})[n.phase] = cell[n.lane][n.phase] || []).push(n);
    const colX = {}; let x = GUTTER;
    for (const ph of view.phases) { colX[ph.id] = x; x += NW + GX; }
    const W = x + 10;
    const rowY = {}; let y = PHEAD + 6; const laneRows = [];
    for (const lane of view.lanes) {
      const depth = Math.max(1, ...view.phases.map(p => (cell[lane.id] && cell[lane.id][p.id] || []).length));
      const h = LPAD * 2 + depth * (NH + GY) - GY;
      rowY[lane.id] = y; laneRows.push({ ...lane, y, h });
      y += h + 12;
    }
    const H = y + 6;

    const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, width: Math.max(W, 900) });
    svg.append(arrowDefs());
    for (const lane of laneRows) {
      svg.append(svgEl('rect', { x: 2, y: lane.y - 4, width: W - 6, height: lane.h + 8, rx: 10, class: 'lane-bg' }));
      const t = svgEl('text', { x: 10, y: lane.y + 14, class: 'lane-title' }); t.textContent = lane.title; svg.append(t);
      const b = svgEl('text', { x: 10, y: lane.y + 27, class: 'lane-blurb' }); b.textContent = lane.blurb; svg.append(b);
    }
    for (const ph of view.phases) {
      const t = svgEl('text', { x: colX[ph.id] + NW / 2, y: 18, class: 'phase-title', 'text-anchor': 'middle' }); t.textContent = ph.title; svg.append(t);
      svg.append(svgEl('line', { x1: colX[ph.id] - GX / 2, y1: 26, x2: colX[ph.id] - GX / 2, y2: H - 4, class: 'edge', 'stroke-dasharray': '2 5', opacity: .25 }));
    }

    const pos = {};
    for (const n of view.nodes) {
      const stack = cell[n.lane][n.phase];
      const idx = stack.indexOf(n);
      pos[n.id] = { x: colX[n.phase], y: rowY[n.lane] + LPAD + idx * (NH + GY), node: n };
    }

    const adjacency = {};
    const touch = (a, b) => { (adjacency[a] = adjacency[a] || new Set([a])).add(b); (adjacency[b] = adjacency[b] || new Set([b])).add(a); };
    for (const e of view.edges || []) {
      const a = pos[e.from], b = pos[e.to];
      if (!a || !b) continue;
      touch(e.from, e.to);
      let d, mid;
      const samePhase = a.node.phase === b.node.phase, sameLane = a.node.lane === b.node.lane;
      if (samePhase && !sameLane) {
        const [top, bot] = a.y < b.y ? [a, b] : [b, a];
        const x0 = a.x + NW / 2 + hashOff(e.from + e.to);
        d = `M ${x0} ${a.y < b.y ? a.y + NH : a.y} L ${x0} ${a.y < b.y ? b.y : b.y + NH}`;
        mid = { x: x0 + 4, y: (top.y + NH + bot.y) / 2 };
      } else if (sameLane) {
        const y0 = a.y + NH / 2 + hashOff(e.from + e.to) / 2;
        d = `M ${a.x + NW} ${y0} L ${b.x} ${y0}`;
        mid = { x: (a.x + NW + b.x) / 2, y: y0 - 6 };
      } else {
        d = sideElbow(a.x + NW, a.y + NH / 2, b.x + (b.x > a.x ? 0 : NW), b.y + NH / 2);
        mid = { x: (a.x + NW + b.x) / 2, y: (a.y + b.y + NH) / 2 - 6 };
      }
      const p = svgEl('path', { d, class: `edge ${e.style || ''}`, 'marker-end': 'url(#arr)' });
      if (e.bidir) p.setAttribute('marker-start', 'url(#arr)');
      p.dataset.from = e.from; p.dataset.to = e.to; svg.append(p);
      if (e.label) { const t = svgEl('text', { x: mid.x, y: mid.y, class: 'edge-label', 'text-anchor': 'middle' }); t.textContent = e.label; svg.append(t); }
    }

    for (const [id, p] of Object.entries(pos)) {
      const g = nodeGroup(p.node, p, p.node.lane, p.node.dashed ? 'dashed' : '');
      g.addEventListener('click', () => openNode(view.id, id));
      svg.append(g);
    }
    pane.innerHTML = ''; pane.append(svg);
    attachHover(svg, adjacency);
  }

  /* ---------- sheet ---------- */
  function closeSheet() { document.body.classList.remove('sheet-open'); state.active = null; render(); setHash(); }
  $('#backdrop').addEventListener('click', closeSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && document.body.classList.contains('sheet-open')) closeSheet(); });

  function sheetChrome(title, desc, fm, node) {
    const head = $('#sheet-head'); head.innerHTML = '';
    head.append(el('div', { class: 'node-head' },
      el('h2', {}, title), el('p', { class: 'desc' }, desc || '')));
    if (fm) {
      const chips = el('div', { class: 'chips' });
      if (fm.invocation) chips.append(el('span', { class: 'chip' }, `invocation: ${fm.invocation}`));
      if (fm.execution) chips.append(el('span', { class: 'chip' }, `execution: ${fm.execution}`));
      for (const r of fm.requires || []) chips.append(el('span', { class: 'chip dep', onclick: () => openNode('sdlc', r) }, `requires ${r}`));
      for (const o of fm.optional || []) chips.append(el('span', { class: 'chip dep opt', onclick: () => openNode('sdlc', o) }, `optional ${o}`));
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) chips.append(el('span', { class: 'chip dep ext', onclick: () => window.open(e.source, '_blank') }, `external ${e.name}`));
      head.querySelector('.node-head').append(chips);
    }
  }

  async function renderFile(path, noteExtra = '') {
    const body = $('#sheet-body'); body.innerHTML = '';
    body.append(el('p', { class: 'filepath' }, path + noteExtra));
    const target = el('div', { id: 'md' }, 'Loading…'); body.append(target);
    try {
      const text = await fetchText(path);
      const { fm, body: mdBody } = parseFrontmatter(text);
      target.innerHTML = '';
      if (Object.keys(fm).length) {
        const card = el('dl', { class: 'fm-card' });
        for (const [k, v] of Object.entries(fm)) { card.append(el('dt', {}, k)); card.append(el('dd', {}, typeof v === 'string' ? v : JSON.stringify(v))); }
        target.append(card);
      }
      const div = el('div'); div.innerHTML = md.render(mdBody);
      div.querySelectorAll('a[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (/^https?:/.test(href)) { a.target = '_blank'; return; }
        if (href.includes('.md')) {
          a.addEventListener('click', (ev) => {
            ev.preventDefault();
            const dir = path.split('/').slice(0, -1).join('/');
            const resolved = new URL(href.split('#')[0], `http://x/${dir}/`).pathname.slice(1);
            renderFile(resolved, '  (followed link)');
          });
        }
      });
      target.append(div);
      body.scrollTop = 0;
    } catch (e) {
      target.innerHTML = '';
      target.append(el('div', { class: 'err' }, `Could not load ${path}: ${e.message}. Serve the repo root (python3 -m http.server) — file:// cannot fetch.`));
    }
  }

  function skillTabs(node, activeFull) {
    const files = node.files.map(f => ({ ...f, full: `${node.source}/${f.path}` }));
    for (const p of node.playbooks || []) files.push({ group: 'Playbooks (this repo)', label: p.split('/').pop().replace('.md', ''), path: p, full: p });
    const tabs = $('#sheet-tabs'); tabs.innerHTML = '';
    const bar = el('div', { class: 'tabs' });
    let lastGroup = null;
    for (const f of files) {
      if (f.group !== lastGroup) { bar.append(el('span', { class: 'grp' }, f.group)); lastGroup = f.group; }
      const b = el('button', { onclick: () => { openNode('sdlc', node.id, f.full); } }, f.label);
      if (f.full === activeFull) b.classList.add('active');
      bar.append(b);
    }
    tabs.append(bar);
    return files;
  }

  async function openNode(viewId, nodeId, filePath) {
    const sdlc = state.views.sdlc;
    const view = state.views[viewId];
    const node = view.nodes.find(n => n.id === nodeId);
    if (!node) return;

    // flow/backlog nodes: resolve their open target
    if (node.open) {
      if (node.open.jump) { switchView(node.open.jump, () => openNode(node.open.jump, node.open.node)); return; }
      if (node.open.node) { openSkillSheet(sdlc.nodes.find(n => n.id === node.open.node), undefined, viewId, nodeId); return; }
      if (node.open.file) {
        state.active = nodeId; render();
        sheetChrome(node.title, node.blurb, null);
        $('#sheet-tabs').innerHTML = '';
        document.body.classList.add('sheet-open');
        setHash(viewId, nodeId);
        renderFile(node.open.file);
        return;
      }
    }
    openSkillSheet(node, filePath, viewId, nodeId);
  }

  function openSkillSheet(node, filePath, viewId, activeNodeId) {
    if (!node) return;
    state.active = activeNodeId || node.id; render();
    const fm = state.fm[node.id] || {};
    sheetChrome(node.title, fm.description || node.blurb, fm, node);
    const files = skillTabs(node, filePath || `${node.source}/${node.files[0].path}`);
    const file = files.find(f => f.full === filePath) || files[0];
    document.body.classList.add('sheet-open');
    setHash(viewId || 'sdlc', node.id, file.full);
    renderFile(file.full);
  }

  /* ---------- routing / shell ---------- */
  function setHash(viewId, nodeId, file) {
    const parts = [viewId || state.current];
    if (nodeId) parts.push(nodeId);
    if (file) parts.push(encodeURIComponent(file));
    history.replaceState(null, '', '#' + parts.join('/'));
  }

  function render() {
    const view = state.views[state.current];
    $('#view-subtitle').textContent = view.subtitle;
    document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('active', b.dataset.view === state.current));
    (view.type === 'swimlane' ? renderSwimlane : renderGraph)(view);
  }

  function switchView(id, after) {
    state.current = id; state.active = null;
    document.body.classList.remove('sheet-open');
    render(); setHash(id);
    if (after) after();
  }

  async function init() {
    await Promise.all(VIEW_IDS.map(async id => {
      state.views[id] = JSON.parse(await fetchText(`site/views/${id}.json`).catch(() => fetchText(`views/${id}.json`)));
    }));
    const nav = $('#nav');
    for (const id of VIEW_IDS) {
      nav.append(el('button', { 'data-view': id, onclick: () => switchView(id) }, state.views[id].title));
    }
    await Promise.all(state.views.sdlc.nodes.map(async n => {
      try { state.fm[n.id] = parseFrontmatter(await fetchText(`${n.source}/SKILL.md`)).fm; }
      catch { state.fm[n.id] = {}; }
    }));
    const h = location.hash.slice(1);
    if (h) {
      const [v, nodeId, ...rest] = h.split('/');
      if (state.views[v]) state.current = v;
      render();
      if (nodeId) openNode(state.current, nodeId, rest.length ? decodeURIComponent(rest.join('/')) : undefined);
    } else render();
    window.addEventListener('resize', () => render());
  }
  init().catch(e => { $('#graph-pane').innerHTML = `<div class="err" style="margin:2rem">Failed to load: ${e.message}. Serve from the repo root: <code>python3 -m http.server</code>, open <code>/site/</code>.</div>`; });
})();
