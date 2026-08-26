---
name: typescript-best-practices
description: Apply when shaping, reading, or editing TypeScript and TSX. Express domain variants, branded values, boundary parsing, schema-derived contracts, safe narrowing, and exhaustive handling in TypeScript.
---

# TypeScript best practices

- Model domain variants as discriminated unions with a literal `kind` or `type` field. Give each member its required fields instead of sharing a bag of optionals.
- Brand identifiers and other semantic primitives so values with the same runtime type stay distinct.
- Receive external data as `unknown`. Parse it into a named domain type at the network, storage, process, or configuration boundary.
- Derive request, response, and domain types from the authoritative schema or implementation with `typeof`, `Awaited`, `ReturnType`, `Parameters`, `Pick`, and `Omit`. Keep one owner for each shape.
- Use `satisfies` to check a value while preserving its literal types.
- Narrow with a discriminant switch, `in`, `typeof`, or `instanceof`. A user-defined type guard verifies every fact its return type claims.
- Make switches exhaustive with a `never` assignment so a new union member points to every stale handler.
- Treat each `as`, non-null assertion, and `any` as a missing proof. Add validation or reshape the type at the first trustworthy point.
- Use constructive types where partiality appears, such as `[T, ...T[]]` for a non-empty collection. Keep `T[]` when all consumers handle emptiness.

For an end-to-end TypeScript contract, share or generate the compile-time types and still parse the payload at runtime. Shared types catch stale code during development. Boundary parsing catches untrusted data and version skew in production.
