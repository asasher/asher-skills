# Recap what shipped

Create a report someone outside the development team can read and use. Explain changes to people's experience and the system's behavior, with sources for the claims.

## Resolve the period

Use the current repository and the user's requested range. With no range, use the past seven days. Interpret `last week` as seven days ending now, and `last month` or `last 6 months` as that many calendar months ending now. Clamp a missing day to the destination month's last day. Named calendar periods such as `August 2026` use that complete period; an explicit end date includes that day.

Resolve the range once to a start-inclusive, end-exclusive interval in the user's timezone, falling back to UTC. Cap future endpoints at generation time. Show the exact dates, timezone, and generation time in the report so the interpretation is visible. Resolve an ambiguous or reversed explicit range before collecting history.

## Establish what shipped

Read the environment playbook if present for the base branch and release process. Otherwise use repository metadata and existing release documentation. Recap can run without a playbook, artifact bucket, or build environment.

1. Collect release or deployment records for the interval and map their revisions to delivered changes, including changes merged before the interval. Read merged PRs, linked tickets and comments, published specs and proof, and relevant Git history. Use `gh` with pagination; partition queries that hit search limits. Include direct-to-base commits. Retrieve older context where needed to explain an in-period delivery.
2. Establish the delivery boundary the project actually uses: deployment for a service, a published version for a package, or the documented distribution boundary. Use its event timestamp for inclusion. A draft release, a closed ticket, or a child PR merged into a spec branch is insufficient evidence of shipping. Trace split children through promotion and release; count the resulting outcome once.
3. Where only a base-branch merge is verifiable, show the work separately as **Merged; release unconfirmed**, using its merge date. State this limitation prominently. Label a Git-only account as partial when integration dates or release coverage cannot be established. Access failures and truncated history mean incomplete coverage, not an empty period.
4. Account for rollbacks, removals, fixes, and limited rollouts through the period's end. State who actually received a change and whether it was withdrawn. Label any later information separately with its date. Keep open or unreleased work outside shipped totals.

For each candidate, retain the delivery event and date, affected audience, source links, and enough before/after evidence to explain the outcome. Group related PRs, commits, and tickets by the change people experience. Retain smaller maintenance changes in a compact supporting list. Every included source belongs to an outcome or that list; counts describe outcomes rather than commits or tickets.

## Explain the changes

Lead with a short overview of the most consequential outcomes. For each outcome, answer these questions in plain language, using headings only where they help:

- **What changed for people?** Who is affected, what they could do before, and what they can do now. Mention any action they need to take.
- **What changed in the system?** Explain observable behavior such as retrying a failed payment, retaining a draft, or restricting access. For internal maintenance, say when there is no direct change to the user's experience.
- **Why?** Describe the problem and recorded reason for the change. Distinguish intended benefits from measured results.
- **Why this approach?** Include documented tradeoffs, alternatives declined, and deliberately excluded scope when they explain the outcome. If a material reason is absent, say it was not recorded; keep inference explicitly tentative.
- **What's the situation now?** Describe availability, rollout limits, reversals, and known remaining issues at the end of the period. Link recorded follow-up work without promising a delivery date.

Write titles about outcomes: "Drafts survive a lost connection" communicates more than "Add persistence middleware". Explain necessary technical terms on first use. Put descriptive source links beside claims or in expandable details; issue numbers and commit subjects alone are not explanations. Ground motivations, alternatives, adoption, and performance claims in the record.

## Deliver the HTML

Write one self-contained HTML file with inline CSS and no required network assets or JavaScript. Use the requested output location, or `reports/backlog-recap-<start-date>-<end-date>.html`; choose a unique suffix if that path already exists. Keep the document readable on mobile, desktop, and in print, with semantic headings, sufficient contrast, and descriptive links. For longer periods, group outcomes by theme and provide an in-page contents list.

Include the project, resolved period, overview, outcome explanations, and a source/coverage note. Add separate sections for merged work with unconfirmed releases and material follow-ups when present. An empty period still gets a report stating that no shipped changes were found in the checked sources. If access failed, name the missing coverage and label the report incomplete.

Inspect the rendered file at narrow and wide widths when a browser is available; check headings, overflow, and source links. Otherwise inspect the HTML and disclose that visual verification was unavailable. Check every outcome's date, delivery status, and supporting evidence before handback.

Return a clickable file link and a short summary of the period and coverage. Tracker state stays unchanged. A request for a report authorizes the local artifact; publish through `to-web` when the user requests publication or a shareable URL, using existing authorization. If publication is unavailable, return the local file and identify that remaining blocker.
