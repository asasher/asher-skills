# Research — situated probes

Run each probe through both deployment executors with `SKILL.md`, `reference/research-contract.md`, and, when
named, the project playbook in context. Give P11 `reference/setup.md` as well because it exercises the setup
command. Require file-and-sentence citations and ambiguity flags. Grade against `answer-key.md`, written
before execution.

## Probes

**P1 — primary-source boundary.** A respected consultancy blog summarizes a vendor API, and the vendor's
versioned API reference is available. Which source supports the dossier's factual API claims, and what role
may the blog play?

**P2 — snippets and summaries.** Search results contain a snippet that appears to answer the question, but the
linked page has not been opened. May the snippet enter the claim ledger as support?

**P3 — fact versus inference.** Source code shows retries stop after three attempts. You conclude the service
will recover from any two transient failures. Record both statements with their correct classes and linkage.

**P4 — contradiction.** Two official documents give different limits. One was updated this month; the other
names an older API version. What must happen before synthesis, and what if the conflict remains?

**P5 — absence.** You searched official docs and source but found no statement that a feature is supported.
May the dossier state that the feature is unsupported?

**P6 — fan-out.** A research issue has four independent jurisdiction questions while backlog is already
running three issues in parallel. Describe the safe nested research shape, ownership, and capacity rule.

**P7 — no fan-out.** The question is one fact in one short specification. Should the skill dispatch several
researchers for confidence?

**P8 — artifact routing.** The user asks for an HTML explanation of an external Wayfinder skill “for review.”
This project playbook uses `research/<slug>/`; `evidence/` already contains screenshots and eval transcripts.
Where do the editable findings and rendered HTML go, and does “for review” change their type?

**P9 — backlog lifecycle.** A groomed issue has work-type `research`. Which skill owns source gathering and
audit, and which lifecycle actions must it return to backlog rather than performing?

**P10 — audit failure.** The draft dossier is polished, but one material inference has no supporting claim IDs
and one mutable web claim has no date. Can the skill return successfully?

**P11 — setup reconciliation.** The research playbook already routes dossiers to `notes/investigations/` and
records a private connector. On rerun, may setup replace it with the default `research/` tree?
