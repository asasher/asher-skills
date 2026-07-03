# Prototype

Target: a design question — stated directly (`triage prototype "<question>"`), extracted from an issue, or handed over by `reference/plan.md` when planning hits something paper cannot settle. A prototype is **throwaway code that answers a question**; the answer is the only deliverable.

The technique — the two prototype shapes and their rules — lives in `docs/agents/prototyping.md`; the app drivers for building and capturing live in `docs/agents/environment.md`. If either is missing, report a setup gap and stop.

## Gates

1. **Question stated** — one explicit design question, recorded at the prototype's location, and the shape picked per the playbook (logic vs UI). A prototype answering a vague or wrong question is pure waste — this gate is where that is caught.
2. **Built and handed over** — the prototype runs from one command (or one URL), surfaces its state, and the human has what they need to drive it. Extend it on request; prototypes evolve.
3. **Answer captured** — the decision and its why are written somewhere durable: into the consuming plan when called from planning (with variant screenshots per the playbook), otherwise into the record the playbook names. The prototype itself is never the record.
4. **Cleaned up** — the prototype is deleted, or its validated core (a pure logic module, a winning variant) is properly absorbed into real code. Nothing throwaway is left in the repo.
