---
name: principle-type-system-discipline
description: Apply when designing types, schemas, function signatures, or network contracts in a statically typed system. Model valid states, distinguish semantic primitives, parse external data, derive from authoritative schemas, and exhaust variants.
---

# Type system discipline principle

Use the type checker as a proof tool. Put domain facts in the model so invalid states, mismatched identifiers, and missed variants fail before runtime.

## Model the domain

- Represent variants with sum types such as discriminated unions or sealed classes. Give each variant exactly the fields it needs.
- Construct valid values directly. A non-empty collection is a head plus a tail. A valid range is a start plus a duration. Prefer a representation that can build only valid values.
- Give semantic primitives distinct types. `UserId` and `OrderId` may share a runtime representation while remaining different domain values.
- Strengthen a type where a loose type makes an operation partial. Keep the simpler type where every operation remains total.

## Carry types across boundaries

- Choose one authoritative contract for each network boundary. Generate or infer client, server, and test types from it.
- Treat incoming JSON, RPC payloads, messages, database rows, configuration, and environment values as untyped input. Parse them once at the receiving boundary into domain types.
- Make a contract change fail typechecking at every stale producer and consumer. Runtime parsing then protects deployments where the two sides run different versions.
- Derive types from protocol, schema, migration, or existing domain definitions. One owner prevents parallel shapes from drifting.

## Keep proofs honest

- Replace unchecked casts and assertions with parsing, narrowing, or a stronger model.
- Match every variant exhaustively so a new case identifies each handler that needs work.
- Trace each runtime assertion or impossible-case error to the type that admitted it. Tighten that type at the earliest trustworthy boundary.

The design is complete when valid values have a clear construction path, external values have a parse point, and schema changes produce useful compiler errors from one end of the system to the other.
