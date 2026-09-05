# Project DESIGN.md

Use the project's root `DESIGN.md` as the visual system for the current diagram. Resolve it for each artifact.

## Precedence

Resolve visual choices in this order:

1. An explicit user choice for the current diagram, limited to the value it names.
2. The project's `DESIGN.md`.
3. The shipped values in `style-guide.md`.

Read both the YAML tokens and the relevant prose sections. A concrete role in the prose, such as a named background or link color, is more specific than a generic YAML token.

## Map the tokens

Build an in-memory map from the project system to the semantic roles in `style-guide.md`:

| Diagram role | Project source |
| --- | --- |
| `paper` | Page or canvas background; otherwise `colors.surface` |
| `paper-2` | Secondary surface or container background; otherwise derive a quiet contrast from `paper` |
| `ink` | Primary text; otherwise `colors.text` |
| `muted` | Secondary text or subdued stroke |
| `soft` | Tertiary text or boundary label |
| `rule`, `rule-solid` | Border and divider tokens |
| `accent` | Focal or primary action color; otherwise `colors.primary` |
| `accent-tint` | The accent at the project's subtle-fill opacity |
| `link` | Link color; otherwise the nearest project color distinct from `accent` and readable on `paper` |

Use project typography by semantic role where it is specified. Otherwise use `typography.family` for titles and node names, and a project mono family or the system monospace stack for technical labels. Select sizes from the project scale where possible. Keep labels readable at the selected output size.

Use project spacing and radius values where they fit the diagram grammar. Connector clearance, attach-point separation, legibility, contrast, accessibility, and the complexity budget remain hard requirements when a project token would break them.

When `DESIGN.md` leaves a role unspecified, fill that role from `style-guide.md`. Keep the resolved mapping with the generated artifact.

Before returning the diagram, verify primary and secondary text contrast against `paper`. Report any project token that required a legibility fallback.
