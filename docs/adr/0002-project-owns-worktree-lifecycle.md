---
status: accepted
---

# The project owns worktree lifecycle; harnesses only dispatch into prepared directories

Claude Code, Codex, and T3 Code expose different isolation surfaces. Letting each dispatch adapter
request its harness-native worktree made the checkout boundary implicit: the primary checkout could
be changed without a visible prepare step, paths and bases differed by harness, and T3's native
worktree behavior was considerably harder to coordinate with the backlog lifecycle. We decided that
the project prepares, inspects, and removes every shaping and build worktree through one deterministic
`worktree` primitive. Dispatch adapters receive exact workflow directories without adding
harness-native isolation; on direct invocation, they compose the same primitive only for an explicit
isolation request.

`backlog groom` owns one worktree per approved shaping batch, including a single batch.
`backlog build` owns one worktree per issue for the entire implementation-through-evidence pipeline.
The primary checkout is never a dispatched-work fallback. A shaping batch advances atomically only
after a clean worktree is removed or its shaping change is merged, verified, and cleaned up.
The exact shaping change-request head is presented before the readiness signal that authorizes its
merge; a signal never applies retroactively to a later or unpresented head.

## Considered options

**Use each harness's native worktrees and normalize only the prompt** — rejected because ownership,
base selection, cleanup, and recovery would still vary by harness. It also leaves outer T3 dispatch
dependent on a harder native-worktree API while embedded Codex may misleadingly appear to be the owner.

**Prefer project worktrees but fall back to native isolation** — rejected because two creation paths
make the exact failure we need to prevent non-deterministic. A missing project capability is surfaced;
it is not permission to mutate the primary checkout.

**Serialize unsupported repositories in the primary checkout** — rejected because serialization
prevents concurrency but not accidental checkout mutation or contamination.

## Consequences

The lifecycle is inspectable and testable across harnesses, and one directory now carries all artifacts
needed by a build or shaping thread. The T3 adapter can use its local authenticated HTTP dispatch path
and register the externally prepared worktree instead of reproducing T3-native creation.

The project now owns branch/path naming, remote-base freshness, dirty-worktree refusal, recovery, and
cleanup. Harness capabilities can change without changing that contract, but their dispatch adapters
still require regular effect probes. Repositories that cannot isolate do not build until their
environment contract is fixed. After this source change merges, installed skill packages and
consumer-owned playbooks require an explicit reconcile; asher-skills#144 tracks that rollout.
