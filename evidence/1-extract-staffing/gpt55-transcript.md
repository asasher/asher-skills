# gpt-5.5 executor (`codex exec -s read-only`) — full 14-probe transcript (HEAD 1f05997)

Executor: gpt-5.5 via `codex exec --skip-git-repo-check`, answer key withheld, skill files read from disk, citation required. Graded 14/14 PASS.

P1: Yes. `skills/staffing/SKILL.md` says `"A global-capable primitive"` and `user-invocable: true`. It also says `"Sibling skills — none"` and `"imports no other skill's files"`.

P2: The three dependency pointer kinds are bundled references, project playbooks, and sibling skills. `SKILL.md` lists `"Bundled references"`, `"Project playbooks"`, and `"Sibling skills — none. staffing is a root primitive."`

P3: Walk the succession line: the next most capable reachable model with sufficient UI taste takes it. `roles-and-fallback.md` says `"the next most capable reachable model with sufficient taste for ui work (taste ≥ 7...)"`; if none clears that, `"run the ui work on the current model in a subagent"`.

P4: Consult pins first, then the capability matrix, then rank surviving candidates. `rankings-and-routing.md` says `"Task-type pin?"`, then `"Capability gate"`, then `"Rank the survivors by intelligence > taste > cost"`. The browser requirement is decided by the capability matrix: `"filter to models the capability matrix marks browser-use: true"`.

P5: Use the pinned bulk model. `rankings-and-routing.md` says `"mechanical / bulk work ... → the pinned bulk model"` and `"A pin short-circuits the ranking"`. This is not a ranking derivation.

P6: No. `rankings-and-routing.md` says `"Capabilities are booleans keyed by model, in their own matrix, never columns in the rankings table"`. The failure mode is that you either let capability outrank intelligence on unrelated work or let intelligence pick a model that `"physically cannot do the job"`.

P7: Write rows only for models the fresh audit finds reachable, with a separate rankings table, capability matrix, task-pins, CLI mechanics only for present tools, and a floor. `machine-audit.md` says `"Seed only rows for models the audit found reachable"` and `"Cost/intelligence/taste can't be probed, so the audit seeds them from a documented default"`. No, you may not ship the four-model example as the roster: `"Never present the four-model rows as the canonical staffing roster"`.

P8: It is illustrative example output only, not the shipped roster. `machine-audit.md` labels it `"Example of audit output (illustrative only — NOT the shipped roster)"`.

P9: The override contains just the raised floor. `install-and-reconcile.md` says `"The override file contains just that one delta — the raised floor — and nothing else."` It also says a project override `"carries only deltas"` and `"never re-copies the base"`.

P10: Show the existing global rules and offer a project override. `install-and-reconcile.md` says `"Global staffing rules already exist → show them to the user and offer to add a project override"` and `"Do not silently overwrite the existing global base"`.

P11: Ask the user to choose global-with-overrides or project-only. `install-and-reconcile.md` says `"No staffing rules exist yet → ask the user which install shape they want"`. Before any global write, consent is required: `"Global writes are gated on consent"`.

P12: Reconcile by auditing installed text against the skill definition and reporting drift/conflict in prose. `install-and-reconcile.md` says `"audits the installed base + overrides against this skill's own definition"` and gives examples including `"lists a model the current harness can no longer reach"` and `"re-copies the base table"`. It does not use stamps: `"Staffing introduces no such stamp or marker"`.

P13: Yes, it is well-formed: `openai.yaml` has `interface.display_name`, `short_description`, `default_prompt`, and `policy.allow_implicit_invocation: false`. `docs/patterns/codex-compat.md` requires that shape and says `"Default allow_implicit_invocation to false for operator-style skills"`, which fits staffing because `SKILL.md` calls it `"a configuration/operator primitive"`.

P14: Consult task pins first, then gates; there is no capability requirement, but the taste gate applies because the task is user-facing. `rankings-and-routing.md` says user-facing work filters candidates to `"taste ≥ 7"` and that `"a model below taste 7 is out of contention ... no matter how high its intelligence."` The lower-intelligence taste-qualified model gets the work; the taste-5 model is removed at step 2, and ranking `"never resurrects a model a gate removed"`.
