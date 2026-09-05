# Diagram design

Create editorial diagrams as standalone HTML, SVG, or PNG files, or as inline figures within a larger self-contained HTML artifact. The skill includes diagram-selection guidance, type-specific layout references, templates, importers, accessible SVG rules, and validation scripts.

## Local integration

- A project `DESIGN.md` supplies the visual tokens when present. The skill maps them for each artifact without modifying the project file or the installed package.
- Embedded mode returns a scoped, accessible `<figure>` for artifacts such as research dossiers and specs.
- The repository's `research` and `to-spec` skills compose this sibling only when a diagram materially improves the artifact. `prototype` does not depend on it.

## Credits

- **Relationship:** vendored with local integration changes.
- **Source:** Cathryn Lavery's MIT-licensed [`diagram-design`](https://github.com/cathrynlavery/diagram-design/tree/4faae6696c2953b59dee2b89ad89c688f80c3a67/skills/diagram-design), reviewed at commit [`4faae6696c2953b59dee2b89ad89c688f80c3a67`](https://github.com/cathrynlavery/diagram-design/commit/4faae6696c2953b59dee2b89ad89c688f80c3a67), upstream version 2.6.
- **Local changes:** resolves each artifact from explicit visual choices, project `DESIGN.md`, and shipped fallbacks; adds embedded-figure output, this repository's interface metadata, and sibling composition from `research` and `to-spec`. Reskins the shipped defaults from the upstream warm light palette to a dark skin whose values are read off Vercel's Geist color scales (near-black paper, gray-100 surfaces, gray-alpha borders, gray-900/1000 text, blue-900 accent), with light as the alternate variant; the pre-baked `assets/example-*.html` files keep the upstream skin.
- **License/notices:** [LICENSE](LICENSE) and [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
