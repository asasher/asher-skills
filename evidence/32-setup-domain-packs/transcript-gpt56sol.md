# Probe transcript — Executor B (gpt-5.6-sol via codex exec)

- Date: 2026-07-11
- HEAD: aafe7e650406661c3ac630c95910f9cd26b630a9 (branch `32-setup-domain-packs`)
- Executor: gpt-5.6-sol via `codex exec -s read-only --skip-git-repo-check -m gpt-5.6-sol`, reasoning effort high, context-clean (same prompt as Executor A; codex read the three named files itself)
- Note: the leading `rmcp` transport-channel-closed lines in the raw session log are an unrelated MCP-worker warning at startup; the read-only file reads and the answer ran to completion. This is the executor's verbatim final message.

---

### P1

Before scaffolding, I ask:

> "what kind of work does this repo track?"

I offer exactly:

`software` / `writing` / `research` / `ops` / `general`

I propose `writing` as the default because the repository is a manuscript, then ask the user to confirm it.

Citation — setup.md:

> "Fresh install: **before scaffolding anything**, ask the user "what kind of work does this repo track?" with exactly five options: `software` / `writing` / `research` / `ops` / `general`."

Citation for the default and confirmation posture — setup.md:

> "Default the answer from repo evidence and confirm rather than interrogate, in the same posture as step 3's binding questions: a code repo (`package.json`, `src/`, a test runner) defaults to `software`; a manuscript defaults to `writing`; ambiguous evidence defaults to `software`."

### P2

Because no `templates/writing/` pack appears in the supplied template listing, I install these common templates:

- `templates/common/backlog-policy.md` → `docs/agents/backlog-policy.md`
- `templates/common/change-description.md` → `docs/agents/change-description.md`
- `templates/common/environment.md` → `docs/agents/environment.md`
- `templates/common/platform.md` → `docs/agents/platform.md`

I then install every software step baseline as a stand-in:

- `templates/software/change-fixer.md` → `docs/agents/change-fixer.md`
- `templates/software/change-reviewer.md` → `docs/agents/change-reviewer.md`
- `templates/software/diagnosing-bugs.md` → `docs/agents/diagnosing-bugs.md`
- `templates/software/evidence.md` → `docs/agents/evidence.md`
- `templates/software/implementing.md` → `docs/agents/implementing.md`
- `templates/software/refactoring.md` → `docs/agents/refactoring.md`
- `templates/software/verifying.md` → `docs/agents/verifying.md`

Citation for the normal scaffold set — setup.md:

> "Scaffolding and reconciliation draw from the **scaffold set**: `templates/common/` overlaid by `templates/<domain>/`; a pack file with the same name shadows the common file."

Citation for using the software pack when writing has no shipped pack — setup.md:

> "Missing-pack degrade: when the chosen domain has no shipped pack (today, every domain except `software`), install the `templates/software/` step baselines as stand-ins."

Each installed software stand-in gets a header line saying it is a code-flavored stand-in to tailor for `writing`, and I name the missing writing-pack gap in the setup report.

Citation — setup.md:

> "Add one flag line to each installed file's header naming it a code-flavored stand-in to tailor for `<domain>`, and name the gap in the setup report."

I do not omit any required playbook:

> "Never leave a required playbook uninstalled."

The selected domain is recorded in `docs/agents/backlog-policy.md` under `§ Work domain`.

Citation — setup.md:

> "Record the answer in the installed `backlog-policy.md` § Work domain."

### P3

I treat the repository as domain `software`, because the installed policy lacks `§ Work domain`.

Citation — setup.md:

> "If § Work domain is absent, use `software` and record it there during reconciliation."

The corresponding scaffold set is `templates/common/` overlaid by `templates/software/`, giving the same eleven templates listed in P2, except the seven software files are native domain templates rather than degraded stand-ins.

Citation — setup.md:

> "Scaffolding and reconciliation draw from the **scaffold set**: `templates/common/` overlaid by `templates/<domain>/`; a pack file with the same name shadows the common file."

I add `§ Work domain` to the installed `docs/agents/backlog-policy.md` and record:

```md
- Domain: software.
```

The deciding setup sentence is:

> "If § Work domain is absent, use `software` and record it there during reconciliation."

The policy template independently confirms the legacy default. Citation — backlog-policy.md:

> "Absent this section (an install from before domain packs existed), the domain is `software`."

I do not silently choose a different domain:

> "Changing an installed repo's domain is a user decision, never a silent reconciliation outcome."

### P4

`templates/writing/change-description.md` lands in `docs/agents/change-description.md`. It shadows `templates/common/change-description.md` because a same-name domain-pack file takes precedence.

Citation — setup.md:

> "Scaffolding and reconciliation draw from the **scaffold set**: `templates/common/` overlaid by `templates/<domain>/`; a pack file with the same name shadows the common file."

### P5

With recorded domain `writing` and no shipped writing pack in the supplied listing, `backlog run` requires counterparts for all four common templates plus the seven flagged software stand-ins:

- `docs/agents/backlog-policy.md`
- `docs/agents/change-description.md`
- `docs/agents/environment.md`
- `docs/agents/platform.md`
- `docs/agents/change-fixer.md`
- `docs/agents/change-reviewer.md`
- `docs/agents/diagnosing-bugs.md`
- `docs/agents/evidence.md`
- `docs/agents/implementing.md`
- `docs/agents/refactoring.md`
- `docs/agents/verifying.md`

Citation — run.md:

> "Completion criterion: every template in the skill's scaffold set — `templates/common/` plus the recorded work domain's pack (`docs/agents/backlog-policy.md` § Work domain; absent → `software`; for a domain whose pack is not yet shipped, the flagged `software` stand-ins setup installed are those counterparts) — has its `docs/agents/` counterpart, the parallelism verdict is known, and the staffing roster resolves in this harness — or the user has been told to run setup."
