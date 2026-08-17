# Bars, pins, and providers

Keep three structures separate: the roster table, declared capability routes, and explicit pins. Models supply judgment; installed harnesses, skills, plugins, and machine tools supply effects. Never infer a capability from a model name.

## Roster table

Roster rows are higher-is-better and contain exactly:

- **affordability** — how cheap this machine's owner runs the model (higher = cheaper, so the cheapest survivor is the highest affordability score);
- **intelligence** — unsupervised problem difficulty;
- **taste** — UI/UX, code/API quality, and copy judgment;

plus **effort** — see § Effort. No capability boolean belongs in this table.

## Bars

Judgment, design, and hard diagnosis mean a high intelligence bar; routine and mechanical work a modest one; a user-facing surface adds the taste bar. A caller that states neither bar nor the coordination class and surface that imply them gets the bars derived from the task description, said out loud so a wrong derivation is catchable.

The **taste bar is hard** for user-facing UI, copy, or API design: default taste ≥ 7 on the seed scale, and no amount of intelligence buys past it. A bar is a gate, not a preference — nothing below it survives, and nothing above it earns rank.

## Declared capability routes

A capability — `browser-use`, `computer-use`, `imagegen`, or another required effect — is supplied by a **declared provider route** in the playbook: the skill, plugin, harness, or tool that performs it, with any declared fallback route. Routes are tried at the point of use, not pre-verified: a route that fails when tried is warned about and its declared fallback tried next.

A missing provider is a **capability gap reported to the user — never substituted**: never swap in a different effect, and never pretend a model has the capability natively.

## Pins

A pin is an explicit routing decision resolved before everything else: a **task pin** binds a task type (e.g. mechanical/bulk work) to a named worker route; a **provider pin** binds a need to a named provider route. A matching pin short-circuits resolution — but the pinned route is still tried at use like any other, and on failure the warning fires and resolution continues from the bars.

## Escalation is the quality mechanism

Cost only ever chooses among models that already clear the task's bars. **Escalate to a more capable survivor without asking when cheaper output misses the bar.** The cheapest survivor is the opening bid, not a ceiling: output that misses the stated bar means the next-cheapest survivor above it takes the retry, and a task that keeps missing means the bar was stated too low — restate it and re-resolve. Reviews favor high taste and intelligence and may add an independent second model.

## Runtime fallback — try, warn, fall back

Checks are runtime-only — there is no recorded reachability to consult and none to write. The protocol is **try, warn, fall back**:

- **try** the selected route at the point of use;
- on failure, **warn the user** — the warning is the record;
- **fall back to the next-cheapest survivor above the same bars** and continue; a provider route falls back only to its declared fallback — exhausting those is a capability gap, not a model substitution.

A route that fails repeatedly across sessions is retro fodder — a note for the retrospective, never grounds for recorded state. If no survivor is reachable at all, run the work on the current model — in a subagent when the harness allows one, inline only when no subagent is possible — and report the staffing gap; never skip the stage, and never silently ship user-facing work through a model below the taste bar — the gap report makes the degradation visible.

## Effort

**Effort** is the model row's default dispatch level where the harness exposes one; dispatch at that value. One exception: pure wait/relay duty runs at **low** regardless of model. Effort never substitutes for a missed bar or a missing capability.
