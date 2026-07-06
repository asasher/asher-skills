# Design language

<!-- Distilled from shadixfy@a58e37d; keep in sync deliberately, not automatically. -->

Priority order, decided at intake and recorded in `BRIEF.md`:

1. **Client brand tokens** if the intake produced guidelines — map them onto shadcn's semantic variables
   (`--primary`, `--ring`, chart/status tokens); leave the neutral ramp intact unless the brand demands
   otherwise.
2. **Stock shadcn/ui** otherwise: neutral base (zinc default; neutral for pure gray, stone for warm), one
   restrained accent at most. Never invent a third option mid-build.

The blueprint is shadcn/ui itself: Radix primitives, Tailwind utilities, semantic CSS variables. If a
choice isn't expressible in shadcn's token vocabulary, it's probably the wrong choice.

## Build with the tokens, not around them

Style everything through the semantic variables — `background`/`foreground`, `card`, `popover`, `primary`,
`secondary`, `muted`, `accent` (hover/active surface, NOT a brand pop), `destructive`, `border`/`input`/
`ring`, one `--radius`. Never hardcode a hex when a token exists. If you're reaching for a value with no
token, stop — you're decorating.

## Keep it normal

Compose registry components as shipped (`npx shadcn add`), don't redesign the primitive. Sidebars fixed and
flat with a single `border-r`; plain `h1`/`h2` headers; `Button` variants only; `Card` = border + `bg-card`
+ `shadow-sm` at most; labels above inputs with a real focus ring; centered `Dialog`; left-aligned `Table`
with `border-b` rows and `hover:bg-muted/50`; lucide icons 16–20px in `text-muted-foreground`; Tailwind
spacing scale (`2/3/4/6/8`); 1px borders; `transition-colors` ~150ms; everything off one `--radius`
(`rounded-md`/`rounded-lg`); predictable grid/flex layouts. A dashboard gets sidebar + content — use the
standard layout, do not invent one.

## Hard no (the default-AI-aesthetic list)

- Gradients as decoration (backgrounds, buttons, brand marks, progress fills); colored or dramatic shadows;
  glassmorphism/backdrop-blur shells; floating detached rounded sidebars.
- Eyebrow/kicker labels (uppercase + letter-spacing), hero blocks inside app UIs, decorative section notes
  explaining what the UI does, ornamental status dots, footer meta lines.
- Oversized radii (20–32px everywhere), pill overload, overpadding, manufactured dead space.
- Default-blue/cyan/indigo AI accent — only when the domain genuinely calls for it. Prefer orange, amber,
  green, emerald, teal, rose, or purple when an accent is needed.
- KPI-card grid as the reflex dashboard layout; fake charts that exist to fill space; a colored badge on
  every table row; nav badges as decoration.
- `Inter`/`Roboto`/`Segoe UI`/safe stacks — use **Geist** (or the brand's font from intake).
- Transform animations on nav hover; `transition: all`.
- In your reasoning, list every decorative move you'd normally make — then don't make it.

## Charts and status

Charts: 2–4 palette stops plus neutral grid/text tokens; charts must plot the fixture data (a chart is mock
data too — believable trend, seasonality, ragged values). Status color only where status exists
(`destructive`, success, warning) — never color for color's sake.
