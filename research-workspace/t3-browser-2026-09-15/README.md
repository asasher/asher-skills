# T3 Code browser exploration

Tested on 2026-09-15 with T3 Code (Alpha) 0.0.40 on the Mac and T3 0.0.40 on CXbox.
The desktop build reports commit `09e8de9c655a` and Chromium 150.0.7871.224.

T3's browser works for interactive verification without writing a Playwright script.
It preserves login state, exposes useful failure diagnostics, and produces screenshots and recordings.
Use it for exploratory checks and reviewing an agent's changes. Keep executable tests for repeatable regression coverage.

This exploration demonstrated local browser control and verification of an app hosted on CXbox through SSH.
It did not run an agent in another chat or on CXbox. Those checks require additional agent sessions, for which authorization was requested but had not arrived.

## Findings and confidence

| Question | Finding | Evidence level |
| --- | --- | --- |
| Can it hold a login session? | Yes. Synthetic HttpOnly session and persistent cookies survived navigation and opening another tab. | Live, local and CXbox-hosted app. |
| Does storage survive navigation? | localStorage and sessionStorage survived same-tab navigation. A new tab shared localStorage and cookies but had empty sessionStorage. | Live, local. |
| Does login survive restarting T3? | Persistent profiles use Electron disk partitions; the persistent probe cookie appeared in the partition's cookie database. | Implementation and disk inspection. App restart was not tested. Session cookies have a different lifetime. |
| Is the session different per chat? | Tabs are keyed by thread and tab ID. Cookies and origin storage are scoped by environment and browser profile, so chats using the same profile are expected to share logins. | Implementation. Two tabs in this chat shared state; two separate chats were not tested. |
| Can local and remote environments have different sessions? | Yes by implementation: their environment IDs produce different browser partitions, even under the Default profile. | Implementation. The tunnel experiment used the local environment's browser partition. |
| Can it verify changes without a Playwright script? | Yes. Browser tools found a failed save, exposed its HTTP 500 and console error, then verified the successful result after changing the server behavior. | Live, local and CXbox-hosted app. |
| Can a CXbox agent drive it? | The broker can route requests to a connected desktop host for that environment. | Implementation only; remote-agent control remains unverified. |
| Does the CXbox web UI supply browser automation by itself? | The web client does not register an automation host without the desktop bridge. A connected desktop client can supply the host separately. | Implementation. The unauthenticated web pairing page loaded, but authenticated web-only operation was not tested. |
| Is it faster? | The small warm-browser benchmark favored standalone Playwright for execution time. T3 avoids creating a script and launching a separate browser for exploratory work. | Five measured runs per path; no agent-productivity benchmark. |

## What ran

The disposable app has a Name input, a synthetic sign-in button, and a Save change button.
Sign-in sets two HttpOnly cookies, localStorage, and sessionStorage. The server returns only probe cookie names and values.
The save handler waits 200 ms, then returns HTTP 500 or 200 according to a local file.
This is a controlled cookie test, not a production OAuth or SSO test.

The local app listened on `127.0.0.1:48765` and was reached through T3's environment-port target.
The second app ran as the regular user on CXbox, also on `127.0.0.1:48765`.
An SSH tunnel exposed that second app on the Mac at `127.0.0.1:48766`.
The remote page identified its server as `cx-box`, and the server behavior was changed over SSH.

The browser interactions used `preview_open`, `preview_navigate`, `preview_type`, `preview_click`, and `preview_wait_for`.
Read-only page evaluations checked the probe storage values and server-observed cookies.
JavaScript could not read the HttpOnly cookies; the server received them.
The error-to-success check used real clicks and HTTP responses, without changing the result text through evaluation.

Screenshots, dark appearance, a 390 × 844 viewport, and MP4 recording all worked.
The phone preset retained a desktop user agent and reported zero touch points. It checks layout breakpoints, not mobile-browser compatibility.
Automation worked with `visible: false`. Even an explicit `open: true` reported false in this run, so showing the preview to the human was not verified.

## Session model

There are three separate identities:

- The agent's current tab assignment is scoped by environment and provider session.
- T3's tab records are keyed by thread ID and tab ID.
- Electron's cookie and storage partition is scoped by environment and browser profile.

The Default profile hashes the environment ID. Named profiles hash the environment/profile pair in a separate namespace.
Incognito uses a non-persistent partition. This does not establish that every Incognito tab gets its own isolated login.
The agent tools exposed in this session have no profile-selection parameter; newly created tabs use the configured default profile.

Different chats therefore should not be treated as separate test accounts.
Choose separate profiles when two flows need different users. A logout in one tab can affect other tabs sharing that profile and cookie scope.
Cookies also ignore port numbers: two localhost apps can share cookies even though their localStorage origins differ.

The probe's persistent cookie was present on disk in the partition derived from the actual local environment ID.
No application restart, profile switch, browser import, IndexedDB, service worker, or user-assisted SSO test was performed.

## CXbox constraint

The browser engine lives in the desktop client. The agent and application server can live on CXbox.
The server's automation broker routes requests to a desktop client connected to the appropriate environment.
The desktop client must remain connected for this route to work; a headless T3 server does not launch its own browser here.

An environment-port target currently substitutes the environment server's private-network hostname and the requested port.
It does not create an SSH tunnel or proxy a loopback-only dev server through T3.
Connecting directly to the CXbox tailnet IP at port 48765 failed because the app listened only on loopback.
The explicit SSH tunnel worked.

