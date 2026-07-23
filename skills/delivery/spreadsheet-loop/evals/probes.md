# Spreadsheet-loop — situated dry-run probes

Method: situated probes against executor models (a Claude subagent via the Agent tool + `codex exec --sandbox
read-only`), with SKILL.md (and only the reference named by the probe's phase, when stated) in context.
Require the executor to cite the file and exact sentence that decided each answer, and to flag ambiguity as a
valid answer. Grade pass/fail against the key in `answer-key.md` — kept in that separate file, out of executor
context, and written before any runs. Executors must not read `evals/`.

## Probes

**P1.** User's first message: "Build me a Q3 revenue model, here's roughly the structure. I'm busy, go."
What is your next concrete action?

**P2.** During intake the user says the workbook should include a bar chart of revenue by product. Is that
supported, and how do you handle it?

**P3.** In the loop the user says: "make Tax Rate an input, put it at B2, and colour it blue." Which
document(s) change, in what order, and is there anything you should confirm first?

**P4.** It's the loop. You need to add a `SUM` formula to a range and give it a currency format. Do you
hand-edit `workbook.snapshot.json` or go through the Facade API — and why?

**P5.** In a lane-1 browser-native build, the human edited cells directly in the browser and then left. You
pick the task back up next turn. Where is the current truth of the workbook, and what do you do first?

**P6.** You ran a lane-1 compile. A grand total in `dist/workbook.xlsx` shows the wrong number. What do you do
— and what must you NOT do?

**P7.** You've finished `SPEC.md` and want the user to sign off. What is your next concrete action?

**P8.** User: "here's my existing `budget.xlsm` — bring it in and improve the layout." Where do you start,
and what still has to happen before you iterate?

**P9.** The user wants a pivot table of revenue by region that they can drag fields around in inside Excel. Is
that supported, and what do you tell them?

**P10.** Is the live Univer spreadsheet surface presented for sign-off through the `serve-via-tailnet` skill, the
same way `SPEC.md` is? Explain.

**P11.** The compile succeeded and the file opens. What is the minimum you must run before telling the user
the `.xlsx` is faithful?

**P12.** Preflight finds 77 sheets, VBA, 17 native charts, external links, and images. The user only wants the
Revenue assumptions block changed. What lane and scope do you propose?

**P13.** A lane-2 browser iteration is approved and complete. What is the integration deliverable, and what
must the merge verify before you call it done?

**P14.** The only available writer would fully re-save the source and may drop unknown OOXML extensions. What
do you do?

## Scoring

14 probes × executors. A probe passes only with the correct action AND a correct citation. Ambiguity flags
count as findings, not failures — feed them back into wording fixes before shipping. Run before first real
use; re-run after any substantial rework. (The method above is self-contained; in the asher-skills repo the
governing discipline is the `docs/agents/probe-evals.md` playbook.) Graded runs are recorded in `runs/`.
