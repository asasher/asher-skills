# Deployment binding

The bundled API is provider-neutral source. The consumer's `deployment.json` initially binds it to Railway.

1. Materialize first. Never deploy from the installed package mount.
2. Verify `railway whoami`; select or create the intended project, production environment, and dedicated
   `runway-api` service only with the user's authorization.
3. Attach persistent storage at `/data`; set `QUEUE_DIR=/data/runway-queue`, independent freshly generated
   `RUNWAY_PRODUCER_TOKEN` and `RUNWAY_DRAIN_TOKEN`, and bounded `RECEIPT_RETENTION_DAYS` as provider secrets.
   Keep the service at one replica because the file-backed queue's mutex is process-local. Put matching tokens
   in the consumer's ignored mode-0600 `.env` without printing them.
4. Deploy the materialized `until-zero/api/`, wait for deployment completion, and resolve HTTPS.
5. Verify health reports both auth roles configured; unauthenticated calls fail; producer can append but not
   lease; drain can lease but not append; a lease/ack smoke item is removed exactly once.
6. Record only provider, URL, project, environment, service, and volume identities in `deployment.json`. After
   verification, set `verified_origin` to the exact HTTPS origin and `verification_status` to `verified`; bind
   that same origin privately as `RUNWAY_API_ORIGIN` beside `RUNWAY_DRAIN_TOKEN` in `.env`. Refresh refuses any
   mismatch, arbitrary token name/path, embedded URL credentials, or unverified non-loopback origin.

If CLI/auth is absent, stop before provider mutation and give exact missing steps. Record the pending gate and
resume with the same verification. On rerun, reuse healthy resources and require confirmation before changing
any bound identity.
