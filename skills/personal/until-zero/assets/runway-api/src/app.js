// Adapted from skills/personal/capture-to-inbox/assets/capture-api/src/app.js.
// This dedicated service intentionally shares no runtime files with that skill.
import crypto from "node:crypto";
import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";

const DEFAULT_QUEUE_DIR = "/data/runway-queue";
const ID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const MAX_BODY_BYTES = 128 * 1024;

class HttpError extends Error {
  constructor(status, code, details = {}) {
    super(code);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

function sendJson(res, status, body) {
  const bytes = Buffer.from(`${JSON.stringify(body)}\n`);
  res.writeHead(status, {
    "cache-control": "no-store",
    "content-length": bytes.length,
    "content-type": "application/json; charset=utf-8",
    "x-content-type-options": "nosniff",
  });
  res.end(bytes);
}

function safeEqual(leftValue, rightValue) {
  const left = Buffer.from(String(leftValue || ""));
  const right = Buffer.from(String(rightValue || ""));
  return left.length === right.length && crypto.timingSafeEqual(left, right);
}

function bearer(req) {
  const match = String(req.headers.authorization || "").match(/^Bearer\s+(.+)$/i);
  return match ? match[1] : "";
}

function authorize(req, expected, unavailableCode) {
  if (!expected) throw new HttpError(503, unavailableCode);
  if (!safeEqual(bearer(req), expected)) throw new HttpError(401, "unauthorized");
}

async function readJson(req) {
  const declared = Number(req.headers["content-length"] || 0);
  if (declared > MAX_BODY_BYTES) throw new HttpError(413, "payload_too_large");
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY_BYTES) throw new HttpError(413, "payload_too_large");
    chunks.push(chunk);
  }
  try {
    const value = JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
    if (!value || Array.isArray(value) || typeof value !== "object") throw new Error("object required");
    return value;
  } catch {
    throw new HttpError(400, "invalid_json");
  }
}

function text(value, limit) {
  return String(value ?? "").replace(/[\u0000-\u001f\u007f]/g, "").trim().slice(0, limit);
}

function validIsoDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const parsed = new Date(`${value}T00:00:00.000Z`);
  return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
}

function validateEnvelope(value) {
  if (value.version !== 1 || value.source !== "ios-wallet") throw new HttpError(400, "unsupported_envelope");
  const transaction = value.transaction;
  if (!transaction || Array.isArray(transaction) || typeof transaction !== "object") {
    throw new HttpError(400, "transaction_required");
  }
  const amount = String(transaction.amount_minor ?? "");
  const currency = text(transaction.currency, 3).toUpperCase();
  const dateIso = text(transaction.date_iso, 10);
  const externalId = text(transaction.external_id, 160);
  if (!/^-?\d+$/.test(amount)) throw new HttpError(400, "invalid_amount_minor");
  if (!/^[A-Z]{3}$/.test(currency)) throw new HttpError(400, "invalid_currency");
  if (!validIsoDate(dateIso)) throw new HttpError(400, "invalid_date_iso");
  if (!externalId) throw new HttpError(400, "external_id_required");
  const card = transaction.card && typeof transaction.card === "object" ? transaction.card : {};
  return {
    version: 1,
    source: "ios-wallet",
    captured_at: text(value.captured_at, 40) || null,
    client: text(value.client, 80) || null,
    transaction: {
      amount_minor: amount,
      currency,
      description: text(transaction.description, 240),
      date_iso: dateIso,
      external_id: externalId,
      category: text(transaction.category, 120),
      card: {
        last4: text(card.last4, 8).replace(/\D/g, "").slice(-8),
        label: text(card.label, 80),
      },
    },
  };
}

async function atomicJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true, mode: 0o700 });
  const temporary = `${file}.tmp-${crypto.randomUUID()}`;
  const handle = await fs.open(temporary, "wx", 0o600);
  try {
    await handle.writeFile(`${JSON.stringify(value, null, 2)}\n`);
    await handle.sync();
  } finally {
    await handle.close();
  }
  await fs.rename(temporary, file);
  const directory = await fs.open(path.dirname(file), "r");
  try { await directory.sync(); } finally { await directory.close(); }
}

