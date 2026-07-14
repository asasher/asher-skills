# until-zero

Workspace-owned personal cash runway with deterministic projection, review-before-apply mutations, a
dedicated Wallet capture API template, and a self-contained HTML review surface.

The published package owns reusable behavior only. A setup run materializes editable state, API source,
deployment bindings, generated reports, and Shortcut artifacts in the consumer project. This source never
contains financial data, secrets, provider identities, or a generated/signed Shortcut.

The projection semantics and Wallet normalization are ported from the historical Until Zero Lakebed
application. The materialization/upgrade pattern is adapted from this repository's `capture-to-inbox` skill;
the two skills remain independent and share no runtime files.

Legacy data migration is intentionally outside this package. After installation, a separate one-time cutover
may generate a source dump and import it into the consumer-owned instance; no migration code or data ships here.

Validate the package with:

```bash
python3 -m unittest discover -s skills/personal/until-zero/evals -p 'test_*.py'
node --test skills/personal/until-zero/assets/runway-api/test/runway.test.js
```
