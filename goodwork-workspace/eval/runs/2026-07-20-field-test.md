# Goodwork v3 — Tier-3 field test findings (2026-07-20)

Human QA of the installed skill in a separate project. Findings recorded as reported, verbatim first,
then the coordinator's read on the likely home in the skill. Issues get filed in one pass when Asher
says so — nothing here is fixed mid-test.

## FT-1 — Setup asks the user technical transport questions (tailnet/tailscale vocabulary)

**Reported (screenshot, `goodwork setup` in test project, Opus 4.8):** setup's phone-loop step asked
"How should I expose the approval page to your phone?" with options "Expose on tailnet (Recommended) — I
run `tailscale serve` to publish the page at https://ashers-macbook-pro.tail045dd5.ts.net…" and
"Desk-only for now — keep the page on this machine only (localhost)… I'll record tailscale as desk-only."
Asher: "this is too technical… the skill does not have to talk about tailscale or tailnet and all that
stuff."

**Read:** the plain-language core rule ("never file names, IDs, hashes, schemas, or gate mechanics")
stops at setup's door — `reference/setup.md` step 6 explicitly instructs installing/verifying Tailscale
and asking the user, and step 9 asks about presentation rungs. Setup's own closing line ("present this to
the user as plumbing they don't need to understand") is contradicted by the steps above it. Minimal fix:
setup asks the *outcome* question only ("Want to approve things from your phone, or just at this
computer?") and handles transport silently, reporting failures as capabilities gaps, not vendor names.

**Design direction raised by Asher (bigger than goodwork):** the local-HTML-review-surface +
agent-talking-to-it pattern recurs (review-loop, goodwork, plan/prototype presentations). Proposal: a
small shared primitive — a *temporary relay between the agent and the human* — that owns serving,
reachability (desk/phone), and teardown, so consuming skills speak only "I'll put this on your phone" and
never name Tailscale/tailnet/ports. Fits the repo convention exactly ("a capability that several skills
genuinely share — the review surface … — is extracted into its own skill and referenced by name").
Naming note: `relay` is already taken by the AgentMail comms skill (`skills/personal/relay`); the new
primitive needs a different name (e.g. `handoff`, `surface`, `bridge`). Candidate consumers: goodwork
(approval page, board), review-loop (its serve/tailnet section would *become* this), plan/prototype via
review-loop. This is an extraction issue, not a goodwork wording patch — both are worth filing.

## FT-2 — Setup output far too verbose; user wants concise step-by-step

**Reported (screenshot, setup completion message):** the wrap-up ran to ~8 sections — "what you actually
get" bullets, a choices table, "two things still need you", a "role you mentioned" digression pitching
the interview's epistemics ("I don't guess at your profile — I elicit it"), a ≈20-min next step, and a
closing question. Asher: "Too verbose for this skill; at least during setup the user needs concise step
by step instructions."

**Read:** three compounding causes. (1) No brevity contract anywhere — SKILL.md Output Standards govern
*content* (files updated, one next action) but never length, and setup.md's Output section lists many
required elements, which the executor dutifully renders as sections. (2) Setup runs as one long
monologue at the end instead of step-by-step narration while it works ("Step 3 of 8 — Gmail connected")
with a short wrap. (3) Scope creep: the interview-pitch paragraph is interview.md's voice leaking into
setup — beyond setup's output contract entirely. Also note the choices table STILL says "via your
tailnet" — FT-1's vocabulary surviving in output even after the user chose desk-only. Likely fixes:
a brevity rule in SKILL.md Output Standards ("short by default; setup speaks in numbered steps as it
works and ends in ≤5 lines: what works, what's missing, one next step"), plus a setup.md line replacing
the Output prose. Tier-1 probes graded plain language but never brevity — worth a probe in the next
eval round (P9-style, graded on length budget).

## FT-3 — Next steps are phrased as commands to run, not offers

**Reported (screenshot, same setup wrap-up):** "Next step (≈20 min): Run `goodwork interview`. I'll
start from that forward-deploy hypothesis…" Asher: "This could simply be *shall I interview you* —
instead of telling the user to run the goodwork skill."

**Read:** command tokens are internal routing vocabulary leaking into the user's face — a sibling of the
plain-language rule that the rule as written doesn't catch (it bans file names/IDs/hashes/gate mechanics
but not command names). The agent is *right there*; a handoff should be an offer ("Shall I interview you
now? Takes about 20 minutes.") that the agent routes internally, never an instruction to type an
incantation. Implication reaches beyond this one line: the cold-open menu itself (Routing 1) presents
raw command tokens grouped by category — for a non-technical user it should read as things-I-can-do in
plain language ("we can figure out what good work means for you", "I can sweep your inbox"), with
command tokens as an optional power-user layer. Likely fixes: extend the plain-language core rule to
cover command names in user-facing output ("offer actions, don't instruct commands"); adjust Routing 1's
menu presentation; sweep references for "run `<command>`" phrasing in user-visible outputs (interview.md
output, prototype/daily handoffs, etc.).
