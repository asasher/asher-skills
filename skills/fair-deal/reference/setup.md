# setup — Party A scaffolds the deal

Run by the partner who starts the deal. Goal: a private GitHub repo with the skill committed, the canvas and
negotiation files scaffolded, a gitignored private scratchpad, and Party B invited. Idempotent — if a piece
already exists, leave it. Read `protocol.md` first.

## Steps

1. **Confirm context.** Ensure the cwd is where the deal should live and that the skill is installed in this
   project (not global). If there's no git repo yet, you'll create one below. If the skill was invoked
   globally, stop: tell the user to `mkdir <deal-name> && cd <deal-name>` and install the skill there.

2. **Gather the basics (short, conversational):** a deal name (repo slug), your name (Party A), the other
   partner's name and **GitHub username** (for the invite), and a one-line description of the deal.

3. **Scaffold files** from `templates/` into the repo root:
   - `.gitignore` ← `templates/gitignore` (must list `private/`).
   - `canvas.json` ← `templates/canvas.seed.json` (set `partyA`, `partyB`, `deal`, `date`).
   - `canvas.html` ← `templates/canvas.html` (the review surface).
   - `negotiation/state.json` ← `templates/state.json` (set `parties`, `phase:"interview"`, `turn:"A"`).
   - `negotiation/log.md` ← a one-line header.
   - `negotiation/from-A/.gitkeep`, `negotiation/from-B/.gitkeep`.
   - `README.md` ← `templates/README-deal.md` (fill in names/deal).

4. **Create the private scratchpad** (gitignored — never committed):
   - `private/whoami` → `A`
   - `private/solo-prep.md` ← `templates/solo-prep.md`
   - `private/notes/.gitkeep`
   Verify `git status` does **not** show anything under `private/`. If it does, fix `.gitignore` before any commit.

5. **Commit the scaffold** (the skill dir is included so Party B gets it on clone). Confirm `private/` is absent
   from the commit.

6. **Create the PRIVATE GitHub repo and push.** Use `gh`:
   ```
   gh repo create <slug> --private --source . --remote origin --push
   ```
   If `gh` isn't authenticated, guide the user to run `gh auth login` (suggest they type `! gh auth login`).
   **The repo must be private** — it carries a real business negotiation. Verify with `gh repo view --json visibility`.

7. **Invite Party B** as a collaborator:
   ```
   gh repo invite <owner>/<slug> <partnerB-github-username>   # or: gh api ... /collaborators
   ```
   Tell the user what Party B must do: accept the invite, clone the repo, open it with their agent, and run
   `fair-deal join`. Give them the clone URL.

8. **Hand off to interview.** Tell the user setup is done and that you'll now interview them privately to
   capture their true goals, concerns, and floor (`fair-deal interview`). Offer to start immediately.

## Guardrails
- Never push anything under `private/`. Double-check before the first push.
- The repo is private by default and must stay private; never create it public.
- Don't ask the human to run git/gh commands themselves unless auth genuinely requires it (e.g. `gh auth login`).
