# Shadixfy

A shadcn-pegged fork of [cyxzdev/Uncodixfy](https://github.com/cyxzdev/uncodixfy). Same goal — keep AI-generated UI from sliding into the generic "Codex" aesthetic (soft gradients, floating glass cards, eyebrow labels, oversized radii, dramatic shadows) — but instead of "channel Linear/Raycast," the blueprint is **shadcn/ui**: Radix primitives, Tailwind classes, and a small set of semantic CSS variables.

The skill auto-loads when generating frontend code and enforces:

- **Token-driven styling** — everything maps to `background` / `card` / `muted` / `border` / `ring` / `--radius`; no hardcoded values when a token exists.
- **Registry-first components** — compose shadcn primitives, don't reinvent them.
- A **neutral, non-blue** color base. Ships the verified shadcn v3 (HSL) token sets for **Zinc** (default), **Neutral**, and **Stone**, light + dark, at `--radius: 0.5rem`. Slate/Gray are excluded for leaning cool.
- **Geist** over Inter/Roboto/system stacks.

## Differences from Uncodixfy

- Color section replaced: 20 invented palettes → shadcn's actual semantic token system (3 neutral bases, drop-in `:root`/`.dark`).
- Visual language pinned to shadcn components and tokens rather than described by reference apps.
- Kept Uncodixfy's taste where it conflicts with shadcn defaults: no Inter, no blue-leaning base.

## Install

```bash
npx skills add <repo-url> --skill shadixfy -g
```
