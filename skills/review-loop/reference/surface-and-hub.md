# The presentation surface and the hub

Where a reviewed artifact reaches the human, and the repo-scoped inbox that lists everything awaiting them.
The surface is chosen by where the human is, not where the agent runs. Its repo-specific config — the root
URL, the surface directory, the publish/proxy commands, the keep-awake choice — lives in a `docs/agents/`
surface-config playbook (on this repo, `environment.md` § Presenting to the human). This doc is the
artifact-agnostic contract those settings implement.

## The surface contract

- **One surface, one root.** Everything reviewable lives under a single stable URL root — documents as
  static paths, live prototypes as port proxies, one grammar. The shipped default is a **tailnet** surface
  (`tailscale serve`): private to the human's own devices, persistent config, no public exposure — **Funnel
  stays off.** Where the platform's tailscale client cannot serve file paths (the sandboxed macOS app), the
  document half is a small local static server rooted at the surface directory, proxied once.
- **Publish, don't fork.** A presented artifact is the committed file, served in place — never a diverging
  copy. The review server serves the file on disk and injects the chrome at serve time, so the committed
  file stays byte-pure while the human still gets the review UI.
- **The pause is the notification.** Any step that stops for a human ends its message with **two links,
  always both**: the artifact's surface URL first, the hub URL second — so the review is findable even
  without the message. The harness's own notification says the thread stopped; the URLs are what the human
  taps.
- **Local fallback.** When **no surface is recorded**, or the playbook says local-only, open the rendered
  file or running app on the machine and say remote review is unavailable — **never improvise a public
  tunnel.** The server's own `/hub` endpoint is the local fallback for the hub in this mode.
- **Reap with the worktree.** A worktree's path handlers are removed at its teardown, alongside its stack;
  an orphaned handler on a tailnet surface is clutter, not exposure — a setup health check also sweeps them
  (see Sweep below).
- **The surface is only as awake as the machine.** That is the accepted default — harnesses hold sleep
  assertions while runs are active, and an awake machine serves. Keeping it awake beyond that (long pauses,
  lid-closed on battery) is the user's setup-time choice, recorded as the playbook's keep-awake line.

## Path-prefix mounts

The real deployment serves the artifact under a tailnet path prefix (e.g. `/asher-skills/2/review/`), not at
the domain root. The chrome therefore builds every client→server call **mount-relative** — it derives a base
from the served page's path rather than posting to root-absolute `/event` or `/version` — so requests
resolve whether the page is served at `/` (loopback) or under a prefix. The server matches its endpoints
(`/`, `/version`, `/event`, `/hub`) **suffix-tolerantly**, so it works whether the proxy strips the prefix
before forwarding (the backend sees `/event`) or preserves it (the backend sees `/asher-skills/2/review/event`).

## The hub

The surface root serves a repo-scoped review inbox — one bookmarkable URL listing everything awaiting the
human:

- **A static file, not a daemon.** The hub is `index.html` at the surface directory root, regenerated from
  `registry.json` beside it. Each review server registers itself on start and removes itself on clean exit
  (approval, teardown, idle) — atomic writes, no lifecycle owner, no new port. Whatever already serves the
  surface serves the hub. The review server also answers `/hub` itself as a **local fallback** when no
  external static server fronts the surface dir.
- **Dumb, read-only, derived.** Rows show title, kind, scope tag, state, and age, linking to the direct URL
  — nothing more. No hub event log, no approve-from-the-hub (approval binds to a rendered document's hash),
  no history. Nothing reads the hub but the human; registry loss degrades to an empty index while every
  direct URL keeps working. An optional `--surface-label` adds a suffix to the hub heading (e.g. a repo
  name); default none.
- **Swept, not trusted.** A crashed run leaves an orphaned registry entry — clutter, not exposure. A setup
  health check runs `review-server.py --sweep --surface <dir>`, which probes each entry's URL, drops the
  dead, regenerates the index, and prints `{"swept":[…]}`.
