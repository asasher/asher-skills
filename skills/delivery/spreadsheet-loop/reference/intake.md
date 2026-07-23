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
3. **Greenfield or existing.** Starting from scratch, or from an existing `.xlsx`/`.xlsm`? If existing, get
   the path and identify the authoritative file. Run capability preflight before promising that an import can
   replace it; see [lanes-and-merge](lanes-and-merge.md).
4. **Scale, shape, and components.** Roughly how many sheets, how big, and do sheets reference each other?
   Propose coherent components (Inputs, Revenue, Staffing, Reporting) rather than treating a large workbook
   as one grid. Ask which component the user actually needs changed.
5. **The numbers that matter.** The core inputs a human will change, and the key derivations
   (`Revenue = Units × UnitPrice`, running totals, growth rates). You are eliciting the *data model* in
   embryo — enough to write `MODEL.md` next.
6. **The look.** Any brand colours, an existing template to match, or house conventions (how inputs vs.
   outputs are signalled). Enough to write `LAYOUT.md`.
7. **Capability and lane.** For an existing workbook, inventory VBA, external links/connections, charts,
   pivots, drawings/images, names, extensions, and formula errors. Classify them as browser-safe, declared,
   preserve-only, or Excel-native. Propose lane 1 (browser-native), lane 2 (scoped browser + merge), or lane 3
   (Excel-native), with an explicit fallback. Never quietly promise that a full re-export preserves an
   authoritative workbook.

## Writing `SPEC.md`

Synthesize — don't transcribe the Q&A. `SPEC.md` is direction, not detail:

- **Purpose** — the workbook and the job it does, in a sentence or two.
- **Audience & use** — who opens it and how they interact.
- **Authority & lane** — greenfield/browser-native, scoped merge into an authoritative source, or Excel-native.
- **Capability table** — feature, location/count, classification, consequence, and owner.
- **Scope** — the sheets and the rough structure; what's explicitly *out* (including any fenced feature the
  user agreed to drop or hand-finish).
- **Components** — proposed work units, dependencies, and which are in this task.
- **Integration** — compile, preservation-safe merge, or Excel handoff; include the source hash for lane 2.
- **The model, in brief** — the core inputs and the headline derivations. The full data model comes in
  phase 2; here, just the shape.
- **The look, in brief** — brand or template to match, and the input/output signalling convention.
- **Open questions** — anything undecided, recorded rather than guessed.

Keep it in the project root. **Gate:** present `SPEC.md` for sign-off through `serve-via-tailnet`
(see [sign-off](sign-off.md)); proceed to model & layout only on an approving verdict.
