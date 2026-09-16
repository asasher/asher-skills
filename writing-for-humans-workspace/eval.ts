import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const workspace = dirname(fileURLToPath(import.meta.url));
const root = dirname(workspace);
const skills = ["writing-for-humans", "unslop"];
const hash = (text: string) => createHash("sha256").update(text).digest("hex");
const json = async (path: string) => JSON.parse(await readFile(path, "utf8"));
const save = (path: string, value: unknown) =>
  writeFile(path, JSON.stringify(value, null, 2) + "\n");
const [command, name, ...args] = process.argv.slice(2);
if (!name || !/^iteration-[1-9]\d*$/.test(name)) {
  throw new Error(
    "Usage: bun writing-for-humans-workspace/eval.ts <prepare|next|record|summarize|compare> iteration-N [arguments]",
  );
}
const dir = join(workspace, name);

if (command === "prepare") {
  const [participant, ...settingParts] = args;
  if (!participant || !settingParts.length)
    throw new Error(
      "prepare requires a model and quoted harness/settings description",
    );
  const inputs: Record<string, string> = {};
  for (const file of [
    "scenario.json",
    "rubric.json",
    "participant-protocol.txt",
  ])
    inputs[file] = await readFile(join(workspace, file), "utf8");
  for (const skill of skills)
    inputs[`${skill}.md`] = await readFile(
      join(root, "skills/software-development", skill, "SKILL.md"),
      "utf8",
    );
  await mkdir(dir); // An existing iteration is never overwritten.
  for (const [file, body] of Object.entries(inputs))
    await writeFile(join(dir, file), body);
  const revision = Bun.spawnSync(["git", "rev-parse", "HEAD"], { cwd: root });
  if (revision.exitCode) throw new Error("Cannot record source revision");
  await save(join(dir, "run.json"), {
    created: new Date().toISOString(),
    participant,
    settings: settingParts.join(" "),
    sourceRevision: revision.stdout.toString().trim(),
    hashes: Object.fromEntries(
      Object.entries(inputs).map(([file, body]) => [file, hash(body)]),
    ),
    status: "collecting",
    participantSession: null,
  });
  await save(join(dir, "transcript.json"), []);
  const scenario = JSON.parse(inputs["scenario.json"]);
  const rubric = JSON.parse(inputs["rubric.json"]);
  await save(join(dir, "feedback.json"), {
    reviewer: null,
    source: "human",
    decision: null,
    overallNotes: "",
    turns: scenario.turns.map((_: unknown, i: number) => ({
      turn: i + 1,
      scores: Object.fromEntries(
        Object.keys(rubric.dimensions).map((key) => [key, null]),
      ),
      cutOrRewrite: "",
      missing: "",
      notes: "",
    })),
  });
  console.log(
    `Prepared ${name}. Run next to get the first participant prompt.`,
  );
} else if (command === "next") {
  const scenario = await json(join(dir, "scenario.json"));
  const transcript = await json(join(dir, "transcript.json"));
  const turn = scenario.turns[transcript.length];
  if (!turn) throw new Error("All turns have been recorded");
  let prompt = "";
  if (!transcript.length) {
    prompt += `${scenario.context} ${await readFile(join(dir, "participant-protocol.txt"), "utf8")}\nApply these communication skills:\n`;
    for (const skill of skills)
      prompt += `\n${await readFile(join(dir, `${skill}.md`), "utf8")}\n`;
  }
  prompt += `\nWork observations:\n${turn.observations}\n\nUser:\n${turn.user}\n`;
  await writeFile(join(dir, `prompt-${transcript.length + 1}.txt`), prompt);
  console.log(prompt);
} else if (command === "record") {
  if (!args[0])
    throw new Error(
      "record requires a file containing the participant's verbatim reply",
    );
  const scenario = await json(join(dir, "scenario.json"));
  const transcript = await json(join(dir, "transcript.json"));
  const turn = scenario.turns[transcript.length];
  if (!turn) throw new Error("All turns have been recorded");
  await readFile(join(dir, `prompt-${transcript.length + 1}.txt`), "utf8");
  const reply = await readFile(resolve(args[0]), "utf8");
  if (!reply.trim()) throw new Error("An empty reply is not a completed turn");
  await writeFile(join(dir, `reply-${transcript.length + 1}.txt`), reply, {
    flag: "wx",
  });
  transcript.push({ turn: transcript.length + 1, ...turn, assistant: reply });
  await save(join(dir, "transcript.json"), transcript);
  await writeFile(
    join(dir, "transcript.md"),
    transcript
      .map(
        (t: any) =>
          `## Turn ${t.turn}\n\n**User**\n\n${t.user}\n\n**Assistant**\n\n${t.assistant}`,
      )
      .join("\n\n"),
  );
  const run = await json(join(dir, "run.json"));
  run.status =
    transcript.length === scenario.turns.length
      ? "awaiting-human"
      : "collecting";
  await save(join(dir, "run.json"), run);
  console.log(`Recorded turn ${transcript.length}; ${run.status}.`);
} else if (command === "summarize") {
  const transcript = await json(join(dir, "transcript.json"));
  const feedback = await json(join(dir, "feedback.json"));
  const scenario = await json(join(dir, "scenario.json"));
  const rubric = await json(join(dir, "rubric.json"));
  const dimensions = Object.keys(rubric.dimensions);
  const complete = transcript.length === scenario.turns.length;
  const validScores =
    feedback.turns.length === scenario.turns.length &&
    feedback.turns.every(
      (t: any, i: number) =>
        t.turn === i + 1 &&
        dimensions.every(
          (key) =>
            Number.isInteger(t.scores[key]) &&
            t.scores[key] >= 1 &&
            t.scores[key] <= 5,
        ),
    );
  const rated =
    complete &&
    feedback.source === "human" &&
    typeof feedback.reviewer === "string" &&
    feedback.reviewer.trim().length > 0 &&
    validScores;
  const summary = {
    status: rated ? "human-rated" : complete ? "awaiting-human" : "incomplete",
    turns: transcript.map((t: any) => ({
      turn: t.turn,
      words: t.assistant.trim().split(/\s+/).length,
    })),
    scores: rated
      ? Object.fromEntries(
          dimensions.map((key) => [
            key,
            feedback.turns.reduce(
              (sum: number, t: any) => sum + t.scores[key],
              0,
            ) / feedback.turns.length,
          ]),
        )
      : null,
    decision:
      rated && ["keep", "revise", "stop"].includes(feedback.decision)
        ? feedback.decision
        : null,
  };
  await save(join(dir, "benchmark.json"), summary);
  console.log(JSON.stringify(summary, null, 2));
} else if (command === "compare") {
  const other = args[0];
  if (!other || !/^iteration-[1-9]\d*$/.test(other))
    throw new Error("compare requires another iteration-N");
  const otherDir = join(workspace, other);
  const a = await json(join(dir, "run.json"));
  const b = await json(join(otherDir, "run.json"));
  for (const path of [dir, otherDir]) {
    const run = await json(join(path, "run.json"));
    for (const [file, expected] of Object.entries(run.hashes)) {
      if (hash(await readFile(join(path, file), "utf8")) !== expected)
        throw new Error(`${path}/${file} changed after snapshot`);
    }
  }
  if (
    ["scenario.json", "rubric.json", "participant-protocol.txt"].some(
      (key) => a.hashes[key] !== b.hashes[key],
    ) ||
    a.participant !== b.participant ||
    a.settings !== b.settings
  ) {
    throw new Error(
      "Different scenario, rubric, model, or settings: start a new baseline.",
    );
  }
  for (const path of [dir, otherDir]) {
    const result = Bun.spawnSync([
      "bun",
      fileURLToPath(import.meta.url),
      "summarize",
      path.split("/").at(-1)!,
    ]);
    if (result.exitCode) throw new Error(result.stderr.toString());
  }
  const previous = await json(join(dir, "benchmark.json"));
  const next = await json(join(otherDir, "benchmark.json"));
  console.log(
    JSON.stringify(
      {
        previous: name,
        next: other,
        skillsChanged: skills.filter(
          (skill) => a.hashes[`${skill}.md`] !== b.hashes[`${skill}.md`],
        ),
        scores: { previous: previous.scores, next: next.scores },
        words: { previous: previous.turns, next: next.turns },
        decision: next.decision,
      },
      null,
      2,
    ),
  );
} else {
  throw new Error(`Unknown command: ${command}`);
}
