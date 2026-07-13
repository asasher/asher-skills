# Setup

Reconcile only `docs/agents/environment.md` § **Presenting to the human**. Preserve every other section and
every deliberate project delta inside this one.

1. Read any existing presentation section and determine the usable channel: local-only, the machine's
   private tailnet surface, or a project-specified equivalent. Local-only is the safe default.
2. Record the surface root, repo-scoped surface directory, URL/path pattern, proxy/publish and teardown
   commands, hub location, keep-awake rule, and the local fallback. Never enable a public tunnel implicitly.
3. Record the bundled detached `serve`, `stop`, `sweep`, and verdict-await commands. The server owns receipt
   of browser events; a watcher only delivers a recorded verdict.
4. Exercise one throwaway serve: verify `/version`, submit or simulate a hash-matching event, stop twice, and
   confirm the registry entry disappears. If a remote channel is unavailable, prove the local fallback and
   record the blocker.

Completion criterion: the section names an effect-verified serve/stop path and an openable fallback, while
the rest of `environment.md` is byte-for-byte unchanged.
