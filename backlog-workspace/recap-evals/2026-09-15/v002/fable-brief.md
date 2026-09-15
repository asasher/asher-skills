# Redesign the recap for a tired executive

Work in `/Users/asher/Projects/asher-skills`. You are the requested Fable UX consultant and designer. Read the project instruction file. Use the repo-authored `diagram-design` and `writing-for-humans` skills directly from `skills/`, with the diagram type and embedded-output references you select.

## The user's feedback

> Yeah this is still too verbose. Where are my diagrams? I want a timeline man. I want it to be nice and easy to read. I want some nice charts in it. I do like the color scheme, I will admit, but consult with Fable to improve the UX of this report

## Inputs

All paths below are relative to `backlog-workspace/recap-evals/2026-09-15/`:

- `v001/report.html`: the delivered report.
- `v001/rendering/desktop-collapsed.png` and `v001/rendering/mobile-collapsed.png`: its visible layout.
- `v001/sources/delivery-ledger.json`: the verified event records and counts.
- `v001/sources/`: supporting evidence for the report's claims.
- `v001/feedback.md`: human feedback.
- `v001/run.json` and `v001/completion.json`: provenance and verification context.

The repository history and facts are pinned to `10f388ac6b97fbd11360a88ce94e1d460dcfc304`. The reporting interval remains `[2026-09-08T00:02:04+04:00, 2026-09-15T00:02:04+04:00)`, Asia/Dubai. Use the saved evidence; this is a redesign of the same period.

## Deliverable

Create `v002/report.html`, a self-contained HTML report with a much shorter main view, a shipment timeline, and useful charts. Keep the dark color scheme. Make what shipped understandable by scanning the visuals and short labels. Move audit detail behind expandable sections. Preserve the source evidence, material limitations, and necessary upgrade action without letting them dominate the page.

Choose the chart types and hierarchy. Distinguish shipped outcome groups, merged PRs, direct commits, and documentation deployments. Chart event timestamps in the reporting timezone. Do not treat four editorial groups as seven features, or documentation deployment counts as customer adoption. Preserve any uncertainty in exact main publication times. Use the available evidence rather than inventing richer data to fill a chart.

Follow `diagram-design` in embedded mode, including accessible SVG and the selected type references. Keep the report readable at desktop and phone widths, without required external assets or JavaScript. Relative audit links can point into `../v001/sources/`. Preserve v001 unchanged.

Also write `v002/design-notes.md`: concise UX findings, the choices you made, and any narrow changes you recommend to the recap skill based on the observed failure. Distinguish report design decisions from proposed skill instructions. Report your actual model and any incomplete checks.

## Boundaries and completion

Write only under `v002/`. Do not edit skill sources, v001, tracker state, or Git history. Do not publish or launch other agents. The parent owns final verification and archival. If a required tool is unavailable, report it without substituting another model.

Completion means the report contains the requested timeline and charts, explains the same verified history with less reading, and the design notes are ready for the parent's review. The dispatch supplies an absolute deadline and confirms the authorized execution route before launch.
