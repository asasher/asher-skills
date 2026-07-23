# The structural bar

The second baseline the Standards axis always carries, beside the [smells](smells.md): review the
diff's structure with ambition, not local tidiness. For every meaningful change, ask whether a
reframing would make it dramatically simpler — whole branches, helpers, modes, or layers disappearing
rather than being rearranged. Prefer the solution that feels inevitable in hindsight; when complexity
can be deleted instead of moved, push for that path.

## Presumptive blockers

Each is a finding the author must justify, not a nit:

- **Preserved incidental complexity** when a visibly simpler reframing exists.
- **A file growing past ~1000 lines** in this change — ask for decomposition first; waive only for a
  compelling structural reason with the file still clearly organized.
- **Ad-hoc conditionals, one-off flags, or scattered special cases** bolted into unrelated flows — a
  design problem, not a stylistic nit; the logic wants a dedicated abstraction, policy object, or
  module.
- **Feature logic leaking into shared paths**, or a bespoke helper duplicating a canonical one — push
  code to the layer that already owns the concept.
- **Thin wrappers, identity abstractions, magic genericity, or cast/`any`/optionality churn** that
  obscures the real contract — prefer direct, boring code with explicit type boundaries.
- **Avoidably sequential orchestration or non-atomic updates** where the cleaner structure is obvious —
  without over-indexing on micro-optimizations.

## Remedies point the same direction

Delete a layer of indirection rather than polishing it; reframe the state model so conditionals
disappear; move logic to the module that owns the concept; extract the helper or split the file;
convert special cases into simpler default flows with fewer exceptions.

## Weight and tone

Within the Standards report, structural regressions and missed simplifications outrank boundary and
type-contract problems, which outrank file size, which outranks legibility. A few high-conviction
findings beat a long list of nits. Be direct and demanding about quality without rudeness; report a
structural issue at its real severity rather than softening it into a mild suggestion.

## The bar for a clean pass

Correct behavior alone is not a clean Standards pass. A clean pass has no structural regression, no
obvious missed simplification, no unjustified file-size explosion, no spaghetti growth from
special-case branching, and no boundary leak or avoidable canonical-helper duplication.
