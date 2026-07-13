import crypto from "node:crypto";
import fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";

const DEFAULT_QUEUE_DIR = "/data/queue";
const DEFAULT_MAX_UPLOAD_MB = 100;
const QUEUE_ID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const MAX_FIELDS = 64;
const MAX_FIELD_BYTES = 64 * 1024;

class HttpError extends Error {
  constructor(status, code, details = {}) {
    super(code);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

function sendJson(res, status, body) {
  const data = Buffer.from(`${JSON.stringify(body)}\n`);
  res.writeHead(status, {
    "cache-control": "no-store",
    "content-length": data.length,
    "content-type": "application/json; charset=utf-8",
    "x-content-type-options": "nosniff",
  });
  res.end(data);
}

function timingSafeEqualString(leftValue, rightValue) {
  const left = Buffer.from(String(leftValue || ""));
  const right = Buffer.from(String(rightValue || ""));
  return left.length === right.length && crypto.timingSafeEqual(left, right);
}

function requireBearerToken(req, expectedToken) {
  if (!expectedToken) throw new HttpError(503, "capture_token_not_configured");
  const match = String(req.headers.authorization || "").match(/^Bearer\s+(.+)$/i);
  if (!match || !timingSafeEqualString(match[1], expectedToken)) {
    throw new HttpError(401, "unauthorized");
  }
}

function sanitizeFileName(name) {
  const base = path.basename(String(name || "payload.bin"));
  const clean = base.replace(/[^A-Za-z0-9._-]/g, "_").slice(0, 180);
  return clean || "payload.bin";
}

function cleanText(value) {
  return String(value ?? "").replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "");
}

async function ensureQueueDir(queueDir) {
  await fs.mkdir(queueDir, { recursive: true, mode: 0o700 });
}

async function readBody(req, maxBytes) {
  const declared = Number(req.headers["content-length"] || 0);
  if (Number.isFinite(declared) && declared > maxBytes) {
    throw new HttpError(413, "payload_too_large", { max_bytes: maxBytes });
  }

  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > maxBytes) {
      throw new HttpError(413, "payload_too_large", { max_bytes: maxBytes });
    }
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

function checkFields(fields) {
  const entries = Object.entries(fields);
  if (entries.length > MAX_FIELDS) throw new HttpError(400, "too_many_fields");
  for (const [key, value] of entries) {
    if (Buffer.byteLength(key) > 256 || Buffer.byteLength(String(value)) > MAX_FIELD_BYTES) {
      throw new HttpError(400, "capture_field_too_large", { field: key.slice(0, 256) });
    }
  }
}

async function parseCapture(req, body) {
  const contentType = String(req.headers["content-type"] || "").toLowerCase();
  const fields = {};
  let payload = null;

  if (contentType.startsWith("multipart/form-data") || contentType.startsWith("application/x-www-form-urlencoded")) {
    let form;
    try {
      const request = new Request("http://capture.local/capture", {
        method: "POST",
        headers: { "content-type": req.headers["content-type"] },
        body,
      });
      form = await request.formData();
    } catch {
      throw new HttpError(400, "invalid_form_data");
    }

    for (const [key, value] of form.entries()) {
      if (key === "payload") {
        if (typeof value === "string") {
          payload = {
            buffer: Buffer.from(value),
            mimeType: "text/plain; charset=utf-8",
            originalName: "payload.txt",
          };
        } else {
          payload = {
            buffer: Buffer.from(await value.arrayBuffer()),
            mimeType: cleanText(value.type || "application/octet-stream"),
            originalName: cleanText(value.name || "payload.bin"),
          };
        }
      } else {
        fields[cleanText(key)] = cleanText(value);
      }
    }
  } else if (contentType.startsWith("application/json")) {
    let parsed;
    try {
      parsed = JSON.parse(body.toString("utf8"));
    } catch {
      throw new HttpError(400, "invalid_json");
    }
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
      throw new HttpError(400, "invalid_json");
    }
    for (const [key, value] of Object.entries(parsed)) {
      if (key === "payload" && value != null) {
        payload = {
          buffer: Buffer.from(String(value)),
          mimeType: "text/plain; charset=utf-8",
          originalName: "payload.txt",
        };
      } else if (value != null && typeof value !== "object") {
        fields[cleanText(key)] = cleanText(value);
      }
    }
  } else {
    throw new HttpError(415, "unsupported_content_type");
  }

  checkFields(fields);
  return { fields, payload };
}

async function writeQueueItem(queueDir, req, capture) {
  await ensureQueueDir(queueDir);
  const id = crypto.randomUUID();
  const itemDir = path.join(queueDir, id);
  const temporaryDir = path.join(queueDir, `.tmp-${id}`);
  await fs.mkdir(temporaryDir, { mode: 0o700 });

  try {
    let payloadMeta = {
      filename: null,
      original_name: null,
      mime_type: null,
      size: 0,
      sha256: null,
      path: null,
    };

    if (capture.payload) {
      const filename = sanitizeFileName(capture.payload.originalName);
      await fs.writeFile(path.join(temporaryDir, filename), capture.payload.buffer, { mode: 0o600 });
      payloadMeta = {
        filename,
        original_name: cleanText(capture.payload.originalName).slice(0, 500),
        mime_type: cleanText(capture.payload.mimeType).slice(0, 200),
        size: capture.payload.buffer.length,
        sha256: crypto.createHash("sha256").update(capture.payload.buffer).digest("hex"),
        path: filename,
      };
    }

    const fields = capture.fields;
    const meta = {
      id,
      received_at: new Date().toISOString(),
      captured_at: fields.captured_at || null,
      source: fields.source || null,
      client: fields.client || null,
      context: fields.context || "",
      item_index: fields.item_index || null,
      shared_item: fields.shared_item || null,
      shared_input_text: fields.shared_input_text || null,
      shared_urls: fields.shared_urls || null,
      payload: payloadMeta,
      request: {
        user_agent: cleanText(req.headers["user-agent"] || "").slice(0, 500) || null,
        forwarded_for: cleanText(req.headers["x-forwarded-for"] || "").slice(0, 500) || null,
      },
      fields,
    };
    await fs.writeFile(path.join(temporaryDir, "meta.json"), `${JSON.stringify(meta, null, 2)}\n`, {
      mode: 0o600,
    });
    await fs.rename(temporaryDir, itemDir);
    return meta;
  } catch (error) {
    await fs.rm(temporaryDir, { recursive: true, force: true });
    throw error;
  }
}

