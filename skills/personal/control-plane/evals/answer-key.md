# Control Plane — answer key

| Probe | Pass condition |
|---|---|
| P1 | No. An optional sibling joins only by explicit command or separately configured cadence, never implicitly in a morning run (SKILL.md Commands; reference/cadence.md). |
| P2 | Independent source pulls continue after one source fails; any Pull failure blocks Start Work; the brief names the failed source, distinguishing an empty source from one that could not be checked (reference/morning-run.md). |
| P3 | Invoke `capture-to-inbox setup` by name; that sibling owns every listed artifact/effect; control-plane records only bindings, cadence, phase status, and brief results (reference/setup.md step 1). |
