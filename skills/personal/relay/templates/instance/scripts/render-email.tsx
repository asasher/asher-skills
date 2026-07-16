import { render } from "react-email";
import React from "react";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { InternalDigestEmail } from "../templates/src/internal-digest.js";
import { ProjectUpdateEmail } from "../templates/src/project-update.js";
import type { RelayBag, TemplateConfig } from "../templates/src/types.js";

function option(name: string): string {
  const index = process.argv.indexOf(name);
  const value = index >= 0 ? process.argv[index + 1] : undefined;
  if (!value) throw new Error(`Missing ${name}`);
  return value;
}
function forceTheme(html: string, theme: "light" | "dark"): string {
  return html.replace(/<html([^>]*)>/i, `<html$1 class="${theme}-preview">`);
}

const bagPath = path.resolve(option("--bag"));
const outDir = path.resolve(option("--out"));
const instance = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const bag = JSON.parse(await readFile(bagPath, "utf8")) as RelayBag;
const config = JSON.parse(await readFile(path.join(instance, "template-config.json"), "utf8")) as TemplateConfig;
if (bag.schema_version !== 2) throw new Error("Relay bag schema_version must be 2");
const component = bag.kind === "internal_digest" ? <InternalDigestEmail bag={bag} config={config} /> : <ProjectUpdateEmail bag={bag} config={config} />;
const html = await render(component);
const text = await render(component, { plainText: true });
await mkdir(outDir, { recursive: true });
await Promise.all([
  writeFile(path.join(outDir, "rendered-email.html"), html, "utf8"),
  writeFile(path.join(outDir, "rendered-email.txt"), text, "utf8"),
  writeFile(path.join(outDir, "rendered-email-light.html"), forceTheme(html, "light"), "utf8"),
  writeFile(path.join(outDir, "rendered-email-dark.html"), forceTheme(html, "dark"), "utf8"),
]);
console.log(JSON.stringify({ bag: bag.id, out: outDir, template: "relay-compact-default@2.0.0" }));
