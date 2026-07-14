# until-zero

Workspace-owned personal cash runway with deterministic projection, review-before-apply mutations, a
dedicated Wallet capture API template, and a self-contained HTML review surface.

The published package owns reusable behavior only. A setup run materializes editable state, API source,
deployment bindings, generated reports, and Shortcut artifacts in the consumer project. This source never
contains financial data, secrets, provider identities, or a generated/signed Shortcut.

The projection semantics and Wallet normalization are ported from the historical Until Zero Lakebed
application. The materialization/upgrade pattern is adapted from this repository's `capture-to-inbox` skill;
the two skills remain independent and share no runtime files.
