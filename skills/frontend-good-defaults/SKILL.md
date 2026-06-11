---
name: frontend-good-defaults
description: "Use whenever designing, implementing, reviewing, or polishing frontend UI for web or app surfaces, including HTML/CSS, React, Vue, Svelte, landing pages, dashboards, internal tools, prototypes, demos, and games. This is a self-contained visual-design reset for agents: it blocks generic AI UI patterns and uses a framework-agnostic baseline for hierarchy, layout, typography, semantic tokens, components, motion, states, and verification."
---

# Frontend Good Defaults

This skill is a reset. Use it to stop the usual AI-generated UI habits before writing or reviewing frontend code. The goal is not decoration. The goal is a useful, deliberate interface that looks like a competent product designer shaped it.

The default taste reference is restrained product UI: semantic tokens, composable primitives, accessible states, neutral surfaces, clear variants, and source-code ownership. Use that visual and structural baseline without assuming React, Tailwind, or any specific implementation unless the project already uses them.

## Priority Order

1. Existing product UI, components, tokens, typography, spacing, brand assets, and codebase conventions.
2. User-provided screenshots, design direction, product voice, and target audience.
3. These defaults.

Do not invent a new visual language when the project already has one. Do not use style choices because they are easy to generate.

## The Reset

- Start with the real feature, workflow, content, or object. Do not start with a shell, hero, nav, dashboard grid, or decorative cards.
- Build the smallest complete version that can work. Do not imply uploads, filters, charts, collaboration, realtime state, AI magic, or controls that are not implemented.
- Treat UI as hierarchy, not styling. Make the important thing obvious by making competing things quieter.
- Work in structure first: spacing, alignment, size, weight, and contrast. Add color and effects only after the layout reads clearly.
- Prefer normal, useful, durable UI over "premium" composition. If a choice feels like an AI default, remove it.
- Use product language. Never include design commentary, prompt language, or text explaining the UI's visual choices inside the interface.
- Verify the result in a browser or screenshot at desktop and mobile sizes before calling it done.

## Component Baseline

- Prefer clear component anatomy: small composable primitives, predictable variants, semantic tokens, keyboard-accessible behavior, and local ownership of component code.
- If the project already uses a component system, read its config, tokens, installed components, aliases, icon set, and primitives before inventing styles.
- If it does not, emulate the pattern, not the React code: use semantic CSS/custom-property tokens, accessible HTML, and the closest framework-native primitive library.
- Use token pairs: `background/foreground`, `card/card-foreground`, `popover/popover-foreground`, `primary/primary-foreground`, `secondary/secondary-foreground`, `muted/muted-foreground`, `accent/accent-foreground`, `destructive/destructive-foreground`, plus `border`, `input`, `ring`, `radius`, and sidebar tokens when needed.
- Start from neutral base colors such as neutral, stone, zinc, taupe, olive, or mist. Let one restrained primary token do most of the action work.
- Model states explicitly: hover, focus-visible ring, active/selected, disabled, loading, empty, invalid/error, destructive confirmation, and reduced-motion.
- Use established primitive families when available: dialog/alert dialog, dropdown/menu, popover, tooltip, command palette, tabs, accordion/collapsible, sidebar, resizable panels, scroll area, field/input group, table/data table, skeleton, empty state, toast.
- Keep variants consistent across implementations: button `default`, `secondary`, `outline`, `ghost`, `destructive`, `link`; size `sm`, `default`, `lg`, `icon`.
- Treat framework ports as first-class. Vue, Svelte, plain HTML/CSS, Web Components, or native platform components should still follow the same anatomy, tokens, and states.

## First Pass

Before building substantial UI, decide internally:

- Surface type: app/workspace, landing/editorial page, focused tool, game, or demo.
- Primary user action: what should the user do first?
- Real content: what data, media, states, or controls actually exist?
- Visual thesis: what mood, material, and density fit the product?
- System choices: spacing scale, type scale, color tokens, radii, shadows, and motion.

For small tasks, do this mentally and proceed. For larger visual work, keep the plan short and implement.

## App UI

App screens are working surfaces. Start with the table, list, editor, form, board, chart, map, calendar, canvas, inbox, settings panel, or inspector that the user came to use.

