---
name: eloquent
description: Career-document and job-search workflows through one command surface — resumes/CVs (creation, ATS optimization, tailoring), cover letters, LinkedIn, job-description analysis, interview prep, salary negotiation, and offer comparison.
argument-hint: "[command] [target]"
user-invocable: true
---

Eloquent career document and job-search workflows through one command surface. Load the narrow reference file for the requested task, preserve truthfulness, and produce usable artifacts.

## Core Rules

- Do not invent experience, employers, credentials, compensation, awards, publications, or metrics.
- Separate verified facts from inferred positioning. Label estimates clearly.
- When improving text, keep the candidate's real scope, seniority, and domain intact.
- Prefer specific evidence: scope, scale, tools, outcomes, audience, constraints, and before/after deltas.
- If a task depends on current salary, market, company, or job-posting facts, verify with current sources before giving concrete guidance.
- If inputs are missing, ask for the smallest missing piece needed to proceed.

## Inputs To Gather

Ask only for missing inputs relevant to the command:

- Resume or CV text
- Target role, seniority, industry, location, and job description
- Candidate constraints: remote, visa, compensation floor, industries to avoid
- Existing LinkedIn, portfolio, reference, or offer details
- Output format: bullets, rewritten section, full document, checklist, script, or comparison table

## Document Workflow

For full resume creation, use Markdown as the source of truth. Draft, revise, tailor, and approve the resume in Markdown first. Treat PDF, DOCX, HTML, and plain text as generated delivery artifacts.

Default delivery, when the user does not specify, is DOCX plus ATS-safe PDF. Ask for a different delivery target only at the delivery gate:

1. DOCX + ATS-safe PDF, recommended.
2. Markdown only.
3. HTML + PDF.
4. Plain text for job portals.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `compile` | Guided Workflow | Create a resume end-to-end from raw career material to approved Markdown and delivery files | [reference/compile.md](reference/compile.md) |
| `ats` | Resume Optimization | Check ATS compatibility, parsing risk, keywords, and formatting | [reference/ats.md](reference/ats.md) |
| `bullets` | Resume Optimization | Rewrite weak bullets into achievement-focused statements | [reference/bullets.md](reference/bullets.md) |
| `quantify` | Resume Optimization | Find credible metrics and impact numbers | [reference/quantify.md](reference/quantify.md) |
| `format` | Resume Optimization | Improve resume layout, readability, and ATS-safe structure | [reference/format.md](reference/format.md) |
| `templates` | Resume Optimization | Choose proven resume templates for DOCX, PDF, and HTML delivery | [reference/templates.md](reference/templates.md) |
| `sections` | Resume Optimization | Build summaries, skills, experience, education, and supplemental sections | [reference/sections.md](reference/sections.md) |
| `analyze-job` | Job Search Strategy | Parse a job description, score fit, identify gaps, and decide whether to apply | [reference/analyze-job.md](reference/analyze-job.md) |
| `tailor` | Job Search Strategy | Customize a resume for a specific posting while staying truthful | [reference/tailor.md](reference/tailor.md) |
| `versions` | Job Search Strategy | Manage master resumes and tailored versions | [reference/versions.md](reference/versions.md) |
| `cover-letter` | Supporting Documents | Write a personalized cover letter from resume and job details | [reference/cover-letter.md](reference/cover-letter.md) |
| `linkedin` | Supporting Documents | Optimize LinkedIn headline, About, Experience, and recruiter keywords | [reference/linkedin.md](reference/linkedin.md) |
| `portfolio-case-study` | Supporting Documents | Turn resume achievements into portfolio case studies | [reference/portfolio-case-study.md](reference/portfolio-case-study.md) |
| `references` | Supporting Documents | Build and prepare professional reference lists | [reference/references.md](reference/references.md) |
| `interview` | Interview and Negotiation | Generate STAR stories, questions, talking points, and prep plans | [reference/interview.md](reference/interview.md) |
| `salary` | Interview and Negotiation | Research market ranges and prepare negotiation scripts | [reference/salary.md](reference/salary.md) |
| `compare-offers` | Interview and Negotiation | Compare offers by compensation, risk, role fit, and tradeoffs | [reference/compare-offers.md](reference/compare-offers.md) |
| `tech` | Specialized Roles | Optimize software, PM, data, DevOps, and other technical resumes | [reference/tech.md](reference/tech.md) |
| `executive` | Specialized Roles | Build VP, C-suite, board, and senior leadership resumes | [reference/executive.md](reference/executive.md) |
| `academic-cv` | Specialized Roles | Build academic CVs for faculty, research, postdoc, and teaching roles | [reference/academic-cv.md](reference/academic-cv.md) |
| `creative` | Specialized Roles | Balance portfolio-forward design with ATS compatibility | [reference/creative.md](reference/creative.md) |
| `career-change` | Specialized Roles | Translate experience and transferable skills for a new field | [reference/career-change.md](reference/career-change.md) |

## Routing

1. **No argument**: show the command menu grouped by category, then show the Common Workflows list as quick-start hints. Ask which workflow or command the user wants to run.
2. **First word matches a command**: load the matching reference and follow it. Everything after the command name is the target.
3. **First word does not match**: infer the best command from the user's request, state the inferred command, load its reference, and proceed. If the user asks to create, make, build, draft, or start a resume without naming a command, infer `compile`.
4. **Compound requests**: load references in workflow order, not all at once. For example: `analyze-job` before `tailor`, `tailor` before `cover-letter`, `bullets` before `ats` when rewriting content first.

## Common Workflows

- Scratch resume for a specific job: `compile` orchestrates `analyze-job` -> `sections` -> `bullets` -> `quantify` -> `format` -> `ats` -> `tailor` -> delivery.
- Scratch master resume: `compile` orchestrates `sections` -> `bullets` -> `quantify` -> `format` -> `ats` -> delivery -> `versions`.
- Full application pass: `analyze-job` -> `tailor` -> `ats` -> `cover-letter`.
- Resume refresh: `sections` -> `bullets` -> `quantify` -> `format` -> `ats`.
- Interview package: `analyze-job` -> `interview` -> `references`.
- Offer decision: `salary` -> `compare-offers`.
- Career pivot: `career-change` -> `sections` -> `tailor` -> `cover-letter`.

## Output Standards

- Make edits directly when the user provides text and asks for improvement.
- Preserve a concise explanation of what changed and why.
- For scoring, include the rubric and confidence level.
- For scripts, emails, cover letters, summaries, and bullets, provide polished final text first, then notes.
- For uncertain metrics, give discovery questions or ranges instead of fake precision.
