/* asher-skills documentation app — v4 (AntV X6 canvas: obstacle-avoiding manhattan edges,
 * lanes with headers attached to the lane shape, grid placement computed from the manifests).
 * Drift design unchanged: content + dependency edges come from the real files; views/*.json holds only
 * rosters/lanes/blurbs, gated by site/check.py. See site/MAINTENANCE.md. */
(() => {
  const params = new URLSearchParams(location.search);
  const BASE = (params.get('base') || '..').replace(/\/$/, '');
  const VIEW_IDS = ['sdlc', 'flow', 'backlog'];
  const md = window.markdownit({ html: false, linkify: true });

  const state = { views: {}, fm: {}, current: 'sdlc', active: null };
  let graph = null;
  let activeCell = null;

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
  const esc = (s) => String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const cssVar = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim();

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

  /* ---------- geometry (positions are node centers; lanes/phases carry px rects) ---------- */
  const NW = 172, NH = 56;

  const kindVars = (laneId) => {
    if (['services', 'probes', 'sub', 'siblings'].includes(laneId)) return ['--lane', '--lane-line'];
    if (['ux', 'you'].includes(laneId)) return ['--human', '--human-line'];
    if (['repo', 'playbooks', 'setup'].includes(laneId)) return ['--artifact', '--artifact-line'];
    return ['--stage', '--stage-line'];
  };

  function buildGraphElements(view) {
    const W = 1500, GX = 36, GY = 30, LPAD = 26, LHEAD = 42, LGAP = 48;
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
    const lanes = [], nodes = [];
    let y = 0;
    for (const lane of view.lanes) {
      const laneNodes = perLane[lane.id] || [];
      if (!laneNodes.length) continue;
      const cols = Math.max(1, Math.floor((W - 2 * LPAD + GX) / (NW + GX)));
      const rows = Math.ceil(laneNodes.length / cols);
      const laneH = LHEAD + rows * (NH + GY) + LPAD - GY + 14;
      lanes.push({ id: `lane:${lane.id}`, title: lane.title, blurb: lane.blurb, x: 0, y, w: W, h: laneH });
      laneNodes.forEach((n, i) => {
        nodes.push({
          ...n,
          cx: LPAD + (i % cols) * (NW + GX) + NW / 2,
          cy: y + LHEAD + Math.floor(i / cols) * (NH + GY) + NH / 2,
        });
      });
      y += laneH + LGAP;
    }
    const have = new Set(nodes.map(n => n.id));
    const edges = [];
    const addEdge = (from, to, cls, label) => {
      if (have.has(from) && have.has(to)) edges.push({ from, to, style: cls, label });
    };
    for (const f of view.flow || []) addEdge(f.from, f.to, 'flow', f.label);
    for (const e of view.edges || []) addEdge(e.from, e.to, e.style || '', e.label);
    if (view.id === 'sdlc') for (const n of view.nodes) {
      const fm = state.fm[n.id] || {};
      for (const r of fm.requires || []) addEdge(n.id, r, '');
      for (const o of fm.optional || []) addEdge(n.id, o, 'optional');
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) addEdge(n.id, e.name, 'external');
    }
    return { lanes, phases: [], nodes, edges };
  }

  function buildSwimElements(view) {
    const GX = 40, GY = 26, LPAD = 42, LGAP = 46, PHEAD = 46;
    const cell = {};
    for (const n of view.nodes) ((cell[n.lane] = cell[n.lane] || {})[n.phase] = cell[n.lane][n.phase] || []).push(n);
    const colX = {}; let x = 0;
    for (const ph of view.phases) { colX[ph.id] = x + NW / 2; x += NW + GX; }
    const totalW = x - GX + 2 * LPAD;
    const phases = view.phases.map(ph => ({ id: `phase:${ph.id}`, title: ph.title, cx: colX[ph.id] + LPAD, cy: PHEAD / 2 }));
    const lanes = [], nodes = [];
    let y = PHEAD;
    for (const lane of view.lanes) {
      const depth = Math.max(1, ...view.phases.map(p => (cell[lane.id] && cell[lane.id][p.id] || []).length));
      const laneH = LPAD + depth * (NH + GY) - GY + 24;
      lanes.push({ id: `lane:${lane.id}`, title: lane.title, blurb: lane.blurb, x: 0, y, w: totalW, h: laneH });
      for (const ph of view.phases) {
        (cell[lane.id] && cell[lane.id][ph.id] || []).forEach((n, idx) => {
          nodes.push({ ...n, cx: colX[ph.id] + LPAD, cy: y + LPAD + idx * (NH + GY) + NH / 2 });
        });
      }
      y += laneH + LGAP;
    }
    const edges = (view.edges || []).map(e => ({ from: e.from, to: e.to, style: e.style || '', label: e.label, bidir: e.bidir }));
    return { lanes, phases, nodes, edges };
  }

  /* ---------- X6 renderer ---------- */
  let shapesRegistered = false;
  function registerShapes() {
    if (shapesRegistered) return;
    shapesRegistered = true;
    X6.Shape.HTML.register({
      shape: 'skill-node', width: NW, height: NH,
      html(cell) {
        const d = cell.getData() || {};
        const div = document.createElement('div');
        div.className = 'x-node';
        div.innerHTML = `<b>${esc(d.title)}</b><span>${esc(d.blurb)}</span>`;
        return div;
      },
    });
    X6.Shape.HTML.register({
      shape: 'lane-box', width: 100, height: 100,
      html(cell) {
        const d = cell.getData() || {};
        const div = document.createElement('div');
        div.className = 'x-lane';
        div.innerHTML = `<b>${esc(d.title)}</b>${d.blurb ? `<span> — ${esc(d.blurb)}</span>` : ''}`;
        return div;
      },
    });
    X6.Shape.HTML.register({
      shape: 'phase-head', width: NW, height: 26,
      html(cell) {
        const d = cell.getData() || {};
        const div = document.createElement('div');
        div.className = 'x-phase';
        div.textContent = d.title || '';
        return div;
      },
    });
  }

  const ROUTER = { name: 'manhattan', args: { step: 10, padding: 14, excludeShapes: ['lane-box'] } };

  /* Measure a lane header's rendered width with the real CSS so an invisible obstacle node can
   * cover exactly the title text — the router then avoids the text but can still cross the lane
   * boundary elsewhere. */
  const headerWidths = {};
  function laneHeaderWidth(title, blurb) {
    const key = `${title}|${blurb || ''}`;
    if (headerWidths[key]) return headerWidths[key];
    const probe = document.createElement('div');
    probe.className = 'x-lane';
    probe.style.cssText = 'position:absolute;visibility:hidden;width:auto;height:auto;left:-9999px';
    probe.innerHTML = `<b>${esc(title)}</b>${blurb ? `<span> — ${esc(blurb)}</span>` : ''}`;
    document.body.append(probe);
    const w = probe.offsetWidth;
    probe.remove();
    return (headerWidths[key] = w);
  }

  function drawCells(built, viewId) {
    const muted = cssVar('--muted'), accent = cssVar('--accent'), line = cssVar('--line'),
      card = cssVar('--card'), bg = cssVar('--bg'), artifact = cssVar('--artifact-line');
    for (const l of built.lanes) {
      graph.addNode({
        id: l.id, shape: 'lane-box', x: l.x, y: l.y, width: l.w, height: l.h, zIndex: 1,
        data: { title: l.title, blurb: l.blurb },
        attrs: { body: { fill: card, fillOpacity: .55, stroke: line, strokeWidth: 1, rx: 10, ry: 10 } },
      });
      // invisible router obstacle over the header text (lane-box itself is excluded from obstacles)
      graph.addNode({
        id: `${l.id}:title-block`, shape: 'rect', zIndex: 0,
        x: l.x, y: l.y, width: Math.min(l.w - 40, laneHeaderWidth(l.title, l.blurb) + 8), height: 34,
        attrs: { body: { fill: 'none', stroke: 'none' } },
      });
    }
    for (const p of built.phases) {
      graph.addNode({
        id: p.id, shape: 'phase-head', x: p.cx - NW / 2, y: p.cy - 13, width: NW, height: 26, zIndex: 2,
        data: { title: p.title },
        attrs: { body: { fill: 'transparent', stroke: 'none' } },
      });
    }
    for (const n of built.nodes) {
      const gate = n.id === 'merge-changes';
      const [fv, sv] = gate ? ['--gate', '--gate-line'] : n.external ? ['--artifact', '--artifact-line'] : kindVars(n.lane);
      const stroke = cssVar(sv);
      graph.addNode({
        id: n.id, shape: 'skill-node', x: n.cx - NW / 2, y: n.cy - NH / 2, width: NW, height: NH, zIndex: 20,
        data: { title: n.title, blurb: n.blurb, stroke, item: true, external: n.external || null, view: viewId },
        attrs: { body: {
          fill: cssVar(fv), stroke, strokeWidth: 1.5, rx: 8, ry: 8,
          ...(n.external || n.dashed ? { strokeDasharray: '5 3' } : {}),
        } },
      });
    }
    for (const e of built.edges) {
      const flow = e.style === 'flow', ext = e.style === 'external', opt = e.style === 'optional';
      const stroke = flow ? accent : ext ? artifact : muted;
      const marker = { name: 'block', width: 8, height: 6 };
      graph.addEdge({
        source: { cell: e.from }, target: { cell: e.to }, zIndex: 10,
        router: ROUTER, connector: { name: 'rounded', args: { radius: 10 } },
        attrs: { line: {
          stroke, strokeWidth: flow ? 2.2 : 1.5, opacity: flow || ext ? .85 : .5,
          targetMarker: marker, ...(e.bidir ? { sourceMarker: marker } : {}),
          ...(opt || ext ? { strokeDasharray: '5 3' } : {}),
        } },
        ...(e.label ? { labels: [{ position: 0.5, attrs: {
          label: { text: e.label, fontSize: 9.5, fill: muted },
          body: { fill: bg, stroke: line, strokeWidth: 1, rx: 4, ry: 4, refWidth2: 10, refHeight2: 6, refX: -5, refY: -3 },
        } }] } : {}),
      });
    }
  }

  /* Hover + click are driven by plain DOM delegation on the container (bubbling mouseover/click
   * against the data-cell-id the engine stamps on every cell <g>) — no dependency on X6's
   * synthetic delegated-mouseenter events. */
  let hoverId = null, downAt = null;
  function cellFromEvent(ev) {
    const g = ev.target.closest && ev.target.closest('g[data-cell-id]');
    if (!g || !graph) return null;
    const cell = graph.getCellById(g.getAttribute('data-cell-id'));
    return cell && cell.isNode() && (cell.getData() || {}).item ? cell : null;
  }
  function wireCanvasEvents() {
    const pane = $('#cy');
    pane.addEventListener('mouseover', (ev) => {
      const cell = cellFromEvent(ev);
      const id = cell ? cell.id : null;
      if (id === hoverId) return;
      hoverId = id;
      if (cell) focusNode(cell); else unfocus();
    });
    pane.addEventListener('mouseleave', () => { hoverId = null; unfocus(); });
    pane.addEventListener('mousedown', (ev) => { downAt = [ev.clientX, ev.clientY]; });
    pane.addEventListener('click', (ev) => {
      if (downAt && Math.hypot(ev.clientX - downAt[0], ev.clientY - downAt[1]) > 6) return; // a pan, not a click
      const cell = cellFromEvent(ev);
      if (!cell) return;
      const v = state.views[state.current];
      const vn = v.nodes.find(n => n.id === cell.id);
      if (!vn) { // synthesized external node
        const owner = v.nodes.map(n => (state.fm[n.id] || {}).external || []).flat().find(x => x && x.name === cell.id);
        if (owner) window.open(owner.source, '_blank');
        return;
      }
      openNode(state.current, cell.id);
    });
  }

  function focusNode(node) {
    const keep = new Set([node.id]);
    for (const e of graph.getConnectedEdges(node)) {
      keep.add(e.id); keep.add(e.getSourceCellId()); keep.add(e.getTargetCellId());
    }
    for (const cell of graph.getCells()) {
      if (cell.shape === 'lane-box' || cell.shape === 'phase-head') continue;
      const v = graph.findViewByCell(cell);
      if (v) v.container.classList.toggle('dim', !keep.has(cell.id));
    }
  }
  function unfocus() {
    if (!graph) return;
    for (const cell of graph.getCells()) {
      const v = graph.findViewByCell(cell);
      if (v) v.container.classList.remove('dim');
    }
  }

  function setActiveCell(nodeId) {
    if (activeCell) {
      activeCell.attr({ body: { stroke: (activeCell.getData() || {}).stroke, strokeWidth: 1.5 } });
      activeCell = null;
    }
    const cell = nodeId && graph && graph.getCellById(nodeId);
    if (cell && (cell.getData() || {}).item) {
      cell.attr({ body: { stroke: cssVar('--accent'), strokeWidth: 3 } });
      activeCell = cell;
    }
  }

  function renderView() {
    const view = state.views[state.current];
    $('#view-subtitle').textContent = view.subtitle;
    document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('active', b.dataset.view === state.current));
    registerShapes();
    if (graph) { graph.dispose(); graph = null; activeCell = null; }
    $('#cy').innerHTML = '';
    graph = new X6.Graph({
      container: $('#cy'), autoResize: true, interacting: false,
      panning: { enabled: true }, mousewheel: { enabled: true, minScale: .25, maxScale: 2.75 },
    });
    const built = view.type === 'swimlane' ? buildSwimElements(view) : buildGraphElements(view);
    drawCells(built, view.id);
    hoverId = null;
    graph.zoomToFit({ padding: 28, maxScale: 1 });
    if (state.active) setActiveCell(state.active);
  }

  /* ---------- sheet ---------- */
  function closeSheet() {
    document.body.classList.remove('sheet-open');
    state.active = null;
    setActiveCell(null);
    setHash();
  }
  $('#backdrop').addEventListener('click', closeSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && document.body.classList.contains('sheet-open')) closeSheet(); });

  function markActive(nodeId) {
    state.active = nodeId;
    setActiveCell(nodeId);
  }

  function sheetChrome(title, desc, fm) {
    const head = $('#sheet-head'); head.innerHTML = '';
    head.append(el('div', { class: 'node-head' }, el('h2', {}, title), el('p', { class: 'desc' }, desc || '')));
    if (fm) {
      const chips = el('div', { class: 'chips' });
      if (fm.invocation) chips.append(el('span', { class: 'chip' }, `invocation: ${fm.invocation}`));
      if (fm.execution) chips.append(el('span', { class: 'chip' }, `execution: ${fm.execution}`));
      for (const r of fm.requires || []) chips.append(el('span', { class: 'chip dep', onclick: () => jumpTo('sdlc', r) }, `requires ${r}`));
      for (const o of fm.optional || []) chips.append(el('span', { class: 'chip dep opt', onclick: () => jumpTo('sdlc', o) }, `optional ${o}`));
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
      const b = el('button', { onclick: () => openSkillSheet(node, f.full, state.current, state.active) }, f.label);
      if (f.full === activeFull) b.classList.add('active');
      bar.append(b);
    }
    tabs.append(bar);
    return files;
  }

  function jumpTo(viewId, nodeId) {
    if (state.current !== viewId) { state.current = viewId; renderView(); }
    openNode(viewId, nodeId);
  }

  async function openNode(viewId, nodeId, filePath) {
    const view = state.views[viewId];
    const node = view.nodes.find(n => n.id === nodeId);
    if (!node) return;
    if (node.open) {
      if (node.open.jump) { jumpTo(node.open.jump, node.open.node); return; }
      if (node.open.node) { openSkillSheet(state.views.sdlc.nodes.find(n => n.id === node.open.node), undefined, viewId, nodeId); return; }
      if (node.open.file) {
        markActive(nodeId);
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
    markActive(activeNodeId || node.id);
    const fm = state.fm[node.id] || {};
    sheetChrome(node.title, fm.description || node.blurb, fm);
    const files = skillTabs(node, filePath || `${node.source}/${node.files[0].path}`);
    const file = files.find(f => f.full === filePath) || files[0];
    document.body.classList.add('sheet-open');
    setHash(viewId || 'sdlc', state.active, file.full);
    renderFile(file.full);
  }

  /* ---------- shell ---------- */
  function setHash(viewId, nodeId, file) {
    const parts = [viewId || state.current];
    if (nodeId) parts.push(nodeId);
    if (file) parts.push(encodeURIComponent(file));
    history.replaceState(null, '', '#' + parts.join('/'));
  }

  function switchView(id) {
    state.current = id; state.active = null;
    document.body.classList.remove('sheet-open');
    renderView(); setHash(id);
  }

  async function init() {
    await Promise.all(VIEW_IDS.map(async id => {
      state.views[id] = JSON.parse(await fetchText(`site/views/${id}.json`).catch(() => fetchText(`views/${id}.json`)));
    }));
    const nav = $('#nav');
    for (const id of VIEW_IDS) nav.append(el('button', { 'data-view': id, onclick: () => switchView(id) }, state.views[id].title));
    await Promise.all(state.views.sdlc.nodes.map(async n => {
      try { state.fm[n.id] = parseFrontmatter(await fetchText(`${n.source}/SKILL.md`)).fm; }
      catch { state.fm[n.id] = {}; }
    }));
    wireCanvasEvents();
    $('#zoom-in').addEventListener('click', () => graph && graph.zoom(0.25));
    $('#zoom-out').addEventListener('click', () => graph && graph.zoom(-0.25));
    $('#zoom-fit').addEventListener('click', () => graph && graph.zoomToFit({ padding: 28, maxScale: 1 }));

    const h = location.hash.slice(1);
    if (h) {
      const [v, nodeId, ...rest] = h.split('/');
      if (state.views[v]) state.current = v;
      renderView();
      if (nodeId) openNode(state.current, nodeId, rest.length ? decodeURIComponent(rest.join('/')) : undefined);
    } else renderView();
  }
  init().catch(e => { $('#cy').innerHTML = `<div class="err" style="margin:2rem">Failed to load: ${e.message}. Serve from the repo root: <code>python3 -m http.server</code>, open <code>/site/</code>.</div>`; });
})();
