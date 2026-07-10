---
name: shadixfy
description: Pin generated frontend UI to the shadcn/ui visual language and tokens, stripping the default AI aesthetic. Use whenever generating or restyling any frontend UI.
---

# Shadixfy

A shadcn-pegged fork of Uncodixfy. Same job — strip the default AI aesthetic out of generated UI — but the blueprint is not "vibes of Linear/Raycast." The blueprint is **shadcn/ui**: Radix primitives, Tailwind utility classes, and a small set of semantic CSS variables. If a choice isn't expressible in shadcn's token vocabulary, it's probably the wrong choice.

Codex UI is the default AI aesthetic: soft gradients, floating glass panels, eyebrow labels, decorative copy, hero sections inside dashboards, oversized rounded corners, transform animations, dramatic shadows, and layouts that try too hard to look premium. It screams "an AI made this" because it follows the path of least resistance.

shadcn/ui is the opposite by construction. Every surface maps to a token (`background`, `card`, `muted`, `border`, `ring`). Radius comes from one variable. Color is one neutral base plus a restrained accent. Components are copied from a fixed registry, not invented. Your job: recognize the Codex patterns, refuse them, and reach for the shadcn primitive instead.

This is how you Shadixfy.

## Build With The Tokens, Not Around Them

shadcn/ui's whole system is a handful of semantic variables. Style **everything** through them — never hardcode a hex when a token exists.

- `background` / `foreground` — the page and its text.
- `card` / `card-foreground`, `popover` / `popover-foreground` — raised surfaces.
- `primary` / `primary-foreground` — the one solid action color.
- `secondary` / `secondary-foreground` — quieter solid actions.
- `muted` / `muted-foreground` — subdued surfaces and secondary text.
- `accent` / `accent-foreground` — hover/active surface, NOT a brand pop color.
- `destructive` — danger only.
- `border`, `input`, `ring` — hairlines, field borders, focus ring.
- `--radius` — one radius variable everything derives from (`0.5rem` base; `calc()` for `sm`/`md`/`lg`).

If you're reaching for a value that has no token, stop — you're probably decorating.

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
- Switches: normal (`Switch` track/thumb, functional state only). In single-file HTML, use utility classes such as `rounded-full`; do not handwrite `border-radius: 9999px`.
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

Build it like you'd `npx shadcn@latest add` the component and use it as-is. Don't redesign the primitive — compose it.

- A landing page still gets its sections; a dashboard still gets sidebar + content. Use the standard layout, do not invent one.
- In your internal reasoning, list every decorative move you'd normally make, then DON'T make it.
- Replicate registry/Figma components. Do not invent your own.

## Hard No

Everything you reflexively reach for and treat as an automatic "yes." Refuse all of it:

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

No headlines-with-eyebrow blocks of any sort. `<small>` eyebrow headers are not allowed; rounded decorative `span`s are not allowed:

```html
<div class="headline">
  <small>Team Command</small>
  <h2>One place to track what matters today.</h2>
  <p>Live project health, team activity, and near-term priorities…</p>
</div>
```

This card structure is the biggest no:

```html
<div class="team-note">
  <small>Focus</small>
  <strong>Keep updates brief, blockers visible, next actions easy to spot.</strong>
</div>
```

## Color

If a UI choice feels like a default AI move, ban it and pick the cleaner option. Colors can exist, but they must behave like shadcn tokens, not decoration. Start neutral, add one restrained accent when it helps the product, and keep everything wired through CSS variables.

You are bad at picking colors. Follow this priority:

1. **Highest priority:** use the existing tokens from the user's project if present (read `globals.css` / `tailwind.config` / `components.json` and reuse the `--background`, `--primary`, … they already define).
2. If the project has none, **adopt one of the shadcn base palettes** verbatim. Copy it from [references/palettes.md](references/palettes.md) — **Zinc** (default), **Neutral** (pure gray), or **Stone** (warm gray).
3. For new standalone UIs with no existing brand tokens, choose exactly one non-blue accent family from the shadcn/Tailwind color library by default. Map it to `--primary`, `--primary-foreground`, `--ring`, and chart/status tokens. Do not leave `--primary` black unless the user explicitly asks for a monochrome UI or the existing project already uses monochrome tokens. Keep `--accent` as the muted hover/active surface.
4. Do **not** invent random color combinations. Do not use gradients or colored shadows to make the accent feel bigger. Everything still sits on the neutral ramp.

The shadcn v3 color library is the source for palette values: Tailwind colors in HSL, RGB, HEX, and OKLCH formats. Use those values directly. Prefer warm or organic accents for generic products: **orange**, **amber**, **green**, **emerald**, **teal**, **rose**, or **purple**. Use **blue**, **sky**, **cyan**, or **indigo** only when the product domain calls for a cool color; never as the default AI SaaS reflex.

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

For charts, use 2–4 shadcn palette stops plus neutral grid/text tokens. For status, use semantic color only when the status exists (`destructive`, success, warning); do not color every badge or row just because a palette is available.

Avoid **Slate** and **Gray** as generic bases — they lean cool/blue. If the product needs color, change only the semantic accent tokens (`--primary`, `--primary-foreground`, `--ring`, and chart/status variables) and leave the neutral ramp intact.