- Use utility copy: labels, state, freshness, scope, and action.
- No marketing hero inside dashboards, admin tools, or operational surfaces unless explicitly requested.
- Use a predictable structure: navigation, primary workspace, and optional secondary context.
- Add a sidebar only when the information architecture needs it. When needed, keep it ordinary: 240-260px, solid background, border-right, no floating shell, no rounded outside corners. If collapse or icon-only mode is useful, implement the state.
- Sidebar navigation should read as navigation, not a stack of cards. Use flat rows, text weight, and subtle background for active state; avoid full bordered rounded nav tiles and chunky active accent bars.
- Prefer dense but readable layouts. Internal tools should feel efficient, not like a landing page.
- Use cards only for repeated objects, modals, or framed interactions. If a card can become plain layout without losing meaning, remove the card.
- Prefer lists, tables, split panes, toolbars, filters, detail drawers, and inspectors over KPI-card mosaics.
- If a split pane is useful, make it actually resizable or choose fixed, intentional dimensions. Do not show resize affordances that do nothing.
- Action hierarchy matters more than button semantics: one primary action, quiet secondary actions, unobtrusive tertiary actions.
- Destructive actions are not automatically big red buttons. Entry points to destructive flows should usually be secondary/outline; make the destructive treatment dominant only in the confirmation step where destruction is the primary action.

## Landing Pages

Landing pages need composition, not component soup. The first viewport should identify the brand, product, place, person, object, game, or offer immediately.

- Use one dominant visual idea per section.
- First viewport order: brand/product signal, short promise, primary action, dominant visual.
- Default section flow: hero, support/proof, detail/depth, final CTA.
- For branded or image-led pages, use a full-bleed hero or full-canvas visual anchor. Do not put hero text in a card.
- The hero image or media must do real narrative work. If the first viewport still works after removing the image, the image is too weak.
- Keep copy short enough to scan in seconds. Delete repeated mood statements.
- Each section should explain, prove, deepen, or convert. If it does none of these, remove it.
- Text over imagery needs a calm tonal area, strong contrast, and usable tap targets.
- If there is a fixed or sticky header, it counts against the first viewport. The hero must still fit on common desktop and mobile sizes.

## Layout And Spacing

- Use a spacing scale instead of one-off values: `4, 8, 12, 16, 24, 32, 48, 64, 96, 128`.
- At small sizes, adjacent values need meaningful jumps; do not nitpick 12px vs 13px or 120px vs 125px.
- Start with more whitespace than feels necessary, then remove it deliberately. Dense UI is allowed when density is the point.
- Group relationships must be obvious: space inside a group is smaller than space around the group.
- Do not fill the screen just because space exists. Give each element the width it needs.
- Constrain paragraph widths even inside wide layouts. Wider media does not require wider text.
- Use fixed or max widths for elements with an intended size. Sidebars, forms, cards, icon buttons, boards, and toolbars should not stretch just because a grid can stretch them.
- Use fluid grids only when the content should actually scale.
- Large elements should shrink faster on small screens than already-small elements. Do not encode all relationships with proportional `em` math.
- Use stable dimensions for boards, grids, counters, tiles, icon buttons, and media so hover, loading, labels, and dynamic values cannot shift the layout.
- If a narrow component feels lost in a wide area, split supporting content into a second column instead of making the component too wide.

## Hierarchy

- Not everything is equal. Decide what is primary, secondary, and tertiary before styling.
- Use font weight, color, contrast, spacing, and position before increasing font size.
- Two or three text colors are usually enough: primary, secondary, and muted.
- Two font weights are usually enough for UI: regular/medium for most text and semibold/bold for emphasis.
- Avoid font weights below 400 for interface text.
- Labels for displayed data are a last resort. Prefer recognizable formats or combined phrasing such as "12 left in stock" or "3 bedrooms".
- When labels are necessary, make the label secondary unless the user is scanning for labels, such as in technical specs.
- Semantic markup does not dictate visual size. Style headings according to hierarchy, not tag name.
- Heavy icons should usually be lower contrast than adjacent text so they do not steal attention.
- Links inside dense UI do not all need bright color. Use weight, darker text, or hover treatment when the link is not the main path.

## Typography

