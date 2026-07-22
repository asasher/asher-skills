/* asher-skills documentation app — v4 (AntV X6 canvas: obstacle-avoiding manhattan edges,
 * lanes with headers attached to the lane shape, grid placement computed from the manifests).
 * Drift design unchanged: content + dependency edges come from the real files; views/*.json holds only
 * rosters/lanes/blurbs, gated by site/check.py. See site/MAINTENANCE.md. */
(() => {
  const params = new URLSearchParams(location.search);
  const BASE = (params.get('base') || '..').replace(/\/$/, '');
  const VIEW_IDS = ['sdlc', 'flow', 'sequence', 'tickets', 'backlog'];
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
    const addEdge = (from, to, cls, label, labelAt) => {
      if (have.has(from) && have.has(to)) edges.push({ from, to, style: cls, label, labelAt });
    };
    for (const f of view.flow || []) addEdge(f.from, f.to, 'flow', f.label, f.labelAt);
    for (const e of view.edges || []) addEdge(e.from, e.to, e.style || '', e.label, e.labelAt);
    if (view.id === 'sdlc') for (const n of view.nodes) {
      const fm = state.fm[n.id] || {};
      for (const r of fm.requires || []) addEdge(n.id, r, '');
      for (const o of fm.optional || []) addEdge(n.id, o, 'optional');
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) addEdge(n.id, e.name, 'external');
    }
    return { lanes, phases: [], nodes, edges };
  }

  function buildSwimElements(view) {
    const GX = view.gapX || 40, GY = view.gapY || 26, LPAD = 42, LGAP = view.laneGap || 46, PHEAD = 46;
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
    const edges = (view.edges || []).map(e => ({ from: e.from, to: e.to, style: e.style || '', label: e.label, labelAt: e.labelAt, bidir: e.bidir }));
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
        div.className = 'x-node' + (d.ports ? ' has-ports' : '') + (d.center ? ' center' : '');
        div.innerHTML = `<b>${esc(d.title)}</b><span>${esc(d.blurb)}</span>`
          + (d.ports ? `<em class="pb">${d.ports} port${d.ports > 1 ? 's' : ''}</em>` : '');
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
      const [fv, sv] = gate ? ['--gate', '--gate-line']
        : n.tone ? [`--tone-${n.tone}`, `--tone-${n.tone}-line`]
        : n.external ? ['--artifact', '--artifact-line'] : kindVars(n.lane);
      const stroke = cssVar(sv);
      const r = n.pill ? NH / 2 : 8;
      graph.addNode({
        id: n.id, shape: 'skill-node', x: n.cx - NW / 2, y: n.cy - NH / 2, width: NW, height: NH, zIndex: 20,
        data: { title: n.title, blurb: n.blurb, stroke, item: true, external: n.external || null, view: viewId,
          center: !!n.center, ports: (n.bindings || []).length },
        attrs: { body: {
          fill: cssVar(fv), stroke, strokeWidth: 1.5, rx: r, ry: r,
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
        ...(e.label ? { labels: [{ position: e.labelAt ?? 0.5, attrs: {
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

  /* Sequence diagrams: actor heads over dashed lifelines, messages as straight point-to-point
   * arrows in time order — same canvas, no router (nothing to route around on a fixed y). */
  function drawSequence(view) {
    const muted = cssVar('--muted'), accent = cssVar('--accent'), line = cssVar('--line'), bg = cssVar('--bg');
    const GAP = 96, TOP = 16, ROW = 46, LPAD = 40;
    const ax = {};
    view.actors.forEach((a, i) => { ax[a.id] = LPAD + i * (NW + GAP) + NW / 2; });
    const startY = TOP + NH + 34;
    const endY = startY + view.messages.length * ROW + 10;
    const totalW = LPAD * 2 + view.actors.length * NW + (view.actors.length - 1) * GAP;
    for (const a of view.actors) {
      graph.addEdge({
        source: { x: ax[a.id], y: TOP + NH }, target: { x: ax[a.id], y: endY }, zIndex: 1,
        attrs: { line: { stroke: line, strokeWidth: 1.5, strokeDasharray: '4 4', targetMarker: null } },
      });
    }
    for (const a of view.actors) {
      const [fv, sv] = kindVars(a.kind);
      graph.addNode({
        id: `actor:${a.id}`, shape: 'skill-node', x: ax[a.id] - NW / 2, y: TOP, width: NW, height: NH,
        zIndex: 20, data: { title: a.title, blurb: a.blurb, stroke: cssVar(sv) },
        attrs: { body: { fill: cssVar(fv), stroke: cssVar(sv), strokeWidth: 1.5, rx: 8, ry: 8 } },
      });
    }
    view.messages.forEach((m, i) => {
      const y = startY + i * ROW;
      if (m.phase) {
        graph.addNode({
          id: `seq-phase:${i}`, shape: 'phase-head', x: totalW / 2 - NW, y: y - 13, width: NW * 2, height: 26,
          zIndex: 2, data: { title: `— ${m.phase} —` },
          attrs: { body: { fill: 'transparent', stroke: 'none' } },
        });
        return;
      }
      const ret = m.style === 'return';
      const marker = { name: 'block', width: 8, height: 6 };
      graph.addEdge({
        source: { x: ax[m.from], y }, target: { x: ax[m.to], y }, zIndex: 10,
        attrs: { line: {
          stroke: ret ? muted : accent, strokeWidth: ret ? 1.5 : 2, opacity: ret ? .6 : .85,
          targetMarker: marker, ...(m.style === 'bidir' ? { sourceMarker: marker } : {}),
          ...(ret ? { strokeDasharray: '5 3' } : {}),
        } },
        labels: [{ position: 0.5, attrs: {
          label: { text: m.label, fontSize: 9.5, fill: muted },
          body: { fill: bg, stroke: line, strokeWidth: 1, rx: 4, ry: 4, refWidth2: 10, refHeight2: 6, refX: -5, refY: -3 },
        } }],
      });
    });
  }

  /* State machine: label-role states as pills on a manifest grid — an initial dot, double-ring
   * final states, tone fills matching the label colors, transitions routed like every other view. */
  function drawStateMachine(view) {
    const GX = 104, GY = 92, PAD = 30;
    const px = NW + GX, py = NH + GY;
    const cx = (n) => PAD + n.col * px + NW / 2, cy = (n) => PAD + n.row * py + NH / 2;
    for (const n of view.nodes.filter(n => n.kind === 'initial')) {
      graph.addNode({
        id: n.id, shape: 'circle', x: cx(n) - 8, y: cy(n) - 8, width: 16, height: 16, zIndex: 20,
        attrs: { body: { fill: cssVar('--ink'), stroke: 'none' } },
      });
    }
    const nodes = view.nodes.filter(n => n.kind !== 'initial').map(n => ({
      ...n, tone: n.tone || 'none', pill: true, center: true, cx: cx(n), cy: cy(n),
    }));
    for (const n of nodes.filter(n => n.kind === 'final')) {
      graph.addNode({
        shape: 'rect', x: n.cx - NW / 2 - 5, y: n.cy - NH / 2 - 5, width: NW + 10, height: NH + 10,
        zIndex: 19, attrs: { body: {
          fill: 'none', stroke: cssVar(`--tone-${n.tone}-line`), strokeWidth: 1.5,
          rx: NH / 2 + 5, ry: NH / 2 + 5,
        } },
      });
    }
    drawCells({ lanes: [], phases: [], nodes, edges: (view.edges || []).map(e => ({ ...e, style: e.style || '' })) }, view.id);
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
      panning: { enabled: true },
      // default wheel factor is 1.2× per event — a trackpad flick fires dozens and compounds wildly
      mousewheel: { enabled: true, minScale: .25, maxScale: 2.75, factor: 1.04 },
    });
    if (view.type === 'sequence') {
      drawSequence(view);
    } else if (view.type === 'statemachine') {
      drawStateMachine(view);
    } else {
      const built = view.type === 'swimlane' ? buildSwimElements(view) : buildGraphElements(view);
      drawCells(built, view.id);
    }
    hoverId = null;
    graph.zoomToFit({ padding: 28, maxScale: 1 });
    if (state.active) setActiveCell(state.active);
  }

  /* ---------- sheets (stackable: named references open on top; Esc/× pops one,
   * clicking a peeking lower sheet returns to it, backdrop closes all) ---------- */
  const sheetStack = [];
  const topKey = () => sheetStack.length ? sheetStack[sheetStack.length - 1].key : null;
  function restack() {
    sheetStack.forEach((s, i) => {
      const above = sheetStack.length - 1 - i;
      s.root.style.setProperty('--shift', `${-above * 34}px`);
      s.root.style.zIndex = 50 + i;
      s.root.classList.toggle('under', above > 0);
    });
    document.body.classList.toggle('sheet-open', sheetStack.length > 0);
  }
  function pushSheet(key) {
    const sheet = { key };
    sheet.root = el('aside', { class: 'sheet', role: 'dialog', 'aria-modal': 'true',
      // under-sheets make their children pointer-inert, so a direct root hit means
      // "bring this sheet back" — pop everything stacked above it
      onclick: (ev) => { if (ev.target === sheet.root) popAbove(sheet); } });
    sheet.head = el('div', { class: 'sheet-head' });
    sheet.tabs = el('div', { class: 'sheet-tabs' });
    sheet.body = el('div', { class: 'sheet-body' });
    sheet.root.append(
      el('button', { class: 'sheet-close', title: 'Close (Esc)', onclick: (ev) => { ev.stopPropagation(); popAbove(sheet); popSheet(); } }, '×'),
      sheet.head, sheet.tabs, sheet.body);
    document.body.append(sheet.root);
    sheetStack.push(sheet);
    requestAnimationFrame(() => sheet.root.classList.add('open'));
    restack();
    return sheet;
  }
  function popSheet() {
    const s = sheetStack.pop();
    if (!s) return;
    s.root.classList.remove('open');
    setTimeout(() => s.root.remove(), 240);
    restack();
    if (!sheetStack.length) { state.active = null; setActiveCell(null); setHash(); }
  }
  function popAbove(sheet) {
    while (sheetStack.length && sheetStack[sheetStack.length - 1] !== sheet) popSheet();
  }
  function closeAllSheets() { while (sheetStack.length) popSheet(); }
  $('#backdrop').addEventListener('click', closeAllSheets);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && sheetStack.length) popSheet(); });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.file-menu')) document.querySelectorAll('.file-menu[open]').forEach(d => d.removeAttribute('open'));
  });

  function markActive(nodeId) {
    state.active = nodeId;
    setActiveCell(nodeId);
  }

  function sheetChrome(sheet, title, desc, fm, bindings) {
    sheet.head.innerHTML = '';
    sheet.head.append(el('div', { class: 'node-head' }, el('h2', {}, title), el('p', { class: 'desc' }, desc || '')));
    if (fm) {
      const chips = el('div', { class: 'chips' });
      if (fm.invocation) chips.append(el('span', { class: 'chip' }, `invocation: ${fm.invocation}`));
      if (fm.execution) chips.append(el('span', { class: 'chip' }, `execution: ${fm.execution}`));
      for (const r of fm.requires || []) chips.append(el('span', { class: 'chip dep', title: 'opens on top', onclick: () => pushSkill(r) }, `requires ${r}`));
      for (const o of fm.optional || []) chips.append(el('span', { class: 'chip dep opt', title: 'opens on top', onclick: () => pushSkill(o) }, `optional ${o}`));
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) chips.append(el('span', { class: 'chip dep ext', onclick: () => window.open(e.source, '_blank') }, `external ${e.name}`));
      sheet.head.querySelector('.node-head').append(chips);
    }
    if (bindings && bindings.length) {
      const fileLink = (path) => el('a', {
        href: '#', onclick: (ev) => { ev.preventDefault(); fileSheet(path); },
      }, path.includes('templates/') ? path.slice(path.indexOf('templates/')) : path);
      const tbl = el('table', { class: 'ports-table' },
        el('thead', {}, el('tr', {},
          el('th', {}, 'port'), el('th', {}, 'expects'), el('th', {}, 'shipped default'))),
        el('tbody', {}, ...bindings.map(b => el('tr', {},
          el('td', {}, el('code', {}, b.port)),
          el('td', {}, b.expects || ''),
          el('td', {}, b.default ? fileLink(b.default) : '—')))));
      sheet.head.querySelector('.node-head').append(
        el('details', { class: 'ports' }, el('summary', {}, `Ports & bindings (${bindings.length})`), tbl));
    }
  }

  /* Resolve a reference found in prose: repo-rooted prefixes stay, everything else is relative
   * to the current file's directory. */
  function repoPath(t, dir) {
    if (/^(docs|skills|site|tools)\//.test(t)) return t;
    return new URL(t, `http://x/${dir}/`).pathname.slice(1);
  }

  /* Make named references clickable: markdown links, sibling-skill names in backticks, and
   * file paths in backticks — each opens a stacked sheet on top of this one. */
  function wireRefs(div, path) {
    const dir = path.split('/').slice(0, -1).join('/');
    div.querySelectorAll('a[href]').forEach(a => {
      const href = a.getAttribute('href');
      if (/^https?:/.test(href)) { a.target = '_blank'; return; }
      a.addEventListener('click', (ev) => { ev.preventDefault(); fileSheet(repoPath(href.split('#')[0], dir)); });
    });
    const skills = new Set(state.views.sdlc.nodes.map(n => n.id));
    const BARE = {
      'CONTEXT.md': 'CONTEXT.md', 'AGENTS.md': 'AGENTS.md',
      'platform.md': 'docs/agents/platform.md', 'backlog-policy.md': 'docs/agents/backlog-policy.md',
      'environment.md': 'docs/agents/environment.md', 'evidence.md': 'docs/agents/evidence.md',
    };
    div.querySelectorAll('code').forEach(c => {
      if (c.closest('pre') || c.closest('a')) return;
      const t = c.textContent.trim();
      const fileRef = BARE[t]
        || (t.includes('/') && !t.includes(' ') && /^[\w./-]+\.(md|py|html|yaml|yml|json|txt)$/.test(t) ? repoPath(t, dir) : null);
      if (skills.has(t)) {
        c.classList.add('ref'); c.title = `open the ${t} skill on top`;
        c.addEventListener('click', () => pushSkill(t));
      } else if (fileRef) {
        c.classList.add('ref'); c.title = 'open this file on top';
        c.addEventListener('click', () => fileSheet(fileRef));
      }
    });
  }

  /* Wrap each `## section` of the rendered markdown in an open <details> card so a long file
   * reads (and collapses) in parts. */
  function sectionize(container) {
    const kids = [...container.childNodes];
    const out = []; let cur = null;
    for (const k of kids) {
      if (k.nodeName === 'H2') {
        cur = el('details', { class: 'sec', open: '' }, el('summary', {}, ...[...k.childNodes]));
        out.push(cur);
      } else if (cur) cur.append(k);
      else out.push(k);
    }
    container.innerHTML = '';
    container.append(...out);
  }

  async function renderFile(sheet, path) {
    const body = sheet.body; body.innerHTML = '';
    const bar = el('p', { class: 'filebar' },
      el('a', { class: 'filepath', href: `${BASE}/${path}`, target: '_blank', title: 'open raw in a new tab' }, path));
    body.append(bar);
    const target = el('div', { class: 'md' }, 'Loading…'); body.append(target);
    try {
      const text = await fetchText(path);
      target.innerHTML = '';
      if (!/\.(md|markdown)$/i.test(path)) {
        target.append(el('pre', { class: 'raw' }, text));
      } else {
        const { fm, body: mdBody } = parseFrontmatter(text);
        if (Object.keys(fm).length) {
          const card = el('dl', { class: 'fm-card' });
          for (const [k, v] of Object.entries(fm)) { card.append(el('dt', {}, k)); card.append(el('dd', {}, typeof v === 'string' ? v : JSON.stringify(v))); }
          target.append(el('details', { class: 'fm' }, el('summary', {}, 'frontmatter'), card));
        }
        const div = el('div'); div.innerHTML = md.render(mdBody);
        wireRefs(div, path);
        sectionize(div);
        target.append(div);
        const secs = div.querySelectorAll('details.sec');
        if (secs.length > 1) bar.append(el('span', { class: 'sec-ctl' },
          el('button', { onclick: () => secs.forEach(s => s.setAttribute('open', '')) }, 'expand all'),
          el('button', { onclick: () => secs.forEach(s => s.removeAttribute('open')) }, 'collapse all')));
      }
      body.scrollTop = 0;
    } catch (e) {
      target.innerHTML = '';
      target.append(el('div', { class: 'err' }, `Could not load ${path}: ${e.message}. Serve the repo root (python3 -m http.server) — file:// cannot fetch.`));
    }
  }

  function fileMenu(sheet, files, activeFull, onPick) {
    sheet.tabs.innerHTML = '';
    const cur = files.find(f => f.full === activeFull) || files[0];
    const det = el('details', { class: 'file-menu' });
    const menu = el('div', { class: 'menu' });
    let lastGroup = null;
    for (const f of files) {
      if (f.group !== lastGroup) { menu.append(el('div', { class: 'mgrp' }, f.group || 'files')); lastGroup = f.group; }
      const b = el('button', { onclick: () => { det.removeAttribute('open'); onPick(f); } }, f.label);
      if (f.full === cur.full) b.classList.add('active');
      menu.append(b);
    }
    det.append(el('summary', {},
      el('span', { class: 'grp' }, cur.group || 'file'), el('b', {}, cur.label), el('span', { class: 'car' }, '▾')), menu);
    sheet.tabs.append(det,
      el('span', { class: 'file-count' }, `${files.length} files · named references open stacked`));
  }

  function skillSheet(node, filePath) {
    const key = `skill:${node.id}`;
    if (topKey() === key) return;
    const fm = state.fm[node.id] || {};
    const sheet = pushSheet(key);
    sheetChrome(sheet, node.title, fm.description || node.blurb, fm, node.bindings);
    const files = node.files.map(f => ({ ...f, full: `${node.source}/${f.path}` }));
    for (const p of node.playbooks || []) files.push({ group: 'Playbooks (this repo)', label: p.split('/').pop().replace('.md', ''), path: p, full: p });
    const pick = (f) => {
      fileMenu(sheet, files, f.full, pick);
      renderFile(sheet, f.full);
      if (sheet === sheetStack[0]) setHash(state.current, state.active, f.full);
    };
    pick(files.find(f => f.full === filePath) || files[0]);
  }

  function pushSkill(name) {
    const node = state.views.sdlc.nodes.find(n => n.id === name);
    if (node) skillSheet(node);
  }

  function fileSheet(path) {
    const key = `file:${path}`;
    if (topKey() === key) return;
    const sheet = pushSheet(key);
    sheetChrome(sheet, path.split('/').pop(), path, null);
    renderFile(sheet, path);
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
      if (node.open.node) {
        const target = state.views.sdlc.nodes.find(n => n.id === node.open.node);
        if (!target) return;
        closeAllSheets(); markActive(nodeId); setHash(viewId, nodeId);
        skillSheet(target, filePath);
        return;
      }
      if (node.open.file) {
        closeAllSheets(); markActive(nodeId); setHash(viewId, nodeId);
        const sheet = pushSheet(`file:${node.open.file}`);
        sheetChrome(sheet, node.title, node.blurb, null);
        renderFile(sheet, node.open.file);
        return;
      }
    }
    closeAllSheets(); markActive(nodeId);
    skillSheet(node, filePath);
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
    closeAllSheets();
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
