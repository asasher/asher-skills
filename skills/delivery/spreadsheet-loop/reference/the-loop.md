# The loop — iterating on the browser surface

Phase 4 is the heart of the browser lanes: the human and agent shape an approved workbook component **in
turns** on the running Univer surface. In lane 1, `workbook.snapshot.json` + `objects.json` is authoritative.
In lane 2 it is a workbench that must emit a bounded changeset; the original Excel file remains authoritative.

## Serve it

Start the scaffolded app (see [univer-surface](univer-surface.md)) and present it on the repo's presentation
surface (the tailnet root from `docs/agents/environment.md`), so the human can open it from wherever they
are. The live surface is **not** a `serve-via-tailnet` artifact — it is a live interactive surface, driven
directly. Sign-off gates are for the paper artifacts (`SPEC.md`, `MODEL.md`, `LAYOUT.md`), not for the loop.

## Turn-based: one pen at a time

The two files are the **board**; exactly one party holds the **pen** at a time. This is deliberate — it makes
the collaboration robust without any merge/OT machinery. There are two kinds of turn:

- **Human turn.** The human edits live in the browser — types values, drags, restyles. The app autosaves the
  snapshot to disk (debounced). The human ends the turn by handing back (a message, or just "your turn").
  When you take over, **re-read `workbook.snapshot.json`** — it is the truth, not your memory of the prior
  state.
- **Agent turn.** The agent edits the **files**, not the human's live browser: small surgical value/style
  fixes by editing `workbook.snapshot.json` directly; anything non-trivial (formulas, named ranges,
  validation, conditional formatting) through a **headless Node Facade** script (`univerAPI`/`FWorkbook`
  builders → `fWorkbook.save()`), which produces the correct plugin-resource shape. Declared charts/pivots go
  in `objects.json`. When the agent writes a file, the app **reloads the human's browser** to the new state.
  End the turn by narrating what changed and handing back.

**Use browser automation for verification, not as the primary write path.** The agent normally edits files or
the headless Facade while the browser remains the human's window. Agent-browser/Chrome may drive smoke tests,
capture screenshots, inspect console errors, and validate autosave/reload behaviour. Do not mix those QA
actions with a simultaneous human editing turn.

**Two mechanics keep turns safe** (both in `vite.config.js`; see [univer-surface](univer-surface.md)):

- **Reload-on-agent-edit.** The dev server watches the two files; when the agent writes one, it pushes a
  browser reload, so the human never keeps editing a stale in-memory workbook.
- **Version-guarded save.** Every save carries the version the browser loaded; a save that raced an agent
  edit is refused (HTTP 409) and the browser reloads instead of overwriting. Last-write-wins is safe because
  there is never a stale writer.

If you ever find yourself wanting *both* parties editing at once, that's a signal to slow down and take
turns — the safety rails assume it.

## Keep the docs and the snapshot together

Every iteration is checked against `MODEL.md`, `LAYOUT.md`, and `COMPONENTS.md`, per the
[separation doctrine](model-vs-layout.md):

- A change of **meaning** (new input, changed derivation, new named range) updates `MODEL.md` first — including
  its named-range registry — then the snapshot.
- A change of **appearance** (colour, format, merge, placement) updates `LAYOUT.md` first, then the snapshot.
- Realize named ranges as actual snapshot defined names as soon as they're placed, so the vocabulary is live
  in the workbook and will survive the compile.

If the snapshot drifts from the docs — a formula that no longer matches the model, a colour with no
convention — that's debt to reconcile, not to leave. The docs are the reason the workbook stays legible.

## Closure and changesets

In lane 1, closure means what the browser shows is what compiles and re-imports. In lane 2, closure means every
browser-authored operation is represented in the changeset, stays inside the approved component, merges into
a source copy, and passes assertions while preserve-only package parts remain intact.

**Charts and pivots are different: they are declared objects, not browser-drawn ones.** A chart or pivot is
recorded in `objects.json` (which fields, which ranges, which placement — from the model/layout decisions),
shown in the browser as a **preview** of that declaration, and materialized natively on compile. Never let a
chart or pivot exist in the browser that isn't in `objects.json` — that would be a thing the browser shows but
the exporter can't write, which is exactly the asymmetry closure forbids. The one honest caveat to state to
the human: a default (Tier A) pivot compiles to a faithful *static* table, not a draggable Excel pivot; if
they need interactivity, that's the LibreOffice pass ([converter](converter.md)). Macros are a hard limit —
name it, don't fake it.

## Exiting the loop

Leave phase 4 when the human agrees the component is right on the surface. Then compile (lane 1), merge (lane
2), or hand off to Excel (lane 3), and verify. If verification surfaces a gap, return to the correct source:
the snapshot in lane 1; the reviewed changeset/component in lane 2; the authoritative Excel workflow in lane
3. Never disguise a lossy full re-export as a merge.
