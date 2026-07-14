# Capture refresh

The dedicated Runway API accepts only the version-1 `ios-wallet` transaction envelope. Its producer token can
append only. Its drain token can lease, release, and acknowledge only. Neither credential may substitute for
the other.

Run:

```bash
python3 <skill>/scripts/drain_capture_queue.py --project <consumer-root>
```

The refresh leases the oldest page, normalizes each capture, maps last digits then aliases then exact account
name, commits mapped rows as uncleared transactions or unmapped rows as pending, records an audit event, and
only then acknowledges with the local result hash. Local failure leaves the remote item unacknowledged for
lease expiry/retry. A recovery journal binds state and audit writes, while Queue IDs make local retries
idempotent. The producer also deduplicates retries by the required stable transaction `external_id`, including
bounded acknowledgement receipts.

Use `--dry-run` to lease then release without local mutation. A partial refresh returns nonzero and names only
capture IDs, never tokens or raw sensitive payloads.

The API template is consumer-owned after setup. Its public seam is `/healthz`, `POST /v1/captures`,
`POST /v1/captures/lease`, and per-ID `ack`/`release`. It stores queue files privately and retains bounded
acknowledgement receipts. Never broaden it into the general Inbox queue or add full financial mutation APIs.
Run only one API replica unless its mutex and storage are replaced with a multi-process transactional store.

## Assignment

An unmapped capture stays in `pending_captures.json` and affects no projection. Resolve it with:

```bash
python3 <skill>/scripts/until_zero.py assign --project <root> --queue-id <id> --account <id> --actor <actor>
```

Completion means one uncleared transaction exists, the pending row is gone, and the audit row names the Queue ID.
