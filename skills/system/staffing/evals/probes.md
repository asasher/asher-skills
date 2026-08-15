# Staffing — situated dry-run probes

Method: situated probes against the actual deployment targets — an in-session subagent on the Claude route and `codex exec --sandbox read-only` on the Codex route — with `SKILL.md` in context, plus the one `reference/` file named by the probe when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. **The answer key is written before any runs** and grades against the bars-then-cheapest redesign's settled decisions (plans/2026-08-14-backlog-family-refactor-review.html, the staffing lines): bars stated by the caller, cheapest survivor, hard taste bar, pins short-circuit, capability gaps never substituted, runtime-only checks with warn-and-fall-back, escalation without asking, template-fill setup.

All probes use the seed table's values (gpt-5.6-sol cost 4/int 9/taste 5; gpt-5.6-terra 6/5/3; sonnet-5 5/5/5; opus-5 3/7/7; fable-5 1/9/9; cost higher = cheaper).

## Probes

**P1 (cheapest survivor).** Read `reference/rankings-and-routing.md`. A backend refactor arrives with intelligence bar 7 and no taste bar; no pin matches and no capability is required. Using the seed table, which model gets the work? Walk each step and say where each losing model dropped out.

**P2 (hard taste bar).** Read `reference/rankings-and-routing.md`. A task needs user-facing onboarding copy and a public API surface designed — no browser or other capability. The roster's highest-intelligence cheap model sits at taste 5; two models clear taste ≥ 7. Which gets the work, at which step is the taste-5 model removed, and does its higher intelligence ever get to reconsider it?

**P3 (pin short-circuit).** "Who should do a large mechanical find-and-replace across the whole codebase?" Give the route and the exact basis. Is this a derivation from the rankings table or something else, and what still happens if the pinned route fails when tried?

**P4 (capability gap).** Read `reference/rankings-and-routing.md`. A task needs a real browser driven. The playbook declares no browser-use route (or the declared route and its fallback both fail when tried). May the resolver hand the task to the smartest model anyway, or swap in a different effect? What does it do?

**P5 (runtime fallback).** Read `reference/rankings-and-routing.md`. The cheapest survivor's route fails at dispatch with a usage-limit error. What are the resolver's next two actions, what record of the failure is kept and where, and what — if anything — is written into the playbook or any overlay? The same route has now failed in three separate sessions this week: what is that a signal for?

**P6 (escalation without asking).** A cheaper survivor returned work that misses the stated bar. Does the resolver ask the user before re-routing? What route takes the retry, and what does a task that keeps missing the bar indicate?

**P7 (no playbook).** You are asked to staff a subagent in a repo with **no** staffing playbook. The skill's bundled seed is right there in the installed package and contains a complete table. What do you do? Cite the rule, and state what "degrade" concretely means here.

**P8 (no survivor).** Read `reference/roles-and-fallback.md`. A ui change needs the taste bar cleared, but no model above it is reachable from this harness at all. Do you hand it to a below-bar model, stop, or something else? Cite.

**P9 (setup is a template fill).** Read `reference/setup.md`. Invoke `staffing setup` in a repo whose playbook already exists and carries owner-tuned judgment numbers. What does setup read, ask, and write; which values must survive untouched; and does any step probe a CLI, write an overlay, or stamp a machine name? What does a re-run that changes no answer leave behind?

**P10 (data vs doctrine).** You are writing a project's staffing playbook. For each of these, say whether it belongs in the playbook or in the skill, and where: the model rows; the bars-then-cheapest resolution rule; the mechanical/bulk pin; the `codex exec` command shape; the declared browser-use route; a table of which routes were verified reachable last Tuesday.

**P11 (invocation shape).** Read `reference/harness.md`. Your wrapper is ready to launch its bounded sibling-CLI worker. A reviewer suggests three simplifications: run the CLI from a background shell so the wrapper stays free, leave stdin attached, and drop the explicit timeout since the shell tool has a default. For each, accept or reject, name the concrete failure it risks, and cite the exact sentence that decides it.

**P12 (alias rejection at use).** Read `reference/harness.md`. A Codex parent passes the roster name `sonnet-5` to `claude -p --model` and the CLI rejects it. Is this a recorded state to look up or update anywhere? What does the dispatcher do, in order?

