// Vite config with tiny persistence middleware so the browser can save the Univer snapshot
// and the declared-object sidecar without a separate backend.
import { randomUUID } from 'node:crypto';
import { readFile, rename, unlink, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const SNAPSHOT = resolve(process.cwd(), 'workbook.snapshot.json');
const OBJECTS = resolve(process.cwd(), 'objects.json');
const MAX_JSON_BYTES = 25 * 1024 * 1024;

function sendJson(res, statusCode, payload) {
  res.statusCode = statusCode;
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(payload));
}

async function readJsonBody(req) {
  const chunks = [];
  let size = 0;

  for await (const chunk of req) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += buffer.length;
    if (size > MAX_JSON_BYTES) {
      const error = new Error('JSON body exceeds 25 MiB');
      error.statusCode = 413;
      throw error;
    }
    chunks.push(buffer);
  }

  try {
    return JSON.parse(Buffer.concat(chunks).toString('utf8'));
  } catch {
    const error = new Error('Request body must be valid JSON');
    error.statusCode = 400;
    throw error;
  }
}

async function atomicWriteJson(target, value) {
  const temporary = `${target}.${process.pid}.${randomUUID()}.tmp`;
  try {
    await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
    await rename(temporary, target);
  } catch (error) {
    await unlink(temporary).catch(() => {});
    throw error;
  }
}

function serveJson(path, target, fallback) {
  return (server) => {
    server.middlewares.use(path, async (req, res, next) => {
      if (req.method !== 'GET') return next();
      try {
        res.setHeader('Cache-Control', 'no-store');
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(await readFile(target, 'utf8'));
      } catch {
        sendJson(res, 404, fallback);
      }
    });
  };
}

function persistJson(path, target) {
  return (server) => {
    server.middlewares.use(path, async (req, res, next) => {
      if (req.method !== 'POST') return next();
      try {
        const value = await readJsonBody(req);
        await atomicWriteJson(target, value);
        sendJson(res, 200, { ok: true });
      } catch (error) {
        const statusCode = error.statusCode || 500;
        const message = statusCode < 500 ? error.message : 'Could not persist JSON';
        sendJson(res, statusCode, { ok: false, error: message });
      }
    });
  };
}

function workbookPersistence() {
  return {
    name: 'workbook-persistence',
    configureServer(server) {
      serveJson('/snapshot', SNAPSHOT, {})(server);
      serveJson('/objects', OBJECTS, { charts: [], pivots: [] })(server);
      persistJson('/save-objects', OBJECTS)(server);
      persistJson('/save', SNAPSHOT)(server);
    },
  };
}

export default {
  plugins: [workbookPersistence()],
  server: { host: true }, // Listen on all interfaces so the presentation surface can proxy it.
};
