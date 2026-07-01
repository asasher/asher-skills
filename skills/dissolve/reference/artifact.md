# The artifact

How to create and maintain `dissolution.html` — the single source of truth. Read when scaffolding a new
dissolution or writing into the page.

## Scaffolding a new dissolution (`new`)

1. **Slugify** the question into a short kebab-case folder name (`Is free will real?` → `free-will`; keep it
   under ~4 words). If the folder exists, append `-2`.
2. `mkdir -p <slug>/sources`.
3. Copy `templates/dissolution.html` → `<slug>/dissolution.html`.
4. Replace the three placeholders: `{{QUESTION}}` (verbatim question, twice — `<title>` and `<h1>`) and
   `{{DATE}}` (today, `YYYY-MM-DD`, everywhere it appears).
5. Open with move 1.

## The layout of the page

The page is both the state and the artifact. Its five sections mirror the five moves, plus a running **Session
log** and a **References** list. Each move-section carries `data-status="empty|active|done"` and a matching rail
chip at the top — this is how `resume` reads where the work stands. There is **no separate state file**; if it
isn't in the HTML, it isn't saved.

## Editing rules

- **Edit only between markers.** Every fillable region is bracketed by `<!-- FILL: name -->` … `<!-- /FILL: name
  -->`. Replace the content between them; leave the markers, the `.hint` paragraphs, and the section scaffolding
  in place. The hints are authoring guidance and stay for the next session.
- **Keep edits surgical.** Use `Edit` on the specific region, not a full-file rewrite — the page accumulates
  across sessions and a rewrite risks dropping earlier thinking.
- **Drive status from reality.** When a move becomes active, set its `<section data-status>` **and** its rail
  chip `data-s` to `active`; when its *done-when* signal is met, set both to `done`. Update the `<b id="updated">`
  date and, once move 5's gate passes, `<b id="overall">` to `dissolved`.
- **Every session leaves a log entry.** Prepend a new `.log-entry` (newest on top) to the `FILL: log` region:
  the date, what moved, what the human reported, and the pick-up point for next time.

## Writing each section

- **taboo** — fill the two-column table: banned word → what it stands for. For an irreplaceable word, say so in
  the right column ("can't restate without it — this is the confusion").
- **trace** — prose stack trace, then a Mermaid `graph TD` decomposing the question into sub-questions. Write
  real Mermaid inside `<pre class="mermaid">`; it renders on load. Keep node labels short.
- **anticipate** — one table row per sub-question: *if yes* / *if no* predictions, and a **Verdict** cell
  (`empty`, `empirical`, or `value`).
- **resolution** — the `.verdict` sentence (what's left of the question), the lingering-confusion check (what the
  human reported at the gate), and open threads as `<li>`s.

## Diagrams

Mermaid is loaded from CDN in the template — no setup. Use `graph TD` for the sub-question tree (move 3),
`flowchart LR` for a stack trace, `mindmap` for a concept's facets. If a diagram fails to render, it's almost
always a label with an unescaped `(` `)` or `:` — wrap the label in quotes: `a["is it (their) fault?"]`.

## Sources & citations

This is where references live when they can't be inline:

- **Save the source.** Copy files (PDFs, saved articles, screenshots) into the dissolution's `sources/` folder.
- **Register it.** Add an `<li>` to the `FILL: refs` ordered list: author/title, and a link — `sources/paper.pdf`
  for a local file, or the URL for an external one.
- **Cite inline.** Reference it in the thinking with a superscript anchor: `<a class="cite" href="#refs">[3]</a>`.
  The number is the source's position in the References list.
- **Never inline a wall of text.** A long quote goes to `sources/` (or a `<blockquote>` trimmed to the load-
  bearing sentence) and is cited — the page stays readable and shareable.
