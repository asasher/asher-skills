import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { afterEach, beforeEach, describe, it } from "node:test";
import { createCaptureServer } from "../src/app.js";

let queueDir;
let server;
let baseUrl;

beforeEach(async () => {
  queueDir = await fs.mkdtemp(path.join(os.tmpdir(), "capture-api-"));
  server = createCaptureServer({ queueDir, token: "test-token", logger: { error() {} } });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

afterEach(async () => {
  await new Promise((resolve) => server.close(resolve));
  await fs.rm(queueDir, { recursive: true, force: true });
});

function auth() {
  return { authorization: "Bearer test-token" };
}

describe("capture API", () => {
  it("exposes health without leaking the queue path", async () => {
    const response = await fetch(`${baseUrl}/healthz`);
    const body = await response.json();
    assert.equal(response.status, 200);
    assert.deepEqual(body, { name: "capture-to-inbox-api", ok: true, auth_configured: true });
    assert.equal(JSON.stringify(body).includes(queueDir), false);
  });

  it("rejects missing authentication", async () => {
    const response = await fetch(`${baseUrl}/capture`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: "{}",
    });
    assert.equal(response.status, 401);
    assert.deepEqual(await response.json(), { error: "unauthorized" });
  });

  it("atomically stores, hashes, serves, lists, and deletes multipart payloads", async () => {
    const bytes = Buffer.from("hello capture");
    const form = new FormData();
    form.set("source", "ios-shortcut");
    form.set("client", "test-phone");
    form.set("context", "save this");
    form.set("payload", new Blob([bytes], { type: "text/plain" }), "../note name.txt");

    const captured = await fetch(`${baseUrl}/capture`, {
      method: "POST",
      headers: auth(),
      body: form,
    });
    const result = await captured.json();
    assert.equal(captured.status, 201);
    assert.match(result.id, /^[0-9a-f-]{36}$/);

    const listed = await fetch(`${baseUrl}/queue/items`, { headers: auth() });
    const item = (await listed.json()).items[0];
    assert.equal(item.context, "save this");
    assert.equal(item.payload.filename, "note_name.txt");
    assert.equal(item.payload.size, bytes.length);
    assert.equal(item.payload.sha256, crypto.createHash("sha256").update(bytes).digest("hex"));

    const payload = await fetch(`${baseUrl}/queue/items/${result.id}/payload`, { headers: auth() });
    assert.deepEqual(Buffer.from(await payload.arrayBuffer()), bytes);
    assert.deepEqual((await fs.readdir(queueDir)).filter((name) => name.startsWith(".tmp-")), []);

    const deleted = await fetch(`${baseUrl}/queue/items/${result.id}`, {
      method: "DELETE",
      headers: auth(),
    });
    assert.equal(deleted.status, 200);
    assert.deepEqual(await fs.readdir(queueDir), []);
  });

  it("stores text-only captures without inventing payload bytes", async () => {
    const form = new URLSearchParams({
      source: "ios-shortcut",
      shared_item: "https://example.com/item",
      shared_urls: "https://example.com/item",
    });
    const captured = await fetch(`${baseUrl}/capture`, {
      method: "POST",
      headers: { ...auth(), "content-type": "application/x-www-form-urlencoded" },
      body: form,
    });
    const result = await captured.json();
    const item = await fetch(`${baseUrl}/queue/items/${result.id}`, { headers: auth() });
    const body = await item.json();
    assert.equal(body.shared_item, "https://example.com/item");
    assert.equal(body.payload.size, 0);
    assert.equal(body.payload.path, null);

    const payload = await fetch(`${baseUrl}/queue/items/${result.id}/payload`, { headers: auth() });
    assert.equal(payload.status, 404);
  });

  it("rejects invalid IDs and oversized request bodies", async () => {
    const invalid = await fetch(`${baseUrl}/queue/items/not-an-id`, { headers: auth() });
    assert.equal(invalid.status, 400);

    await new Promise((resolve) => server.close(resolve));
    server = createCaptureServer({ queueDir, token: "test-token", maxUploadMb: 0.0001, logger: { error() {} } });
    await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
    baseUrl = `http://127.0.0.1:${server.address().port}`;
    const oversized = await fetch(`${baseUrl}/capture`, {
      method: "POST",
      headers: { ...auth(), "content-type": "application/json" },
      body: JSON.stringify({ context: "x".repeat(500) }),
    });
    assert.equal(oversized.status, 413);
    assert.equal((await oversized.json()).error, "payload_too_large");
  });

  it("returns not found for missing valid items and refuses idempotent-looking deletes", async () => {
    const id = "00000000-0000-4000-8000-000000000000";
    const read = await fetch(`${baseUrl}/queue/items/${id}`, { headers: auth() });
    const deleted = await fetch(`${baseUrl}/queue/items/${id}`, { method: "DELETE", headers: auth() });
    assert.equal(read.status, 404);
    assert.equal(deleted.status, 404);
  });
});
