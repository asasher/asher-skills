# Video eval coordination

Read `README.md` and the selected iteration's `run.json` before acting. The participant is an ordinary production agent in a separate T3 thread. Keep these coordinator records, rubric, source revisions, feedback, and prior outputs outside its project. Give it only the production brief, raw inputs, production style/toolchain docs, and the relevant installed skills. Its thread name, branch, and directory describe the editing task.

## Agent execution

Use the recorded T3 provider with the current session's model, effort, and permission mode. `codex-video` is a separate Codex provider instance using the same transport and auth as `codex`, plus startup flags disabling unrelated skill paths. Workspace-only enablement overrides were ineffective in the installed runtime; verify the actual injected catalog. Preserve the user's global skill installations and original providers. This uses the existing provider transport and auth; no additional billing route is selected.

## Iteration contract

Prepare a fresh standalone project for each comparison run from the recorded raw input hashes, production brief, and project inputs. Copy complete packages from the candidate skill revision into `.agents/skills`. Install only the required toolchain. Keep source raw recordings unchanged; APFS clones allow independent read-only copies. Use the toolchain versions recorded in the prior run unless changing the environment is the explicit subject of a new baseline.

From the authoring repo, use `python3 video-edit-workspace/eval.py prepare iteration-N --directory PROJECT --prompt-file PROMPT --thread-helper HELPER --provider codex-video`, then `start iteration-N`. The thread helper is the current `to-thread` adapter. After launch, run `python3 video-edit-workspace/verify-launch.py iteration-N` and inspect the first reply for errors. Compare the actual cwd, model, effort, and skill list with the intended run. Preserve and stop invalid launches before scoring them.

Use `eval.py status iteration-N` while the worker runs. Observe outputs without changing its project or sending hints about desired results. A normal human clarification is allowed and must remain in the captured transcript. Keep skill source edits separate from the participant's installed packages during its run.

When the turn finishes, `eval.py capture iteration-N` saves a versioned transcript and output hashes. Grade technical facts against `rubric.json` in a separate `review.json`; preserve human feedback verbatim in `feedback.md`. The coordinator can mark measurable defects, but cannot invent human ratings for sound, graphics, or pacing. A ready video and captured evidence end the first run; human acceptance remains pending until actual feedback arrives.

Change instructions only for a demonstrated failure. Save the proposed diff, evidence, and rationale, then start a fresh project/thread from raw inputs with the same brief. Keep prior runs intact. Changed footage, brief, format, model, or rubric starts a new comparison baseline. Historical ad hoc videos are references, not controlled proof that the new instructions caused an improvement.

## Isolation limits

The normal full-access permission mode remains enabled. Context isolation removes eval material and unrelated skill instructions from the task environment; it does not restrict filesystem access. Check actual file-read/tool evidence for contamination and mark uncertainty honestly. Do not tell the participant that it is being evaluated or ask it to report eval scores.
