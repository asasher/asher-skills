# Global staffing surface — removal backups (asher-skills#114)

The machine-level staffing surface was removed from `Ashers-MacBook-Pro` on 2026-07-30 (the contract
phase of #107's expand → migrate → contract sequencing). These are byte-exact copies of the four removed
files, taken immediately before removal; md5 of each backup was verified identical to the live file it
copies.

| removed path | backup | md5 |
|---|---|---|
| `~/.claude/CLAUDE.md` | `backup/claude/CLAUDE.md` | `ed964c93b33357fb95ef7ec89da277c6` |
| `~/.claude/asher-skills/staffing.md` | `backup/claude/staffing.md` | `22f57c905160b6e512afce86f3d8e06f` |
| `~/.codex/AGENTS.md` | `backup/codex/AGENTS.md` | `4e7280bdb7b5651ff194baaa0e44cfd3` |
| `~/.codex/asher-skills/staffing.md` | `backup/codex/staffing.md` | `fe13fe3d4063680a2d0a30102eae3372` |

The `asher-skills` directories under `~/.claude/` and `~/.codex/` contained only their `staffing.md` and
were removed whole. Both global instruction files contained nothing but the staffing block (verified before
removal), so they were deleted outright rather than left empty — an empty always-loaded instruction file is
a standing invitation for unversioned knowledge to accumulate, which is the failure mode this removal ends.

To restore (recovery only — resolution must never route through these paths again):

```sh
cp backup/claude/CLAUDE.md ~/.claude/CLAUDE.md
mkdir -p ~/.claude/asher-skills && cp backup/claude/staffing.md ~/.claude/asher-skills/staffing.md
cp backup/codex/AGENTS.md ~/.codex/AGENTS.md
mkdir -p ~/.codex/asher-skills && cp backup/codex/staffing.md ~/.codex/asher-skills/staffing.md
```

Verification records: preconditions and post-removal probe results are on the ticket
(asher-skills#114); every migrated repo resolves its roster from its own `docs/agents/staffing.md`.
