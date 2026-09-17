import { Database } from "bun:sqlite";
import { createHash } from "node:crypto";
import {
  mkdir,
  mkdtemp,
  readFile,
  writeFile,
  readdir,
  realpath,
} from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const workspace = dirname(fileURLToPath(import.meta.url));
const root = dirname(workspace);
const [command, name] = process.argv.slice(2);
if (!name || !/^iteration-[1-9]\d*$/.test(name))
  throw new Error(
    "Usage: bun writing-for-humans-workspace/eval.ts <prepare|start|status|capture> iteration-N",
  );
const dir = join(workspace, "live", name);
const readJSON = async (path: string) =>
  JSON.parse(await readFile(path, "utf8"));
const saveJSON = (path: string, value: unknown) =>
  writeFile(path, JSON.stringify(value, null, 2) + "\n");
const hash = (text: string) => createHash("sha256").update(text).digest("hex");
const db = () =>
  new Database(
    process.env.WRITING_EVAL_DB || join(homedir(), ".t3/userdata/state.sqlite"),
    {
      readonly: true,
    },
  );
function git(...args: string[]) {
  const result = Bun.spawnSync(["git", ...args], { cwd: root });
  if (result.exitCode) throw new Error(result.stderr.toString());
  return result.stdout.toString().trim();
}
async function verifyInputs(run: any) {
  for (const [file, digest] of Object.entries(run.hashes))
    if (hash(await readFile(join(dir, file), "utf8")) !== digest)
      throw new Error(`Saved input changed: ${file}`);
}
function inspect(threadId: string) {
  const connection = db();
  try {
    return {
      thread: connection
        .query(
          "SELECT thread_id, title, worktree_path, model_selection_json, runtime_mode, interaction_mode, deleted_at FROM projection_threads WHERE thread_id = ?",
        )
        .get(threadId) as any,
      session: connection
        .query(
          "SELECT status, active_turn_id, last_error, provider_name FROM projection_thread_sessions WHERE thread_id = ?",
        )
        .get(threadId) as any,
      turns: connection
        .query(
          "SELECT turn_id, state, started_at, completed_at FROM projection_turns WHERE thread_id = ? ORDER BY requested_at, row_id",
        )
        .all(threadId),
      messages: connection
        .query(
          "SELECT message_id, turn_id, role, text, is_streaming, created_at, updated_at, attachments_json FROM projection_thread_messages WHERE thread_id = ? ORDER BY created_at, rowid",
        )
        .all(threadId) as any[],
    };
  } finally {
    connection.close();
  }
}