async function readQueueItem(queueDir, id) {
  try {
    const raw = await fs.readFile(path.join(queueDir, id, "meta.json"), "utf8");
    const meta = JSON.parse(raw);
    if (meta.id !== id) throw new Error("queue metadata ID mismatch");
    return meta;
  } catch (error) {
    if (error.code === "ENOENT") throw new HttpError(404, "queue_item_not_found");
    throw error;
  }
}

async function listItems(queueDir) {
  await ensureQueueDir(queueDir);
  const entries = await fs.readdir(queueDir, { withFileTypes: true });
  const items = [];
  for (const entry of entries) {
    if (entry.isDirectory() && QUEUE_ID_PATTERN.test(entry.name)) {
      items.push(await readQueueItem(queueDir, entry.name));
    }
  }
  return items.sort((left, right) =>
    String(left.received_at || "").localeCompare(String(right.received_at || ""))
  );
}

function queueRoute(pathname) {
  const match = pathname.match(/^\/queue\/items\/([^/]+)(\/payload)?$/);
  if (!match) return null;
  if (!QUEUE_ID_PATTERN.test(match[1])) throw new HttpError(400, "invalid_queue_item_id");
  return { id: match[1], payload: Boolean(match[2]) };
}

async function handleRequest(req, res, options) {
  const url = new URL(req.url || "/", "http://capture.local");
  const pathname = url.pathname;

  if (req.method === "GET" && (pathname === "/" || pathname === "/healthz")) {
    sendJson(res, 200, {
      name: "capture-to-inbox-api",
      ok: true,
      auth_configured: Boolean(options.token),
    });
    return;
  }

  if (pathname === "/capture" && req.method === "POST") {
    requireBearerToken(req, options.token);
    const body = await readBody(req, options.maxUploadBytes);
    const capture = await parseCapture(req, body);
    const meta = await writeQueueItem(options.queueDir, req, capture);
    sendJson(res, 201, { ok: true, id: meta.id, received_at: meta.received_at });
    return;
  }

  if (pathname === "/queue/items" && req.method === "GET") {
    requireBearerToken(req, options.token);
    sendJson(res, 200, { ok: true, items: await listItems(options.queueDir) });
    return;
  }

  const route = queueRoute(pathname);
  if (route) {
    requireBearerToken(req, options.token);
    if (req.method === "GET" && !route.payload) {
      sendJson(res, 200, await readQueueItem(options.queueDir, route.id));
      return;
    }
    if (req.method === "GET" && route.payload) {
      const meta = await readQueueItem(options.queueDir, route.id);
      if (!meta.payload?.path || !meta.payload?.size) {
        throw new HttpError(404, "queue_payload_not_found");
      }
      const data = await fs.readFile(path.join(options.queueDir, route.id, meta.payload.path));
      const filename = sanitizeFileName(meta.payload.original_name || meta.payload.filename);
      res.writeHead(200, {
        "cache-control": "no-store",
        "content-disposition": `attachment; filename="${filename}"`,
        "content-length": data.length,
        "content-type": meta.payload.mime_type || "application/octet-stream",
        "x-content-type-options": "nosniff",
      });
      res.end(data);
      return;
    }
    if (req.method === "DELETE" && !route.payload) {
      await readQueueItem(options.queueDir, route.id);
      await fs.rm(path.join(options.queueDir, route.id), { recursive: true });
      sendJson(res, 200, { ok: true, id: route.id, deleted: true });
      return;
    }
  }

  throw new HttpError(404, "not_found");
}

export function createCaptureServer({
  queueDir = process.env.QUEUE_DIR || DEFAULT_QUEUE_DIR,
  token = process.env.CAPTURE_TOKEN || "",
  maxUploadMb = Number(process.env.MAX_UPLOAD_MB || DEFAULT_MAX_UPLOAD_MB),
  logger = console,
} = {}) {
  const parsedMax = Number.isFinite(maxUploadMb) && maxUploadMb > 0 ? maxUploadMb : DEFAULT_MAX_UPLOAD_MB;
  const options = {
    queueDir: path.resolve(queueDir),
    token,
    maxUploadBytes: Math.max(1, Math.floor(parsedMax * 1024 * 1024)),
  };

  return http.createServer((req, res) => {
    handleRequest(req, res, options).catch((error) => {
      if (error instanceof HttpError) {
        sendJson(res, error.status, { error: error.code, ...error.details });
        return;
      }
      if (error?.code === "ENOENT") {
        sendJson(res, 404, { error: "queue_item_not_found" });
        return;
      }
      logger.error(error);
      sendJson(res, 500, { error: "internal_server_error" });
    });
  });
}
