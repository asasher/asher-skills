# Bare-minimum-ux — situated dry-run probes

Per `docs/agents/probe-evals.md`; surface: `SKILL.md` only. Key written before any runs.

**P1 (precedence).** The project has Impeccable installed and its DESIGN.md suggests a pattern that puts an
add-row button at the top of a table, with rows appended at the bottom. What wins, and why? Cite.

**P2 (external, not copied).** You're asked to "just inline the useful impeccable rules into this file so we
don't depend on it." Correct response? Cite.

### Answer key

- **P1:** The overlay wins — rule 3 (co-locate actions and consequences) conflicts, and "on any conflict,
  these five rules win — this file is Asher's personal policy overlay on top of whatever design system runs
  underneath." Either move the button or append rows where the action is. Following DESIGN.md over the
  overlay = **fail**.
- **P2:** Refuse: "Its rules are never copied here — a fork goes stale." Impeccable stays the declared,
  consent-gated external loaded per its own SKILL. Inlining = **fail**.

Pass bar: 2/2 on both executors.
