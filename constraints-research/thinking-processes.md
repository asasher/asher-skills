# TOC Thinking Processes Facilitator Reference

Source basis: TOCICO’s TP exams explicitly cover UDEs, Three-UDE Cloud, Core Conflict, CRT/CCRT, Evaporating Cloud, FRT, NBR, Prerequisite Tree, Transition Tree, and disciplined use of reservations. ([tocico.org](https://www.tocico.org/tp-practitioner-exam)) TOCICO also treats CLRs and generic TP building blocks as fundamentals. ([tocico.org](https://www.tocico.org/tp-fundamentals-exam)) Scheinkopf’s *Thinking for a Change* is explicitly a field guide with step-by-step guidelines for the five application tools and both sufficient-cause and necessary-condition logic. ([routledge.com](https://www.routledge.com/Thinking-for-a-Change-Putting-the-TOC-Thinking-Processes-to-Use/Scheinkopf/p/book/9781574441017)) Dettmer’s *Logical Thinking Process* streamlines tree construction, integrates CRTs with Clouds, and de-emphasizes the Transition Tree in favor of detailed Prerequisite Trees and project planning. ([amazon.com](https://www.amazon.com/Logical-Thinking-Process-Systems-Approach/dp/0873897234)) Goldratt’s *It’s Not Luck* is the classic novelized application of these processes. ([amazon.com](https://www.amazon.com/Its-Not-Luck-Eliyahu-Goldratt/dp/0884271153)) TOCICO’s current BOK points to the official TOCICO Dictionary and recognizes later Six Questions / Standing-on-the-Shoulders variants. ([tocico.org](https://www.tocico.org/toc-body-of-knowledge))

## Common Diagram Language

Use two edge types:

- **Sufficiency logic:** `IF cause(s), THEN effect.` Used in CRT, FRT, NBR, Transition Tree.
- **Necessary-condition logic:** `IN ORDER TO have X, WE MUST have Y.` Used in Clouds and Prerequisite Trees.

Suggested HTML/SVG conventions:

- **Entity/state:** rectangle.
- **UDE:** rectangle, red tag `UDE`.
- **DE:** rectangle, green tag `DE`.
- **Injection/action:** rounded rectangle, blue/green tag `INJ` or `ACT`.
- **Obstacle/NBR:** red-outlined hexagon or rectangle tagged `OBS` / `NBR`.
- **AND connector:** small circle/ellipse labeled `AND`; all incoming causes are jointly required.
- **Assumption:** small note attached to an edge.
- **Conflict:** double-headed line, lightning mark, or red bar between incompatible prerequisites.
- **Layout:** cause/current-condition nodes lower or left; effects/objectives higher or right. Preserve semantic edge labels, not just color.

## Facilitation Run Sheet

1. Define system boundary, goal, and necessary conditions.
2. Elicit UDEs.
3. Build CRT or Three-UDE Cloud to expose root cause / core conflict.
4. Build Evaporating Cloud and surface assumptions.
5. Create injections.
6. Test injections with FRT.
7. Run NBRs and add trim injections.
8. Convert solution to implementation with Prerequisite Tree.
9. Detail critical steps with Transition Tree or modern project plan.

## 1. UDEs

**Purpose:** Capture observable symptoms that show the system is not meeting its goal or necessary conditions.

**When to use:** First diagnostic step; also before Three-UDE Cloud or CRT.

**Facilitator procedure:**

1. Ask: “What keeps recurring despite effort?” “What do customers complain about?” “Where do we firefight?” “Which metrics are persistently off?”
2. Capture raw complaints without debating causes.
3. Rewrite each into a well-formed UDE.
4. Remove duplicates and merge near-equivalents.
5. Keep 10-30 UDEs for broad diagnosis; select 3-7 strong UDEs for quick cloud work.
6. Check each UDE against the goal: “Why is this undesirable for the system?”

**Well-formed UDE statement:**

- Present-tense factual condition.
- Observable or evidence-backed.
- Single effect, not a bundle.
- Undesirable relative to the agreed goal.
- Not a proposed solution.
- Not framed as blame.
- Not already a root-cause theory.

Good: `Customer onboarding takes more than 30 days for 40% of enterprise accounts.`  
Weak: `Sales is bad.` `We need a better CRM.` `Support is incompetent.`

**Visual:** UDE nodes are top-level symptom rectangles in CRT, usually near the top of a bottom-up tree.

**Common mistakes:** listing absences of preferred solutions, mixing causes and effects, using vague adjectives, blaming departments, accepting compound statements, skipping goal relevance.

## 2. Current Reality Tree

**Purpose:** Explain how scattered UDEs arise from a small number of shared causes, ideally one core problem or core conflict.

**When to use:** When symptoms look unrelated, debate is fragmented, or leadership is treating symptoms independently.

**Construction procedure:**

1. Place UDEs near the top.
2. Pick two UDEs and ask: “Could one cause the other?” If yes, draw sufficiency edge.
3. If neither causes the other, ask: “What condition could cause both?”
4. Insert missing intermediate entities until every link reads cleanly.
5. Read every link aloud: `IF [cause], THEN [effect].`
6. For multiple causes, use `AND`: `IF A AND B, THEN C.`
7. Apply CLRs continuously.
8. Add more UDEs into the same structure.
9. Identify low-level entities that feed many paths upward.
10. Test candidate root cause: “If we removed or changed this, would most UDEs disappear?”

**Root cause / core conflict heuristic:** In a well-bounded system, TOC facilitators expect most UDEs, often roughly 70% or more, to trace to one core problem or one core conflict. If the tree does not converge, revisit system boundary, UDE quality, or hidden segmentation.

**Visual:** Bottom-up. Root/core problem low. UDEs high. Arrows point from cause to effect. AND connectors merge jointly sufficient causes.

**Common mistakes:** building a chronology instead of causality, accepting `A causes B` without a mechanism, overusing AND, forcing one root across multiple systems, choosing an external fact as “root cause,” stopping at a symptom with many arrows.

## 3. Evaporating Cloud / Conflict Resolution Diagram

**Purpose:** Resolve the conflict that keeps a core problem in place.

**When to use:** When a root cause persists because people feel forced into incompatible actions.

**5-box structure:**

- `A` Objective: shared goal.
- `B` Requirement: one necessary condition for A.
- `C` Requirement: another necessary condition for A.
- `D` Prerequisite/want/action needed for B.
- `D'` Opposing prerequisite/want/action needed for C.

**Construction procedure:**

1. Name the conflict as two opposing wants: `D` vs `D'`.
2. Ask one side: “Why is D necessary?” Write requirement `B`.
3. Ask the other side: “Why is D' necessary?” Write requirement `C`.
4. Ask: “What common objective needs both B and C?” Write `A`.
5. Read: `In order to A, we must B`; `in order to B, we must D`; same for C/D'.
6. Mark D and D' as mutually incompatible.
7. Surface assumptions on every arrow: A-B, A-C, B-D, C-D', and D-D'.
8. Generate injections that invalidate at least one assumption while preserving A, B, and C.
9. Reject compromises that merely weaken both sides.
10. Carry best injections into FRT.

**Visual:** Classic layout: A left, B/C middle, D/D' right. Arrows usually point from prerequisite toward objective (`D -> B -> A`, `D' -> C -> A`). Conflict line between D and D'.

**Common mistakes:** putting people in boxes instead of needs/actions, making B/C negotiable wants, hiding the real assumption, solving by compromise, attacking a person’s position rather than breaking an assumption.

## 4. FRT and Negative Branch Reservations

**Purpose:** Show that injections produce desired effects without unacceptable side effects.

**When to use:** After candidate injections exist.

**FRT procedure:**

1. Convert UDEs to DEs.
2. Place injections low in the diagram.
3. Add existing enabling conditions.
4. Build upward with `IF...THEN` sufficiency logic.
5. Add intermediate effects until DEs are reached.
6. Validate every edge with CLRs.
7. Check whether all major UDEs are neutralized.

**NBR procedure:**

1. Ask: “If we implement this injection, what bad thing could happen?”
2. Build a sufficiency branch from injection to negative effect.
3. Do not dismiss the reservation; model it.
4. Find the earliest assumption or causal link that can be broken.
5. Add a trim injection.
6. Re-test the FRT with the trim injection included.

**Visual:** FRT bottom-up, injections low, DEs high. NBRs are red side branches to negative effects; trim injections cross into the branch.

**Common mistakes:** making FRT a wish list, omitting existing conditions, treating NBRs as resistance, adding trim injections too late, proving only local benefits.

## 5. Prerequisite Tree

**Purpose:** Turn the desired future into ordered intermediate objectives by exposing obstacles.

**When to use:** After FRT/NBR proves directionally sound.

**Construction procedure:**

1. State the ambitious objective.
2. Ask: “Why can’t we have this now?”
3. Write each answer as an obstacle.
4. For each obstacle, write an intermediate objective that overcomes it.
5. Check each IO is a state, not an action.
6. Sequence IOs with necessary-condition logic: `In order to achieve IO-X, must IO-Y already exist?`
7. Build an IO map from current state to objective.
8. Convert IOs into work packages only after logic is stable.

**Visual:** Objective top or far right. IOs below/left. Obstacles adjacent to the gap they block. Arrows mean prerequisite, not causation.

**Common mistakes:** writing tasks instead of IOs, skipping obstacles, sequencing by calendar preference, hiding political constraints, making the objective vague.

## 6. Transition Tree

**Purpose:** Detail the action logic that moves from current reality to an IO or objective.

**When to use:** For high-risk, ambiguous, or coordination-heavy implementation steps.

**Construction procedure:**

1. Select one IO or objective from the Prerequisite Tree.
2. State the current reality.
3. State the need for the next action.
4. State the specific action.
5. State the expected effect.
6. Read: `IF current reality AND need/action, THEN expected effect.`
7. Make the expected effect the next current reality.
8. Repeat until the IO is achieved.
9. Add owners, dates, and dependencies after the logic is accepted.

**Visual:** Bottom-up or left-to-right chain. Current states and effects are rectangles; actions are rounded rectangles. AND connectors combine current condition, need, and action.

**Common mistakes:** jumping from objective to project schedule, vague actions, missing expected effects, no owner, no testable completion state.

## 7. The Three Questions

- **What to change?** UDEs, CRT, Three-UDE Cloud, Core Conflict.
- **What to change to?** Cloud injections, FRT, NBR trim injections.
- **How to cause the change?** Prerequisite Tree, Transition Tree, project plan / S&T Tree.

Use these as the session spine. Do not let the group design actions before agreeing on the problem and direction.

## 8. Categories of Legitimate Reservation

Use these as AI prompts on every node and edge:

1. **Clarity:** Is the wording unambiguous?
2. **Entity existence:** Is this statement real in the relevant system?
3. **Causality existence:** Does this cause really produce this effect?
4. **Cause insufficiency:** Is another necessary cause missing?
5. **Additional cause:** Is there another independent cause of this effect?
6. **Cause-effect reversal:** Is the arrow backward?
7. **Predicted effect existence:** If this cause exists, what else should we observe?
8. **Tautology:** Is the cause just restating the effect?

## 9. Simplified / Modern Variants

**Goldratt later simplification:** Use lighter-weight questioning when full trees are too costly: What is the power of the change/technology? What limitation does it remove? What old rules existed because of that limitation? What new rules are now needed? What must be changed to support the new rules? How do we cause the change? TOCICO recognizes Six Questions / Standing-on-the-Shoulders materials in its BOK. ([tocico.org](https://www.tocico.org/toc-body-of-knowledge))

**Dettmer Logical Thinking Process:** Adds stronger front-end goal clarification, often via Goal Tree; integrates CRT and Cloud work more tightly; uses IO maps and detailed prerequisite planning more heavily; may replace classic Transition Trees with detailed PrT plus project management. ([amazon.com](https://www.amazon.com/Logical-Thinking-Process-Systems-Approach/dp/0873897234))

**Three-cloud method:** Select three strong UDEs from different parts of the system, build one cloud per UDE, compare the D/D' conflicts, abstract the common conflict, then validate it with a compact CRT/CCRT. TOCICO’s practitioner structure explicitly tests UDEs, Three-UDE Cloud, Core Conflict, CRT/CCRT, injections, FRT, NBR, PrT, and TT in that flow. ([tocico.org](https://www.tocico.org/tp-practitioner-exam))