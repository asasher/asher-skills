# To spec

Synthesizes a conversation or shaping record that already reached a decision into one self-contained HTML spec. It writes the artifact as untracked scratch and returns its path, summary, Notes, and fidelity result. Interview, publication, ticket projection, and approval stay outside this skill.

## Shape

- Pure synthesis, no interview. Undecided points become classified Notes.
- Every spec opens with a diagram and follows one template for dev and non-dev work.
- Dev specs declare test seams and the durable-test or throwaway-script split.
- The spec carries no file paths or code snippets except a prototype-validated decision fragment and durable pointers in Supporting artifacts.
- A direction too large for one build ends with a recommended split; it does not create tickets.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-spec`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-spec/SKILL.md).
- **Borrowed:** conversation synthesis, decision capture, and test-seam sketching.
- **Local changes:** HTML output, dev and non-dev gates, test declarations, no-interview rule, generic vocabulary, and producer-only ownership.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
