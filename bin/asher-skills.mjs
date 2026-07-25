#!/usr/bin/env node
// Thin shim so consumers can install without a local checkout:
//
//     npx github:asasher/asher-skills install --skill backlog build staffing
//
// npx runs a public GitHub repo directly, so this needs no npm publish — the
// package is marked private and exists only to expose this bin. All logic lives
// in tools/install.py (stdlib Python, per this repo's script convention); this
// file only locates the interpreter and forwards argv.

import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const installer = join(root, "tools", "install.py");

// `python3` first: macOS ships no bare `python`, and where it exists it is often 2.x.
const candidates = ["python3", "python"];
let status = null;

for (const python of candidates) {
  const run = spawnSync(python, [installer, ...process.argv.slice(2)], {
    stdio: "inherit",
    // The installer defaults --into to the working directory, which must stay
    // the consumer's repo, not the temporary directory npx unpacked us into.
    cwd: process.cwd(),
  });
  if (run.error?.code === "ENOENT") continue;
  status = run.status ?? 1;
  break;
}

if (status === null) {
  console.error(
    "error: no Python 3 interpreter found (tried: " + candidates.join(", ") + ").\n" +
    "The installer is stdlib-only Python 3; install it, or run tools/install.py from a checkout."
  );
  process.exit(127);
}

process.exit(status);
