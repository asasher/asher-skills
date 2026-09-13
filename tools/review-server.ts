import { realpathSync } from "node:fs";
import { dirname, extname, join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { Marked } from "marked";
import { gfmHeadingId, getHeadingList } from "marked-gfm-heading-id";

const root = realpathSync(join(dirname(fileURLToPath(import.meta.url)), ".."));
const guide = "/docs/software-development.html#review";
const checklist = "/docs/software-development-review.md";
const escape = (text: string) =>
  text.replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ]!,
  );
const urlPath = (path: string) =>
  "/" + path.split("/").map(encodeURIComponent).join("/");
const sourceList = Bun.spawnSync(["git", "ls-files", "-z"], { cwd: root });
if (sourceList.exitCode !== 0)
  throw new Error("Cannot read the review source inventory.");
const tracked = sourceList.stdout.toString().split("\0").filter(Boolean);
const skillFiles = new Map<string, string>();
for (const path of tracked) {
  const match = path.match(/^skills\/[^/]+\/([^/]+)\/SKILL\.md$/);
  if (match) skillFiles.set(match[1], path);
}
// Serve reviewed sources, not the repository's private workspaces or machine state.
const allowed = new Set(
  tracked.filter(
    (path) =>
      path.startsWith("docs/") ||
      ["README.md", "CONTEXT.md", "AGENTS.md"].includes(path) ||
      path.startsWith(".agents/skills/writing-for-agents/") ||
      (path.startsWith("skills/") && skillFiles.has(path.split("/")[2])),
  ),
);
const review = await Bun.file(join(root, checklist.slice(1))).text();
const order = [...review.matchAll(/- \[.\] \*\*\d+\. \[([^\]]+)\]/g)].map(
  (match) => match[1],
);

const css = `
:root{color-scheme:dark;--bg:#0a0a0a;--raised:#1a1a1a;--text:#ededed;--muted:#a1a1a1;--line:#333;--accent:#52a8ff;font:17px/1.7 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text)}
*{box-sizing:border-box}body{margin:0}a{color:var(--accent);text-underline-offset:4px;overflow-wrap:anywhere}a:hover{color:var(--text)}a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
header{border-bottom:1px solid var(--line);padding:12px max(20px,calc((100vw - 960px)/2));background:var(--bg)}nav{display:flex;flex-wrap:wrap;gap:4px 20px;align-items:center}nav a{min-height:44px;display:inline-flex;align-items:center;font-size:14px;color:var(--muted)}main{max-width:960px;margin:auto;padding:28px 24px 80px;min-width:0}.path{font:12px/1.6 ui-monospace,monospace;color:var(--muted);overflow-wrap:anywhere;margin-bottom:20px}
h1,h2,h3,h4,h5,h6{line-height:1.3;scroll-margin-top:20px}h1{font-size:36px;letter-spacing:-.035em;margin-top:24px}h2{font-size:26px;margin-top:40px;border-bottom:1px solid var(--line);padding-bottom:12px}h3{font-size:21px;margin-top:28px}h4{font-size:18px}p{margin:16px 0}li{margin:8px 0}ul,ol{padding-left:26px}li>p{margin:8px 0}
code,pre{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}code{font-size:.86em;background:var(--raised);padding:2px 5px;border-radius:4px;overflow-wrap:anywhere}a code{color:inherit}pre{background:var(--raised);border:1px solid var(--line);padding:16px;overflow:auto;border-radius:6px;font-size:14px;line-height:1.6;tab-size:2}pre code{background:none;padding:0;white-space:pre;overflow-wrap:normal}blockquote{margin:20px 0;border-left:2px solid var(--accent);padding:0 20px;color:var(--muted)}
.table-scroll{overflow-x:auto;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid var(--line);min-width:120px}th{color:var(--muted);font-size:13px}img,svg,video{max-width:100%;height:auto}details{border:1px solid var(--line);border-radius:6px;padding:12px 16px;margin:16px 0}summary{cursor:pointer;min-height:32px}details>summary{font-size:15px}.contents ul{font-size:14px;list-style:none;padding:0}.contents li{margin:8px 0}.contents a{display:inline-block;padding:4px 0}.contents .level-3{padding-left:16px}.frontmatter pre{margin-bottom:4px}hr{border:0;border-top:1px solid var(--line);margin:32px 0}.reader-footer{border-top:1px solid var(--line);margin-top:48px;padding-top:20px}
@media(max-width:600px){main{padding:20px 18px 60px}header{padding:8px 18px}h1{font-size:30px}h2{font-size:24px}pre{font-size:13px}details{padding:10px 12px}th,td{padding:10px}}
`;

