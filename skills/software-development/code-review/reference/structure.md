# The structural bar

Review changed logic for complexity that leaks across module boundaries or grows the cost of the requested behavior. Consider a reframing when it removes that cost at the scope of this change.

## Findings worth raising

- Special cases or feature logic spread through unrelated shared paths.
- A new helper duplicates a canonical abstraction or hides an important contract behind forwarding layers.
- Casts, optional fields, or generic interfaces weaken a previously explicit domain contract.
- A growing file combines responsibilities that now prevent independent reasoning or changes.
- Sequential work or non-atomic updates cause a concrete delay, race, or inconsistent state.

Each blocking finding names the changed hunk, a concrete failure scenario or maintenance cost, and a proportionate remedy. A file-size threshold, a smell name, or the existence of another design alone does not establish a blocker. Label suggestions without that evidence as optional.

Respect the spec's settled module and scope decisions. Surface a real contradiction for a ruling; avoid turning a review-scale fix into an unapproved redesign. Existing complexity matters when this change introduces or worsens its cost.

Rank findings by their actual impact. A structural preference never automatically outranks a broken type boundary or incorrect behavior. A clean Standards pass has no unresolved blocking findings; optional suggestions may remain.
