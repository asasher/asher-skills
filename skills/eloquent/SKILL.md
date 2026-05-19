---
name: eloquent
description: Use when the user wants help with resumes, CVs, ATS optimization, resume bullets, job description analysis, resume tailoring, cover letters, LinkedIn profiles, interview prep, salary negotiation, offer comparison, references, portfolios, academic CVs, executive resumes, technical resumes, creative resumes, career changes, or resume version management. Provides one entry point with subcommands that load focused reference guidance only when needed.
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

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `ats` | Resume Optimization | Check ATS compatibility, parsing risk, keywords, and formatting | [reference/resume-ats-optimizer.md](reference/resume-ats-optimizer.md) |
| `bullets` | Resume Optimization | Rewrite weak bullets into achievement-focused statements | [reference/resume-bullet-writer.md](reference/resume-bullet-writer.md) |
| `quantify` | Resume Optimization | Find credible metrics and impact numbers | [reference/resume-quantifier.md](reference/resume-quantifier.md) |
| `format` | Resume Optimization | Improve resume layout, readability, and ATS-safe structure | [reference/resume-formatter.md](reference/resume-formatter.md) |
| `sections` | Resume Optimization | Build summaries, skills, experience, education, and supplemental sections | [reference/resume-section-builder.md](reference/resume-section-builder.md) |
| `analyze-job` | Job Search Strategy | Parse a job description, score fit, identify gaps, and decide whether to apply | [reference/job-description-analyzer.md](reference/job-description-analyzer.md) |
| `tailor` | Job Search Strategy | Customize a resume for a specific posting while staying truthful | [reference/resume-tailor.md](reference/resume-tailor.md) |
| `versions` | Job Search Strategy | Manage master resumes and tailored versions | [reference/resume-version-manager.md](reference/resume-version-manager.md) |
| `cover-letter` | Supporting Documents | Write a personalized cover letter from resume and job details | [reference/cover-letter-generator.md](reference/cover-letter-generator.md) |
| `linkedin` | Supporting Documents | Optimize LinkedIn headline, About, Experience, and recruiter keywords | [reference/linkedin-profile-optimizer.md](reference/linkedin-profile-optimizer.md) |
| `portfolio-case-study` | Supporting Documents | Turn resume achievements into portfolio case studies | [reference/portfolio-case-study-writer.md](reference/portfolio-case-study-writer.md) |
| `references` | Supporting Documents | Build and prepare professional reference lists | [reference/reference-list-builder.md](reference/reference-list-builder.md) |
| `interview` | Interview and Negotiation | Generate STAR stories, questions, talking points, and prep plans | [reference/interview-prep-generator.md](reference/interview-prep-generator.md) |
| `salary` | Interview and Negotiation | Research market ranges and prepare negotiation scripts | [reference/salary-negotiation-prep.md](reference/salary-negotiation-prep.md) |
| `compare-offers` | Interview and Negotiation | Compare offers by compensation, risk, role fit, and tradeoffs | [reference/offer-comparison-analyzer.md](reference/offer-comparison-analyzer.md) |
| `tech` | Specialized Roles | Optimize software, PM, data, DevOps, and other technical resumes | [reference/tech-resume-optimizer.md](reference/tech-resume-optimizer.md) |
| `executive` | Specialized Roles | Build VP, C-suite, board, and senior leadership resumes | [reference/executive-resume-writer.md](reference/executive-resume-writer.md) |
| `academic-cv` | Specialized Roles | Build academic CVs for faculty, research, postdoc, and teaching roles | [reference/academic-cv-builder.md](reference/academic-cv-builder.md) |
| `creative` | Specialized Roles | Balance portfolio-forward design with ATS compatibility | [reference/creative-portfolio-resume.md](reference/creative-portfolio-resume.md) |
| `career-change` | Specialized Roles | Translate experience and transferable skills for a new field | [reference/career-changer-translator.md](reference/career-changer-translator.md) |

## Aliases

Map legacy skill names and natural wording to the command table:

- `resume-ats-optimizer` -> `ats`
- `resume-bullet-writer` -> `bullets`
- `resume-quantifier` -> `quantify`
- `resume-formatter` -> `format`
- `resume-section-builder` -> `sections`
- `job-description-analyzer` -> `analyze-job`
- `resume-tailor` -> `tailor`
- `resume-version-manager` -> `versions`
- `cover-letter-generator` -> `cover-letter`
- `linkedin-profile-optimizer` -> `linkedin`
- `portfolio-case-study-writer` -> `portfolio-case-study`
- `reference-list-builder` -> `references`
- `interview-prep-generator` -> `interview`
- `salary-negotiation-prep` -> `salary`
- `offer-comparison-analyzer` -> `compare-offers`
- `tech-resume-optimizer` -> `tech`
- `executive-resume-writer` -> `executive`
- `academic-cv-builder` -> `academic-cv`
- `creative-portfolio-resume` -> `creative`
- `career-changer-translator` -> `career-change`
- `resume-skills` -> `eloquent`

## Routing

1. **No argument**: show the command menu grouped by category and ask what the user wants to do.
2. **First word matches a command or alias**: load the matching reference and follow it. Everything after the command name is the target.
3. **First word does not match**: infer the best command from the user's request, state the inferred command, load its reference, and proceed.
4. **Compound requests**: load references in workflow order, not all at once. For example: `analyze-job` before `tailor`, `tailor` before `cover-letter`, `bullets` before `ats` when rewriting content first.

## Common Workflows

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
