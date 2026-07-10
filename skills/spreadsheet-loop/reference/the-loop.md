# The loop — iterating on the browser surface

Phase 4 is the heart of the skill: the human and the agent edit the workbook **together** on the running
Univer surface, with the snapshot as the persisted state. This is what Excel can't offer — a fast, shared,
inspectable surface where changes are cheap and legible.

## Serve it

Start the scaffolded app (see [univer-surface](univer-surface.md)) and present it on the repo's presentation
surface (the tailnet root from `docs/agents/environment.md`), so the human can open it from wherever they
are. The live surface is **not** a `review-loop` artifact — it is a live interactive surface, driven
directly. Sign-off gates are for the paper artifacts (`SPEC.md`, `MODEL.md`, `LAYOUT.md`), not for the loop.

End any turn where you're handing back to the human with the surface URL, so they can pick up editing.

## Two ways an edit happens

- **The human edits directly** in the browser — types values, drags, restyles. The app persists the snapshot
  on change (autosave to `workbook.snapshot.json`). When you resume, re-read the snapshot; it is the truth.
- **The agent applies changes** through the **Facade API** (`univerAPI` / `FWorkbook`), not by hand-editing
  JSON, for anything non-trivial. Set values and formulas on ranges, apply styles, add named ranges, add
  data-validation and conditional-formatting rules via the builders — then `fWorkbook.save()` and persist.
  The Facade is also how you drive the headless Node instance in [verify](verify.md).

Hand-editing `workbook.snapshot.json` is fine for a small surgical fix to values or a style, but prefer the
Facade for anything touching plugin resources (named ranges, validation, conditional formatting) — the
builders produce the correct resource shape and keep `save()` authoritative.

## Keep the docs and the snapshot together

Every iteration is checked against `MODEL.md` and `LAYOUT.md`, per the
[separation doctrine](model-vs-layout.md):

- A change of **meaning** (new input, changed derivation, new named range) updates `MODEL.md` first — including
  its named-range registry — then the snapshot.
- A change of **appearance** (colour, format, merge, placement) updates `LAYOUT.md` first, then the snapshot.
- Realize named ranges as actual snapshot defined names as soon as they're placed, so the vocabulary is live
  in the workbook and will survive the compile.

If the snapshot drifts from the docs — a formula that no longer matches the model, a colour with no
convention — that's debt to reconcile, not to leave. The docs are the reason the workbook stays legible.

## Closure — declare special objects, don't free-draw them

The loop's promise is **closure: what the browser shows is what compiles, and what imports is what the browser
shows.** Cell-level edits (values, formulas, styles, conditional formatting, validation) round-trip
symmetrically through the converter — edit them freely.

**Charts and pivots are different: they are declared objects, not browser-drawn ones.** A chart or pivot is
recorded in `objects.json` (which fields, which ranges, which placement — from the model/layout decisions),
shown in the browser as a **preview** of that declaration, and materialized natively on compile. Never let a
chart or pivot exist in the browser that isn't in `objects.json` — that would be a thing the browser shows but
the exporter can't write, which is exactly the asymmetry closure forbids. The one honest caveat to state to
the human: a default (Tier A) pivot compiles to a faithful *static* table, not a draggable Excel pivot; if
they need interactivity, that's the LibreOffice pass ([converter](converter.md)). Macros are a hard limit —
name it, don't fake it.

## Exiting the loop

Leave phase 4 when the human agrees the workbook is right on the surface. Then compile ([converter](converter.md))
and verify ([verify](verify.md)). If verification surfaces a gap, come back into the loop to fix the snapshot —
never patch the `.xlsx` directly.