- Use the project's type system first.
- If there is no type system, choose a deliberate, high-quality UI face with multiple weights. Do not default to Inter, Roboto, Arial, Segoe UI, Trebuchet MS, or a safe stack just because it is convenient.
- Use a restrained type scale, for example `12, 14, 16, 20, 24, 32, 40, 56`.
- Body text is usually 14-16px for app UI and 16-18px for reading-heavy pages.
- Keep paragraphs around 45-75 characters per line.
- Use taller line-height for small text and long lines; use tighter line-height for large headings.
- Left-align long text. Center only short, independent text blocks.
- Right-align numeric table columns so values compare cleanly.
- Baseline-align mixed text sizes when they sit on the same row.
- Keep letter spacing at `0` by default. Add slight positive spacing only for rare all-caps labels when legibility needs it.
- Do not use tiny uppercase eyebrow labels as a default section pattern.

## Color

- Use existing project colors first.
- If no palette exists, define semantic tokens before styling: background, foreground, card, popover, primary, secondary, muted, accent, destructive, border, input, ring, radius, and matching foreground tokens.
- Prefer calm neutral bases with one restrained primary token. Avoid default blue as the first instinct unless the product already owns blue.
- Avoid one-note palettes: all purple, all beige, all dark slate, all blue-black, all brown/orange, or all neon.
- Do not rely on five random hex codes. UI needs semantic colors for text, backgrounds, borders, controls, focus, hover, active, disabled, and invalid states.
- Prefer OKLCH/HSL-style thinking for shade systems: hue, saturation/chroma, lightness, and perceived brightness.
- Do not create shades with ad hoc lighten/darken functions that produce dozens of near-identical colors.
- Greys can be warm or cool, but keep the temperature consistent across the palette.
- Do not use gray text on saturated or colored backgrounds. Pick a foreground color related to the background, then adjust saturation and lightness.
- For colored backgrounds that overpower the page, flip the contrast: use dark colored text on a light tint instead of white text on a loud fill.
- Do not rely on color alone. Pair status with text, icon, shape, position, or contrast.
- Meet accessible contrast. Normal text needs strong contrast; large text can tolerate slightly less, but never guess when the color is risky.

Fallback seed direction when no project colors exist: use a neutral/stone/zinc app background, a white or near-white card surface, near-black foreground, muted grey text, low-contrast borders, a black/near-black or brand-informed primary, and one destructive token. Add chart/sidebar tokens only when those surfaces actually exist.

## Components

- Buttons: use consistent variants: default/primary fill, secondary quiet fill, outline, ghost, destructive, and link. Radius follows the token. No pill overload. No gradients by default.
- Inputs: clear labels above fields, solid border, simple focus-visible ring, clear description/error text, `aria-invalid` or equivalent invalid state. No floating labels, morphing shapes, or animated underlines by default.
- Forms: use field groups with label, control, description, and message slots. Avoid equal spacing between label-control and control-next-label.
- Editable billing, payment, account, and destructive-flow forms must include at least one visible validation/error path, not only disabled buttons or native `required` attributes.
- Tables: use table anatomy: caption when useful, header, body, rows, cells, optional footer. Left-align text, right-align numbers, subtle row hover, functional sorting/filtering only. Do not badge every cell.
- Tabs: use list/trigger/content anatomy with underline, border, or quiet active background. No sliding pill animation by default.
- Badges: small, functional, and sparse. Radius 6-8px. No glow.
- Dialogs: use a normal dialog for forms/detail and an alert dialog for destructive confirmation. Centered, direct, with obvious close/cancel/confirm. Use stronger elevation because the dialog must own focus.
- Dropdowns/menus/popovers: simple list or structured menu with clear selected state. Use sections only if they improve scanning.
- Toolbars: 48-56px high, compact, icon-first where icons are familiar, labels where clarity needs them.
- Icons: 16-20px in normal UI. Keep them consistent, monochrome or quietly colored, and near their intended size.
- Cards: simple containers with subtle border or background. Use radius 6-8px. No dramatic shadows. No cards inside cards.
- Resizable panes, collapsible sidebars, command palettes, empty states, skeletons, and toasts are normal product primitives. Include them when the workflow naturally needs them; do not fake their behavior.

## Depth, Radius, Borders

- Use fewer borders. Separate groups with spacing, background changes, or subtle elevation before adding lines everywhere.
- When using borders, keep them 1px and low contrast unless stronger separation is truly needed.
- Shadows express elevation or interaction, not taste. Use a small shadow for raised controls, a medium shadow for dropdowns/popovers, and a larger shadow for modals.
- A good shadow system has a few fixed levels, not one-off dramatic values.
- Light comes from above: raised elements can have a slightly lighter top edge and a small shadow below; inset elements can have a subtle darker top and lighter bottom.
- Flat designs still need depth. Use tonal changes, layering, and short solid shadows when full shadows are too decorative.
- Radius communicates personality. Keep it consistent. Use 6-8px for most UI, 10-12px only for large surfaces or media when the system supports it.
- Do not repeat the same rounded rectangle treatment across sidebar, cards, buttons, badges, panels, and callouts.

