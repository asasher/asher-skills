---
name: shadixfy
description: Pin generated frontend UI to the shadcn/ui visual language and tokens, stripping the default AI aesthetic. Use whenever generating or restyling any frontend UI.
---

# Shadixfy

A shadcn-pegged fork of Uncodixfy. Build from shadcn/ui: Radix primitives, Tailwind utilities, and semantic CSS variables. Every surface maps to a token, radius derives from one variable, and components come from the registry. Use one neutral base plus a restrained accent.

## Build With The Tokens

Style **everything** through shadcn/ui’s semantic variables.

- `background` / `foreground` — the page and its text.
- `card` / `card-foreground`, `popover` / `popover-foreground` — raised surfaces.
- `primary` / `primary-foreground` — the one solid action color.
- `secondary` / `secondary-foreground` — quieter solid actions.
- `muted` / `muted-foreground` — subdued surfaces and secondary text.
- `accent` / `accent-foreground` — hover/active surface.
- `destructive` — danger only.
- `border`, `input`, `ring` — hairlines, field borders, focus ring.
- `--radius` — one radius variable everything derives from (`0.5rem` base; `calc()` for `sm`/`md`/`lg`).

## Keep It Normal (shadcn Standard)

- Sidebars: normal (fixed ~16rem, `bg-background` or `bg-muted/40`, single `border-r`, no floating shell, no rounded outer corners).
- Headers: normal (plain `h1`/`h2` with `text-foreground`, no eyebrows, no uppercase kicker, no gradient text).
- Sections: normal (consistent `p-4`/`p-6`, no hero block inside an app, no decorative copy).
- Navigation: normal (links with `text-muted-foreground` → `text-foreground` on hover, `bg-accent` for active, no transform, no badges unless functional).
- Buttons: normal (shadcn `Button` variants only — `default`/`secondary`/`outline`/`ghost`/`destructive`/`link`; no pills, no gradient fills).
- Cards: normal (`Card` = `rounded-lg border bg-card`, `shadow-sm` at most, no glow, no float).
- Forms: normal (`Label` above `Input`, real focus ring, no floating labels, no morphing).
- Inputs: normal (`border-input bg-transparent`, `ring` on focus via `focus-visible`, no animated underline).
- Modals/Dialogs: normal (`Dialog` — centered, `bg-background/80` backdrop, simple close; no slide-in theatrics).
- Dropdowns/Menus: normal (`DropdownMenu`/`Select` — `bg-popover`, subtle shadow, clear selected state).
- Tables: normal (`Table` — `border-b` rows, `hover:bg-muted/50`, left-aligned, no zebra unless data demands it).
- Tabs: normal (underline or `bg-muted` track with one active segment; no sliding animation).
- Badges: normal (shadcn `Badge` variants, small, only when they carry state).
- Avatars: normal (`Avatar` circle with fallback initials, no status ring unless functional).
- Switches: normal (`Switch` track/thumb, functional state only). In single-file HTML, use utility classes such as `rounded-full`.
- Icons: normal (lucide-react, 16–20px, `text-muted-foreground` or `currentColor`, no icon background tiles).
- Typography: normal (Geist or the project's existing sans; clear hierarchy; body 14–16px; no serif/sans mixing).
- Spacing: normal (Tailwind scale — `2/3/4/6/8`; no random gaps, no overpadding).
- Borders: normal (`border` token, 1px; no thick or gradient borders).
- Shadows: normal (`shadow-sm`, occasionally `shadow-md` for popovers; no dramatic or colored shadows).
- Transitions: normal (`transition-colors`, 150ms; no bounce, no transform effects).
- Radius: normal (everything off `--radius`; `rounded-lg`/`rounded-md`; no `rounded-3xl` everywhere).
- Layouts: normal (standard grid/flex, predictable structure, `max-w-screen-xl`-ish containers, no creative asymmetry).
- Panels: normal (separate surfaces by token — `bg-muted`, `border` — not by floating, not by glass).
- Toolbars/Footers/Breadcrumbs: normal (simple, standard height, functional only).

Compose components as shipped by `npx shadcn@latest add` or the project’s Figma library. Use sections for landing pages and sidebar + content for dashboards.

## Hard No

Use the token and component rules above to correct these recurring visual failures:

- Oversized decorative radii — the 20–32px range across everything, or the same fat rounded rectangle repeated on sidebar, cards, buttons, and panels. One `--radius`, derived consistently.
- Glass, glow, and haze as decoration: floating glassmorphism shells as the default language, frosted panels, blur haze, random glows, conic-gradient donuts.
- Soft corporate gradients used to fake taste. Brand marks with gradient backgrounds (`linear-gradient(135deg, …)`). Pipeline/progress bars with gradient fills; quota panels with progress bars as decoration.
- Generic dark SaaS: radial-gradient backgrounds, blue-black "premium dark mode" gradients, cyan/indigo accents as the default reflex (see Color for when a cool accent is earned).
- `Inter`, `Roboto`, `Segoe UI`, `Trebuchet MS`, `Arial`, or safe default stacks. Use **Geist** (Geist Sans / Geist Mono) — or whatever font the project already ships.
- Metric/KPI-card grid as the first instinct or default dashboard layout.
- Fake charts that exist only to fill space — e.g. a canvas/donut dropped into a glass card with no product reason, paired with hand-wavy percentages.
- Hero section inside an internal UI without a real product reason — hero strips and decorative page headers like "Operational clarity without the clutter."
- Alignment that manufactures dead space to look expensive; mixed alignment where some content hugs the left and some floats center-ish.
- Mobile collapse that stacks everything into one long sandwich.
- Decorative sidebar blobs or workspace CTA blocks in the rail; a right rail with a "Today" schedule; multiple nested panel types (`panel`, `panel-2`, `rail-panel`, `table-panel`).
- "Control room" cosplay unless explicitly requested.
- Ornamental labels ("live pulse", "night shift", "operator checklist") unless they come from the product voice. Section notes and mini-notes everywhere explaining what the UI does. "Team focus" / "Recent activity" panels with decorative internal copy. Footer meta lines ("Northstar dashboard • dark mode • single-file HTML"). Generic startup copy, or any style decision made because it's easy to generate.
- Eyebrow labels — uppercase + letter-spacing kickers like "MARCH SNAPSHOT".
- Dramatic box shadows (`0 24px 60px rgba(0,0,0,.35)`). Cap at `shadow-sm`/`shadow-md`.
- Transform animations on hover (`translateX(2px)` on nav links). Use `transition-colors` only.
- Status dots via `::before` pseudo-elements; muted uppercase + letter-spacing labels.
- Muted gray-blue text that weakens contrast — use `muted-foreground`, which is tuned for it.
- Tables that slap a colored tag badge on every row. Trend indicators as colored text classes (`trend-up`, `trend-flat`).
- Sticky headers/top bars that copy shadcn block glass (`bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60`). Even if a registry block ships it, use solid `bg-background` with `border-b` instead.

Replace decorative eyebrow headers with a plain heading. Example to simplify:

```html
<div class="headline">
  <small>Team Command</small>
  <h2>One place to track what matters today.</h2>
  <p>Live project health, team activity, and near-term priorities…</p>
</div>
```

Remove cards whose only content is decorative advice:

```html
<div class="team-note">
  <small>Focus</small>
  <strong>Keep updates brief, blockers visible, next actions easy to spot.</strong>
</div>
```

## Color

Resolve color tokens in this order:

1. **Highest priority:** use the existing tokens from the user's project if present (read `globals.css` / `tailwind.config` / `components.json` and reuse the `--background`, `--primary`, … they already define).
2. If the project has none, **adopt one of the shadcn base palettes** verbatim. Copy it from [references/palettes.md](references/palettes.md) — **Zinc** (default), **Neutral** (pure gray), or **Stone** (warm gray).
3. For new standalone UIs with no existing brand tokens, choose exactly one non-blue accent family from the shadcn/Tailwind color library by default. Map it to `--primary`, `--primary-foreground`, `--ring`, and chart/status tokens. Black `--primary` is reserved for an explicitly requested monochrome UI or an existing monochrome project. Keep `--accent` as the muted hover/active surface.
4. Keep surfaces on the neutral ramp and use solid accent fills.

The shadcn v3 color library is the source for palette values: Tailwind colors in HSL, RGB, HEX, and OKLCH formats. Use those values directly. Prefer warm or organic accents for generic products: **orange**, **amber**, **green**, **emerald**, **teal**, **rose**, or **purple**. Use **blue**, **sky**, **cyan**, or **indigo** only when the product domain calls for a cool color.

Good accent examples from shadcn v3 HSL values:

```css
/* Orange */
--primary: 20.5 90.2% 48.2%;       --primary-foreground: 0 0% 9%;
--ring: 20.5 90.2% 48.2%;

/* Emerald */
--primary: 161.4 93.5% 30.4%;      --primary-foreground: 0 0% 9%;
--ring: 161.4 93.5% 30.4%;

/* Rose */
--primary: 346.8 77.2% 49.8%;      --primary-foreground: 0 0% 98%;
--ring: 346.8 77.2% 49.8%;

/* Purple */
--primary: 271.5 81.3% 55.9%;      --primary-foreground: 0 0% 98%;
--ring: 271.5 81.3% 55.9%;
```

For charts, use 2–4 shadcn palette stops plus neutral grid/text tokens. For status, use semantic color only when the status exists (`destructive`, success, warning).

If the product needs color, change only the semantic accent tokens (`--primary`, `--primary-foreground`, `--ring`, and chart/status variables) and leave the neutral ramp intact.
