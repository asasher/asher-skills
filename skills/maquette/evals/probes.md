# Maquette — situated dry-run probes

Method: situated probes against executor models (Opus subagent + `codex exec`), SKILL.md (and only the
reference named by the probe's phase, when stated) in context. Require the executor to cite the file and
exact sentence that decided each answer, and to flag ambiguity as a valid answer. Grade pass/fail against
the key. Answer key written before any runs.

## Probes

**P1.** User's first message: "Build me a prototype for a gym-management SaaS, here's a Loom of how gyms
work today. Get started, I'm busy." What is your next concrete action?

**P2.** During intake the user answers the look-and-feel question with "you pick, make it pretty." What do
you record in BRIEF.md for design language?

**P3.** You are in phase 5 (build). A screen needs a list of members. Where does the component get the
data, and what two things must be true about how that read behaves?

**P4.** You realize mid-build that member check-in needs a barcode-scanner integration you can't do in a
browser. What do you build, and what artifact(s) must record this?

**P5.** The user says "skip the interview, here's a complete PRD with journeys and brand tokens." Which
phases do you skip, and what must you still do before building?

**P6.** You've built 9 screens; a "Reports" nav item exists but reports were fenced out of scope in
BRIEF.md. The nav item currently links to `#`. What does the skill require?

**P7.** It's phase 4. The domain is freight brokerage; intake said "~200 loads/day, one big customer is
40% of volume." Name three concrete properties your fixture generators must have, citing the reference.

**P8.** The demo is tomorrow on the client's projector over their wifi. Name the two hardening checks most
specific to that situation and where the demo panel must NOT appear.

**P9.** The user asks: "can the client's engineer poke at it after the meeting via a link?" What mode does
that imply and what stops working in it?

**P10.** A fixture timestamp renders as "3 days ago" but the console shows a hydration mismatch warning.
Why did this happen and what is the prescribed fix?

**P11.** You've finished `BRIEF.md` and want the user to sign off. What is your next concrete action?

**P12.** You've drafted `JOURNEYS.md` after intake/research. What must happen before phase 4 data design
starts?

## Answer key

- **P1:** Do NOT start building or researching. Watch/ingest the provided Loom material first, then begin
  the intake interview — one question at a time — toward an approved BRIEF.md (intake.md: ingest before
  asking; SKILL.md gate: no work past an unapproved brief). Starting the interview by acknowledging what
  the Loom answered = pass. Building anything = fail.
- **P2:** Stock shadcn/ui defaults (neutral base, at most one restrained accent), recorded explicitly in
  BRIEF.md and confirmed with the user ("never assume a brand… say so and get a nod"). Inventing a custom
  design language = fail.
- **P3:** Through a `lib/api/*.ts` async function — never importing fixtures/store internals directly.
  Must have (a) simulated latency (~250–550ms) and (b) a rendered loading state (skeleton). Citing the
  seam non-negotiable or architecture.md = pass.
- **P4:** Build the UI flow with the scanner interaction faked (e.g. demo-panel-triggered or simulated
  input) behind the api seam, marked with `// @mock: <what real impl needs>`; it must appear in
  HANDOFF.md's mock inventory. Bonus: note it in DEMO.md if it's part of a beat. Dropping the flow
  silently or building a real integration = fail.
- **P5:** May skip the interview questions the PRD answers (potentially most of intake) and enter at the
  matching phase — but must still produce/confirm BRIEF.md and JOURNEYS.md equivalents and get the gates
  approved through review-loop approval events before building. Deal context and demo beats are rarely in a
  PRD — asking for those = pass signal.
- **P6:** No dead clicks: wire it or delete it. Since reports are fenced out, delete the nav item (a `#`
  link fails the dead-click sweep). Adding a "coming soon" page = fail (demo.md bans it).
- **P7:** Any three of: volumes matching intake magnitudes (lists that scroll, ~30–80+ rows); skewed
  distribution incl. the 40%-of-volume customer; cross-referenced entity graph; seeded PRNG determinism;
  relative dates; ragged realistic numbers; one deliberate edge case per entity. Must cite mock-data.md.
- **P8:** Zero-external-requests-after-load check (fonts/assets local — kill network and click through)
  and projector contrast/font-size check at 1366×768 / screen-share zoom. Demo panel must never be visible
  to (or discoverable by) the buyer — hidden behind the shortcut, and not left open.
- **P9:** Deployed share-link mode: static/Vercel deploy; store + localStorage work per visitor, but the
  agent bus / MCP live demo is absent (gated behind env), falling back to the Integrations screen story.
- **P10:** Relative-to-now dates differ between server render and client hydration. Fix per
  web-quality.md/mock-data.md: render timestamps after mount (hydration guard) or format
  deterministically.
- **P11:** Render `BRIEF.md` to self-contained HTML with stable ids and present it through the
  `review-loop` skill: serve, await, and branch on the verdict. Proceed only on an approving verdict;
  request_changes means revise the brief, ledger every annotation, and re-serve. Citing SKILL.md's phase-1
  gate and references/sign-off.md = pass. Reading it back in chat, inventing chat approval, or building a
  maquette review server = fail.
- **P12:** Present `JOURNEYS.md` for sign-off through the `review-loop` skill before data design: render to
  HTML with stable ids, serve, await, and branch on the verdict. Proceed only on an approving verdict;
  request_changes means revise, ledger every annotation, and re-serve. Citing SKILL.md's phase-3 gate and
  references/sign-off.md = pass. Treating the journey map as internally approved = fail.

## Scoring

12 probes × executors. A probe passes only with the correct action AND a correct citation. Ambiguity
flags count as findings, not failures — they are the most valuable output; feed them back into wording
fixes before shipping.
