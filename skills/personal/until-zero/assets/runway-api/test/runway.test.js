import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { afterEach, beforeEach, describe, it } from "node:test";
import { createRunwayServer } from "../src/app.js";

let queueDir;
let server;
let baseUrl;

beforeEach(async () => {
  queueDir = await fs.mkdtemp(path.join(os.tmpdir(), "until-zero-api-"));
  server = createRunwayServer({ queueDir, producerToken: "producer", drainToken: "drain", logger: { error() {} } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

afterEach(async () => {
  await new Promise((resolve) => server.close(resolve));
  await fs.rm(queueDir, { recursive: true, force: true });
});

const auth = (token) => ({ authorization: `Bearer ${token}` });
const envelope = (description = "Coffee") => ({
  version: 1,
  source: "ios-wallet",
  captured_at: "2026-07-14T08:00:00Z",
  transaction: { amount_minor: "-2500", currency: "AED", description, date_iso: "2026-07-14", external_id: description },
});

async function capture(description = "Coffee") {
  const response = await fetch(`${baseUrl}/v1/captures`, {
    method: "POST",
    headers: { ...auth("producer"), "content-type": "application/json" },
    body: JSON.stringify(envelope(description)),
  });
  assert.equal(response.status, 201);
  return response.json();
}

async function lease(worker = "test", limit = 25) {
  const response = await fetch(`${baseUrl}/v1/captures/lease`, {
    method: "POST",
    headers: { ...auth("drain"), "content-type": "application/json" },
    body: JSON.stringify({ worker_id: worker, limit }),
  });
  assert.equal(response.status, 200);
  return response.json();
}

describe("Until Zero Runway API", () => {
  it("reports auth readiness without paths or secrets", async () => {
    const response = await fetch(`${baseUrl}/healthz`);
    const body = await response.json();
    assert.deepEqual(body, { name: "until-zero-runway-api", ok: true, producer_auth_configured: true, drain_auth_configured: true, auth_roles_separated: true });
    assert.equal(JSON.stringify(body).includes(queueDir), false);
    assert.equal(JSON.stringify(body).includes("producer"), true); // field name only
    assert.equal(JSON.stringify(body).includes('"drain"'), false);
  });

  it("enforces separate producer and drain authority", async () => {
    const badAppend = await fetch(`${baseUrl}/v1/captures`, { method: "POST", headers: { ...auth("drain"), "content-type": "application/json" }, body: JSON.stringify(envelope()) });
    const badDrain = await fetch(`${baseUrl}/v1/captures/lease`, { method: "POST", headers: { ...auth("producer"), "content-type": "application/json" }, body: JSON.stringify({ worker_id: "x" }) });
    assert.equal(badAppend.status, 401);
    assert.equal(badDrain.status, 401);
  });

  it("refuses traffic when producer and drain tokens are equal", async () => {
    await new Promise((resolve) => server.close(resolve));
    server = createRunwayServer({ queueDir, producerToken: "shared", drainToken: "shared", logger: { error() {} } });
    await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
    baseUrl = `http://127.0.0.1:${server.address().port}`;
    const healthResponse = await fetch(`${baseUrl}/healthz`);
    const health = await healthResponse.json();
    assert.equal(healthResponse.status, 503);
    assert.equal(health.ok, false);
    assert.equal(health.auth_roles_separated, false);
    const response = await fetch(`${baseUrl}/v1/captures`, { method: "POST", headers: { ...auth("shared"), "content-type": "application/json" }, body: JSON.stringify(envelope()) });
    assert.equal(response.status, 503);
    assert.equal((await response.json()).error, "role_tokens_not_separated");
  });

  it("rejects unrelated capture shapes", async () => {
    const response = await fetch(`${baseUrl}/v1/captures`, { method: "POST", headers: { ...auth("producer"), "content-type": "application/json" }, body: JSON.stringify({ source: "anything" }) });
    assert.equal(response.status, 400);
    assert.equal((await response.json()).error, "unsupported_envelope");
  });

  it("rejects impossible dates", async () => {
    const invalid = envelope();
    invalid.transaction.date_iso = "2026-99-99";
    const response = await fetch(`${baseUrl}/v1/captures`, { method: "POST", headers: { ...auth("producer"), "content-type": "application/json" }, body: JSON.stringify(invalid) });
    assert.equal(response.status, 400);
    assert.equal((await response.json()).error, "invalid_date_iso");
  });

  it("deduplicates producer retries before and after acknowledgement", async () => {
    const first = await capture("stable-wallet-id");
    const duplicate = await fetch(`${baseUrl}/v1/captures`, { method: "POST", headers: { ...auth("producer"), "content-type": "application/json" }, body: JSON.stringify(envelope("stable-wallet-id")) });
    assert.equal(duplicate.status, 200);
    assert.equal((await duplicate.json()).id, first.id);
    const leased = await lease();
    const ack = await fetch(`${baseUrl}/v1/captures/${first.id}/ack`, { method: "POST", headers: { ...auth("drain"), "content-type": "application/json" }, body: JSON.stringify({ lease_id: leased.lease_id }) });
    assert.equal(ack.status, 200);
    const acknowledgedRetry = await fetch(`${baseUrl}/v1/captures`, { method: "POST", headers: { ...auth("producer"), "content-type": "application/json" }, body: JSON.stringify(envelope("stable-wallet-id")) });
    assert.equal(acknowledgedRetry.status, 200);
    const body = await acknowledgedRetry.json();
    assert.equal(body.id, first.id);
    assert.equal(body.acknowledged, true);
    assert.equal((await lease()).items.length, 0);
  });

  it("leases oldest-first pages without concurrent duplication", async () => {
    const first = await capture("first");
    const second = await capture("second");
    const [left, right] = await Promise.all([lease("left", 1), lease("right", 1)]);
    const ids = [left.items[0]?.id, right.items[0]?.id].sort();
    assert.deepEqual(ids, [first.id, second.id].sort());
    assert.notEqual(left.lease_id, right.lease_id);
  });

  it("requires the matching lease to acknowledge and removes only after ack", async () => {
    const stored = await capture();
    const leased = await lease();
    const mismatch = await fetch(`${baseUrl}/v1/captures/${stored.id}/ack`, { method: "POST", headers: { ...auth("drain"), "content-type": "application/json" }, body: JSON.stringify({ lease_id: "wrong" }) });
    assert.equal(mismatch.status, 409);
    assert.equal((await lease("other")).items.length, 0);
    const ack = await fetch(`${baseUrl}/v1/captures/${stored.id}/ack`, { method: "POST", headers: { ...auth("drain"), "content-type": "application/json" }, body: JSON.stringify({ lease_id: leased.lease_id, result_hash: "abc" }) });
    assert.equal(ack.status, 200);
    assert.equal((await lease("after")).items.length, 0);
  });
});
