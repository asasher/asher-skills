# Recap what shipped

Create a report a tired executive can understand in 30–60 seconds. Use `writing-for-humans` for the prose and `diagram-design` for visual explanations and charts. Lead with what shipped and why it matters; keep the evidence available behind the summary.

## Resolve the period

Use the current repository and the user's requested range. With no range, use the past seven days. Interpret `last week` as seven days ending now, and `last month` or `last 6 months` as that many calendar months ending now. Clamp a missing day to the destination month's last day. Named calendar periods such as `August 2026` use that complete period; an explicit end date includes that day.

Resolve the range once to a start-inclusive, end-exclusive interval in the user's timezone, falling back to UTC. Cap future endpoints at generation time. Show the exact dates, timezone, and generation time in the report so the interpretation is visible. Resolve an ambiguous or reversed explicit range before collecting history.

## Establish what shipped

Read the environment playbook if present for the base branch and release process. Otherwise use repository metadata and existing release documentation. Recap can run without a playbook, artifact bucket, or build environment.

1. Collect release or deployment records for the interval and map their revisions to delivered changes, including changes merged before the interval. Read merged PRs, linked tickets and comments, published specs and proof, and relevant Git history. Use `gh` with pagination; partition queries that hit search limits. Include direct-to-base commits. Retrieve older context where needed to explain an in-period delivery.
2. Establish the delivery boundary the project actually uses: deployment for a service, a published version for a package, or the documented distribution boundary. Use its event timestamp for inclusion. A draft release, a closed ticket, or a child PR merged into a spec branch is insufficient evidence of shipping. Trace split children through promotion and release; count the resulting outcome once.
3. Where only a base-branch merge is verifiable, show the work separately as **Merged; release unconfirmed**, using its merge date. State this limitation prominently. Label a Git-only account as partial when integration dates or release coverage cannot be established. Access failures and truncated history mean incomplete coverage, not an empty period.
4. Account for rollbacks, removals, fixes, and limited rollouts through the period's end. State who actually received a change and whether it was withdrawn. Label any later information separately with its date. Keep open or unreleased work outside shipped totals.

For each candidate, retain the delivery event and date, affected audience, source links, and enough before/after evidence to explain the outcome. Group related PRs, commits, and tickets by the change people experience. Retain smaller maintenance changes in a compact supporting list. Every included source belongs to an outcome or that list. Count shipped outcomes once; report PR or release-event counts as separate, explicitly labeled measures.

## Make the main view a quick read

Keep the main view readable in 30–60 seconds, even for a six-month period. Lead with one sentence about the period, a few useful numbers, and the most consequential shipped outcomes. Group a busy period by theme. Each highlight gets an outcome title and one or two short sentences about who benefits and what they can now do. For example, "Drafts survive a lost connection" communicates more than "Add persistence middleware".

Keep required user actions, material rollout limits, reversals, and coverage gaps visible beside the affected claim. Distinguish intended benefits from measured results. Explain necessary technical terms on first use.

Put smaller changes, system behavior, recorded reasons and tradeoffs, follow-ups, and descriptive source links in expandable details. Include these only where they help explain the outcome; each outcome needs no fixed set of explanatory sections. Ground claims in the record and mark inference when necessary. A missing rationale needs mention only when it materially limits understanding. Preserve the full supporting account without making the executive read it to understand what shipped.

## Choose useful metrics and visuals

Select metrics and charts for the period's evidence and story. Useful candidates include confirmed shipped outcomes, merged PRs, a delivery timeline, or activity by day or hour. A few numbers may be enough for a quiet period; use a chart when it makes a pattern easier to see. Use `diagram-design` in embedded mode for charts and visual explanations of related outcomes.

- Define each metric's unit and inclusion rule. Shipped outcomes use the delivery boundary above; merged PRs use their merge timestamps in the resolved interval. Deduplicate PRs by repository and number. A release containing older PRs can increase shipped outcomes without increasing that period's merged-PR count.
- Label release events, shipped outcomes, and merged PRs separately. Keep unconfirmed releases outside shipped totals. Retain withdrawn or limited outcomes' status alongside the numbers they affect.
- For activity charts, name the event being counted, the time bucket, and the timezone. Describe "most active" as observed merge or shipment activity; timestamps do not establish hours worked or productivity.
- Use complete, comparable coverage for trends and comparisons. Label partial metrics and coverage gaps; omit numbers the evidence cannot support. An unavailable count is not zero.
- Give each chart a takeaway title, readable labels, and a short caption with its measure and source. Prefer a few legible charts over a dashboard of every available statistic.

## Deliver the HTML

Write one self-contained HTML file with inline CSS and no required network assets or JavaScript. Use the requested output location, or `reports/backlog-recap-<start-date>-<end-date>.html`; choose a unique suffix if that path already exists. Keep the document readable on mobile, desktop, and in print, with semantic headings, sufficient contrast, and descriptive links. Use native HTML details for supporting material, keep the main view concise, and make expanded content readable in print. Add navigation when the supporting account needs it.

Include the project, resolved period, executive overview, selected metrics or visuals, expandable outcome details, and a source/coverage note. Keep merged work with unconfirmed releases clearly separate; place routine follow-ups in supporting detail. An empty period still gets a report stating that no shipped changes were found in the checked sources. If access failed, name the missing coverage and label the report incomplete.

Run the diagram skill's checks on each embedded figure. Inspect the rendered file at narrow and wide widths when a browser is available; check headings, chart labels, overflow, source links, and expandable details. Otherwise inspect the HTML and disclose that visual verification was unavailable. Confirm the main view tells the shipping story without opening details. Check every outcome's date, delivery status, and supporting evidence, and reconcile every metric and chart with its source records before handback.

Return a clickable file link and a short summary of the period and coverage. Tracker state stays unchanged. A request for a report authorizes the local artifact; publish through `to-web` when the user requests publication or a shareable URL, using existing authorization. If publication is unavailable, return the local file and identify that remaining blocker.
