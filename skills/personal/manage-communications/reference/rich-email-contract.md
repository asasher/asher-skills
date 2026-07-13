# Rich email contract

Render one React Email component from each validated comms bag and produce both
`rendered-email.html` and `rendered-email.txt` in its immutable run directory.

- Use table-safe email structure, inline styles, a preheader, one primary heading, and restrained Dunn
  Harland branding.
- Keep the hierarchy readable when images, custom fonts, CSS classes, and dark-mode overrides are removed.
- Project updates lead with the client-safe summary, then status-grouped highlights and next steps.
- Internal digests show delivery, pending work, cash, and growth. They may group delivery and pending work by
  project/client for scanability, with Cash and Growth following the project sections.
- End with visible provenance: “Prepared with AI, reviewed and sent by Dunn Harland.”
- Keep HTML and plain text semantically equivalent. Never place internal evidence IDs or file paths in the
  visible body.

Rendering is complete only after both files exist, contain the subject/audience content, and the HTML has
been visually checked locally. Before any provider write, present every message in scope together in a
browser review surface and wait for explicit approval. Record the approved rendered-content hash in the run
manifest; any visible copy or template change invalidates approval and returns the message to review.
