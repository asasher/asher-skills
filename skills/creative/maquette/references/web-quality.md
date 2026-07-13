# Web-quality pass

The browser artifact must survive a buyer exploring outside the rehearsed click path.

## Gates

- Use links for navigation and buttons for actions. Every control has a visible keyboard focus state; icon-only
  controls have accessible names; status updates are announced without stealing focus.
- Labels, input types, autocomplete, validation placement, and error focus make every form usable without
  guesswork. Paste remains enabled.
- The URL preserves shareable navigation state such as the selected record, tab, filter, or page. Refreshing a
  prepared demo URL restores the same screen.
- Dates, numbers, and currency use locale-aware formatting. Time-relative fixture values render deterministically.
- Images reserve dimensions; heavy off-journey work loads lazily; long fixture lists remain responsive.
- Browser console, network panel, dead-link sweep, keyboard traversal, narrow viewport, and refresh-on-each-demo
  URL are clean before handoff.

Prefer explicit variants and small state interfaces over boolean-prop combinations. The handoff should expose
one comprehensible seam per behavior, not a matrix of hidden modes.