## Answer key

- **P1:** Survivors above intelligence 7: sol (9), opus (7), fable (9) — terra and sonnet drop at the bar step. Cheapest survivor by cost score: **sol (cost 4)** beats opus (3) and fable (1). PASS requires the bar filter before any cost comparison and no ranking of survivors by intelligence — picking fable "because it is smartest" is the exact defect this design replaces and = fail.
- **P2:** The taste bar (≥ 7, hard for user-facing work) removes the taste-5 model at the bar step, **before cost is consulted**; survivors opus (taste 7) and fable (taste 9); cheapest survivor = **opus (cost 3 > fable's 1)**. Intelligence never reconsiders it — a bar either holds or was stated wrong. Treating taste as a tie-break or soft default = fail.
- **P3:** The **mechanical/bulk task pin** selects its named worker route at step 1 and stops — a pin, not a table derivation. But a pin does not manufacture reachability: if the pinned route fails when tried, warn and continue from the bars like any route failure. Deriving the answer from the rankings table, or treating the pin as infallible, = fail.
- **P4:** **Neither.** A capability resolves only through a declared provider route; exhausting the route and its declared fallback is a **capability gap reported to the user — never substituted** with another effect or a smarter model. Cite § Declared capability routes. Substituting = fail.
- **P5:** Warn the user, then fall back to the **next-cheapest survivor above the same bars** and continue. **The warning is the record** — nothing is written to the playbook, and there is no overlay to write to. Three failures across sessions are **retro fodder** — a note for the retro pass, not a state machine's job. Any answer that records reachability state, retry-at tokens, or probe results = fail.
- **P6:** No ask: **"escalate to a more capable reachable route without asking when cheaper output misses the bar"** — the next-cheapest survivor above the bar takes the retry. Repeated misses mean the bar was stated too low: restate it and re-resolve. Asking permission first, or retrying the same model, = fail.
- **P7:** **Do not resolve from the seed** — its values are unreviewed defaults, and resolution reads the playbook alone. Degrade per `reference/roles-and-fallback.md`: run the delegated step on the current model in a subagent, **report the staffing gap**, and suggest `staffing setup`. Resolving from the seed or a home-directory path = fail; so does refusing to proceed at all.
- **P8:** Neither hand-off nor stop: run the ui work **on the current model in a subagent** and **report the staffing gap** — never quietly ship user-facing work through a below-bar model (the gap report is the honesty mechanism), and never skip the change. Cite § Fallback or the worked example.
- **P9:** Setup reads the existing playbook plus the bundled seed, runs the short repo-deltas interview, and writes the playbook (roster table, pins, declared capability routes, deltas) plus the instruction-file trigger. **Owner-tuned judgment numbers survive**; reconcile is clause by clause, never wholesale. **No probes, no overlay, no machine stamps** — any probing step = fail. A no-change re-run leaves the file **byte-identical**.
- **P10:** **Playbook (data):** model rows, the pin, the declared browser-use route. **Skill (doctrine):** the resolution rule (`rankings-and-routing.md`), the `codex exec` shape (`harness.md`). **The reachability table belongs nowhere** — recorded machine state is deleted; routes are tried at use. Placing the reachability table in the playbook or an overlay = fail.
- **P11:** **All three rejected.** Background launch: "backgrounded, the exec CLI hangs waiting to read stdin and dies silently with its dispatcher, leaving empty teed output while unrelated stderr noise masks the real cause." Attached stdin: same hazard — redirect from `/dev/null` or close outright. Default timeout: "the shell tool's default is shorter than a typical bounded worker's runtime; without the override even a healthy worker is killed mid-task." Accepting any, or citing the command block without the doctrine sentence, = fail.
- **P12:** **Not a recorded state** — no alias table exists. It is an ordinary route failure at the point of use: warn, retry with the bare form (`sonnet`), and if the route still fails fall back to the next-cheapest survivor. Looking up or writing an alias mapping = fail.

## Scoring

12 probes × 2 executors (one Claude route + one Codex route). A probe passes only with the **correct action AND a correct citation**. Ambiguity flags are recorded as findings, not failures — they are the most valuable output and should drive wording fixes before ship. Report a verdict table mapping each probe → pass/fail per executor.