function itemFile(queueDir, id) {
  if (!ID_PATTERN.test(id)) throw new HttpError(400, "invalid_capture_id");
  return path.join(queueDir, "items", `${id}.json`);
}

async function readItem(queueDir, id) {
  try {
    const value = JSON.parse(await fs.readFile(itemFile(queueDir, id), "utf8"));
    if (value.id !== id) throw new Error("capture ID mismatch");
    return value;
  } catch (error) {
    if (error.code === "ENOENT") throw new HttpError(404, "capture_not_found");
    throw error;
  }
}

async function listItems(queueDir) {
  const directory = path.join(queueDir, "items");
  await fs.mkdir(directory, { recursive: true, mode: 0o700 });
  const names = await fs.readdir(directory);
  const items = [];
  for (const name of names.sort()) {
    if (name.endsWith(".json") && ID_PATTERN.test(name.slice(0, -5))) {
      items.push(JSON.parse(await fs.readFile(path.join(directory, name), "utf8")));
    }
  }
  return items.sort((left, right) => String(left.received_at).localeCompare(String(right.received_at)) || left.id.localeCompare(right.id));
}

function publicItem(item) {
  return {
    id: item.id,
    received_at: item.received_at,
    envelope: item.envelope,
    lease: item.lease,
  };
}

function idempotencyKey(envelope) {
  return crypto.createHash("sha256").update(`${envelope.source}\u0000${envelope.transaction.external_id}`).digest("hex");
}

async function findExisting(queueDir, key) {
  const queued = (await listItems(queueDir)).find((item) => item.idempotency_key === key);
  if (queued) return { id: queued.id, received_at: queued.received_at, acknowledged: false };
  const receipts = path.join(queueDir, "receipts");
  await fs.mkdir(receipts, { recursive: true, mode: 0o700 });
  for (const name of await fs.readdir(receipts)) {
    if (!name.endsWith(".json")) continue;
    const receipt = JSON.parse(await fs.readFile(path.join(receipts, name), "utf8"));
    if (receipt.idempotency_key === key) return { id: receipt.id, received_at: receipt.received_at, acknowledged: true };
  }
  return null;
}

async function storeCapture(queueDir, envelope) {
  const key = idempotencyKey(envelope);
  const existing = await findExisting(queueDir, key);
  if (existing) return { ...existing, duplicate: true };
  const id = crypto.randomUUID();
  const item = { id, received_at: new Date().toISOString(), idempotency_key: key, envelope, lease: null };
  await atomicJson(itemFile(queueDir, id), item);
  return { ...item, duplicate: false };
}

async function pruneReceipts(queueDir, retentionDays) {
  const directory = path.join(queueDir, "receipts");
  await fs.mkdir(directory, { recursive: true, mode: 0o700 });
  const cutoff = Date.now() - retentionDays * 86400 * 1000;
  for (const name of await fs.readdir(directory)) {
    const target = path.join(directory, name);
    const stat = await fs.stat(target);
    if (stat.mtimeMs < cutoff) await fs.rm(target, { force: true });
  }
}

function createMutex() {
  let chain = Promise.resolve();
  return async (operation) => {
    const prior = chain;
    let release;
    chain = new Promise((resolve) => { release = resolve; });
    await prior;
    try { return await operation(); } finally { release(); }
  };
}

