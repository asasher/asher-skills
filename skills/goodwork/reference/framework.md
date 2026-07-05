# The Good Work Framework

The synthesis underneath every goodwork command. Read this before running any command for the first time in a session.

## What "good work" means here

Good work is work that is good in three senses at once, per person, per season of life:

1. **Feels good** — engaging, energizing, produces flow (Csikszentmihalyi; Self-Determination Theory: autonomy, competence, relatedness).
2. **Is good** — meets a craft standard the person cares about; uses and grows their strongest skills (Newport's career capital; shokunin craft orientation).
3. **Does good** — serves someone or something the person endorses, within ethical lines they won't cross (Gardner/Csikszentmihalyi/Damon's three Es: excellence, engagement, ethics).

The person's own weighting of these three is part of the profile, not an assumption. Some people want a calling; some want a well-paid job that funds a life. Both are good work. Never moralize the answer.

## Advising priors

Two research findings that shape advice everywhere and live nowhere else:

- **Interest match alone predicts satisfaction weakly.** The stronger predictors are work design (autonomy, variety, feedback, task significance), relationships, strength use, needs-supplies values fit, and visible progress on meaningful work (80,000 Hours evidence review; work-design meta-analyses; Amabile). Profile and weigh all of these, not just interests.
- **Don't follow passion; follow evidence forward.** Passion usually develops from getting good at valuable work with autonomy and feedback (Newport; O'Keefe/Dweck/Walton). Treat persistent curiosity — what keeps tugging at your attention (ki ni naru) — as a weak signal to test, not a verdict.

## The Good Work Profile (canonical schema)

Every command reads and writes `goodwork/PROFILE.md`. Sections, with source frameworks:

1. **Snapshot** — one-paragraph statement of what good work is for this person, in their own words, plus current status (employed/searching/redesigning) and review date.
2. **Energy map** — energizers, drainers, anti-spark (competent but depleting), flow conditions (challenge level, feedback loop, interruption tolerance). *(Good Time Journal, Sparketype, flow theory)*
3. **Activities & interests** — preferred work activities in RIASEC vocabulary (building/fixing, investigating, creating, helping, persuading/leading, organizing), persistent curiosities that keep tugging. *(Holland/O*NET, ki ni naru)*
4. **Strengths & proof** — what they learn faster than peers, what people repeatedly ask them for, recent episodes of unusually strong performance, overuse risks. Each strength needs at least one concrete episode. *(CliftonStrengths/VIA method, strengths interviewing)*
5. **Anchors & values** — the one or two things they will not give up (Schein anchors), top five values force-ranked, resolved tradeoffs (autonomy vs. security, pay vs. mission, novelty vs. predictability), dealbreakers. Evidence: what they actually chose when values conflicted. *(Schein, Schwartz, values card sort)*
6. **Motivation conditions** — which autonomy matters (goals, methods, schedule, tools, collaborators), what feedback makes them feel effective, what relatedness they need, what progress signals count as a win, what makes a day feel wasted. *(SDT, Pink, Amabile)*
7. **Meaning & service** — who or what the work serves, calling status (searching / perceiving / living), the ethical lines they won't cross, what should stay unmonetized. *(Good Work 3 Es, Dik & Duffy calling research, ikigai)*
8. **Craft** — the craft they'd still refine after ten years, standards they hold when nobody is watching, mastery vs. novelty orientation. *(shokunin, Newport)*
9. **Market position** — career capital (rare-and-valuable skills, connections, credentials, reputation, runway), the hard-to-copy intersection, candidate-market fit hypotheses to test. *(Newport, 80,000 Hours, Perell, Never Search Alone)*
10. **Constraints & risk budget** — gravity constraints (accept/design around) vs. actionable ones, financial runway, visa/location/caregiving/health facts, decent-work floor (minimum pay, benefits, conditions). *(DYL gravity problems, Duffy work volition, small-bets risk budget)*
11. **Whole-life dashboard** — work/play/love/health gauges and what work must not cost. *(DYL dashboard, Adler's life tasks)*
12. **Work orientation & weighting** — job / career / calling orientation, and how they weight feels-good / is-good / does-good. *(Wrzesniewski)*

Confidence marks: label each section **reported** (they said it), **evidenced** (backed by a story or observed choice), or **tested** (confirmed by a prototype or market feedback). The point of prototypes and the campaign is to move items rightward.

## The arc

Define → Test → Position → Campaign → Sustain.

- **Define**: `interview` produces the profile; `odysseys` turns it into three alternative futures.
- **Test**: `prototype` converts futures into cheap experiments; `craft` redesigns the current job when leaving isn't wanted or possible yet.
- **Position**: `niche` fixes candidate-market fit and communities; `assets` builds CV, LinkedIn, and proof of work.
- **Campaign**: `targets` → `outreach` → `apply`, tracked in `pipeline`.
- **Sustain**: `daily` runs the action queue and journal; `review` closes the weekly loop and updates the profile.

People enter anywhere. Someone mid-search can start at `targets` and backfill the profile; someone burnt out starts at `interview` or `craft`.

## Workspace

Goodwork v2 is one project folder per person. The `goodwork/` folder holds two tiers of state:

- Operational JSON/JSONL consumed by matchers, schedulers, approvals, and UI projections.
- Narrative Markdown consumed by the person, interview, and weekly reflection.

The state model, file inventory, schemas, ID rules, agent-sole-writer rule, and evidence inbox live in [state.md](state.md). Create files on first use. Update cumulatively; don't regenerate. Treat contents as sensitive personal data: never share or publish them without explicit instruction.

The full source list behind this synthesis lives in the skill's `README.md`.
