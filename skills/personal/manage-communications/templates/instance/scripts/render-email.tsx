import { render } from "react-email";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { InternalDigestEmail } from "../templates/src/internal-digest.js";
import { ProjectUpdateEmail } from "../templates/src/project-update.js";
import type { CommsBag } from "../templates/src/types.js";

function option(name: string): string {
  const index = process.argv.indexOf(name);
  const value = index >= 0 ? process.argv[index + 1] : undefined;
  if (!value) throw new Error(`Missing ${name}`);
  return value;
}

const bagPath = path.resolve(option("--bag"));
const outDir = path.resolve(option("--out"));
const bag = JSON.parse(await readFile(bagPath, "utf8")) as CommsBag;
const component = bag.kind === "internal_digest"
  ? <InternalDigestEmail bag={bag} />
  : <ProjectUpdateEmail bag={bag} />;

await mkdir(outDir, { recursive: true });
await Promise.all([
  writeFile(path.join(outDir, "rendered-email.html"), await render(component), "utf8"),
  writeFile(path.join(outDir, "rendered-email.txt"), await render(component, { plainText: true }), "utf8"),
]);
console.log(JSON.stringify({ bag: bag.id, out: outDir }));
