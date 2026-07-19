/* asher-skills documentation app — v3 (Cytoscape canvas: zoom/pan, engine-routed edges).
 * Drift design unchanged: content + dependency edges come from the real files; views/*.json holds only
 * rosters/lanes/blurbs, gated by site/check.py. See site/MAINTENANCE.md. */
(() => {
  const params = new URLSearchParams(location.search);
  const BASE = (params.get('base') || '..').replace(/\/$/, '');
  const VIEW_IDS = ['sdlc', 'flow', 'backlog'];
  const md = window.markdownit({ html: false, linkify: true });

  const state = { views: {}, fm: {}, current: 'sdlc', active: null };
  let cy = null;

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

  /* ---------- element builders (positions are node centers) ---------- */
  const NW = 172, NH = 56;

  function laneKind(laneId) { return `k-${laneId}`; }

  function buildGraphElements(view) {
    const W = 1500, GX = 20, GY = 18, LPAD = 26, LHEAD = 34, LGAP = 46;
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
    const elements = []; const pos = {};
    let y = 0;
    for (const lane of view.lanes) {
      const nodes = perLane[lane.id] || [];
      if (!nodes.length) continue;
      elements.push({ data: { id: `lane:${lane.id}`, title: lane.title, blurb: lane.blurb }, classes: 'lane', selectable: false, grabbable: false });
      const cols = Math.max(1, Math.floor((W - 2 * LPAD + GX) / (NW + GX)));
      const rows = Math.ceil(nodes.length / cols);
      nodes.forEach((n, i) => {
        const cx = LPAD + (i % cols) * (NW + GX) + NW / 2;
        const cyy = y + LHEAD + Math.floor(i / cols) * (NH + GY) + NH / 2;
        pos[n.id] = { x: cx, y: cyy };
        elements.push({
          data: { id: n.id, parent: `lane:${lane.id}`, title: n.title, blurb: n.blurb, view: view.id },
          position: { x: cx, y: cyy },
          classes: `item ${laneKind(n.lane)}${n.external ? ' external' : ''}${n.id === 'merge-changes' ? ' gate' : ''}`,
        });
        if (n.external) pos[n.id].external = n.external;
      });
      y += LHEAD + rows * (NH + GY) + LGAP;
    }
    const edges = [];
    const addEdge = (from, to, cls, label) => {
      if (!pos[from] || !pos[to]) return;
      const horiz = Math.abs(pos[from].y - pos[to].y) < NH;
      edges.push({ data: { id: `e${edges.length}:${from}:${to}`, source: from, target: to, label: label || '' }, classes: `${cls}${horiz ? ' horiz' : ''}` });
    };
    for (const f of view.flow || []) addEdge(f.from, f.to, 'flow', f.label);
    for (const e of view.edges || []) addEdge(e.from, e.to, e.style || '', e.label);
    if (view.id === 'sdlc') for (const n of view.nodes) {
      const fm = state.fm[n.id] || {};
      for (const r of fm.requires || []) addEdge(n.id, r, '');
      for (const o of fm.optional || []) addEdge(n.id, o, 'optional');
      for (const e of (Array.isArray(fm.external) ? fm.external : [])) if (e.name) addEdge(n.id, e.name, 'external');
    }
    return elements.concat(edges);
  }

  function buildSwimElements(view) {
    const GX = 26, GY = 18, LPAD = 30, LGAP = 44, PHEAD = 44;
    const cell = {};
    for (const n of view.nodes) ((cell[n.lane] = cell[n.lane] || {})[n.phase] = cell[n.lane][n.phase] || []).push(n);
    const colX = {}; let x = 0;
    for (const ph of view.phases) { colX[ph.id] = x + NW / 2; x += NW + GX; }
    const elements = [];
    for (const ph of view.phases) {
      elements.push({ data: { id: `phase:${ph.id}`, title: ph.title }, classes: 'phase-head', position: { x: colX[ph.id], y: 0 }, selectable: false, grabbable: false });
    }
    let y = PHEAD;
    for (const lane of view.lanes) {
      const depth = Math.max(1, ...view.phases.map(p => (cell[lane.id] && cell[lane.id][p.id] || []).length));
      elements.push({ data: { id: `lane:${lane.id}`, title: lane.title, blurb: lane.blurb }, classes: 'lane', selectable: false, grabbable: false });
      for (const ph of view.phases) {
        (cell[lane.id] && cell[lane.id][ph.id] || []).forEach((n, idx) => {
          elements.push({
            data: { id: n.id, parent: `lane:${lane.id}`, title: n.title, blurb: n.blurb, view: view.id },
            position: { x: colX[ph.id], y: y + LPAD + idx * (NH + GY) + NH / 2 },
            classes: `item ${laneKind(n.lane)}${n.dashed ? ' dashedn' : ''}`,
          });
        });
      }
      y += LPAD * 2 + depth * (NH + GY) - GY + LGAP;
    }
    const nodesById = Object.fromEntries(view.nodes.map(n => [n.id, n]));
    return elements.concat((view.edges || []).map((e, i) => {
      const a = nodesById[e.from], b = nodesById[e.to];
      const horiz = a && b && a.lane === b.lane && a.phase !== b.phase;
      return { data: { id: `e${i}:${e.from}:${e.to}`, source: e.from, target: e.to, label: e.label || '' }, classes: `${e.style || ''}${horiz ? ' horiz' : ''}${e.bidir ? ' bidir' : ''}` };
    }));
  }

  /* ---------- cytoscape ---------- */
  function cyStyle() {
    const muted = cssVar('--muted'), accent = cssVar('--accent'), line = cssVar('--line'), card = cssVar('--card'), bg = cssVar('--bg');
    const fill = (v, b) => ({ 'background-color': cssVar(v), 'border-color': cssVar(b) });
    return [
      { selector: 'node.item', style: {
        shape: 'round-rectangle', width: NW, height: NH, 'border-width': 1.5, label: '',
        'transition-property': 'opacity', 'transition-duration': '0.12s', ...fill('--stage', '--stage-line') } },
      { selector: '.k-services, .k-probes, .k-sub, .k-siblings', style: fill('--lane', '--lane-line') },
      { selector: '.k-ux, .k-you', style: fill('--human', '--human-line') },
      { selector: '.k-repo, .k-playbooks, .k-setup', style: fill('--artifact', '--artifact-line') },
      { selector: 'node.gate', style: fill('--gate', '--gate-line') },
      { selector: 'node.external, node.dashedn', style: { 'border-style': 'dashed' } },
      { selector: 'node.external', style: fill('--artifact', '--artifact-line') },
      { selector: 'node.active', style: { 'border-color': accent, 'border-width': 3 } },
      { selector: 'node.lane', style: {
        shape: 'round-rectangle', 'background-color': card, 'background-opacity': .55,
        'border-color': line, 'border-width': 1, label: '', padding: '26px' } },
      { selector: 'node.phase-head', style: { 'background-opacity': 0, 'border-width': 0, width: NW, height: 24, label: '' } },
      { selector: 'edge', style: {
        'curve-style': 'taxi', 'taxi-direction': 'vertical', 'taxi-turn': '45%', 'taxi-turn-min-distance': 12,
        width: 1.5, 'line-color': muted, 'target-arrow-color': muted, 'target-arrow-shape': 'triangle',
        'arrow-scale': .75, opacity: .5, label: 'data(label)', 'font-size': 9.5, color: muted,
        'text-background-color': bg, 'text-background-opacity': 1, 'text-background-shape': 'round-rectangle',
        'text-background-padding': 4, 'text-border-color': line, 'text-border-width': 1, 'text-border-opacity': 1,
        'transition-property': 'opacity', 'transition-duration': '0.12s' } },
      { selector: 'edge.horiz', style: {
        'curve-style': 'unbundled-bezier', 'control-point-distances': [46], 'control-point-weights': [0.5] } },
      { selector: 'edge.optional', style: { 'line-style': 'dashed' } },
      { selector: 'edge.external', style: { 'line-style': 'dashed', 'line-color': cssVar('--artifact-line'), 'target-arrow-color': cssVar('--artifact-line'), opacity: .85 } },
      { selector: 'edge.flow', style: { 'line-color': accent, 'target-arrow-color': accent, width: 2.2, opacity: .85 } },
      { selector: 'edge.bidir', style: { 'source-arrow-shape': 'triangle', 'source-arrow-color': muted } },
      { selector: '.dim', style: { opacity: .12 } },
    ];
  }

  function dimHtmlLabels(keepIds) {
    document.querySelectorAll('#cy .cy-title').forEach(d => {
      d.classList.toggle('dimmed', keepIds ? !keepIds.has(d.dataset.nid) : false);
    });
  }

  function renderView() {
    const view = state.views[state.current];
    $('#view-subtitle').textContent = view.subtitle;
    document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('active', b.dataset.view === state.current));
    const elements = view.type === 'swimlane' ? buildSwimElements(view) : buildGraphElements(view);
    if (cy) { cy.destroy(); cy = null; }
    $('#cy').innerHTML = '';
    cy = window.cytoscape({
      container: $('#cy'), elements, style: cyStyle(), layout: { name: 'preset' },
      autoungrabify: true, boxSelectionEnabled: false, wheelSensitivity: .25,
      minZoom: .25, maxZoom: 2.75,
    });
    cy.nodeHtmlLabel([
      { query: 'node.item', tpl: d => `<div class="cy-title" data-nid="${esc(d.id)}"><b>${esc(d.title)}</b><span>${esc(d.blurb)}</span></div>` },
      { query: 'node.lane', halign: 'left', halignBox: 'right', valign: 'top', valignBox: 'top', tpl: d => `<div class="cy-lane"><b>${esc(d.title)}</b><span> — ${esc(d.blurb)}</span></div>` },
      { query: 'node.phase-head', tpl: d => `<div class="cy-phase">${esc(d.title)}</div>` },
    ], { enablePointerEvents: false });
    cy.on('mouseover', 'node.item', (e) => {
      const hood = e.target.closedNeighborhood();
      cy.elements('node.item, edge').not(hood).addClass('dim');
      dimHtmlLabels(new Set(hood.nodes().map(n => n.id())));
      $('#cy').style.cursor = 'pointer';
    });
    cy.on('mouseout', 'node.item', () => {
      cy.elements().removeClass('dim');
      dimHtmlLabels(null);
      $('#cy').style.cursor = '';
    });
    cy.on('tap', 'node.item', (e) => {
      const id = e.target.id();
      const view = state.views[state.current];
      const node = view.nodes.find(n => n.id === id);
      if (!node) { // synthesized external node
        const owner = view.nodes.map(n => (state.fm[n.id] || {}).external || []).flat().find(x => x && x.name === id);
        if (owner) window.open(owner.source, '_blank');
        return;
      }
      openNode(state.current, id);
    });
    cy.fit(undefined, 28);
    if (state.active) cy.$id(state.active).addClass('active');
  }

  /* ---------- sheet ---------- */
  function closeSheet() {
    document.body.classList.remove('sheet-open');
    state.active = null;
    if (cy) cy.$('.active').removeClass('active');
    setHash();
  }
  $('#backdrop').addEventListener('click', closeSheet);
  $('#sheet-close').addEventListener('click', closeSheet);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && document.body.classList.contains('sheet-open')) closeSheet(); });

  function markActive(nodeId) {
    state.active = nodeId;
    if (cy) { cy.$('.active').removeClass('active'); if (nodeId) cy.$id(nodeId).addClass('active'); }
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
    $('#zoom-in').addEventListener('click', () => cy && cy.zoom({ level: cy.zoom() * 1.25, renderedPosition: { x: $('#cy').clientWidth / 2, y: $('#cy').clientHeight / 2 } }));
    $('#zoom-out').addEventListener('click', () => cy && cy.zoom({ level: cy.zoom() / 1.25, renderedPosition: { x: $('#cy').clientWidth / 2, y: $('#cy').clientHeight / 2 } }));
    $('#zoom-fit').addEventListener('click', () => cy && cy.fit(undefined, 28));
    window.addEventListener('resize', () => cy && cy.resize());

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
