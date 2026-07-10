# Spreadsheet-loop — situated dry-run probes

Method: situated probes against executor models (an Opus subagent via the Agent tool + `codex exec --sandbox
read-only`), with SKILL.md (and only the reference named by the probe's phase, when stated) in context.
Require the executor to cite the file and exact sentence that decided each answer, and to flag ambiguity as a
valid answer. Grade pass/fail against the key. Answer key written before any runs.

## Probes

**P1.** User's first message: "Build me a Q3 revenue model, here's roughly the structure. I'm busy, go."
What is your next concrete action?

**P2.** During intake the user says the workbook should include a bar chart of revenue by product. Is that
supported, and how do you handle it?

**P3.** In the loop the user says: "make Tax Rate an input, put it at B2, and colour it blue." Which
document(s) change, in what order, and is there anything you should confirm first?

**P4.** It's the loop. You need to add a `SUM` formula to a range and give it a currency format. Do you
hand-edit `workbook.snapshot.json` or go through the Facade API — and why?

**P5.** The human edited cells directly in the browser and then left. You pick the task back up next turn.
Where is the current truth of the workbook, and what do you do first?

**P6.** You ran the compile. A grand total in `dist/workbook.xlsx` shows the wrong number. What do you do —
and what must you NOT do?

**P7.** You've finished `SPEC.md` and want the user to sign off. What is your next concrete action?

**P8.** User: "here's my existing `budget.xlsx` — bring it in and improve the layout." Where do you start,
and what still has to happen before you iterate?

**P9.** The user wants a pivot table of revenue by region that they can drag fields around in inside Excel. Is
that supported, and what do you tell them?

**P10.** Is the live Univer spreadsheet surface presented for sign-off through the `review-loop` skill, the
same way `SPEC.md` is? Explain.

**P11.** The compile succeeded and the file opens. What is the minimum you must run before telling the user
the `.xlsx` is faithful?

## Answer key

- **P1:** Do NOT open/edit Excel and do NOT start scaffolding. Begin the intake interview — one question at a
  time — toward an approved `SPEC.md`, acknowledging the structure the user already gave. Excel is a compile
  target, not the workshop (SKILL.md intro + phase-1 gate; intake.md "one question at a time"). Starting
  intake = pass. Building/opening Excel = fail.
- **P2:** Supported — the openpyxl converter creates **native** Excel charts. Handle it as a **declared
  object**: record it in `LAYOUT.md` (a chart is mostly a layout decision — type, placement) referencing the
  model's data range, add it to `objects.json`, and it previews in the browser and compiles natively
  (converter.md "Charts — native, free"; model-vs-layout.md "declared objects"). Treating a chart as
  out-of-scope / a hard limit = fail (that was the old exceljs design). Free-drawing it as an ad-hoc browser
  object instead of declaring it = partial (breaks the closure discipline).
- **P3:** It touches BOTH meaning (a new input + a named range → `MODEL.md` and its named-range registry) and
  appearance (placement B2 + blue convention → `LAYOUT.md`), then the snapshot. A change needing both
  documents is the signal to slow down and confirm with the human that it's a real change, not a tweak
  (model-vs-layout.md "The rule"). Citing that = pass. Editing only the snapshot, or only one doc, = fail.
- **P4:** Use the Facade API (`univerAPI`/`FWorkbook`) for anything non-trivial, then `fWorkbook.save()` and
  persist. Hand-editing `workbook.snapshot.json` is only for a small surgical value/style fix; prefer the
  Facade for anything touching plugin resources (the-loop.md "Two ways an edit happens"). Citing that = pass.
- **P5:** The snapshot is the single source of truth; the browser autosaved edits to
  `workbook.snapshot.json` via `/save`. Re-read that file first — not your in-context memory of the prior
  state (the-loop.md "The human edits directly"; univer-surface.md persistence). Re-reading the snapshot =
  pass. Assuming your remembered state = fail.
- **P6:** Do NOT hand-edit the `.xlsx` — the snapshot is the source of truth and the next compile overwrites
  it. Diagnose whether it's a converter bug (fix the mapper + add a test + recompile) or an out-of-scope
  feature; fix the snapshot through the loop or fix the converter, then recompile (verify.md "Reporting a
  gap"; converter.md "never hand-edit the .xlsx"). Patching the xlsx = fail.
- **P7:** Render `SPEC.md` to self-contained HTML with stable ids and present it through the `review-loop`
  skill: serve, await, branch on the verdict. Proceed only on approve; request_changes means revise, ledger
  every annotation, and re-serve (SKILL.md phase-1 gate; sign-off.md). Reading it back in chat or inventing
  approval = fail.
- **P8:** This is start-from-existing. Seed the snapshot with `npm run import -- budget.xlsx` and sanity-check
  it on the surface; intake becomes "what's wrong / what to change." You still owe the `SPEC.md` and
  `MODEL.md`+`LAYOUT.md` sign-off gates before iterating (intake.md "Greenfield or existing";
  univer-surface.md "Starting from an existing .xlsx"). Bonus: the import recovers cells/styles/formulas/
  conditional-formatting/named-ranges, and **detects and reports** any charts/pivots it can't reconstruct (so
  you re-declare them in `objects.json`) rather than silently dropping them (converter.md "Import"). Skipping
  the gates = fail.
- **P9:** Partly. A pivot is a **declared object**: the values are always faithful, but the *default* compiles
  to a static computed table (Tier A), **not** a draggable Excel pivot. A draggable/interactive pivot needs
  the LibreOffice materialization pass (Tier B) — available when `soffice` is present — or a template (Tier C)
  (converter.md "Pivots — the one hard object"). The right move: name the interactivity caveat at intake, ask
  whether they need drag-to-reconfigure or just the summary numbers, and declare it in `objects.json` (its
  fields are a `MODEL.md` decision). Saying "fully supported, draggable, free" with no caveat = fail; saying
  "not supported at all" = fail (the numbers always compile).
- **P10:** No. The live surface is a live interactive surface, driven directly on the presentation surface;
  only the paper artifacts (`SPEC.md`, `MODEL.md`, `LAYOUT.md`) go through `review-loop` sign-off gates
  (SKILL.md "How it composes"; the-loop.md "Serve it"). Treating the live surface as a gated review-loop
  artifact = fail.
- **P11:** At minimum verify layer 1 (headless recompute vs. the cached `v`) and layer 2 (read-back diff of
  the `.xlsx` against the snapshot); layer 3 (open in a real app) where the machine allows. Never claim
  "looks fine" without layers 1 and 2 (verify.md). Note the headless-Chrome screenshot caveat on this
  machine. Claiming faithful with no checks = fail.

## Scoring

11 probes × executors. A probe passes only with the correct action AND a correct citation. Ambiguity flags
count as findings, not failures — feed them back into wording fixes before shipping. Run before first real
use; re-run after any substantial rework (docs/patterns/probe-evals.md).
