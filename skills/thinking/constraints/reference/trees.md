# trees — the thinking processes (dig · cloud)

Goldratt's logic tools, for the two moments plain hunting isn't enough: **`dig`** when symptoms are scattered
or the constraint smells like a policy/belief (find the *core problem*), and **`cloud`** when a needed change
is blocked by a conflict (find the *injection*). Both are built **with** the user, one link at a time, on the
page — never delivered as a finished diagram. Reading a causal link aloud and asking "is that actually true
here?" is the method; the diagram is the record.

Diagram conventions (node classes, directions) are in [artifact.md](artifact.md). Trees land in the **Find**
section; clouds land in **Plan**.

## dig — from scattered symptoms to the core problem

Two logic modes, so the user can check your links: sufficiency ("IF x THEN y") builds trees; necessity
("in order to have X we must have Y") builds clouds.

### 1. Collect UDEs (undesirable effects)

"What keeps recurring despite effort? What do customers complain about? Which number is persistently off?"
Collect 5–10, then rewrite each as a **well-formed UDE**: present-tense, observable, single effect, undesirable
relative to the goal — not a solution ("we need a CRM"), not blame ("sales is lazy"), not a cause-theory.
Good: *"Enterprise onboarding exceeds 30 days for 40% of accounts."* Show the rewritten list for confirmation.

### 2. Connect them (compact Current Reality Tree)

Take two UDEs: "could one cause the other?" If yes, draw the sufficiency edge; if no, "what condition could
cause *both*?" — add the intermediate. Read every link aloud in IF–THEN form and let the user veto. Add UDEs
one at a time into the same structure. Render the Mermaid `flowchart BT` after every couple of links so the
user watches the tree converge.

Scrutinize links with the reservations that matter most in practice (Categories of Legitimate Reservation,
abridged): *is the arrow backwards? · is a second cause needed for this effect (missing AND)? · is there
another independent cause? · if this cause is real, what else should we observe — do we?* Use the last one to
send the user after cheap confirming evidence.

### 3. Name the core

A candidate core problem is a low node feeding most paths: "if this one condition changed, which UDEs
disappear?" Expect roughly 70% of UDEs to trace to one core in a well-bounded system — if nothing converges,
the boundary is wrong (two systems on one page) or the UDEs are too vague; fix that rather than forcing a root.
Tag it `:::core`.

**Shortcut — the three-cloud method** when a full tree is heavy: pick the 3 strongest UDEs from different
corners of the system, build a mini-cloud for each (below), and look for the same D vs D′ tension underneath
all three — that shared conflict *is* the core problem, and usually a paradigm constraint in the flesh.

*Done when:* the user looks at the core and says some version of "yes — that's the thing." The core goes onto
the suspects board in [find.md](find.md) with the tree as its evidence, and the hunt resumes there.

## cloud — evaporate a conflict

For when action stalls on a tug-of-war: exploit vs "but we can't idle the team", delegate vs "but quality",
publish vs "but it's not ready". The cloud's claim: every stubborn conflict hides an **assumption** that can be
broken, so nobody has to lose.

### Build it (boxes in this order)

1. **D / D′** — the two opposing wants, as actions: "protect two review hours daily" vs "stay available for
   escalations". Wants, not people.
2. **B** (why D: what *need* does it serve?) and **C** (why D′). Needs, not preferences — B and C are both
   legitimate, say so out loud; it defuses the fight.
3. **A** — the shared objective needing both B and C. Read the whole thing back: "In order to [A] we must [B];
   in order to [B] we must [D] — and in order to [A] we must [C]; in order to [C] we must [D′]. But D and D′
   can't coexist."

### Break it

Surface assumptions on each arrow — "why does B *require* D?" — and list them under the diagram. Most clouds
break on B→D or C→D′ ("escalations need *me*" → they need *a fast answer*, which a rotation or a runbook also
provides). Generate **injections**: actions that invalidate one assumption while preserving A, B, *and* C.
Reject the compromise that half-feeds both needs — if the user proposes splitting the difference, hunt the
assumption harder.

*Done when:* the user picks an injection they'd actually run. It goes into the Plan section (tagged `:::inj`
on the cloud) and becomes an experiment card in [act.md](act.md) — an injection is a hypothesis like any other.
