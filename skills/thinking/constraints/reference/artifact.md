# The artifact

How to create and maintain `constraint.html` — the single source of truth for one system under study. Read when
scaffolding a new system or writing into the page.

## Scaffolding a new system (`new`)

1. **Slugify** the system into a short kebab-case folder name (`Acme onboarding funnel` → `acme-onboarding`;
   keep it under ~4 words). If the folder exists, append `-2`.
2. `mkdir -p <slug>/sources`.
3. Copy `templates/constraint.html` → `<slug>/constraint.html`.
4. Replace the placeholders: `{{SYSTEM}}` (the system's name, twice — `<title>` and `<h1>`) and `{{DATE}}`
   (today, `YYYY-MM-DD`, everywhere it appears).
5. Open with the goal conversation ([map.md](map.md)).

## The layout of the page

The page is both the state and the artifact. Six arc sections — **Goal, Map, Find, Plan, Experiments, Loop** —
plus a running **Session log** and **References**. Each arc section carries `data-status="empty|active|done"`
and a matching rail chip in the masthead; this is how `resume` reads where the work stands. The masthead also
carries the **dashboard** — current constraint, type, confidence, cycle number, next review date — which must
answer "what's the constraint?" in one glance. There is **no separate state file**; if it isn't in the HTML, it
isn't saved.

## Editing rules

- **Edit only between markers.** Every fillable region is bracketed by `<!-- FILL: name -->` …
  `<!-- /FILL: name -->`. Replace content between them; leave the markers, the `.hint` paragraphs, and the
  section scaffolding in place. Hints are authoring guidance and stay for the next session.
- **Keep edits surgical.** Use `Edit` on the specific region, not a full-file rewrite — the page accumulates
  across sessions and cycles; a rewrite risks dropping history.
- **Drive status from reality.** When a step becomes active, set its `<section data-status>` **and** its rail
  chip `data-s` to `active`; when its done-when signal (defined in each command reference) is met, set both to
  `done`. The section-header chip text renders itself from `data-status` — leave those `.st` spans empty.
  Update `<b id="updated">` every session.
- **Keep the dashboard true.** Whenever the named constraint, its type, its confidence mark, the cycle number,
  or the next review date changes, update the corresponding `id="d-*"` value in the masthead. The dashboard
  lies to nobody: no named constraint yet → `d-constraint` stays "hunting…".
- **Every session leaves a log entry.** Prepend a `.log-entry` (newest on top) to `FILL: log`: the date, what
  moved, what the user reported or decided, the pick-up point for next time.

## Writing each section

- **goal** — the system and its boundary, the goal in the user's words, the **throughput unit** (bold it — the
  countable thing), necessary conditions, and which value stream this page covers if several exist.
- **map** — the flow diagram (below), then the scan table: one row per finding from the queue / scarcity /
  policy scans, with the observable behind it and a `[n]` cite where a source file backs it.
- **find** — the suspects table (suspect · type · evidence for · evidence against · confidence chip), the two
  doubling tests with their answers, any `dig` trees, and the **verdict block**: fill the placeholder
  `<p class="verdict" hidden>` and remove its `hidden` attribute — the named constraint in one sentence, its
  type, mark, and what evidence would move the mark rightward.
- **plan** — exploit moves as a checked/unchecked task list (unchecked = not yet running), subordination rules
  as policy sentences ("release no new X until…"), any `cloud` diagrams, and the elevate options table — each
  option with its ΔT vs ΔI+ΔOE test — visually gated behind the exploit list.
- **experiments** — one `.xp` card per experiment (markup below), newest first. Cards are never deleted; a
  dead one gets `data-state="abandoned"` and a one-line epitaph.
- **loop** — one `.cycle` entry per completed cycle, newest on top: the constraint that was, what broke it,
  what the system metric did, where the constraint moved, and the **inertia sweep** — which rules/buffers/
  metrics built for that constraint were retired (unretired ones are next cycle's first suspects).

## Confidence marks

Inline chips: `<span class="mark" data-m="suspected">suspected</span>` (also `evidenced`, `validated`). Use
them in the suspects table, the verdict block, and the dashboard `d-conf`. Move a mark rightward only on
observables — the rules live in [framework.md](framework.md).

## Diagrams

Mermaid is loaded from CDN in the template — no setup. Write real Mermaid inside `<pre class="mermaid">`; it
renders on load. Conventions:

- **Flow map** (`map`) — `flowchart LR`, one node per stage, demand on the left, goal on the right. Annotate
  queues inside labels with `<br/>` — `rev["Code review<br/>queue 14 · wait ~5d"]`. Mark the current
  constraint node `:::constraint` and known queue pile-ups `:::queue`; the `classDef`s ship in the template.
  Re-annotate counts as evidence updates — the map is a living instrument, not a sketch.
- **Current Reality Tree** (`dig`) — `flowchart BT`, causes at the bottom, UDEs at the top, so arrows read
  "IF lower THEN upper". Tag UDE nodes `:::ude`, the core problem `:::core`. AND-junctions are small nodes
  labeled `AND`(`:::and`).
- **Evaporating Cloud** (`cloud`) — `flowchart RL` so prerequisites point toward the objective: `D --> B --> A`,
  `Dp --> C --> A`, conflict edge `D <-. conflict .-> Dp`. Tag `A` `:::obj`, `D`/`Dp` `:::want`. Put the
  assumption being attacked on the edge label; the chosen injection node gets `:::inj`.
- Labels with `(` `)` `:` must be quoted: `a["wait (median 5d)"]`.

## Experiment cards

```html
<div class="xp" data-state="planned">  <!-- planned | running | adopted | abandoned -->
  <div class="xp-head"><span class="xp-id">XP-1</span><h3>Reviewer rotation</h3><span class="st"></span></div>
  <p class="hyp">If we <b>[change]</b> at <b>[constraint]</b>, because <b>[mechanism]</b>,
     then <b>[metric]</b> moves <b>[amount]</b> by <b>[date]</b>, while <b>[guardrail]</b> holds.</p>
  <dl class="xp-meta">
    <dt>Baseline</dt><dd>…</dd> <dt>Predicted</dt><dd>…</dd> <dt>Actual</dt><dd>—</dd>
    <dt>Review</dt><dd>YYYY-MM-DD</dd> <dt>Decision</dt><dd>—</dd>
  </dl>
</div>
```

The status chip text renders from `data-state` automatically. `Decision` is filled at review with one of:
adopt · adapt · abandon · elevate · re-identify.

## Sources & citations

- **Save the evidence.** Metric exports, screenshots, queue snapshots, logs → the system's `sources/` folder.
- **Register it.** Add an `<li>` to `FILL: refs`: what it is, when captured, and a link (`sources/file.png` or
  an external URL).
- **Cite inline.** `<a class="cite" href="#refs">[3]</a>` wherever the number backs a claim — especially in
  the scan table and suspects board, where the marks depend on it.
- **Never inline a wall of data.** The page stays readable; raw data lives in `sources/`.
