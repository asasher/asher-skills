/* asher-skills documentation app.
 * Drift design: node CONTENT and EDGES come from the real files (SKILL.md fetched live, frontmatter
 * parsed from the same bytes the reader sees). Only the roster/lanes/blurbs live in views/*.json —
 * validated by site/check.py. See site/MAINTENANCE.md. */
(() => {
  const params = new URLSearchParams(location.search);
  const BASE = (params.get('base') || '..').replace(/\/$/, '');
  const VIEW = params.get('view') || 'sdlc';
  const md = window.markdownit({ html: false, linkify: true });

  const state = { view: null, fm: {}, active: null, activeFile: null };

  const $ = (sel) => document.querySelector(sel);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'class') n.className = v; else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v);
    }
    for (const k of kids) n.append(k);
    return n;
  };

  async function fetchText(path) {
    const r = await fetch(`${BASE}/${path}`);
    if (!r.ok) throw new Error(`${r.status} ${r.statusText} — ${path}`);
    return r.text();
  }

  /* Minimal frontmatter parser for this repo's disciplined SKILL.md headers:
   * scalar lines, one-line [a, b] lists, and one-line JSON arrays (external). */
  function parseFrontmatter(text) {
    const m = text.match(/^---\n([\s\S]*?)\n---\n?/);
    if (!m) return { fm: {}, body: text };
    const fm = {};
    for (const line of m[1].split('\n')) {
      const kv = line.match(/^\s{0,2}([a-zA-Z-]+):\s*(.*)$/);
      if (!kv) continue;
      const [, key, raw] = kv;
      if (raw.startsWith('[{') || raw.startsWith('[ {')) {
        try { fm[key] = JSON.parse(raw); } catch { fm[key] = raw; }
      } else if (raw.startsWith('[')) {
        fm[key] = raw.replace(/^\[|\]$/g, '').split(',').map(s => s.trim()).filter(Boolean);
      } else if (raw !== '') fm[key] = raw.replace(/^"|"$/g, '');
    }
    return { fm, body: text.slice(m[0].length) };
  }

  /* ---------- graph ---------- */
  const NW = 168, NH = 52, GX = 16, GY = 14, LPAD = 10, LHEAD = 34, LGAP = 12, W = 960;

  function layout(view) {
    const perLane = {};
    for (const n of view.nodes) (perLane[n.lane] = perLane[n.lane] || []).push(n);
    // synthesize external nodes from frontmatter declarations
    for (const n of view.nodes) {
      const ext = (state.fm[n.id] && state.fm[n.id].external) || [];
      for (const e of (Array.isArray(ext) ? ext : [])) {
        if (typeof e !== 'object' || perLane[n.lane].some(x => x.id === e.name)) continue;
        perLane[n.lane].push({ id: e.name, title: e.name, blurb: `external · ${e.kind} · consent-gated`, external: e, lane: n.lane });
      }
    }
    const pos = {}; let y = 0; const lanes = [];
    for (const lane of view.lanes) {
      const nodes = perLane[lane.id] || [];
      const cols = Math.max(1, Math.floor((W - 2 * LPAD + GX) / (NW + GX)));
      const rows = Math.ceil(nodes.length / cols) || 1;
      const h = LHEAD + rows * (NH + GY) + LPAD - GY + 8;
      lanes.push({ ...lane, y, h });
      nodes.forEach((n, i) => {
        pos[n.id] = { x: LPAD + (i % cols) * (NW + GX), y: y + LHEAD + Math.floor(i / cols) * (NH + GY), node: n };
      });
      y += h + LGAP;
    }
    return { pos, lanes, H: y };
  }

  function edgePath(a, b) {
    const x1 = a.x + NW / 2, y1 = a.y + NH, x2 = b.x + NW / 2, y2 = b.y;
    if (y2 > y1) return `M ${x1} ${y1} C ${x1} ${y1 + 30}, ${x2} ${y2 - 30}, ${x2} ${y2}`;
    return `M ${a.x + NW} ${a.y + NH / 2} C ${a.x + NW + 40} ${a.y + NH / 2}, ${b.x - 40} ${b.y + NH / 2}, ${b.x} ${b.y + NH / 2}`;
  }

  function drawGraph() {
    const view = state.view;
    const { pos, lanes, H } = layout(view);
    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);

    for (const lane of lanes) {
      const r = document.createElementNS(svgNS, 'rect');
      Object.entries({ x: 2, y: lane.y, width: W - 4, height: lane.h, rx: 10, class: 'lane-bg' })
        .forEach(([k, v]) => r.setAttribute(k, v));
      svg.append(r);
      const t = document.createElementNS(svgNS, 'text');
      t.setAttribute('x', LPAD + 2); t.setAttribute('y', lane.y + 16); t.setAttribute('class', 'lane-title');
      t.textContent = lane.title; svg.append(t);
      const b = document.createElementNS(svgNS, 'text');
      b.setAttribute('x', LPAD + 2 + lane.title.length * 8.2); b.setAttribute('y', lane.y + 16); b.setAttribute('class', 'lane-blurb');
      b.textContent = '— ' + lane.blurb; svg.append(b);
    }

    const drawEdge = (fromId, toId, cls) => {
      const a = pos[fromId], b = pos[toId];
      if (!a || !b) return;
      const p = document.createElementNS(svgNS, 'path');
      p.setAttribute('d', edgePath(a, b)); p.setAttribute('class', `edge ${cls}`);
      p.setAttribute('marker-end', 'url(#arr)'); svg.append(p);
    };

    const defs = document.createElementNS(svgNS, 'defs');
    defs.innerHTML = `<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor" opacity=".55"/></marker>`;
    svg.append(defs);

    for (const f of view.flow || []) drawEdge(f.from, f.to, 'flow');
    for (const n of view.nodes) {
      const fm = state.fm[n.id] || {};
      for (const r of fm.requires || []) drawEdge(n.id, r, '');
      for (const o of fm.optional || []) drawEdge(n.id, o, 'optional');
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) drawEdge(n.id, e.name, 'external');
    }

    for (const [id, p] of Object.entries(pos)) {
      const n = p.node;
      const g = document.createElementNS(svgNS, 'g');
      g.setAttribute('class', `node lane-${n.lane}${n.external ? ' external' : ''}${state.active === id ? ' active' : ''}`);
      g.dataset.id = id;
      const rect = document.createElementNS(svgNS, 'rect');
      Object.entries({ x: p.x, y: p.y, width: NW, height: NH, rx: 8 }).forEach(([k, v]) => rect.setAttribute(k, v));
      if (id === 'merge-changes') rect.setAttribute('class', 'gate');
      g.append(rect);
      const t = document.createElementNS(svgNS, 'text');
      t.setAttribute('x', p.x + 10); t.setAttribute('y', p.y + 19); t.setAttribute('class', 't');
      t.textContent = n.title; g.append(t);
      const words = (n.blurb || '').split(' '); const lines = ['', ''];
      for (const w of words) { if (lines[0].length + w.length < 30 && !lines[1]) lines[0] += w + ' '; else lines[1] += w + ' '; }
      lines.forEach((ln, i) => {
        if (!ln.trim()) return;
        const b = document.createElementNS(svgNS, 'text');
        b.setAttribute('x', p.x + 10); b.setAttribute('y', p.y + 32 + i * 11); b.setAttribute('class', 'b');
        b.textContent = ln.trim().slice(0, 32); g.append(b);
      });
      g.addEventListener('click', () => n.external ? window.open(n.external.source, '_blank') : selectNode(id));
      svg.append(g);
    }
    const pane = $('#graph-pane'); pane.innerHTML = ''; pane.append(svg);
  }

  /* ---------- reader ---------- */
  function fileList(node) {
    const files = node.files.map(f => ({ ...f, full: `${node.source}/${f.path}` }));
    for (const p of node.playbooks || []) files.push({ group: 'Playbooks (this repo)', label: p.split('/').pop().replace('.md', ''), path: p, full: p });
    return files;
  }

  async function selectNode(id, filePath) {
    const node = state.view.nodes.find(n => n.id === id);
    if (!node) return;
    state.active = id;
    drawGraph();
    const files = fileList(node);
    const file = files.find(f => f.full === filePath) || files[0];
    state.activeFile = file.full;
    location.hash = `#${id}/${encodeURIComponent(file.full)}`;

    const fm = state.fm[id] || {};
    const reader = $('#reader'); reader.innerHTML = '';
    const head = el('div', { class: 'node-head' });
    head.append(el('h2', {}, node.title));
    head.append(el('p', { class: 'desc' }, fm.description || node.blurb));
    const chips = el('div', { class: 'chips' });
    if (fm.invocation) chips.append(el('span', { class: 'chip' }, `invocation: ${fm.invocation}`));
    if (fm.execution) chips.append(el('span', { class: 'chip' }, `execution: ${fm.execution}`));
    for (const r of fm.requires || []) chips.append(el('span', { class: 'chip dep', onclick: () => selectNode(r) }, `requires ${r}`));
    for (const o of fm.optional || []) chips.append(el('span', { class: 'chip dep opt', onclick: () => selectNode(o) }, `optional ${o}`));
    for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) chips.append(el('span', { class: 'chip dep ext', onclick: () => window.open(e.source, '_blank') }, `external ${e.name}`));
    head.append(chips);
    reader.append(head);

    const tabs = el('div', { class: 'tabs' });
    let lastGroup = null;
    for (const f of files) {
      if (f.group !== lastGroup) { tabs.append(el('span', { class: 'grp' }, f.group)); lastGroup = f.group; }
      const b = el('button', { onclick: () => selectNode(id, f.full) }, f.label);
      if (f.full === file.full) b.classList.add('active');
      tabs.append(b);
    }
    reader.append(tabs);
    reader.append(el('p', { class: 'filepath' }, file.full));
    const target = el('div', { id: 'md' }, 'Loading…');
    reader.append(target);

    try {
      const text = await fetchText(file.full);
      const { fm: ffm, body } = parseFrontmatter(text);
      target.innerHTML = '';
      if (Object.keys(ffm).length) {
        const card = el('dl', { class: 'fm-card' });
        for (const [k, v] of Object.entries(ffm)) {
          card.append(el('dt', {}, k));
          card.append(el('dd', {}, typeof v === 'string' ? v : JSON.stringify(v)));
        }
        target.append(card);
      }
      const div = el('div');
      div.innerHTML = md.render(body);
      // intercept relative markdown links → load in-panel
      div.querySelectorAll('a[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (/^https?:/.test(href)) { a.target = '_blank'; return; }
        if (href.endsWith('.md') || href.includes('.md#')) {
          a.addEventListener('click', (ev) => {
            ev.preventDefault();
            const dir = file.full.split('/').slice(0, -1).join('/');
            const resolved = new URL(href.split('#')[0], `http://x/${dir}/`).pathname.slice(1);
            selectNode(id, resolved).catch(() => loadArbitrary(id, resolved));
          });
        }
      });
      target.append(div);
    } catch (e) {
      target.innerHTML = '';
      target.append(el('div', { class: 'err' }, `Could not load ${file.full}: ${e.message}. Serve the repo root (e.g. python3 -m http.server) — file:// cannot fetch.`));
    }
  }

  /* load a file that isn't in the manifest (followed via a relative link) */
  async function loadArbitrary(nodeId, path) {
    const target = $('#md');
    try {
      const text = await fetchText(path);
      const { body } = parseFrontmatter(text);
      $('.filepath').textContent = path + '  (followed link — not in the manifest)';
      target.innerHTML = md.render(body);
    } catch (e) { /* leave the error shown by selectNode */ }
  }

  async function init() {
    const view = JSON.parse(await fetchText(`site/views/${VIEW}.json`).catch(() => fetchText(`views/${VIEW}.json`)));
    state.view = view;
    $('#view-title').textContent = view.title;
    $('#view-subtitle').textContent = view.subtitle;
    await Promise.all(view.nodes.map(async n => {
      try { state.fm[n.id] = parseFrontmatter(await fetchText(`${n.source}/SKILL.md`)).fm; }
      catch { state.fm[n.id] = {}; }
    }));
    drawGraph();
    const h = location.hash.slice(1);
    if (h) { const [id, f] = h.split('/'); selectNode(id, f ? decodeURIComponent(h.slice(id.length + 1)) : undefined); }
  }
  init().catch(e => { $('#reader').innerHTML = `<div class="err">Failed to load view: ${e.message}. Serve from the repo root: <code>python3 -m http.server</code> then open <code>/site/</code>.</div>`; });
})();
