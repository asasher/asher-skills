# Intake

A short interview to reach shared understanding before anything is built. **One question at a time** — read
the answer, then ask the next. Do not dump a questionnaire. The output is `SPEC.md`, the coarse direction the
model and layout are cut from.

## What to establish

Work through these, adapting to what the user volunteers (skip what they've already answered):

1. **The workbook and its job.** What is this — a financial model, pricing sheet, budget, dashboard, tracker?
   What decision or task does it serve?
2. **Who consumes it.** Who opens the final `.xlsx`, and what do they do in it — read it, type inputs into it,
   forward it? This drives how much the layout must guide a stranger.
3. **Greenfield or existing.** Starting from scratch, or from an existing `.xlsx`? If existing, get the path —
   phase 3 imports it to seed the snapshot, and intake becomes "what's wrong with it / what should change."
4. **Scale and shape.** Roughly how many sheets, how big, and do sheets reference each other? Cross-sheet
   references and multi-scenario structure are the difference between a simple and a complex build.
5. **The numbers that matter.** The core inputs a human will change, and the key derivations
   (`Revenue = Units × UnitPrice`, running totals, growth rates). You are eliciting the *data model* in
   embryo — enough to write `MODEL.md` next.
6. **The look.** Any brand colours, an existing template to match, or house conventions (how inputs vs.
   outputs are signalled). Enough to write `LAYOUT.md`.
7. **Fence check.** Almost everything compiles (charts, conditional formatting, validation, images — all
   supported by the openpyxl converter). Two things need a decision, per [converter](converter.md):
   **Pivot tables** — ask whether the deliverable needs an *interactive, draggable* pivot or just the summary
   numbers. Interactive needs the LibreOffice materialization pass (Tier B) or a template (Tier C); summary
   numbers get the default flattened table (Tier A). **Macros** are a genuine hard limit — the options are
   "drop it," "hand-finish in Excel," or "not the right tool." Surface either now if it's load-bearing; never
   quietly promise something the compile can't deliver.

## Writing `SPEC.md`

Synthesize — don't transcribe the Q&A. `SPEC.md` is direction, not detail:

- **Purpose** — the workbook and the job it does, in a sentence or two.
- **Audience & use** — who opens it and how they interact.
- **Source** — greenfield, or the existing `.xlsx` being brought onto the surface.
- **Scope** — the sheets and the rough structure; what's explicitly *out* (including any fenced feature the
  user agreed to drop or hand-finish).
- **The model, in brief** — the core inputs and the headline derivations. The full data model comes in
  phase 2; here, just the shape.
- **The look, in brief** — brand or template to match, and the input/output signalling convention.
- **Open questions** — anything undecided, recorded rather than guessed.

Keep it in the project root. **Gate:** present `SPEC.md` for sign-off through `review-loop`
(see [sign-off](sign-off.md)); proceed to model & layout only on an approving verdict.
