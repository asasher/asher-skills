# setup-asher-skills

The prompt-driven installer for [asher-skills](https://github.com/asasher/asher-skills). Wire the right skills
into a project without hand-wiring: it audits your repo, your machine's reachable models, and what the project
is for, then interviews you one plain-language decision at a time, installs a dependency-complete set **from
this repo only**, and writes the project's `## Agent skills` map. Re-invoke it to audit an existing install for
drift.

Modeled on `setup-matt-pocock-skills` (explore → decide one at a time → confirm → write), adapted as ours: it
audits **three** surfaces, guarantees each skill's **sibling closure**, defaults every install to
**project-local** (global only for `staffing`, with consent), and reconciles by **LLM audit — no version
stamps**.

## Use

```bash
npx skills add https://github.com/asasher/asher-skills --skill setup-asher-skills
```

Then invoke it:

- **`setup`** — set a project up: audit → interview → confirm → write.
- **`audit`** — re-check an existing install against the repo's current catalog.

## What it does not do

Author or change any installed skill, install anything from outside this repo, write `docs/agents/` playbooks
itself (it runs each installed skill's own setup), or ship an `ask-asher` router (the `## Agent skills` block
is the map).

## Layout

- `reference/` — the contract: `interview.md` (audit→decide→confirm→write), `catalog.md` (what fits, the
  closure rules, the this-repo-only invariant), `audit-mode.md` (stampless reconciliation).
- `templates/` — seeds for the `## Agent skills` block and the repo pointer.
- `evals/` — dual-executor probes + answer key.
- `agents/openai.yaml` — Codex presentation.
