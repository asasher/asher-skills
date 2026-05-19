
# Compile

## Purpose

Use `compile` when the user wants to create, make, build, draft, or start a resume and does not want to manually choose each subcommand. It is the guided end-to-end workflow from raw career material to approved Markdown and delivery files.

## Default Approach

- Use Markdown as the editable source of truth.
- Iterate until the Markdown resume is approved.
- Export delivery files only after approval.
- Default delivery is DOCX plus ATS-safe PDF.
- Keep every claim truthful and traceable to user-provided evidence.

## Start Here

Ask one setup question first:

```text
Are we building this for:
1. A specific job posting, recommended if you have one
2. A general master resume
3. A role family, like Senior PM or Backend Engineer
```

Then ask only for the missing inputs needed for that branch.

## Branches

### Specific Job Posting

Workflow:

```text
analyze-job -> sections -> bullets -> quantify -> format -> ats -> tailor -> delivery
```

Use when the user has a job description or a known target company and role.

Minimum inputs:

- Job description or posting URL
- Existing resume, LinkedIn, or raw work history
- Target location and constraints, if relevant

### General Master Resume

Workflow:

```text
sections -> bullets -> quantify -> format -> ats -> delivery -> versions
```

Use when the user wants a reusable source resume before tailoring to jobs.

Minimum inputs:

- Work history
- Education
- Skills
- Target role family or seniority, if known

### Role Family

Workflow:

```text
sections -> bullets -> quantify -> format -> ats -> delivery -> versions
```

Use when the user knows the category, such as Backend Engineer, Senior Product Manager, Account Executive, or Data Analyst, but has no specific posting yet.

Minimum inputs:

- Role family
- Seniority
- Relevant work history
- Skills and tools

## Phase Rules

At the end of every phase, tell the user the next phase in plain language. Do not require the user to know command names.

Example:

```text
I drafted the resume structure in Markdown. Next I will turn your responsibilities into achievement bullets.
```

Load the relevant reference file before each phase. Do not load every reference at once.

## Delivery Gate

After the Markdown resume is approved, ask:

```text
The Markdown source is ready. For delivery, I recommend DOCX + ATS-safe PDF. Choose:
1. DOCX + ATS-safe PDF, recommended
2. Markdown only
3. HTML + PDF
4. Plain text for job portals
```

If the user says they do not care, choose DOCX plus ATS-safe PDF.

## File Convention

Use clear filenames when writing files:

```text
outputs/
  first-last-master.md
  first-last-target-role.md
  first-last-target-role.docx
  first-last-target-role.pdf
  first-last-target-role.html
  first-last-target-role.txt
```

Only create formats the user requested or accepted at the delivery gate.
