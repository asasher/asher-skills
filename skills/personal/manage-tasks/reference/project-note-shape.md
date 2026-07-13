# Project Note Shape

A Project is the delivery or execution source of truth at `Projects/<Name>.md`. Include only applicable
frontmatter fields:

```yaml
---
project: <display name>
company: "[[Company]]"
customers:
  - "[[Customer]]"
sourceOpportunity: "[[Opportunity]]"
localPath: /absolute/path/to/delivery-work
github: owner/repository
Folders:
  - "[[Parent Project]]"
---
```

`sourceOpportunity` is the commercial provenance when an Opportunity created the Project. It is a wikilink
to the retained Opportunity note. `localPath` belongs to Projects for repository triage; an Opportunity's
`workspacePath` never substitutes for it.

The body starts with `# <display name>` and one orienting sentence. Omit empty sections:

- `## Backlog` - inactive Project-origin tasks.
- `## Done` - dated subsections, newest first.
- `## Events Log` - dated delivery or administration events.
- `## Links` - working documents, repository, dashboards, and external entry points.
- `## Map` - child Projects with one orienting line each; each child links back to its parent.

On Opportunity promotion, the Project links back through `sourceOpportunity`, and the Opportunity's
`## Projects` links to this Project. `manage-opportunities` owns that promotion transaction.
