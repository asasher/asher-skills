# Presenting to the Human

Interactive review — a plan awaiting approval, a prototype awaiting driving — reaches the human through the repo's **presentation surface**, chosen by where the human is, not where the agent runs. The surface contract lives in the Presenting section of `docs/agents/environment.md`, written by `backlog setup`. Evidence is not presented here: it is durable proof and follows `docs/agents/evidence.md` into the repo and the PR.

## Contract

- **One surface, one root.** Everything reviewable lives under a single stable URL root — documents as static paths, live prototypes as port proxies, one grammar. The shipped default is a tailnet surface (`tailscale serve`): private to the human's own devices, persistent config, no public exposure — Funnel stays off. Where the platform's tailscale client cannot serve file paths (the sandboxed macOS app), the document half is a small local static server rooted at a surface directory, proxied once — publishing is symlinking the committed file in.
- **The pause is the notification.** Any step that stops for a human ends its message with the surface URL of the thing to review — the harness's own notification tells the human the thread stopped; the URL in the message is what they tap. Mirror the URL to the issue when the tracker is also a review channel.
- **Publish, don't fork.** A presented document is the committed file, served in place — never a diverging copy.
- **Reap with the worktree.** A worktree's path handlers are removed at its teardown, alongside its stack; an orphaned handler on a tailnet surface is clutter, not exposure — the setup health check also sweeps them.
- **Local fallback.** When no surface is recorded, or the section says local-only, open the rendered file or running app on the machine and say remote review is unavailable — never improvise a public tunnel.
- **The surface is only as awake as the machine.** That is the accepted default — harnesses hold sleep assertions while runs are active, and an awake machine serves. Whether to keep it awake beyond that (long pauses, lid-closed on battery) is the user's setup-time choice, recorded as the environment playbook's keep-awake line.
