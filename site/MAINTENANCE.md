# site/ — maintenance contract

The repo's documentation app: a static, framework-free viewer for the skill family, eventually deployed at
skills.ashanjum.com (no deployment yet). Serve locally from the **repo root** — `python3 -m http.server`,
open `http://localhost:8000/site/` — because the app fetches skill files by relative path and `file://`
cannot fetch.

## Drift design — what can and cannot go stale

- **Layer 1 (cannot drift):** everything a reader reads. Skill content is fetched from the real files at
  view time; the dependency edges and header chips are parsed from each `SKILL.md`'s frontmatter — the same
  bytes rendered in the panel. Nothing is copied into the app.
- **Layer 2 (can drift, gated):** `views/*.json` — three views today: `sdlc` (family dependency graph;
  edges from frontmatter), `flow` (the user/orchestrator/subagent/tracker swim-lane; every box opens the
  contract behind it), `backlog` (the skill exploded: seams, references, playbooks, composed siblings).
  Rosters, lanes/phases, blurbs, file lists, open targets, and each skill node's `bindings` table (its
  ports: what the skill expects a project to bind, the playbook this repo binds it to, and the shipped
  template default) live here. `check.py` turns that drift into a failing check — including open targets
  or binding/default paths pointing at missing files or unknown nodes/views.

## Agent instructions

- **Touching a family skill?** The site is part of the change's blast radius. Adding/renaming/removing a
  skill, a reference file, or an attached playbook must update the affected `views/*.json` in the same change (a backlog reference belongs in both `sdlc` and `backlog` views), then run
  `python3 site/check.py` — errors block; warnings mean a file exists that the manifest doesn't list.
- **Never copy skill prose into the site.** If a description reads wrong in the app, fix the skill's
  frontmatter/SKILL.md — the app is a viewer, not a second home for content. Blurbs in the manifest are
  one-line orientation labels only.
- The verify step for changes under `skills/` in this family includes `site/check.py` (see
  `docs/agents/verifying.md` § Checks).

## Vendored dependencies

- `vendor/markdown-it.min.js` — markdown-it **14.1.0**, MIT (`vendor/markdown-it.LICENSE`). CommonMark +
  GFM tables.
- `vendor/x6.min.js` — AntV X6 **3.1.7**, MIT (`vendor/x6.LICENSE`), single UMD bundle (global `X6`,
  all former plugin subpackages merged in as of 3.x). The canvas engine: pan/zoom, obstacle-avoiding
  `manhattan` edge routing, HTML shapes (nodes and lane headers are `Shape.HTML` cells, so lane titles
  are part of the lane shape, not floating labels).
- Layout is deliberately NOT a library: node lane/phase membership is fixed by the manifests, so
  placement is a deterministic grid computed in `app.js` and only edge routing is delegated to the
  engine — the architecture the swimlane-layout literature converges on
  (see `research/site-diagram-stack/findings.md` for the evaluation that chose X6).
- To upgrade any of them: replace the file from the pinned npm dist, update the version here, and reload
  all three views to eyeball parity (edge routing and lane-header alignment are the regressions to watch).

## Future deployment (recorded intent, not built)

- Target: Vercel behind skills.ashanjum.com, still static. Content source becomes either the deployed repo
  files or `raw.githubusercontent.com` via the `?base=` query/`BASE` constant in `app.js` — the app already
  abstracts the content root, so deployment is configuration, not a rewrite.
- A deploy-time roster (all-skills view) can be generated with the installer's compiler:
  `python3 skills/system/setup-asher-skills/scripts/catalog.py compile` — a build product, not a committed
  registry.
