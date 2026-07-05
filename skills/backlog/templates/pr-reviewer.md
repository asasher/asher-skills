# Playbook: PR Reviewer Criteria

> Project playbook for this repo. The triage `adversarial-review` Reviewer subagent reads this file for what to scrutinize, how to comment, and the approval bar; the loop mechanics are in the skill's `reference/adversarial-review.md`. The quality bar below is the shipped default (adapted from Cursor's thermo-nuclear code-quality review; smell baseline from Matt Pocock's `code-review` skill, MIT) — tune it to what matters in this codebase.

## Correctness first

Read the diff for bugs before anything else: logic errors, unhandled edge cases and error paths, races, off-by-ones, broken invariants, security-sensitive changes. Verification checked behavior against the acceptance criteria; this review is the pass that reads the code itself.

## Be ambitious about structure

Do not stop at "this could be a bit cleaner." For every meaningful change, ask whether a reframing would make it dramatically simpler — whole branches, helpers, modes, or layers disappearing rather than being rearranged. Prefer the solution that feels inevitable in hindsight; when complexity can be deleted instead of moved, push hard for that path.

Treat these as presumptive blockers the author must justify:

- The PR preserves incidental complexity when a visibly simpler reframing exists.
- A file grows past ~1000 lines because of this PR — ask for decomposition first; waive only for a compelling structural reason with the file still clearly organized.
- Ad-hoc conditionals, one-off flags, or scattered special cases bolted into unrelated flows — "weird if statements in random places" are a design problem, not a stylistic nit; the logic wants a dedicated abstraction, policy object, or module.
- Feature logic leaking into shared paths, or a bespoke helper duplicating a canonical one — push code to the layer that already owns the concept.
- Thin wrappers, identity abstractions, magic genericity, or cast/`any`/optionality churn that obscures the real contract — prefer direct, boring code with explicit type boundaries.
- Avoidably sequential orchestration or non-atomic updates where the cleaner structure is obvious — without over-indexing on micro-optimizations.

Preferred remedies point the same direction: delete a layer of indirection rather than polishing it; reframe the state model so conditionals disappear; extract the helper or split the file; move logic behind the abstraction that owns it; reuse the canonical utility.

## Smell baseline

Match the diff against this fixed baseline of code smells (Fowler, *Refactoring* ch. 3). Three rules bind it: a documented repo standard **overrides** the baseline — where the repo endorses something a smell would flag, suppress the smell; every smell is a labelled judgement call ("possible Feature Envy"), never a hard violation; and skip anything tooling already enforces.

- **Mysterious Name** — a name that doesn't reveal what it does or holds → rename it; if no honest name comes, the design is murky.
- **Duplicated Code** — the same logic shape in more than one hunk or file → extract the shared shape, call it from both.
- **Feature Envy** — a method reaching into another object's data more than its own → move it onto the data it envies.
- **Data Clumps** — the same few fields or params travelling together (a type wanting to be born) → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurring across the change → polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forcing scattered edits across many files → gather what changes together into one module.
- **Divergent Change** — one module edited for several unrelated reasons → split so each changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks for needs the spec doesn't have → delete it; inline until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward → cut it, call the real target directly.
- **Refused Bequest** — a subclass or implementer ignoring most of what it inherits → drop the inheritance, use composition.

## Also scrutinize

- Testability and test coverage of the change, held to `implementing.md` § Tests worth keeping.
- Duplication and naming; legibility of the surrounding code after the change.
- Behavior risk beyond the issue's scope.
- Repo-specific concerns (performance budgets, security surfaces, accessibility, API compatibility): _<add yours>_.

## How to comment

- Prioritize: correctness, then structural regressions and missed simplifications, then boundary/type-contract problems, then file size, then legibility. A few high-conviction comments beat a long list of nits — do not flood the review with cosmetic notes when a structural issue dominates.
- Leave only actionable comments: each names the expected improvement and why it matters. Be direct and demanding about quality without being rude; do not soften major maintainability issues into mild suggestions.
- Review only the diff since the last seen SHA on re-review.

## Approval bar

Do not approve merely because behavior seems correct. Approve when there is no correctness concern, no clear structural regression, no obvious missed simplification, no unjustified file-size explosion, no spaghetti growth from special-case branching, and no boundary leak or avoidable canonical-helper duplication. When no actionable improvement remains, comment exactly `LGTM`.