For remote work, provide a URL reachable from the Mac, use a tunnel, or bind the dev server appropriately on the private network.
The implementation rejects environment-port resolution for server addresses it does not recognize as private-network reachable, referring to a planned authenticated preview gateway.
Do not assume a remote `localhost` development URL will work automatically.

The Mac and CXbox served byte-identical browser URL-resolution code, SHA-256 `1e90acfd05955220339410e6f4f7d4762e525ab280cefc9d5853f847ba2ee2df`.

## Timing comparison

Each trial clicked Save change and waited for Saved successfully. Both paths included the server's 200 ms delay.
T3 used two browser tool calls per trial. The baseline used Playwright 1.60.0 with a separate headless Chrome 153.0.8010.36 browser.
Both browsers ran on the Mac; the remote measurements used the same SSH tunnel.

| Warm-browser trial | T3 median | Standalone Playwright median | T3 range | Playwright range |
| --- | ---: | ---: | ---: | ---: |
| Local app | 542 ms | 250 ms | 538–573 ms | 246–250 ms |
| CXbox app through SSH | 753 ms | 433 ms | 694–777 ms | 414–484 ms |

The baseline browser took 1,271 ms to launch. This cost is excluded from the warm trials.
T3's initial local navigation took 115 ms with its browser already available.
These numbers are not a controlled browser-engine comparison: Chrome versions, headed state, and tool transports differed.
Some baseline and T3 work overlapped. There were only five trials, with no statistical claim.
The timing excludes model thinking, tool-call planning, writing the script, CI setup, and human review.

The script was written only to establish a comparison; it was not required for the exploratory checks.
T3 did not demonstrate better execution speed. Its likely advantage is lower setup effort for an unfamiliar UI or an already-authenticated session.
Whether that reduces total agent time or improves bug detection needs a task-level comparison on real changes.

## Limits that affect verification

- Snapshots include page text, interactive elements, an accessibility tree, error diagnostics, and an action timeline. This tiny page produced about 14 KB of text. Use targeted evaluations and waits between snapshots when that is enough.
- `includeImage: false` omits the image output. The implementation still builds the screenshot before omitting it, so this is mainly an output-size saving.
- Network diagnostics contain HTTP errors and failed loads, not a complete request log. A successful save did not add a 200 entry.
- Old errors survived navigation and successful retesting. Check timestamps and assert the current outcome. An empty error list is not the only success criterion.
- One remote-app tab contained Electron preload errors as well as the intentional application error. Browser-level noise should not automatically become an application defect.
- Evaluation is documented as limited to 64 KB. A 70,000-character result failed, but the surfaced error was generic.
- There are no dedicated tools here for file upload, request interception, HAR export, hover, or drag-and-drop. Some missing interactions may be possible through evaluation or the UI, but they were not tested.
- A recorded clip or screenshot is evidence of this run. It does not become an executable regression check automatically.
- Screenshots preserved transparency when the page had no explicit background. Black text became unreadable against a black image viewer. The original CXbox screenshot is retained alongside a copy composited onto white for reading.

## Recommended use

Use T3's browser for an agent's first verification pass when a connected desktop host is available.
Start the app, open its reachable URL, inspect the page, perform the real interaction, and assert an observable result.
Use screenshots for layout review and recordings when the sequence matters.
For a fix, demonstrate the failure before changing the app and rerun the same interaction afterward.

Keep a durable test when the behavior is important enough to rerun in CI, when many cases must be covered, or when the test needs capabilities the browser tools lack.
Do not require a new standalone Playwright script merely to inspect every small UI change.
No lifecycle skills were changed by this exploration.

The remaining experiments are two-chat login sharing, remote-agent calls through the actual desktop connection, profile separation, and persistence after restarting T3.
The two-chat and remote-agent runs were left pending the requested authorization for additional agents.

The test servers and SSH tunnel were stopped after the exploration. Probe cookies, localStorage, and sessionStorage were cleared from the test tabs.

## Evidence and reproduction

- [Measured results and selected diagnostics](evidence/results.json)
- [Local mobile-layout screenshot](evidence/local-mobile.png)
- [CXbox app after the fix, composited onto white](evidence/cxbox-over-ssh-on-white.png)
- [Original CXbox screenshot with transparency](evidence/cxbox-over-ssh.png)
- [Local retest recording](evidence/local-retest.mp4)
- [Disposable HTTP app](server.py)
- [Standalone comparison](bench.mjs)

Run the app from a disposable directory containing `server.py` and a `save-mode` file containing `broken` or `fixed`.
Start it with `python3 server.py`; `PROBE_PORT` defaults to 48765.
The baseline expects the local app on port 48765 and the tunneled remote app on port 48766, both in fixed mode.
Install its dependency in that disposable directory with `bun add playwright-core@1.60.0`, then run `bun bench.mjs` with Google Chrome installed.

Implementation evidence came from the installed T3 Code build, not from an assumed latest upstream version:

- Desktop bundle `apps/desktop/dist-electron/main.cjs`: `BrowserSession.getPartition`, `resolvePartitionScope`, and browser diagnostics handling.
- Server bundle `apps/server/dist/bin.mjs`: `PreviewManager`, `PreviewAutomationBroker`, and preview MCP handlers.
- Client assets `main-DEoVnAlc.js` and `browserHistoryStore-D2pfq424.js`: desktop-host registration, default profile selection, and environment-port resolution.

T3 Code and Playwright are the external implementations being evaluated. Their source bundles are not copied into this repository.
