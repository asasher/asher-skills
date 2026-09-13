---
name: principle-codebase-design
description: Apply when choosing module ownership, interfaces, seams, or test placement during shaping, implementation, or refactoring. Prefer deep modules and test observable behavior through their interfaces.
---

# Codebase design principle

Design deep modules: substantial behavior behind a small interface, placed at a deliberate seam.

A **module** is any code with an interface and an implementation. Its **interface** is everything a caller must know, including types, invariants, ordering, errors, configuration, and performance. A **seam** is where that interface lets behavior vary without editing the caller.

## Deep modules

- Give each module one coherent responsibility and enough behavior to remove complexity from its callers.
- Keep the interface smaller and simpler than the implementation. Hide orchestration, policy, and internal collaborators when callers do not need them.
- Use the deletion test. If deleting the module spreads its complexity across several callers, the module has depth. If deleting it removes only forwarding code, reshape it.
- Add a seam where a dependency or behavior genuinely varies. Keep implementation details behind the module's interface.

## Test at the seam

- Let callers and tests use the same interface.
- Assert observable results, emitted effects, and errors through that interface.
- Write tests that survive internal refactors. A test coupled to private state or call order reaches past the seam.
- Run in-process dependencies directly. Use local substitutes for local infrastructure. Put owned remote systems and third-party services behind narrow adapters when the test needs a controlled replacement.
- Keep test-only seams inside the module unless callers also need them.

During shaping, settle module ownership, the smallest sufficient interface, seam placement, and the observable behavior each seam lets tests prove. During implementation, preserve those decisions and deepen a module when reality shows that complexity is leaking into callers.

The design is complete when every new behavior has one owning module, callers know only its interface, and tests can prove the behavior at that seam.
