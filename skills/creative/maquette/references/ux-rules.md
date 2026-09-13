# UX rules (Asher's baseline)

<!-- Adapted from the local skills/bare-minimum-design policy; reconcile deliberately. -->

## Copy

- Write copy around the end user’s task and decisions.
- Integrate supporting information into the microcopy sentence. Bad: "Update supplier price info from this RFQ (all valid quote rows)". Good: "Update supplier price from this RFQ for all valid quote rows".
- Use specific, active-voice labels.

## Interaction

- Numeric inputs: `type="text"` with numeric validation and the right `inputmode`.
- **Co-locate actions and their consequences.** The user must see the effect of a press without scrolling: add-row at the bottom of a table (or insert at top if the button is at top); a filter next to the list it filters.

## Planning checklist (apply per screen during journey design)

1. List the visual hierarchy for each component.
2. List the explicitness spectrum for each action — which are overt (global share button) and which appear only when needed (hover-to-copy on a field).
3. List progressive disclosure points: at each journey step, what does the user need to know, and how is just that much presented?
4. List every action and how its consequence will be co-located and presented.

## Notifications are alarms

If the maquette has any interruption surface (toasts, badges, notification centers):

- Interrupt only when timely user action is required; FYI signals (status, reports, marketing) go to quiet surfaces — feeds, digests, status panels.
- Give human messages, urgent actions, and FYIs distinct visual treatments; differentiate sounds where used.
- Collapse repeats, expire stale items, and tie persistent badge counts to an obvious response.
- Reserve urgency signals for the receiver’s time-sensitive needs.
- Demo relevance: the fixture notification feed must itself obey these rules — a believable product does not show 47 unread red badges.