if (command === "prepare") {
  const files: Record<string, string> = {};
  for (const file of ["topic.md", "settings.json"])
    files[file] = await readFile(join(workspace, file), "utf8");
  for (const skill of ["writing-for-humans", "unslop"])
    files[`${skill}.md`] = await readFile(
      join(root, "skills/software-development", skill, "SKILL.md"),
      "utf8",
    );
  files["prompt.txt"] =
    `${files["topic.md"].trim()}\n\nUse $writing-for-humans and $unslop.\n`;
  const settings = JSON.parse(files["settings.json"]);
  if (!settings.model || !settings.effort || !settings.provider)
    throw new Error("Incomplete participant settings");
  await mkdir(join(workspace, "live"), { recursive: true });
  await mkdir(dir); // Never overwrite a run.
  // A separate repo has no authoring-repo ancestry, instructions, or remote.
  const participantDirectory = await realpath(await mkdtemp("/tmp/team-app-"));
  const init = Bun.spawnSync([
    "git",
    "init",
    "-q",
    "-b",
    "main",
    participantDirectory,
  ]);
  if (init.exitCode) throw new Error(init.stderr.toString());
  for (const skill of ["writing-for-humans", "unslop"]) {
    const target = join(participantDirectory, ".agents/skills", skill);
    await mkdir(target, { recursive: true });
    await writeFile(join(target, "SKILL.md"), files[`${skill}.md`]);
  }
  for (const [file, text] of Object.entries(files))
    await writeFile(join(dir, file), text);
  await saveJSON(join(dir, "run.json"), {
    createdAt: new Date().toISOString(),
    name: "Team invitations",
    status: "prepared",
    sourceRevision: git("rev-parse", "HEAD"),
    sourceBranch: git("branch", "--show-current"),
    branch: "main",
    directory: participantDirectory,
    context:
      "Standalone temporary repo with only the two skill files. No evaluation material or authoring-repo instructions. Normal harness and filesystem permissions still apply.",
    settings,
    hashes: Object.fromEntries(
      Object.entries(files).map(([file, text]) => [file, hash(text)]),
    ),
    threadId: null,
  });
  console.log(`Prepared ${dir}`);
} else {
  const run = await readJSON(join(dir, "run.json"));
  await verifyInputs(run);
  if (command === "start") {
    if (run.status !== "prepared" || run.threadId)
      throw new Error(
        "Launch already attempted. Use status and inspect dispatch.json before taking any recovery action.",
      );
    for (const skill of ["writing-for-humans", "unslop"]) {
      const text = await readFile(
        join(run.directory, ".agents/skills", skill, "SKILL.md"),
        "utf8",
      );
      if (hash(text) !== run.hashes[`${skill}.md`])
        throw new Error(`Participant skill changed before launch: ${skill}`);
    }
    const s = run.settings;
    const args = [
      "python3",
      join(root, "skills/system/to-thread/scripts/t3-thread.py"),
      "--name",
      run.name,
      "--prompt",
      await readFile(join(dir, "prompt.txt"), "utf8"),
      "--project-directory",
      root,
      "--directory",
      run.directory,
      "--branch",
      run.branch,
      "--provider",
      s.provider,
      "--model",
      s.model,
      "--effort",
      s.effort,
      "--runtime-mode",
      s.runtimeMode,
      "--interaction-mode",
      s.interactionMode,
    ];
    if (s.serviceTier) args.push("--service-tier", s.serviceTier);
    run.status = "launch-attempted";
    await saveJSON(join(dir, "run.json"), run);
    const child = Bun.spawn(args, {
      cwd: root,
      stdout: "pipe",
      stderr: "pipe",
    });
    const [stdout, stderr, code] = await Promise.all([
      new Response(child.stdout).text(),
      new Response(child.stderr).text(),
      child.exited,
    ]);
    await writeFile(join(dir, "dispatch.stdout.txt"), stdout);
    await writeFile(join(dir, "dispatch.stderr.txt"), stderr);
    if (stdout.trim()) {
      const result = JSON.parse(stdout);
      await saveJSON(join(dir, "dispatch.json"), result);
      run.threadId = result.thread_id ?? null;
    }
    run.status = code ? "launch-needs-inspection" : "launched-unverified";
    await saveJSON(join(dir, "run.json"), run);
    if (code)
      throw new Error(
        `Launch needs inspection: ${stderr}. Preserve any thread identity in run.json.`,
      );
    console.log(
      `Started ${run.name}: ${run.threadId}. Use status to verify it.`,
    );
  } else if (command === "status") {
    if (!run.threadId)
      throw new Error("No thread identity recorded; inspect dispatch output");
    const state = inspect(run.threadId);
    const selection = state.thread
      ? JSON.parse(state.thread.model_selection_json)
      : null;
    const matches =
      selection?.instanceId === run.settings.provider &&
      selection?.model === run.settings.model &&
      selection?.options?.some(
        (o: any) =>
          o.id === "reasoningEffort" && o.value === run.settings.effort,
      ) &&
      (!run.settings.serviceTier ||
        selection?.options?.some(
          (o: any) =>
            o.id === "serviceTier" && o.value === run.settings.serviceTier,
        )) &&
      state.thread?.runtime_mode === run.settings.runtimeMode &&
      state.thread?.interaction_mode === run.settings.interactionMode &&
      (state.thread?.worktree_path || root) === run.directory;
    const live =
      !state.thread?.deleted_at &&
      state.turns.some((t: any) => t.started_at) &&
      !state.session?.last_error;
    if (!matches || !live)
      throw new Error(
        `Thread not verified: ${JSON.stringify({ thread: state.thread, session: state.session, turns: state.turns })}`,
      );
    run.status =
      run.status === "captured" ? "captured" : "awaiting-human-conversation";
    await saveJSON(join(dir, "run.json"), run);
    console.log(
      JSON.stringify(
        {
          threadId: run.threadId,
          title: state.thread.title,
          selection,
          session: state.session,
          messages: state.messages.length,
          firstAssistant:
            state.messages.find((m) => m.role === "assistant")?.text ?? null,
        },
        null,
        2,
      ),
    );
  } else if (command === "capture") {
    // The coordinator invokes this only after the human returns and says they are done.
    if (!run.threadId) throw new Error("No thread to capture");
    const connection = db();
    let evidence: any;
    try {
      evidence = connection.transaction(() => ({
        thread: connection
          .query(
            "SELECT thread_id, title, model_selection_json, runtime_mode, interaction_mode FROM projection_threads WHERE thread_id = ?",
          )
          .get(run.threadId),
        session: connection
          .query(
            "SELECT status, active_turn_id, last_error FROM projection_thread_sessions WHERE thread_id = ?",
          )
          .get(run.threadId),
        messages: connection
          .query(
            "SELECT message_id, turn_id, role, text, is_streaming, created_at, updated_at, attachments_json FROM projection_thread_messages WHERE thread_id = ? ORDER BY created_at, rowid",
          )
          .all(run.threadId),
        turns: connection
          .query(
            "SELECT turn_id, state, requested_at, started_at, completed_at FROM projection_turns WHERE thread_id = ? ORDER BY requested_at, row_id",
          )
          .all(run.threadId),
      }))();
    } finally {
      connection.close();
    }
    if (!evidence.thread) throw new Error("Thread not found");
    const pendingTurns = evidence.turns.filter(
      (t: any) => !t.completed_at && !t.started_at,
    );
    const acceptIdlePending =
      process.argv.includes("--include-pending") &&
      evidence.session?.status === "ready";
    if (
      evidence.session?.active_turn_id ||
      evidence.messages.some((m: any) => m.is_streaming) ||
      evidence.turns.some(
        (t: any) => !t.completed_at && (t.started_at || !acceptIdlePending),
      )
    )
      throw new Error(
        "Conversation still has an unfinished turn; wait for it to finish before capturing",
      );
    if (evidence.messages.filter((m: any) => m.role === "user").length < 2)
      throw new Error(
        "Only the runner's opening prompt exists; wait for the human conversation",
      );
    const captures = (await readdir(dir)).filter((f) =>
      /^capture-\d+$/.test(f),
    );
    const capture = `capture-${Math.max(0, ...captures.map((f) => Number(f.split("-")[1]))) + 1}`;
    const target = join(dir, capture);
    await mkdir(target);
    const raw = JSON.stringify(evidence, null, 2) + "\n";
    await writeFile(join(target, "transcript.json"), raw);
    const messages = evidence.messages.map(
      (m: any, i: number) =>
        `## ${i + 1}. ${m.role}${i === 0 ? " (runner kickoff)" : ""}\n\nMessage: ${m.message_id} · ${m.created_at}\n\n${m.text}\n`,
    );
    await writeFile(
      join(target, "transcript.md"),
      `# ${run.name}\n\nThread: ${run.threadId}\n\n${messages.join("\n")}`,
    );
    await saveJSON(join(target, "evidence.json"), {
      capturedAt: new Date().toISOString(),
      threadId: run.threadId,
      sha256: hash(raw),
      source: "T3 projection_thread_messages; turn and session metadata",
      coverage:
        "Stored chat messages including kickoff; tool activity and hidden reasoning are not exported. Attachments remain source references.",
      messages: evidence.messages.length,
      pendingTurns: pendingTurns.length,
      captureNote: pendingTurns.length
        ? "Human accepted the visible conversation as-is. The idle session retains unstarted pending turn metadata; preserve it without assuming those turns completed."
        : null,
    });
    run.status = "captured";
    run.latestCapture = capture;
    await saveJSON(join(dir, "run.json"), run);
    console.log(
      `Captured ${target}. Discuss the human's experience before proposing skill edits.`,
    );
  } else throw new Error(`Unknown command: ${command}`);
}
