# Brief: watch-video execution probes

You are an agent that has the `watch-video` skill loaded. First read
`skills/watch-video/SKILL.md` (relative to the repo root you are running in).
You may also read `skills/watch-video/scripts/framesheet.py` to check flags.
Do not run any commands; this is a dry run — answer with the exact commands
you WOULD run.

For EACH probe below:
1. State your next concrete action(s) — exact command lines where applicable.
2. Cite the file and the exact sentence from the skill that decided your move.
3. If the skill genuinely does not cover the situation, SAY SO — flagging a
   gap or ambiguity is a fully valid answer; do not invent procedure the
   skill doesn't license.

Answer all 8 probes, numbered. Be concise: a few lines each.

**P1.** The user gives you `session.mp4`, a 47-minute screen recording, and
asks "at what point does the crash dialog appear?". You already ran ffprobe:
2820.0s, 1920x1080, 30fps. What exactly do you run next, and why?

**P2.** You built a window sheet covering 5:30–6:06. The tile stamped 5:51
appears to show an error toast with a line of text in it. The user's question
is "what does the error say?". Do you answer from this tile? If not, what
exactly do you do?

**P3.** The user asked "summarize this 10-minute video". You read one index
sheet and can already narrate the whole arc scene by scene with timestamps.
Must you build window sheets for every scene before answering?

**P4.** The user asks: "what does the presenter say at 2:10?"

**P5.** You suspect a ~0.5-second logo flash somewhere in a 3-minute clip.
Your 30-frame index sheet (one tile per 6s) shows nothing. Next move?

**P6.** You are drafting your answer and have written: "in the top-right tile
of the second sheet, the dialog appears". Anything wrong with this sentence?

**P7.** The user pastes a YouTube URL. You check: `yt-dlp` is NOT installed
on this machine. What do you do?

**P8.** The user wants a close look at what happens between 4:00 and 4:45 in
`clip.mp4`. Give the exact framesheet command you would run.
