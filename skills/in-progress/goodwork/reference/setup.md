# setup - connect the local career ops workspace

Run once per person; rerun when capabilities change. Can run before a profile exists. Use `scripts/init_workspace.py`, `scripts/server.py`, and `scripts/await.py` from the project root — don't rewrite local equivalents.

## Steps

1. Create or locate the one-person `goodwork/` workspace. Ensure `.env` is gitignored, initialize missing v2 state files per [state.md](state.md), record any legacy Markdown needing migration.
2. Connect Gmail and Calendar MCP connectors when available. Record unavailable connectors rather than blocking.
3. Create or verify the persistent Chrome profile under the workspace. Log into LinkedIn, job boards, and other chosen sites there.
4. Before WhatsApp Web setup, disclose read-only use and account-ban/Terms-of-Service risk. Declined → record WhatsApp unavailable.
5. Vendor `@pierre/diffs` into the workspace for the CV/application review page. Record vendor status in `capabilities.json`.
6. Install or verify Tailscale as the default remote layer — `tailscale serve`, never `tailscale funnel`. Declined → record `desk-only`.
7. Ask for reconcile cadence: `manual`, `on-demand`, or `scheduled`. Write it to `capabilities.json`.
8. Run the live phone loop: start the local server, expose it through the tailnet when available, open the phone URL, tap the test button, confirm the test event lands in `events.jsonl` and the agent can drain it.
9. Record presentation rungs in `capabilities.json` (`presentation.rungs`, best-first from [presentation.md](presentation.md)): probe this session's surface for an inline widget renderer, note whether the server pages open in a browser, and always include `markdown`. Note inline availability is per-surface — sessions re-detect at present time.

Present this to the user as plumbing they don't need to understand: what they get (a board, a yes/no page on their phone), not how it works.

## Output

`capabilities.json` updated, initial state files present, phone loop result recorded, any missing capability named with its fallback rung from [execution.md](execution.md).

## Completion Criteria

`capabilities.json` truthfully records every capability, the approval/event loop is tested or explicitly marked unavailable, and the next command knows whether it can execute or must draft-and-instruct.
