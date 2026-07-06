/* Review chrome — injected at serve time. Click a block's "+ comment" chip to
   annotate; comments batch locally; one submit carries them with a verdict. */
(function () {
  'use strict';
  var B = window.__REVIEW_BOOTSTRAP__ || {};
  var KEY = 'rv-drafts:' + (B.issue || 'doc');
  var drafts = [];
  try { drafts = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { drafts = []; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(drafts)); } catch (e) {} }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  var threads = B.threads || [];
  var round = threads.filter(function (t) { return t.verdict === 'request_changes'; }).length + 1;
  var decided = threads.some(function (t) { return t.verdict === 'approve' || t.verdict === 'approve_with_nits'; });

  // --- skeleton ---------------------------------------------------------------
  var root = document.createElement('div');
  root.id = 'rv-root';
  root.innerHTML =
    '<button id="rv-toggle" title="Review panel">&#9998;<span id="rv-count"></span></button>' +
    '<aside id="rv-panel">' +
    '  <header>' +
    '    <div><strong>Review</strong> <span class="rv-badge">' + esc(B.kind || 'plan') + '</span></div>' +
    '    <div class="rv-sub">' + esc(B.title || '') + ' &middot; round ' + round + ' &middot; v' + esc((B.docHash || '').slice(0, 8)) +
    '      &middot; <a href="' + esc(B.hubUrl || '/hub') + '">hub</a></div>' +
    '  </header>' +
    '  <div id="rv-banner"></div>' +
    '  <div id="rv-body">' +
    '    <div class="rv-h">Your comments</div><div id="rv-drafts"></div>' +
    '    <div class="rv-h">Previous rounds</div><div id="rv-threads"></div>' +
    '  </div>' +
    '  <div id="rv-verdicts">' +
    '    <button id="rv-changes">Request changes</button>' +
    '    <button id="rv-nits">Approve with nits</button>' +
    '    <button id="rv-approve">Approve</button>' +
    '  </div>' +
    '</aside>' +
    '<button id="rv-chip">+ comment</button>' +
    '<div id="rv-modal"><div class="rv-dialog"></div></div>';
  document.body.appendChild(root);

  var $ = function (id) { return document.getElementById(id); };
  var panelOpen = false;
  function setOpen(open) { panelOpen = open; root.classList.toggle('rv-open', open); }
  $('rv-toggle').addEventListener('click', function () { setOpen(!panelOpen); });

  // --- banner -------------------------------------------------------------------
  function banner(html, kind) {
    var el = $('rv-banner');
    el.innerHTML = html;
    el.className = kind || '';
    el.style.display = html ? 'block' : 'none';
  }

  // --- annotate chip --------------------------------------------------------------
  var chip = $('rv-chip');
  var chipTarget = null;
  document.addEventListener('mouseover', function (e) {
    if (decided) return;
    if (e.target.closest('#rv-root')) return;
    var el = e.target.closest('[id]');
    if (!el || /^rv-/.test(el.id) || el === document.body || el === document.documentElement) {
      if (!e.target.closest('#rv-chip')) hideChip();
      return;
    }
    chipTarget = el;
    el.classList.add('rv-hoverable');
    var r = el.getBoundingClientRect();
    chip.style.display = 'block';
    chip.style.top = (window.scrollY + r.top - 12) + 'px';
    chip.style.left = Math.max(8, window.scrollX + r.right - chip.offsetWidth) + 'px';
  });
  document.addEventListener('mouseout', function (e) {
    var el = e.target.closest && e.target.closest('[id]');
    if (el) el.classList.remove('rv-hoverable');
  });
  function hideChip() { chip.style.display = 'none'; if (chipTarget) chipTarget.classList.remove('rv-hoverable'); chipTarget = null; }
  chip.addEventListener('click', function () {
    if (!chipTarget) return;
    var el = chipTarget;
    var quote = '';
    var sel = window.getSelection();
    if (sel && !sel.isCollapsed && el.contains(sel.anchorNode)) quote = sel.toString().trim().slice(0, 300);
    var head = el.querySelector('h1,h2,h3,h4');
    var label = el.getAttribute('data-label') ||
      (head ? head.textContent.trim() : (/^h[1-4]$/i.test(el.tagName) ? el.textContent.trim() : el.id));
    drafts.push({ anchor: el.id, label: label.slice(0, 80), quote: quote || null, text: '' });
    save(); hideChip(); setOpen(true); render();
    var boxes = $('rv-drafts').querySelectorAll('textarea');
    if (boxes.length) boxes[boxes.length - 1].focus();
  });

  // --- rendering ------------------------------------------------------------------
  function anchorLink(anchor, label) {
    return '<span class="rv-anchor" data-goto="' + esc(anchor) + '">' + esc(label || anchor) + '</span>';
  }
  function renderDrafts() {
    var host = $('rv-drafts');
    if (!drafts.length) {
      host.innerHTML = '<div class="rv-empty">Hover any block in the document and hit &ldquo;+ comment&rdquo;. Select text first to quote it.</div>';
    } else {
      host.innerHTML = drafts.map(function (d, i) {
        return '<div class="rv-item">' +
          '<button class="rv-remove" data-i="' + i + '" title="Discard">&times;</button>' +
          anchorLink(d.anchor, d.label) +
          (d.quote ? '<span class="rv-quote">&ldquo;' + esc(d.quote) + '&rdquo;</span>' : '') +
          '<textarea data-i="' + i + '" placeholder="What should change?">' + esc(d.text) + '</textarea>' +
          '</div>';
      }).join('');
    }
    var n = drafts.filter(function (d) { return d.text.trim(); }).length;
    var count = $('rv-count');
    count.style.display = n ? 'block' : 'none';
    count.textContent = n;
  }
  function dispositionBadge(a) {
    var d = a.disposition || 'pending';
    var label = { changed: 'changed', kept: 'kept', orphaned: 'orphaned', pending: 'awaiting agent' }[d] || d;
    return '<span class="rv-badge rv-' + esc(d) + '">' + esc(label) + '</span>';
  }
  function renderThreads() {
    var host = $('rv-threads');
    if (!threads.length) { host.innerHTML = '<div class="rv-empty">None yet — this is the first round.</div>'; return; }
    host.innerHTML = threads.slice().reverse().map(function (t, ri) {
      var n = threads.length - ri;
      var verdictLabel = { approve: 'approved', approve_with_nits: 'approved with nits', request_changes: 'changes requested' }[t.verdict] || t.verdict;
      return '<div class="rv-round">' +
        '<div class="rv-roundhead">Round ' + n + ' &middot; <span class="rv-badge rv-verdict-' + esc(t.verdict) + '">' + esc(verdictLabel) + '</span> &middot; ' + esc((t.timestamp || '').slice(0, 16).replace('T', ' ')) + '</div>' +
        (t.annotations || []).map(function (a) {
          return '<div class="rv-item">' + anchorLink(a.anchor, a.label) + ' ' + dispositionBadge(a) +
            (a.quote ? '<span class="rv-quote">&ldquo;' + esc(a.quote) + '&rdquo;</span>' : '') +
            '<div class="rv-text">' + esc(a.text) + '</div>' +
            (a.note ? '<div class="rv-note">' + esc(a.note) + '</div>' : '') +
            '</div>';
        }).join('') +
        '</div>';
    }).join('');
  }
  function markAnnotated() {
    document.querySelectorAll('.rv-annotated').forEach(function (el) { el.classList.remove('rv-annotated'); });
    var anchors = {};
    drafts.forEach(function (d) { anchors[d.anchor] = 1; });
    threads.forEach(function (t) { (t.annotations || []).forEach(function (a) { anchors[a.anchor] = 1; }); });
    Object.keys(anchors).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.classList.add('rv-annotated');
    });
  }
  function updateVerdicts() {
    var hasText = drafts.some(function (d) { return d.text.trim(); });
    $('rv-approve').disabled = decided || hasText;
    $('rv-approve').title = hasText ? 'You have unsent comments — use "Approve with nits" or discard them.' : '';
    $('rv-nits').disabled = decided || !hasText;
    $('rv-changes').disabled = decided || !hasText;
  }
  function render() { renderDrafts(); renderThreads(); markAnnotated(); updateVerdicts(); }

  document.addEventListener('input', function (e) {
    if (e.target.matches('#rv-drafts textarea')) {
      drafts[+e.target.getAttribute('data-i')].text = e.target.value;
      save(); updateVerdicts();
      var n = drafts.filter(function (d) { return d.text.trim(); }).length;
      var count = $('rv-count');
      count.style.display = n ? 'block' : 'none';
      count.textContent = n;
    }
  });
  document.addEventListener('click', function (e) {
    var rm = e.target.closest('.rv-remove');
    if (rm) { drafts.splice(+rm.getAttribute('data-i'), 1); save(); render(); return; }
    var go = e.target.closest('.rv-anchor');
    if (go) {
      var el = document.getElementById(go.getAttribute('data-goto'));
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.remove('rv-flash'); void el.offsetWidth; el.classList.add('rv-flash');
      }
    }
  });

  // --- submit ----------------------------------------------------------------------
  function post(verdict) {
    var annotations = drafts.filter(function (d) { return d.text.trim(); })
      .map(function (d) { return { anchor: d.anchor, label: d.label, quote: d.quote, text: d.text.trim() }; });
    fetch('/event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: B.token, type: 'feedback_submitted', verdict: verdict, doc_hash: B.docHash, annotations: annotations })
    }).then(function (res) {
      if (res.status === 409) {
        banner('The document changed since you loaded it. <button onclick="location.reload()">Reload latest</button>', 'rv-warn');
        return;
      }
      if (!res.ok) { banner('Submit failed (' + res.status + ').', 'rv-warn'); return; }
      drafts = []; save();
      decided = verdict !== 'request_changes';
      threads.push({ verdict: verdict, timestamp: new Date().toISOString(), annotations: annotations });
      banner(verdict === 'request_changes'
        ? 'Sent — the agent is revising. This page reloads when the new version lands.'
        : 'Approved &middot; v' + esc((B.docHash || '').slice(0, 8)) + ' — the agent has it.', 'rv-ok');
      render();
    }).catch(function () { banner('Submit failed — is the server up?', 'rv-warn'); });
  }
  $('rv-changes').addEventListener('click', function () { post('request_changes'); });
  $('rv-nits').addEventListener('click', function () { post('approve_with_nits'); });
  $('rv-approve').addEventListener('click', function () {
    var criteria = document.querySelectorAll('[data-criterion]').length;
    var dialog = $('rv-modal').querySelector('.rv-dialog');
    dialog.innerHTML = '<h3>Approve this ' + esc(B.kind || 'plan') + '?</h3>' +
      '<div>Version <code>v' + esc((B.docHash || '').slice(0, 8)) + '</code>' +
      (criteria ? ' &middot; ' + criteria + ' acceptance criteria' : '') +
      '. Approval dispatches implementation.</div>' +
      '<div class="rv-actions"><button class="rv-cancel">Cancel</button><button class="rv-confirm">Approve</button></div>';
    $('rv-modal').style.display = 'flex';
    dialog.querySelector('.rv-cancel').onclick = function () { $('rv-modal').style.display = 'none'; };
    dialog.querySelector('.rv-confirm').onclick = function () { $('rv-modal').style.display = 'none'; post('approve'); };
  });

  // --- version polling ---------------------------------------------------------------
  setInterval(function () {
    fetch('/version?token=' + encodeURIComponent(B.token)).then(function (r) { return r.json(); }).then(function (v) {
      if (v.hash && v.hash !== B.docHash) {
        if (drafts.some(function (d) { return d.text.trim(); })) {
          banner('A new version landed. Finish your comments, or <button onclick="location.reload()">reload now</button> (drafts are kept).', 'rv-warn');
        } else {
          banner('New version — reloading&hellip;', 'rv-ok');
          setTimeout(function () { location.reload(); }, 700);
        }
      }
    }).catch(function () {});
  }, 2500);

  if (decided) banner('This ' + esc(B.kind || 'plan') + ' is approved — review is read-only.', 'rv-ok');
  render();
  if (threads.length || drafts.length) setOpen(true);
})();
