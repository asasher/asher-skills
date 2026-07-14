# setup-asher-skills

The prompt-driven installer for [asher-skills](https://github.com/asasher/asher-skills). Wire the right skills
into a project without hand-wiring: it audits your repo, your machine's reachable models, and what the project
is for, then interviews you one plain-language decision at a time, installs a dependency-complete set of
Asher-authored skills from this repo, handles any declared external requirements behind a separate consent
gate, and writes the project's `## Agent skills` map. Re-invoke it to audit an existing install for drift.

It audits **three** surfaces, guarantees each skill's **sibling closure**, defaults every install to
**project-local** (global only for `staffing`, with consent), compiles declared provider variants only for
confirmed active harnesses, and reconciles policy by **LLM audit — no version stamps**.

## Use

```bash
npx skills add https://github.com/asasher/asher-skills --skill setup-asher-skills
```

Then invoke it:

- **`setup`** — set a project up: audit → interview → confirm → write.
- **`add <skill>`** — install one root with its dependency-first sibling closure and owner setup branches.
- **`audit`** — re-check an existing install against the repo's current catalog.

## What it does not do

Author or change any installed skill, auto-install an undeclared external request, write `docs/agents/`
playbooks itself (it runs each installed skill's own setup), or ship an `ask-asher` router (the `## Agent
skills` block is the map). A selected skill may declare an external skill or Codex plugin; setup verifies its
GitHub provenance, discloses version/scope/hooks, asks for explicit consent, uses its provider installer,
verifies the capability, and records it separately in `external-dependencies.lock.json`.

## Layout

- `reference/` — the contract plus generated `catalog.json` snapshot.
- `scripts/catalog.py` — validates source declarations, resolves closure, and materializes declared provider trees.
- `scripts/install.py` — inspects legacy mounts, atomically publishes variants, and audits provider provenance.
- `scripts/render-global.py` — coordinates the fresh four-module barrier, two-file Presentation preflight,
  setup-owned apply, final four-section verification, and barrier cleanup.
- `templates/` — seeds for the skill map, repo pointer, and setup-owned global presentation module/pointers.
- `evals/` — dual-executor probes + answer key.
- `agents/openai.yaml` — Codex presentation.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`setup-matt-pocock-skills`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/setup-matt-pocock-skills/SKILL.md).
- **Borrowed:** explore → decide one item at a time → confirm → write.
- **Local changes:** added three-surface audit, canonical dependency compilation, recursive owner setup, project-first scope, and drift reconciliation.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
