# UX rules (Asher's baseline)

<!-- Adapted from the local skills/bare-minimum-ux policy; reconcile deliberately. -->

## Copy

- **Never surface internal instructions, prompts, implementation details, design constraints, or
  acceptance criteria in user-facing copy.** Only write copy an actual end user should see. In a maquette
  this failure is fatal — one leaked "as per the brief" destroys the illusion.
- No supporting information in brackets in microcopy. Bad: "Update supplier price info from this RFQ (all
  valid quote rows)". Good: "Update supplier price from this RFQ for all valid quote rows".
- Specific, active-voice labels; no generic startup copy.

## Interaction

- Numeric inputs: `type="text"` with numeric validation and the right `inputmode` — not `type="number"`.
- **Co-locate actions and their consequences.** The user must see the effect of a press without scrolling:
  add-row at the bottom of a table (or insert at top if the button is at top); a filter next to the list
  it filters.

## Planning checklist (apply per screen during journey design)

1. List the visual hierarchy for each component.
2. List the explicitness spectrum for each action — which are overt (global share button) and which appear
   only when needed (hover-to-copy on a field).
3. List progressive disclosure points: at each journey step, what does the user need to know, and how is
   just that much presented?
4. List every action and how its consequence will be co-located and presented.

## Notifications are alarms

If the maquette has any interruption surface (toasts, badges, notification centers):

- Interrupt only when timely user action is required; FYI signals (status, reports, marketing) go to quiet
  surfaces — feeds, digests, status panels.
- Human messages, urgent actions, and FYIs never share one default visual treatment or sound.
- No standing alarms: collapse repeats, expire stale items, no persistent badge counts without an obvious
  response.
- Never borrow urgency signals for engagement goals.
- Demo relevance: the fixture notification feed must itself obey these rules — a believable product does
  not show 47 unread red badges.
