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
  stop its review worker first with `review-server.py --stop --state <dir>`, then remove the path handler.
  An orphaned handler on a tailnet surface is clutter, not exposure — a setup health check also sweeps them.
- **The surface is only as awake as the machine.** That is the accepted default — harnesses hold sleep
  assertions while runs are active, and an awake machine serves. Keeping it awake beyond that (long pauses,
  lid-closed on battery) is the user's setup-time choice, recorded as the playbook's keep-awake line.

## Bringing the tailnet up

The tailnet surface presumes the machine's tailscale node is **logged in and connected** — `tailscale serve`
only proxies a path once the node is on the tailnet, so it is a separate concern from *publishing* a path
(`tailscale up` brings the node onto the tailnet; `tailscale serve` mounts the path). When the node is
logged out or stopped, every published URL and the review server's proxy fail with opaque network errors
rather than a clear "tailnet down." So the **serve step owns a connectivity precondition**: before it
publishes an artifact or starts the review server, it confirms the node is up and brings it up only when it
is not.

- **Detect, don't assume.** This applies only when the surface binding is a tailnet — a local-only or custom
  surface skips it entirely. Before publishing, check node state: `tailscale status` exits non-zero and
  prints `Logged out.` / `Tailscale is stopped.` when the node is down. A `tailscale serve` that errors, or a
  freshly published URL that is unreachable, is the same signal caught later. The repo's surface-config
  playbook records the exact check command.
- **Bring it up only as a publish precondition.** Run `tailscale up` only when all three hold: (a) the
  surface is a tailnet, (b) a review is actually being published right now, and (c) the check shows the node
  down or logged out. It is not a warm-up step to run speculatively at the top of a loop.
- **Never toggle a healthy connection.** If the check shows the node already connected (`tailscale status`
  succeeds and lists peers), do nothing — proceed straight to publish. A bare `tailscale up` on a connected
  node is a no-op worth skipping anyway, and one run with flags that differ from the live config can
  silently reconfigure the node; never `tailscale down` then `up` as a "reset." Check first, act only on a
  down node.
- **Interactive auth or a hard failure falls back to local.** `tailscale up` may print an auth URL and wait
  for an interactive login, or fail outright (expired key, SSO required, admin approval). An agent cannot
  complete an interactive login headless and must not loop retrying. Surface the auth URL or the failure to
  the human as the thing that unblocks the review, and **fall back to the local-only review** — open the
  rendered file on the machine and say remote review is unavailable, the same degradation as an unrecorded
  surface. **Never enable Funnel or improvise a public tunnel** to route around a down tailnet.

This is the connectivity companion to *The surface is only as awake as the machine* above: that bullet
covers a sleeping machine, this covers a disconnected node. Both keep the surface honest — a review only
publishes to a URL the human can actually reach.

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
  `registry.json` beside it. Each detached review worker registers on healthy start and removes itself on
  explicit stop or clean exit. Surface-locked atomic updates preserve sibling rows when several workers share
  one hub; the hub itself owns no process or port. The worker also answers `/hub` as a **local fallback** when
  no external static server fronts the surface dir.
- **Dumb, read-only, derived.** Rows show title, kind, scope tag, state, and age, linking to the direct URL
  — nothing more. No hub event log, no approve-from-the-hub (approval binds to a rendered document's hash),
  no history. Nothing reads the hub but the human; registry loss degrades to an empty index while every
  direct URL keeps working. An optional `--surface-label` adds a suffix to the hub heading (e.g. a repo
  name); default none.
- **Swept, not trusted.** A crashed run leaves an orphaned registry entry — clutter, not exposure. A setup
  health check runs `review-server.py --sweep --surface <dir>`, which probes each entry's URL, drops the
  dead, regenerates the index, and prints `{"swept":[…]}`.
