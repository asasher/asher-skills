# setup - connect the local career ops workspace

Run once per person, and rerun when capabilities change. `setup` can run before a profile exists because it prepares the operating layer.

Use `scripts/init_workspace.py`, `scripts/server.py`, and `scripts/await.py` as the setup implementation; run them from the project root instead of rewriting local equivalents.

## Steps

1. Create or locate the one-person `goodwork/` workspace. Ensure `.env` is gitignored, initialize missing v2 state files from [state.md](state.md), and record any legacy Markdown files that need migration.
2. Connect Gmail and Calendar MCP connectors when available. Record unavailable connectors rather than blocking.
3. Create or verify the persistent Chrome profile under the workspace. Log into LinkedIn, job boards, and other chosen sites there.
4. Before WhatsApp Web setup, disclose read-only use and account-ban/Terms-of-Service risk. If the user declines, record WhatsApp as unavailable.
5. Vendor `@pierre/diffs` into the workspace for the CV/application review page. Record vendor status in `capabilities.json`.
6. Install or verify Tailscale as the default remote layer. Use `tailscale serve`, never `tailscale funnel`. If the user declines, record `desk-only`.
7. Ask for reconcile cadence: `manual`, `on-demand`, or `scheduled`. Write it to `capabilities.json`.
8. Run the live phone loop: start the local server, expose it through the tailnet when available, open the phone URL, tap the test button, confirm a test event lands in `events.jsonl`, and confirm the agent can drain it.

## Output

`capabilities.json` updated, initial state files present, phone loop result recorded, and any missing capability named with its fallback rung from [execution.md](execution.md).

## Completion Criteria

Setup is complete when `capabilities.json` truthfully records every capability, the approval/event loop is tested or explicitly marked unavailable, and the next command knows whether it can execute or must draft-and-instruct.
