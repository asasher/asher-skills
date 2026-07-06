# Intake interview

The intake is an interview, not a form. It does the heavy lifting for the entire pipeline: a weak intake
produces a pretty prototype of the wrong product. You are grilling for shared understanding — keep going
until you could pitch the product back to the user and they would say "yes, exactly that."

## Conduct

- **One question at a time.** Never dump a questionnaire. Each question builds on the previous answer.
- **Ingest before asking.** If the user provides process maps, SOPs, decks, screenshots, or an existing
  brief, read them first and skip every question they already answer. Say what you learned from them.
  If provided material can't be consumed in your environment (a video, a walkthrough call, a proprietary
  format), say so and ask for a transcript or export — or cover its content through interview questions.
  Never silently skip provided material.
- **Grill vague answers.** "It's like a CRM for freight" is not an answer — ask what a dispatcher does at
  8am. Prefer questions about concrete moments over questions about abstractions.
- **Offer options to react to.** When the user is stuck, propose two or three concrete alternatives
  ("does an order move through stages like A→B→C, or is it a flat queue?"). People correct better than
  they generate.
- **Play back after each domain.** Summarize what you understood in two or three sentences and let the
  user correct it before moving on.
- **Adaptive depth.** A user who has thought about this for a year needs six questions; a napkin idea
  needs twenty. Judge by the crispness of the answers, not a fixed count.

## Domains to cover

Track these as a checklist; order them by whatever the conversation makes natural.

1. **The deal.** Who is buying? Who is physically in the demo room, and what are their roles? What
   triggers the purchase — what pain, what deadline, what incumbent is being displaced? What are the
   ~3 moments that would make them lean forward? (These become the demo beats and get the fidelity budget.)
2. **The product.** One sentence: what job does it do for whom? What business process does it map — walk
   through the process end to end, with the user naming each actor and artifact.
3. **Personas.** Who uses it day to day? Which roles/permissions are worth *showing* (a persona switcher
   is cheap; real auth is out of scope)?
4. **Journeys and scope fence.** The core journeys, ranked. Then the fence: what are we explicitly NOT
   building? Get the user to say it out loud — unbounded scope is the failure mode of prototype projects.
5. **Look and feel.** Existing brand guidelines, logos, tokens? Reference products ("should feel like
   Linear / like SAP but nicer")? Screenshots they admire? Light or dark default? Data-dense or airy?
   **Never assume a brand.** If nothing is given, the answer is stock shadcn/ui defaults — say so and get
   a nod. Whatever is decided here is recorded in the brief and becomes law for the build.
6. **Data realism inputs.** Real-world example entities (anonymized is fine), the domain's vocabulary,
   realistic magnitudes (how many orders a day? typical price range?), sample documents. This feeds the
   fixture generators — the more real input, the more sellable the demo.
7. **Agent surface.** What should a connected coding agent be able to do to this product over MCP? Which
   one agent action would impress this specific room? (See architecture reference: the maquette ships a
   small real MCP server against the mock store.)
8. **Research mandate.** What should be researched autonomously before design — domain workflows,
   competitors, terminology — and how deep? Agree on it explicitly so research doesn't stall or sprawl.
9. **Logistics.** When is the demo? Presented from whose laptop? Projector or screen-share? Will the
   client get a link to click afterward (affects deployment mode — see architecture)?

## Exit gate

Write `BRIEF.md` covering every domain above, in the user's vocabulary, including the scope fence and the
demo beats. Read it back. The intake ends only when the user approves the brief — corrections loop back
into questions. Do not start research or design on an unapproved brief.

`BRIEF.md` skeleton: Product (one-liner, process map) · The deal (buyers, room, trigger, demo beats) ·
Personas · Journeys (ranked) + scope fence · Look and feel (tokens or "stock shadcn") · Data realism notes ·
Agent surface · Research mandate · Demo logistics.
