# Pose & Frame

The opening two steps: turn a felt uncertainty into a trackable question (`new`), then build the board it
will be tracked on (`frame`). One question at a time, each anchored with your working guess so the user
corrects rather than composes.

## Pose (`new "<question>"`)

### 1. Triage — is this a credence question at all?

Listen to the question's shape before operationalizing it. Three good types (forecast / diagnosis /
standing — see method.md) and three impostors:

- **A value question.** "Should I want to stay in this job?" No observation settles a preference. Say so
  plainly; offer to extract any factual load-bearing sub-questions ("would a move cost me money" *is*
  trackable) and track those.
- **A malformed question.** A loaded word is doing the work: "Is my startup *really* viable?", "Is this
  team *actually* dysfunctional?" Don't frame it — rework it. Ban the loaded word and ask what observable
  the user is actually worried about; usually one word unbundles into two or three answerable questions
  ("will we hit default-alive by Q1", "will either senior engineer quit this year"). Pick the one that
  bites hardest; note the others as candidate questions. If the confusion runs deeper than a quick unbundle
  — the user keeps circling, no substitution satisfies — suggest the question may want *dissolving* rather
  than answering (the `dissolve` skill exists for exactly this), and let them choose.
- **Too small.** Resolvable with one look ("is the meeting tomorrow?") — just tell them to look, or take it
  as a `log` line for the calibration ledger. The apparatus is for questions that need *many* looks.

### 2. Operationalize

Metaculus discipline, conversationally. Draft the sharpened question yourself and offer it for correction:

- **Claim** — one sentence a stranger could referee.
- **Resolution criteria** — what exactly counts as yes/no (or as "hypothesis confirmed"), decided by what
  source. Kill the wiggle words: *soon*, *successful*, *works* become dates and numbers.
- **Horizon** — resolution date (forecast), review cadence (standing), or "resolved when we'd act on it"
  (diagnosis).
- **The rent** — the decision this belief feeds and the threshold that flips it: "above ~60% we renew; below
  ~30% we start sourcing a replacement." If no decision at any threshold, say the honest thing: this is
  curiosity, and a `log` line serves it better than a folder.

*Done when:* the user has said "yes, that's my question" to a sharpened claim with type, criteria, horizon,
and decision + threshold. **Now** scaffold the folder ([artifact.md](artifact.md)) with that claim and fill
the Question section — the page starts existing only once there is a question worth a page.

## Frame (`frame`)

### 3. The hypothesis board

**Silent generation first** (anti-anchoring): draft your own 3–5 candidate hypotheses *before* asking the
user for theirs, then merge. Hypotheses should be competing stories, roughly mutually exclusive, each one
sentence with a name short enough for a column header. For forecasts the board may be just *happens /
doesn't* — but ask whether "happens late" or "happens differently" deserves its own column; the middle
outcome is where forecasts usually hide.

Always add **something else** — the explicit admission that the truth may not be on the board. Give it
real mass (rarely under 5%, more for open-ended diagnoses). It is the misfit alarm: when evidence starts
fitting nothing else, its growth is the signal to reopen the board.

### 4. The base-rate gate

Before any case-specific detail is discussed — enforce this even when the user arrives bursting with
details — pin the **reference class**: "situations that looked like this one from the outside." Name it on
the page. Where does the base rate come from? In order of pedigree: a real dataset or study, the user's own
counted experience ("of the last ~10 vendors like this…"), or a rough placeholder — label which. If the
user resists the outside view ("but this case is different"), write the inside-view arguments down as
*case evidence for later cards* — they'll get counted, once, at their measured strength, which is the whole
point.

### 5. Priors

Elicit per hypothesis in natural frequencies ("of 100 such situations, how many turn out to be ⟨H⟩?"),
ranges welcome, ends capped at 1–99. Then set your **own** priors from the same reference class —
independently, and say so when you differ. Both tracks go on the board and open the trajectory log as its
first appended row.

*Done when:* the board renders — every hypothesis with both priors and a pedigree label, *something else*
holding named mass — and the first trajectory row is appended. The natural exit is straight into `hunt`:
"what's the cheapest look that would split your top two?"
