# Templates

## When to Use This Skill

Use this skill when the user:
- Wants a resume template or starter layout
- Asks for a beautiful but functional resume design
- Needs a template that works for ATS and human review
- Wants a source-controlled resume source that can export to Word, PDF, or HTML
- Mentions: "resume template", "CV template", "beautiful resume", "Jake's resume", "LaTeX resume", "JSON Resume", "RenderCV"

## Scope

The skill should produce resume documents, not resume-builder applications. Treat template repositories and resume-builder projects as design references, conversion pipelines, or upstream examples only. The likely deliverables are:

- **DOCX** for editing and recruiter requests
- **Text-based PDF** for application submission
- **HTML** for portfolio pages, web resumes, or PDF generation

Do not scaffold or build a web app unless the user explicitly asks for software development work outside the resume workflow.

## Template Selection Rules

Prefer templates that:
- Keep contact information in the document body, not headers or footers
- Use one column for ATS submissions
- Use ordinary text, headings, and bullets instead of text boxes, images, icons, charts, or skill bars
- Export cleanly to DOCX, text-based PDF, or HTML
- Make content easy to edit and version
- Have an active upstream project or a stable, well-known community footprint
- Have a clear license before reuse

Avoid starting from:
- Heavy infographic resumes
- Multi-column layouts for online applications
- Templates where essential information is embedded in images
- Templates with decorative sidebars, rating bars, headshots, QR codes, or unusual fonts
- Commercial templates with unclear redistribution rights

## Recommended Starting Points

These are pointers to use as starting points, not files to copy blindly. Check the current upstream license before vendoring or redistributing any template.

### ATS-First Technical Resume

Use for software engineering, data, PM, operations, and most online applications.

- **Jake's Resume**: widely used single-column LaTeX resume. Best when the user wants a compact technical resume and is comfortable with LaTeX. Source: https://jakesresume.github.io/
- **Rover Resume**: ATS-friendly LaTeX template collection built with basic `article` class commands, designed to be easier to customize than custom-class resume templates. Best when the user wants a clean PDF resume with a little more visual personality than Jake's Resume. Licensed CC BY 4.0, so preserve attribution when reusing. Source: https://github.com/subidit/rover-resume
- **RenderCV Engineering Resumes / Sb2nov themes**: YAML-driven, source-control-friendly resumes with clean Typst output. Best when the user wants an editable structured source and reproducible PDF generation. Source: https://github.com/rendercv/rendercv
- **OpenResume**: useful as a reference for U.S. best-practice structure and parser checks. Do not recreate the app; use it to inform DOCX, PDF, or HTML output. Source: https://www.open-resume.com/

### Source-Controlled Resume System

Use when the user wants one canonical data file and multiple outputs or themes.

- **RenderCV**: YAML to PDF, good for engineers and academics who want version control. Source: https://github.com/rendercv/rendercv
- **JSON Resume**: portable JSON schema with many community themes. Best when the user wants data portability and theme swapping. Source: https://docs.jsonresume.org/themes

### HTML and Web Resume Inspiration

Use when the user wants an HTML resume, portfolio page, or styled HTML that can be printed to PDF.

- **JSON Resume themes**: useful design references for semantic HTML resumes and themeable output. Keep the result as standalone HTML/CSS or generated PDF, not a new app. Source: https://docs.jsonresume.org/themes
- **Reactive Resume templates**: useful visual references for polished resume layouts. Do not build or depend on the app unless explicitly requested. Source: https://rxresu.me/

### Designed CV or Direct-Submission Resume

Use for academic CVs, design-forward portfolios, direct referrals, or networking. Keep a separate ATS-safe version for online applications.

- **Awesome CV**: polished LaTeX CV, resume, and cover letter system. Best for a more editorial academic or professional CV, not as the default ATS submission template. Source: https://github.com/posquit0/Awesome-CV
- **Deedy Resume**: well-known one-page two-column XeTeX template. Best for visual inspiration or direct submissions; test parsing before using it in ATS-heavy workflows. Source: https://github.com/deedy/Deedy-Resume

## Default Recommendation

If the user does not specify a format:

1. Use a single-column ATS-safe layout for online applications.
2. Keep Markdown as the editable source while drafting.
3. Deliver DOCX plus text-based PDF.
4. Offer HTML only when the user needs a portfolio/web version or an HTML-to-PDF path.
5. For a code-friendly maintained template, suggest RenderCV as a generation pipeline, not an app.
6. For a familiar software-engineering LaTeX template, suggest Jake's Resume.

## Output Formats

### DOCX

Use for editable delivery and recruiter requests. Keep the layout conservative:

- Body text, headings, and simple bullets
- No text boxes for essential content
- No headers or footers for contact information
- Simple horizontal rules only when they survive export cleanly

### PDF

Use for final application submission. The PDF must be text-based:

- Text can be selected and copied
- Reading order matches the visual order
- Links remain clickable when possible
- File name is clear and professional

### HTML

Use for portfolio/web resumes or as a controlled print-to-PDF source:

- Semantic sections and headings
- Print CSS for letter/A4 output
- Inline or local CSS when portability matters
- No JavaScript dependency for rendering resume content

## How to Apply a Template

1. Choose the least risky format for the submission channel.
2. Map content into standard sections before styling: contact, summary, skills, experience, projects, education, certifications.
3. Keep section names ATS-recognizable.
4. Use layout only to improve scanning; do not let design hide evidence.
5. Test the exported PDF by selecting text, copying it into plain text, and checking whether names, dates, employers, titles, and bullets remain in order.

## Template Recommendation Response Pattern

When recommending a template, include:

- Best fit
- Why it fits the user's target role and submission channel
- Risks or caveats
- Link to upstream source
- Whether to keep a separate ATS-safe version
