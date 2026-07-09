---
applies_to:
  load: "conditional"
  when: "the project uses an ORM or lazy-loaded associations"
  annex: "N_PLUS_1.ANNEX.md"
  purpose: "anti-N+1 rules across ORM, SQL, and GraphQL/resolver-based systems"
  inherits: ["SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md", "LANGUAGE/SQL/SQL.md", "ARCHITECTURE/ARCHITECTURE.md", "LIBRARY/JPA.md", "LIBRARY/JOOQ.md", "ARCHITECTURE/GRAPHQL.md"]
---
# N_PLUS_1

Guidance for AI agents preventing and detecting N+1 query patterns.

## Core Rule
- SHOULD avoid per-entity follow-up queries in loops or repeated resolver calls.
- SHOULD batch related data fetches per logical level of the response graph.

## Detection Heuristics
- SHOULD watch for query execution inside loops over parent entities.
- SHOULD watch for lazy-loaded relation access in serialization/rendering loops.
- In GraphQL, SHOULD watch per-field resolver DB calls without DataLoader/batching.
- SHOULD use query counters and SQL logs in test/profiling environments.

## Prevention Strategy
- SHOULD query parents first.
- SHOULD collect parent keys.
- SHOULD fetch children/related data in one batch (`IN`, joins, dedicated loaders).
- SHOULD reconstruct response graph in memory.
- SHOULD keep batch size and pagination controls explicit.

## ORM-Specific Guardrails
- SHOULD prefer explicit fetch joins/entity graphs/projections for known access paths.
- SHOULD avoid broad eager loading by default; tune fetch plans per use case.
- SHOULD keep lazy loading away from view/serialization layers.
- SHOULD validate generated SQL for non-trivial ORM queries.

## GraphQL/Resolver Guardrails
- SHOULD use per-request DataLoader or equivalent batching abstraction.
- SHOULD ensure loaders are request-scoped to prevent cache leakage across users.
- SHOULD batch by field/resource shape with deterministic key mapping.
- SHOULD avoid nested resolver-side queries without loader mediation.

## Performance and Correctness Tradeoffs
- SHOULD prefer predictable query count over highly dynamic implicit loading.
- SHOULD avoid giant fetch joins that explode row multiplicity without pagination.
- SHOULD keep response payload size aligned with use-case requirements.
- SHOULD combine pagination with batching to bound memory and query costs.

## Override Notes
- Framework/library docs MAY define API-specific mechanisms, but anti-N+1
  guarantees and query-count predictability in this file remain mandatory.