## Imagery And Media

- Websites, landing pages, venues, brands, lifestyle products, games, and visual demos need real visual assets. Decorative texture is not enough.
- Do not design around placeholder images. Choose or generate assets that can survive final implementation.
- Prefer in-situ product, place, person, workflow, gameplay, or object imagery over abstract gradients and fake 3D decoration.
- Avoid images with embedded signage, logos, or text that fights the UI.
- Crop media intentionally. The image should have a stable tonal area when text sits over it.
- If text over an image is hard to read, fix the image: crop, lower contrast, add overlay, colorize, or add a subtle text shadow.
- Do not scale detailed app screenshots down until text becomes unreadable. Use partial screenshots, smaller source layouts, or simplified drawings.
- Do not scale 16-24px icons into giant feature art. Place small icons in a larger shape if needed.
- For user-uploaded media, enforce aspect ratio, object-fit, cropping, and subtle containment so random images cannot break the layout.

## Motion

- Default product motion is quiet: 100-200ms, simple ease, color/opacity/shadow/position only when it clarifies state.
- Visually led pages can use two or three intentional motions: entrance, scroll/depth, and hover/reveal.
- Motion must clarify hierarchy, affordance, or atmosphere. Remove ornamental motion.
- Avoid bouncy transforms, hover shifts that move layout, and animation added only to look expensive.
- Respect reduced-motion preferences.

## Empty, Loading, And Error States

- Empty states are first-use design, not leftovers. Hide filters, tabs, and controls that cannot do anything yet.
- Empty states should name what is empty, explain the next action, and make the primary action obvious.
- Loading states should preserve layout dimensions where possible.
- Error states should say what happened, what can be done, and where the user can recover.
- Disabled states need enough contrast to remain legible.

## Hard Bans

- No generic SaaS card grid as the first impression.
- No dashboard hero sections unless explicitly requested.
- No floating glassmorphism shells, frosted panels, blur haze, glow blobs, gradient orbs, conic-gradient donuts, or decorative sidebar blobs.
- No oversized radii in the 20-32px range across routine UI.
- No pill overload.
- No soft corporate gradients used to fake taste.
- No generic dark blue-black dashboard with cyan accents as the default.
- No serif headline plus default sans body as a shortcut to "premium".
- No tiny uppercase eyebrow labels, decorative `<small>` headers, or rounded `span` labels as a default composition device.
- No section notes explaining what the UI does unless they are genuinely useful product copy.
- No fake charts, fake percentages, fake activity feeds, fake quotas, fake progress bars, or fake "live" badges.
- No nav badges, status dots, trend colors, or tag soup unless the data and behavior are real.
- No card-like sidebar/nav rows with full borders, rounded boxes, or thick active stripes for routine navigation.
- No component styling that only copies rounded boxes and borders while skipping semantic tokens, accessible states, and component anatomy.
- No custom dropdowns, dialogs, tabs, comboboxes, sidebars, or resizable panels that lack keyboard behavior, focus management, and real state.
- No ornamental labels like "live pulse", "control room", "operator checklist", "night shift", or similar invented product voice unless the user asked for that voice.
- No overpadded dead space just to look expensive.
- No mixed alignment that creates accidental empty zones.
- No mobile layout that simply stacks everything into one long undifferentiated column.
- No footer meta lines like "single-file HTML", "dark mode", or implementation notes in the UI.

## Verification

Before finishing frontend work:

- Run the app or open the page.
- Inspect desktop and mobile viewports.
- Confirm the first screen shows the real product, content, or workflow rather than a template.
- Check that a user can understand the screen by scanning headings, labels, values, and actions.
- Confirm one clear primary action or focal point.
- Check text wrapping, clipping, overlap, tap targets, hover/focus/active states, and reduced-motion behavior.
- Check empty, loading, error, disabled, and long-content states.
- Confirm images, canvases, icons, and external assets actually render.
- Remove any card, border, badge, icon, chart, animation, or copy that is not earning its place.
