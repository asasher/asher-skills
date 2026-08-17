# To Subagent

Synchronous dispatch adapter for non-interactive work: one blocking call dispatches one subagent, and how many a piece of work needs is the caller's decision. `SKILL.md` carries the contract.

## When to use

- Any skill or session needs work done outside its own context — a lookup, a probe, a verification pass, an implementation — without the user attending it.
- It is the single sanctioned route to staffed dispatch: other skills say "via `to-subagent`".

## Provenance

No external sources.
