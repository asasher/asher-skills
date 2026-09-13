# Environment doctor

Run when the user requests Diagram Design diagnostics, health checks, or first-run troubleshooting, including `/diagram-design:doctor` or `/doctor`.

Resolve the skill directory from this loaded reference so diagnostics work from any project. Keep the user’s project unchanged; use temporary probes and remove them afterward. Report each check as `pass`, `warn`, or `fail`.

## Inputs

- `--strict` treats warnings as failures in the final summary.
- `--json` adds a machine-readable report.

## Required checks

1. **Python runtime:** resolve a Python interpreter compatible with the shipped helpers (Python 3.10+). Report its path and version; absence or an incompatible version is `fail`.
2. **Shipped package:** verify `SKILL.md`, `scripts/self_check.py`, `scripts/drawio_extract.py`, and `scripts/mermaid_extract.py` exist beneath the resolved skill directory. Missing files are `fail`. Confirm the import helpers handle valid temporary input and the self-check accepts a valid temporary diagram; report execution failures separately from file presence.
3. **Browser capture:** discover an available browser connector or runtime. Launch or connect, then capture a temporary SVG probe with known dimensions. Confirm the output exists, has those dimensions, and shows the probe. Package imports, help output, and browser caches establish presence only. A failed or unavailable capture is `warn` with the failed operation and applicable repair instructions.
4. **Paths and references:** check the active instructions for missing local paths and command quoting problems. Report a precise fix for each finding. A missing resolved `SKILL.md` calls for repairing the skill installation.
5. **Optional repository wiring:** when running in an authoring or plugin checkout, inspect the manifests and routing files that actually exist. Verify their declared entrypoints and referenced files resolve. Run applicable package checks exposed by that checkout; installed skills require only their shipped package, so absent upstream maintainer tooling is not a failure.

## Output

Print a compact summary:

`Doctor summary: <PASS|WARN|FAIL> (<pass_count> pass, <warn_count> warn, <fail_count> fail)`

Follow with one line per check, identifying what was verified, the tool used, and any limitation. Add next actions for warnings and failures, using concrete commands appropriate to the discovered environment when useful.

With `--json`, also emit `status`, `counts`, `checks[]` (`name`, `status`, `message`, optional `fix`), and `timestamp`.

Capture unexpected failures and continue independent checks. Mark a check passed only after verifying it during this run.
