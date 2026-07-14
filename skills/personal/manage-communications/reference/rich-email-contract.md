# Rich email contract

Render one React Email component from each validated comms bag and produce both
`rendered-email.html` and `rendered-email.txt` in its immutable run directory.

- Use table-safe email structure, inline styles, a preheader, one primary heading, and the consumer-owned
  brand system.
- Declare light and dark color-scheme support. Define explicit, readable palettes for the outer canvas,
  message surface, primary and secondary text, dividers, and accents; do not depend on an email client's
  automatic color inversion. Dark mode may use softer contrast when legibility is preserved.
- Use a dark-safe logo asset or an isolated mark with live text; never assume a light-theme wordmark will
  remain visible after forwarding or dark-mode transformation.
- Keep the hierarchy readable when images, custom fonts, CSS classes, and dark-mode overrides are removed.
- Project updates lead with the client-safe summary, then status-grouped highlights and next steps.
- Internal digests show delivery, pending work, cash, and growth. They may group delivery and pending work by
  project/client for scanability, with Cash and Growth following the project sections.
- End with the consumer-configured visible provenance.
- Keep HTML and plain text semantically equivalent. Never place internal evidence IDs or file paths in the
  visible body, and never expose prompts, private instructions, selection rules, or skill terminology.

Rendering is complete only after both files exist, contain the subject/audience content, and the HTML has
been visually checked locally. Before any provider write, present every message in scope together in a
browser review surface with a forced light preview and forced dark preview shown side by side for each
message. Show the proposed recipients in the same review surface, then wait for explicit approval. Record the
approved rendered-content and recipient hashes in the run manifest; any visible copy, template, or proposed
recipient change invalidates approval and returns the message to review unless the user makes that recipient
change directly during the final send. Reconciliation records the actual Sent Items recipients.
