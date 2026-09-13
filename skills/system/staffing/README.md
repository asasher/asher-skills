# Staffing

Maps each task type to four separate dispatch fields: model, effort, route, and execution method. The caller tries the selected route at runtime, reports a route failure, and stops. Behavioral verification has an explicit row, while respecting user overrides.

## Install

`npx skills add github:asasher/asher-skills --skill staffing`.

## Credits

- **Relationship:** extracted from this repository's `backlog` skill.
- **Source:** [`6412325`](https://github.com/asasher/asher-skills/commit/6412325).
- **Authority moved:** roster, role, routing, and fallback policy moved here.
- **Local changes:** slimmed to a roster table; the caller tries the route at runtime and stops on failure. The September 3, 2026 audit's comparison with [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) informed the behavioral-verification row and a then-current preference for a different model family. The current roster makes model diversity optional and is maintained here, with no runtime dependency on that source.
