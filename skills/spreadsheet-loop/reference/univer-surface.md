# The Univer surface — scaffold recipe

Phase 3 stands up the browser surface: a small Vite + Univer app whose only job is to render
`workbook.snapshot.json` and persist edits back to it, so the human and the agent share one source of truth.
The complete, self-contained project template ships in this skill's `templates/app/`.

## What the scaffold is

Copy `templates/app/` into the project (and `templates/MODEL.md` / `templates/LAYOUT.md` to the root if not
already written in phase 2). It contains:

```
package.json          # scripts (dev / compile / import / verify / test:converter / recompute)
requirements.txt      # openpyxl (the converter's only Python dep)
vite.config.js        # dev server + /snapshot (GET) and /save (POST) persistence middleware
index.html            # mount point + a small save-status indicator
src/main.js           # createUniver, load /snapshot, debounced autosave to /save
workbook.snapshot.json# source of truth: Univer-native cells (starts as one empty sheet)
objects.json          # source of truth: declared charts + pivots (starts empty)
converter/            # snapshot-to-xlsx.py, xlsx-to-snapshot.py (Python/openpyxl), sample.*, test.py
verify/               # read-back-check.py (layer 2, openpyxl), recompute.mjs (layer 1, Univer node)
```

The project is polyglot on purpose: **Node/Vite** runs the browser surface, **Python/openpyxl** is the
converter. Then:

```bash
npm install                 # Univer presets + Vite
pip install -r requirements.txt   # openpyxl
npm run test:converter      # sanity-check the converter (19-check self-test) before relying on it
npm run dev                 # serve the surface (Vite, listening on all interfaces for the proxy)
```

## Why persistence lives in the dev server

A browser can't write local files, so `vite.config.js` adds the persistence + turn-safety layer:

- `GET /snapshot` and `GET /objects` serve the two source files, each with an `X-Workbook-Version` header
  (a content hash).
- `POST /save` and `POST /save-objects` write them atomically (temp + rename). Each carries an
  `X-Base-Version` header; a save whose base version is stale (an agent edited during its turn) is refused
  with **HTTP 409**, and the browser reloads instead of clobbering.
- A **file watcher** reloads the browser whenever the agent writes a file directly, so the human never keeps
  editing a stale in-memory workbook.

`src/main.js` autosaves (debounced) on every edit and tracks the loaded version. That loop — browser edits →
`/save` → file on disk, agent edits → file → browser reload — is what makes the [turn-based loop](the-loop.md)
safe. Keep it to one process (`npm run dev`); don't add a separate backend.

## Starting from an existing .xlsx

If intake said "start from this workbook," seed the snapshot before serving:

```bash
npm run import -- path/to/existing.xlsx   # writes workbook.snapshot.json
npm run dev
```

The import recovers values, formulas, styles, merges, sizing, freeze, and named ranges (see
[converter](converter.md) for what it does *not* recover). Sanity-check the imported snapshot on the surface
before iterating.

## Serving on the presentation surface

Present the running dev server on the repo's presentation surface (the tailnet root in
`docs/agents/environment.md`) so the human can open it remotely — the same surface `review-loop` uses, but
here the app is driven live, not gated. End any hand-back turn with the surface URL. Absent surface config,
fall back to a local open and say remote access is unavailable.

## Version pinning

The template pins Univer presets at `^0.10`. Univer's API has moved across minors (e.g. `getSnapshot()` →
`save()`); if a newer major is installed, re-check the Facade calls in `src/main.js` and `verify/recompute.mjs`
against `docs.univer.ai/reference/facade` before relying on them. This is the one place the scaffold is
version-sensitive.

> Phase-3 smoke test (do it once per scaffold, in a browser): `npm run dev`, open the surface, type a value
> and a formula, confirm the status indicator shows "saved," and confirm `workbook.snapshot.json` on disk
> updated. Only then enter the loop.
