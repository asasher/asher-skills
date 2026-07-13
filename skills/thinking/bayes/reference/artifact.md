# The artifact

How to create and maintain `question.html` — the single source of truth for one question under study. Read
when scaffolding a new question or writing into the page.

## Scaffolding a new question (`new`)

Scaffold **after** the pose conversation has produced a sharpened claim — the placeholders want the final
wording, and a question that dies in triage never needs a folder.

1. **Slugify** the question into a short kebab-case folder name (`Will Acme deliver by Q4?` →
   `acme-delivery`; keep it under ~4 words). If the folder exists, append `-2`.
2. `mkdir -p <slug>/sources`.
3. Copy `templates/question.html` → `<slug>/question.html`.
4. Replace the placeholders: `{{QUESTION}}` (the sharpened claim, twice — `<title>` and `<h1>`) and
   `{{DATE}}` (today, `YYYY-MM-DD`, everywhere it appears).
5. If the workspace root has no `calibration.md` yet, create it with the header row from
   [review.md](review.md).
6. Open with the pose conversation ([pose.md](pose.md)).

## The layout of the page

Five arc sections — **Question, Board, Evidence, Trajectory, Resolution** — plus a running **Session log**
and **References**. Each arc section carries `data-status="empty|active|done"` and a matching rail chip in
the masthead. The masthead dashboard — leading hypothesis, the user's credence, the agent's credence, open
cards, next review — must answer "where does this stand?" in one glance. There is **no separate state
file**; if it isn't in the HTML, it isn't saved.

## Editing rules

- **Edit only between markers.** Every fillable region is bracketed by `<!-- FILL: name -->` …
  `<!-- /FILL: name -->`. Replace content between them; leave the markers, the `.hint` paragraphs, and the
  section scaffolding in place.
- **Keep edits surgical.** Use `Edit` on the specific region, not a full-file rewrite — the page
  accumulates across sessions; a rewrite risks dropping history.
- **The trajectory is append-only.** Rows in `FILL: trajectory` and bars in `FILL: waterfall` are *never*
  edited or deleted — this is the skill's hindsight defense and it is absolute. Corrections (a late-merged
  cluster, a vetoed posterior) are **new rows** with a note in the last column. Everything else on the page
  is living material; the trajectory is the sediment.
- **Drive status from reality.** Section `data-status` and its rail chip `data-s` move to `active`/`done`
  when the step's done-when (in each command reference) is met. The `.st` chips render text from
  `data-status` — leave them empty. Update `<b id="updated">` every session.
- **Keep the dashboard true.** Whenever the leader, either credence, the open-card count, or the review
  date changes, update the matching `id="d-*"` value. No leader yet → `d-leader` stays "framing…".
- **Every session leaves a log entry.** Prepend a `.log-entry` (newest on top) to `FILL: log`: date, what
  came back, how the board moved, the card the user left with.

## Writing each section

- **question** — the claim as sharpened, the type chip (`forecast` / `diagnosis` / `standing`), resolution
  criteria as referee instructions, horizon/review cadence, and **the rent**: the decision this feeds and
  its threshold, bolded.
- **board** — the reference class in the blockquote (named, with pedigree), then one `.hy` row per
  hypothesis — *something else* always last. Bar widths and figures update every `update`; the prior tick
  never moves after `frame`.
- **evidence** — one `.ev` card per look (markup below), newest first; below the cards, the ACH matrix
  table — one row per *scored* item or cluster, one column per hypothesis, cells `++ + 0 − −−`. Cards are
  never deleted: a rigged or abandoned card gets `data-state="void"` and one line on why — a void card is
  evidence about how the question is being approached.
- **trajectory** — the append-only table (date · driver · you · agent · leader dB · note) and the waterfall.
- **resolution** — outcome against written criteria, both Brier scores with shape commentary, the evidence
  audit's two or three sentences, the lesson that went to `calibration.md`.

## Hypothesis rows

```html
<div class="hy">
  <div class="hy-head"><b>Failing quietly</b><span class="ped">counted experience</span>
    <span class="cred">you <b>55%</b> · agent <b>62%</b></span></div>
  <div class="track">
    <span class="bar" style="width:55%"></span>
    <span class="tick prior" style="left:35%" title="prior 35%"></span>
    <span class="tick agent" style="left:62%" title="agent 62%"></span>
  </div>
</div>
```

Bar = user's current credence; grey tick = the frozen prior; blue tick = the agent's track. Pedigree label
(`ped`) is one of: `base rate · <class>`, `counted experience`, `calibrated estimate`, `placeholder`.

## Evidence cards

```html
<div class="ev" data-state="open">  <!-- open | scored | void -->
  <div class="ev-head"><span class="ev-id">EV-3</span><h3>Call their other big customer</h3><span class="st"></span></div>
  <dl class="ev-meta">
    <dt>Look</dt><dd>…what, where, by when…</dd>
    <dt>Outcomes</dt><dd><ul>
      <li>they rave → <b>clear</b> toward <i>healthy</i> (−5 dB off the leader)</li>
      <li>lukewarm / evasive → <b>whisper</b> toward <i>failing</i></li>
      <li>can't reach them in a week → <b>whisper</b> toward <i>failing</i></li></ul></dd>
    <dt>Stopping rule</dt><dd>…what makes this line enough, either way…</dd>
    <dt>Lineage</dt><dd>…source; cluster if any…</dd>
    <dt>Result</dt><dd>—</dd>
    <dt>Verdict</dt><dd>—</dd>
  </dl>
</div>
```

`Result` and `Verdict` are filled at scoring: what actually came back, whether the pre-registered update
held (and if the user moved more or less, the stated reason). Unplanned evidence gets a card too, marked
`Lineage: unplanned —` so the flag survives.

## The waterfall

One `.wf` row per applied update (clusters = one row), appended in order:

```html
<div class="wf"><span class="wf-date">2026-07-11</span>
  <span class="wf-label">EV-2 · missed milestone (cluster of 3)</span>
  <span class="wf-track"><span class="wf-bar pos" style="left:50%;width:9.6%"></span></span>
  <span class="wf-db">+4.8 dB</span></div>
```

Scale: **1 dB = 2% width**, center at 50%, cap at ±20 dB. Positive (toward the leader) extends right from
center (`left:50%;width:<2·dB>%`, class `pos`); negative extends left (`left:<50−2·|dB|>%;width:<2·|dB|>%`,
class `neg`). The dB figure is the leader-vs-field shift from method.md.

## Sources & citations

- **Save the evidence.** Screenshots, exports, call notes, links-that-rot → the question's `sources/`
  folder.
- **Register it.** Add an `<li>` to `FILL: refs`: what it is, when captured, link.
- **Cite inline.** `<a class="cite" href="#refs">[3]</a>` on the card's Result and anywhere a number leans
  on it.
- **Never inline a wall of data.** The page stays readable; raw material lives in `sources/`.
