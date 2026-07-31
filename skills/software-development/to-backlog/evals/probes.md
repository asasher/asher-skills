# To-Backlog — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **`SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are mid-way through a user interview about a reporting feature. Along the way the user mentioned: a crash when exporting to CSV (they pasted the error text), "it'd be nice if reports could be scheduled," and a reminder to ask design about the date-picker. The user now says "capture those." The repo's playbooks record GitHub as the tracker, the standard label roles, and native sub-issues as the parent/child relation.

## Probes

**P1 (sweep boundary).** The interview's own subject — the reporting feature being shaped — also isn't in the tracker yet. Does it go in the capture list? Cite.

**P2 (confirm gate).** The three items look obvious. Publish them? Cite.

**P3 (readiness).** The CSV crash is crystal clear — repro, error text, an obvious fix. Do you label it `ready-for-agent` so build can pick it up immediately? Cite.

**P4 (work-type).** What does each of the three items get typed as, and when is the type recorded? Cite.

**P5 (context fidelity).** What must the CSV-crash ticket's body carry, and may the pasted error text appear verbatim? Cite.

**P6 (parent).** The user says the scheduled-reports idea belongs under epic #7. How is that recorded, and what effect does it have on #7 if #7 is a capstone? Cite.

**P7 (scope creep).** While confirming, the user starts describing the scheduled-reports idea in detail — flows, edge cases, a rollout order. Keep growing the capture ticket? Cite.

**P8 (no binding).** Suppose `platform.md` recorded no tracker binding. What happens? Cite.

## Answer key

- **P1:** No — the sweep collects "every item that is real work but **not this conversation's deliverable**"; the interview's subject stays with the interview. Capturing the subject = **fail**.
- **P2:** No — "**nothing publishes before they approve**"; the compact list is presented first. Publishing unconfirmed = **fail**.
- **P3:** No — "**Apply no readiness role**: an un-routed ticket is the groom sweep's intake by design," and "Capture applying a readiness role would make it a second groom." Labelling it ready = **fail**.
- **P4:** Crash → `bug`; scheduled reports → `enhancement`; the design question is judgment — a capture-worthy follow-up (typed per the label roles) or flagged to the user — but the type is recorded **at capture**: "the type is a fact best known now, while the context is live." Deferring all typing to grooming = **fail**.
- **P5:** "the symptom and repro as reported for a bug"; yes on the error text — "a verbatim fragment the reporter themselves gave (an error message, a stack trace, a quoted behavior) is evidence, and evidence is context." Publishing a bare title = **fail**.
- **P6:** "attach each published ticket as a **child** of the given parent through the parent/child relation the platform playbook records"; effect: "attaching them re-blocks a capstone parent by itself." Wiring a blocking edge instead of the child relation = **fail**.
- **P7:** No — "a capture that needs those has outgrown capture and belongs to shaping or `to-slices`." The ticket stays minimal; the detail belongs to the shaping that will pick it up. Growing a spec inside a capture = **fail**.
- **P8:** "state the gap and ask the user before publishing anything." Inventing local ticket files = **fail**.

Pass bar: **8/8 on both executors.**
