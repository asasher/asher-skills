// Vite config with a tiny persistence layer so the browser can save the Univer snapshot and the
// declared-object sidecar without a separate backend — and, for the TURN-BASED loop, two mechanics:
//   1. version guard: each save carries the version it started from; a stale save is refused (409),
//      so the human can't clobber an edit the agent made during its turn.
//   2. reload-on-agent-edit: when the agent writes the files directly (its turn), the watcher pushes a
//      browser reload, so the human never keeps editing a stale in-memory workbook.
// Together these make last-write-wins safe: there is never a stale writer.
import { createHash, randomUUID } from 'node:crypto';
import { readFile, rename, unlink, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const SNAPSHOT = resolve(process.cwd(), 'workbook.snapshot.json');
const OBJECTS = resolve(process.cwd(), 'objects.json');
const MAX_JSON_BYTES = 25 * 1024 * 1024;

// content-hash version per file: opaque token that both the GET response and the watcher agree on,
// regardless of who wrote the file (the browser via /save, or the agent via the Python converter).
const versions = new Map();
const hashText = (text) => createHash('sha256').update(text).digest('hex').slice(0, 16);
async function currentVersion(target) {
  try { return hashText(await readFile(target, 'utf8')); } catch { return ''; }
}

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
  const text = `${JSON.stringify(value, null, 2)}\n`;
  try {
    await writeFile(temporary, text, { flag: 'wx' });
    await rename(temporary, target);
  } catch (error) {
    await unlink(temporary).catch(() => {});
    throw error;
  }
  return hashText(text);
}

function serveJson(path, target, fallback) {
  return (server) => {
    server.middlewares.use(path, async (req, res, next) => {
      if (req.method !== 'GET') return next();
      try {
        const text = await readFile(target, 'utf8');
        const version = hashText(text);
        versions.set(target, version);
        res.setHeader('Cache-Control', 'no-store');
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.setHeader('X-Workbook-Version', version);
        res.end(text);
      } catch {
        res.setHeader('X-Workbook-Version', '');
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
        const base = req.headers['x-base-version'];
        // Optimistic concurrency: if the client sends the version it loaded and the file has since
        // moved on (an agent turn), refuse — the client must reload rather than overwrite.
        if (base !== undefined && base !== '') {
          const current = await currentVersion(target);
          if (current && current !== base) {
            return sendJson(res, 409, { ok: false, error: 'stale — reload for the latest', version: current });
          }
        }
        const value = await readJsonBody(req);
        const version = await atomicWriteJson(target, value);
        versions.set(target, version); // record our own write so the watcher won't treat it as external
        sendJson(res, 200, { ok: true, version });
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

      // reload-on-agent-edit: seed versions, then reload the browser only when a file's content changes
      // to something WE didn't write (i.e. the agent edited it on its turn).
      server.watcher.add([SNAPSHOT, OBJECTS]);
      currentVersion(SNAPSHOT).then((v) => versions.set(SNAPSHOT, v));
      currentVersion(OBJECTS).then((v) => versions.set(OBJECTS, v));
      server.watcher.on('change', async (file) => {
        const target = resolve(file);
        if (target !== SNAPSHOT && target !== OBJECTS) return;
        const version = await currentVersion(target);
        if (version && version !== versions.get(target)) {
          versions.set(target, version);
          server.ws.send({ type: 'full-reload' });
        }
      });
    },
  };
}

export default {
  plugins: [workbookPersistence()],
  server: { host: true }, // Listen on all interfaces so the presentation surface can proxy it.
};
