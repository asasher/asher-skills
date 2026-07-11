# Probe transcript — Executor A (Claude / opus)

- Date: 2026-07-11
- HEAD: aafe7e650406661c3ac630c95910f9cd26b630a9 (branch `32-setup-domain-packs`)
- Executor: Claude Opus 4.8 via the Agent tool, context-clean (given only setup.md, common/backlog-policy.md, run.md + the templates listing; probes verbatim; no probes.md, plan, or key)

---

I've read all three files (setup.md, backlog-policy.md, run.md). Answering the five probes exactly as I would when running the skill, citing the deciding sentence for each.

---

**P1. Fresh manuscript repo — what to ask, what options, what default.**

Before scaffolding anything I ask the domain question. `setup.md` step 2, line 14:

> "Fresh install: **before scaffolding anything**, ask the user 'what kind of work does this repo track?' with exactly five options: `software` / `writing` / `research` / `ops` / `general`."

- **What I ask:** "what kind of work does this repo track?" — and I ask it *before* scaffolding any playbook (same sentence).
- **Options offered:** exactly the five — `software` / `writing` / `research` / `ops` / `general` (same sentence).
- **Default I propose for this repo:** `writing`, offered as a confirm-not-interrogate default. Same line 14:

> "Default the answer from repo evidence and confirm rather than interrogate… a manuscript defaults to `writing`."

The prose-chapters-under-`manuscript/`, no-`package.json`/`src`/test-runner evidence is exactly the "manuscript" case, so I propose `writing` and ask the user to confirm.

---

**P2. User confirms `writing` — which files, from where, what to flag, where recorded.**

`writing` has no shipped pack (the templates listing has only `common/` and `software/` dirs), so the missing-pack degrade fires. `setup.md` line 17:

> "Missing-pack degrade: when the chosen domain has no shipped pack (today, every domain except `software`), install the `templates/software/` step baselines as stand-ins."

Combined with the scaffold-set rule, line 16:

> "Scaffolding and reconciliation draw from the **scaffold set**: `templates/common/` overlaid by `templates/<domain>/`; a pack file with the same name shadows the common file."

So I install **all eleven files** into `docs/agents/`:
- From `templates/common/` (4): `backlog-policy.md`, `change-description.md`, `environment.md`, `platform.md`.
- From `templates/software/` as stand-ins (7): `change-fixer.md`, `change-reviewer.md`, `diagnosing-bugs.md`, `evidence.md`, `implementing.md`, `refactoring.md`, `verifying.md`.

(No name collides between `common/` and `software/`, so nothing is shadowed here — all 11 land.)

**What I flag/report beyond the install** — line 17:

> "Add one flag line to each installed file's header naming it a code-flavored stand-in to tailor for `<domain>`, and name the gap in the setup report."

So: a header flag line on each of the seven `software` stand-ins marking it a code-flavored stand-in to tailor for `writing`, plus naming the missing-`writing`-pack gap in the setup report. And "Never leave a required playbook uninstalled" (same line) is satisfied.

**Where the domain is recorded** — line 14:

> "Record the answer in the installed `backlog-policy.md` § Work domain."

---

**P3. Re-run, all eleven present, legacy install, no Work-domain section.**

**Which domain I reconcile against:** `software`. `setup.md` line 15:

> "Re-run: the recorded domain stands. If § Work domain is absent, use `software` and record it there during reconciliation."

Corroborated by line 8 ("if the section is absent, use `software` (a legacy install)") and `backlog-policy.md` line 9 ("Absent this section (an install from before domain packs existed), the domain is `software`.").

**Which template set that gives:** the `software` scaffold set — `templates/common/` overlaid by `templates/software/` (line 16).

**What I write into the installed `backlog-policy.md`:** I record the domain `software` in § Work domain — same line 15: "use `software` and record it there during reconciliation." (This is the one write; reconciliation otherwise never overwrites repo practice, and changing a domain is never a silent outcome — line 15.)

---

**P4. Future `templates/writing/change-description.md` vs `templates/common/change-description.md`, domain `writing`.**

The **`writing` pack's** `change-description.md` lands in `docs/agents/change-description.md`. Rule — `setup.md` line 16:

> "a pack file with the same name shadows the common file."

(Same rule restated at line 8: "with a same-name pack file shadowing the common file.") The domain pack shadows the common file of the same name, so the `writing/` version wins.

---

**P5. `run` step-1 preflight, recorded domain `writing` — which templates need counterparts.**

All eleven current counterparts: the 4 `common/` files plus the 7 `software` stand-ins. `run.md` step 1 completion criterion, line 11:

> "every template in the skill's scaffold set — `templates/common/` plus the recorded work domain's pack (`docs/agents/backlog-policy.md` § Work domain; absent → `software`; for a domain whose pack is not yet shipped, the flagged `software` stand-ins setup installed are those counterparts) — has its `docs/agents/` counterpart."

Because `writing`'s pack is not yet shipped, the clause "for a domain whose pack is not yet shipped, the flagged `software` stand-ins setup installed are those counterparts" makes the required set = `templates/common/` (4) + the installed `software` stand-ins (7) = **all eleven files** must have `docs/agents/` counterparts for the loop to proceed.

---

Self-summary (executor): All five backlog-setup probes answered with file+sentence citations — P1 asks the five-option domain question before scaffolding, defaulting `writing`; P2 installs all 11 files (4 common + 7 software stand-ins) with header stand-in flags, domain recorded in `backlog-policy.md` § Work domain; P3 reconciles as `software` and writes it to § Work domain; P4 the `writing` pack file shadows the common same-name file; P5 all 11 counterparts (common + software stand-ins) must exist for `run` to proceed. No genuine ambiguities found — every probe is decided by an explicit sentence.
