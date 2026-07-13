# join — Party B joins after cloning

Run by the second partner once they've accepted the GitHub invite and cloned the repo. The shared files
already exist (Party A scaffolded them). Your job is only to create *your* private side and record identity.
Read `protocol.md` first.

## Steps

1. **Confirm you're in the cloned deal repo** (it has `canvas.json` and `negotiation/state.json`). If not,
   tell the user to clone the repo Party A shared and open it with their agent here.

2. **Create your private scratchpad** (gitignored — confirm `.gitignore` already lists `private/`; it should,
   since A committed it):
   - `private/whoami` → `B`
   - `private/solo-prep.md` ← `templates/solo-prep.md`
   - `private/notes/.gitkeep`
   Verify `git status` shows nothing under `private/`.

3. **Confirm your name** in `negotiation/state.json` under `parties.B` (only if blank/incorrect — that's a
   shared-file write, so follow the turn protocol: it's fine to do this as a tiny housekeeping commit, but
   prefer to fold it into your first interview-completion update).

4. **Hand off to interview.** Tell the user you'll now interview them privately (`fair-deal interview`) to
   capture their goals, concerns, and floor — and that the other side's agent is doing the same. Negotiation
   starts automatically once both sides have finished.

## Guardrails
- Never commit anything under `private/`.
- Don't touch Party A's outbox (`negotiation/from-A/`) or overwrite shared files out of turn.
