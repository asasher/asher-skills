# Demo hardening

The maquette is presented under pressure: unfamiliar wifi, a projector, a skeptical room. This phase turns
a working prototype into a performable one.

## DEMO.md — the script

Write `DEMO.md` alongside the code:

- **Beats:** each deal-closing moment from `BRIEF.md` — the setup line to say, the exact click path (with
  deep-link URL), what the audience should see, and the fallback if it stumbles.
- **Full walkthrough:** the ordered route through every journey, persona switches marked.
- **Prep checklist:** commands to run, tabs to open, reset to pristine, agent client connected (if using
  the MCP beat), notifications/Do-Not-Disturb on the presenting machine.

## Demo controls

- **Persona switcher:** `?persona=dispatcher` (URL-backed) plus a switcher in the demo panel. Switching
  persona changes current user, permissions shown, and assigned records — no fake login screen unless the
  login *is* a demo beat.
- **Hidden demo panel** on a keyboard shortcut (e.g. `Ctrl+.` — avoid browser-reserved combos): reset to
  pristine, switch persona, trigger scripted events, time-jump (if built). Invisible otherwise; it must
  never appear in a buyer's hands.
- **Scripted events:** each beat that needs the world to act ("an order just came in") is a demo-panel
  button that injects a fixture through the normal api seam — so the toast, badge, and list update exactly
  as the real product would.
- **The agent beat:** rehearse the MCP moment end to end (agent connected, bus relaying, toasts showing
  the agent's actions). Have the exact prompt to type written in `DEMO.md`. Fallback: the Integrations
  screen + a canned transcript.
- **Reset discipline:** reset to pristine before every meeting; bump the localStorage version key on every
  redeploy so no stale state ever loads.

## Hardening checklist

- **Zero external requests after load:** fonts via `next/font`, no CDN scripts, no remote images
  (generate/inline assets). Load the app, kill the network, click through everything.
- Console clean: no hydration warnings, no red errors — buyers' engineers open devtools.
- Projector realities: default to the brief's chosen theme, check contrast and font sizes at 1366×768 and
  1920×1080, and check the zoomed-in screen-share case.
- Nothing depends on wall-clock luck: relative fixture dates verified fresh, no "today at 00:03" weirdness.
- Runs from a cold `npm run dev` in under a minute; `DEMO.md` prep list tested on the actual presenting
  laptop.

## Dead-click sweep (the gate)

Enumerate every route from the screen inventory and every rendered control on each. Drive the app —
browser automation if the environment has it, manually otherwise — and record: every control either
performs its action or navigates; no dead ends, no `#`, no "coming soon". **Any dead click fails the
phase:** wire it or delete it. Sweep again after any post-sweep edits.
