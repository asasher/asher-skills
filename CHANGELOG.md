# Changelog

Newest first. Each entry names the changed skills and what a reconcile must do.

## 2026-09-01 — writing standard split by register

The writing-for-humans standard split into three skills:

- `unslop` (new): the AI-tell scan for any user-facing writing.
- `writing-for-humans` (changed): now conversation only — replies, questions, plans discussed in chat. Requires `unslop`.
- `technical-writing` (new): specs, tickets, change requests, reports, and documentation. Requires `unslop`.

Sibling skills re-routed to the right register (changed: `research`, `prototype`, `to-spec`, `to-slices`, `build-change`, `prove-your-work`, `verify-your-work`, `shape`, `backlog`).

Reconcile: re-run `npx skills add github:asasher/asher-skills --skill unslop writing-for-humans technical-writing research prototype to-spec to-slices build-change prove-your-work verify-your-work shape backlog` (trimmed to your installed set, plus the two new writing skills). No setups to run.
