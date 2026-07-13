# Issue #57 — detached review server boundary proof

Date: 2026-07-13

One tool invocation launched the public review server and exited after the authenticated health check. It
returned worker PID `92588`, instance `0fbb3d6e01a6ee7b44b9510b`, and registry entry
`57-detached-boundary-0fbb3d6e`.

A later, separate tool invocation used only the persisted `server.json` state to:

1. GET the authenticated `/version` endpoint;
2. POST a hash-matching approval;
3. read the durable `feedback_submitted` event (`doc_hash: 3730fe00dbf8d03d`);
4. stop the verified worker; and
5. confirm the shared registry contained zero entries.

```text
POST result: evt_20260713_3e357d71
event verdict: approve
stop: {"stopped": true, "pid": 92588,
       "instance_id": "0fbb3d6e01a6ee7b44b9510b"}
registry entries after stop: 0
```

The automated lifecycle suite separately covers watcher/no-watcher operation, two concurrent servers,
idempotent stop, and the same-artifact old-instance cleanup race.
