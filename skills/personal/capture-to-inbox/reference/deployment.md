# Deployment Binding

The API is provider-neutral source. The consumer's `deployment.json` binds it to one provider; Railway is the
initial binding.

## Railway

1. Verify `railway whoami` and select or create the intended project, production environment, and service.
2. Attach a persistent volume at `/data`; set `QUEUE_DIR=/data/queue` and a freshly generated
   `CAPTURE_TOKEN` as provider secrets. Put the same token in the consumer root `.env`, which must be ignored
   by Git and mode `0600`. Never print it or write it into tracked project files.
3. From the materialized `control-plane/capture-to-inbox/api/`, deploy with `railway up` against the selected
   project/environment/service. Wait for the deployment rather than treating upload acceptance as success.
4. Provision or resolve the HTTPS domain, then verify `/healthz` reports `ok: true` and
   `auth_configured: true`. Verify an unauthenticated queue request returns `401`.
5. Write only non-secret facts to `deployment.json`: provider, API URL, and the Railway project,
   environment, service, and volume identities.

If a provider action fails, leave the deployment status pending and report the failed effect. Never deploy
from the installed skill mount; the materialized API is the consumer's deployable source.

On rerun, read the binding first. Reuse healthy resources, repair missing effects, and require confirmation
before changing project, service, domain, or volume identity.
