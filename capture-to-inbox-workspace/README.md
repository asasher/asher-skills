# Capture To Inbox Skill Workspace

Author-side development material for `skills/personal/capture-to-inbox/`. This directory is not installed and is never used as consumer runtime state.

`legacy/` preserves the original hand-built Shortcut generator and dated XML snapshots that proved the iPhone-to-Railway capture flow. The shipped skill now delegates Shortcut generation, validation, and signing to its declared Shortcuts Playground external requirement. Active generated Shortcut source belongs in each consumer's skill instance.