function navigation(path: string) {
  const owner = path.startsWith("skills/") ? path.split("/")[2] : "";
  const position = order.indexOf(owner);
  const links = [
    `<a href="${guide}">← Family review</a>`,
    `<a href="${checklist}">Checklist</a>`,
  ];
  if (owner && skillFiles.has(owner) && path !== skillFiles.get(owner))
    links.push(
      `<a href="${urlPath(skillFiles.get(owner)!)}">${escape(owner)}</a>`,
    );
  if (position > 0)
    links.push(
      `<a rel="prev" href="${urlPath(skillFiles.get(order[position - 1])!)}">← ${escape(order[position - 1])}</a>`,
    );
  if (position >= 0 && position < order.length - 1)
    links.push(
      `<a rel="next" href="${urlPath(skillFiles.get(order[position + 1])!)}">${escape(order[position + 1])} →</a>`,
    );
  links.push(`<a href="${urlPath(path)}?raw=1">Raw source</a>`);
  return `<nav aria-label="Review navigation">${links.join("")}</nav>`;
}

async function renderMarkdown(source: string, path: string) {
  const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  const body = frontmatter ? source.slice(frontmatter[0].length) : source;
  const parser = new Marked(gfmHeadingId());
  let content = parser.parse(body, { async: false }) as string;
  const headings = getHeadingList().filter((heading) => heading.level <= 3);
  // Presentation links belong to the reader; skill source keeps name-only composition.
  content = await new HTMLRewriter()
    .on("table", {
      element(el) {
        el.before('<div class="table-scroll">', { html: true });
        el.after("</div>", { html: true });
      },
    })
    .transform(new Response(content))
    .text();
  // Link complete inline skill names, preserving code samples and existing links.
  const parts = content.split(/(<pre\b[\s\S]*?<\/pre>|<a\b[\s\S]*?<\/a>)/gi);
  content = parts
    .map((part, index) =>
      index % 2
        ? part
        : part.replace(/<code>([a-z0-9-]+)<\/code>/g, (match, name) => {
            const target = skillFiles.get(name);
            return target
              ? `<a data-skill-link href="${urlPath(target)}">${match}</a>`
              : match;
          }),
    )
    .join("");
  const toc =
    headings.length > 2
      ? `<details class="contents"><summary>On this page</summary><ul>${headings.map((h) => `<li class="level-${h.level}"><a href="#${escape(h.id)}">${escape(h.raw)}</a></li>`).join("")}</ul></details>`
      : "";
  return {
    title: headings[0]?.raw || path.split("/").at(-1)!,
    content: `${toc}${frontmatter ? `<details class="frontmatter"><summary>Skill metadata</summary><pre><code>${escape(frontmatter[1])}</code></pre></details>` : ""}${content}`,
  };
}

const server = Bun.serve({
  hostname: "127.0.0.1",
  port: Number(process.env.REVIEW_PORT || 8791),
  async fetch(request) {
    if (!["GET", "HEAD"].includes(request.method))
      return new Response("Read-only review server", { status: 405 });
    const url = new URL(request.url);
    if (url.pathname === "/")
      return Response.redirect(new URL(guide, url), 302);
    let path: string;
    try {
      path = decodeURIComponent(url.pathname).slice(1);
    } catch {
      return new Response("Invalid path", { status: 400 });
    }
    if (!allowed.has(path))
      return new Response("Review source not found", { status: 404 });
    let resolved: string;
    try {
      resolved = realpathSync(join(root, path));
    } catch {
      return new Response("Source no longer exists", { status: 404 });
    }
    const withinRoot = relative(root, resolved);
    if (withinRoot === ".." || withinRoot.startsWith(".." + sep))
      return new Response("Review source not found", { status: 404 });
    const file = Bun.file(resolved);
    const headers = {
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    };
    const extension = extname(path).toLowerCase();
    if (url.searchParams.has("raw"))
      return new Response(request.method === "HEAD" ? null : file, {
        headers: { ...headers, "Content-Type": "text/plain; charset=utf-8" },
      });
    if (
      [
        ".html",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".svg",
        ".webp",
        ".mp4",
        ".woff",
        ".woff2",
      ].includes(extension)
    )
      return new Response(request.method === "HEAD" ? null : file, { headers });
    const source = await file.text();
    const rendered =
      extension === ".md"
        ? await renderMarkdown(source, path)
        : {
            title: path.split("/").at(-1)!,
            content: `<h1>${escape(path.split("/").at(-1)!)}</h1><pre><code>${escape(source)}</code></pre>`,
          };
    const nav = navigation(path);
    const page = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(rendered.title)} · Asher Skills</title><style>${css}</style></head><body><header>${nav}</header><main><div class="path">${escape(path)}</div>${rendered.content}<footer class="reader-footer">${nav}</footer></main></body></html>`;
    return new Response(request.method === "HEAD" ? null : page, {
      headers: {
        ...headers,
        "Content-Type": "text/html; charset=utf-8",
        "Content-Security-Policy":
          "default-src 'self'; script-src 'none'; style-src 'unsafe-inline'; img-src 'self' https: data:; object-src 'none'; base-uri 'none'; frame-ancestors 'self'",
      },
    });
  },
});
console.log(`Review server: http://${server.hostname}:${server.port}${guide}`);
