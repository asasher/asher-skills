# capture-to-inbox

Project-bound capture queue setup and draining for an Inbox-based workspace.

The published source ships a Node API template and stdlib Python setup/drain scripts. `setup` materializes
editable API source under the consumer's `control-plane/` instance, deploys it through a provider binding,
and uses the separately installed Shortcuts Playground plugin to generate and sign the Apple Shortcut.

No tokens, queue data, consumer URLs, deployment IDs, generated Shortcut XML, signed Shortcuts, or
`node_modules` belong in this skill source.