export function createRunwayServer({
  queueDir = process.env.QUEUE_DIR || DEFAULT_QUEUE_DIR,
  producerToken = process.env.RUNWAY_PRODUCER_TOKEN || "",
  drainToken = process.env.RUNWAY_DRAIN_TOKEN || "",
  retentionDays = Number(process.env.RECEIPT_RETENTION_DAYS || 30),
  logger = console,
} = {}) {
  const root = path.resolve(queueDir);
  const withLock = createMutex();
  const authRolesSeparated = Boolean(producerToken && drainToken && !safeEqual(producerToken, drainToken));

  function requireSeparatedAuth() {
    if (!authRolesSeparated) throw new HttpError(503, "role_tokens_not_separated");
  }

  async function handle(req, res) {
    const url = new URL(req.url || "/", "http://runway.local");
    if (req.method === "GET" && (url.pathname === "/" || url.pathname === "/healthz")) {
      sendJson(res, authRolesSeparated ? 200 : 503, {
        name: "until-zero-runway-api",
        ok: authRolesSeparated,
        producer_auth_configured: Boolean(producerToken),
        drain_auth_configured: Boolean(drainToken),
        auth_roles_separated: authRolesSeparated,
      });
      return;
    }
    if (req.method === "POST" && url.pathname === "/v1/captures") {
      requireSeparatedAuth();
      authorize(req, producerToken, "producer_token_not_configured");
      const envelope = validateEnvelope(await readJson(req));
      const item = await withLock(() => storeCapture(root, envelope));
      sendJson(res, item.duplicate ? 200 : 201, { ok: true, id: item.id, received_at: item.received_at, duplicate: item.duplicate, acknowledged: Boolean(item.acknowledged) });
      return;
    }
    if (req.method === "POST" && url.pathname === "/v1/captures/lease") {
      requireSeparatedAuth();
      authorize(req, drainToken, "drain_token_not_configured");
      const body = await readJson(req);
      const workerId = text(body.worker_id, 120);
      if (!workerId) throw new HttpError(400, "worker_id_required");
      const requestedLimit = Number(body.limit || 25);
      const requestedLeaseSeconds = Number(body.lease_seconds || 300);
      const limit = Number.isFinite(requestedLimit) ? Math.min(100, Math.max(1, Math.trunc(requestedLimit))) : 25;
      const leaseSeconds = Number.isFinite(requestedLeaseSeconds) ? Math.min(3600, Math.max(30, Math.trunc(requestedLeaseSeconds))) : 300;
      const leased = await withLock(async () => {
        const now = Date.now();
        const leaseId = crypto.randomUUID();
        const output = [];
        for (const item of await listItems(root)) {
          const expires = Date.parse(item.lease?.expires_at || "");
          if (item.lease && Number.isFinite(expires) && expires > now) continue;
          item.lease = {
            id: leaseId,
            worker_id: workerId,
            leased_at: new Date(now).toISOString(),
            expires_at: new Date(now + leaseSeconds * 1000).toISOString(),
          };
          await atomicJson(itemFile(root, item.id), item);
          output.push(publicItem(item));
          if (output.length >= limit) break;
        }
        return { id: leaseId, items: output };
      });
      sendJson(res, 200, { ok: true, lease_id: leased.id, items: leased.items });
      return;
    }
    const match = url.pathname.match(/^\/v1\/captures\/([^/]+)\/(ack|release)$/);
    if (match && req.method === "POST") {
      requireSeparatedAuth();
      authorize(req, drainToken, "drain_token_not_configured");
      const [, id, action] = match;
      const body = await readJson(req);
      const result = await withLock(async () => {
        const item = await readItem(root, id);
        if (!item.lease || !safeEqual(item.lease.id, body.lease_id)) throw new HttpError(409, "lease_mismatch");
        if (action === "release") {
          item.lease = null;
          await atomicJson(itemFile(root, id), item);
          return { ok: true, id, released: true };
        }
        const receipt = {
          id,
          received_at: item.received_at,
          acknowledged_at: new Date().toISOString(),
          lease_id: item.lease.id,
          idempotency_key: item.idempotency_key,
          result_hash: text(body.result_hash, 128) || null,
        };
        await atomicJson(path.join(root, "receipts", `${id}.json`), receipt);
        await fs.rm(itemFile(root, id));
        const keepDays = Number.isFinite(retentionDays) ? Math.max(1, retentionDays) : 30;
        await pruneReceipts(root, keepDays);
        return { ok: true, id, acknowledged: true };
      });
      sendJson(res, 200, result);
      return;
    }
    throw new HttpError(404, "not_found");
  }

  return http.createServer((req, res) => {
    handle(req, res).catch((error) => {
      const status = error instanceof HttpError ? error.status : 500;
      if (status >= 500) logger.error?.(error);
      sendJson(res, status, { error: error instanceof HttpError ? error.code : "internal_error", ...(error.details || {}) });
    });
  });
}
