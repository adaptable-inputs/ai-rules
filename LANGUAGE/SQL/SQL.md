---
applies_to:
  load: "conditional"
  when: "the project authors SQL"
  languages: ["sql"]
  globs: ["**/*.sql"]
  annex: "SQL.ANNEX.md"
---
# SQL

Guidance for AI agents implementing and reviewing SQL.

## Scope
- Define SQL correctness, safety, and performance baseline.
- Apply this file for handwritten SQL, generated SQL review, and database
  migration scripts.

## Semantic Dependencies
- Inherit security constraints from `SECURITY/SECURITY.md`.
- Inherit testing expectations from `TEST/TEST.md`.
- Inherit naming/readability constraints from
  `LANGUAGE/CONVENTIONS.md` and `LANGUAGE/READABILITY.md`.
- Inherit architecture guidance from `ARCHITECTURE/N_PLUS_1.md` where relevant.
- Library docs (JPA/jOOQ) MAY specialize query construction but MUST preserve
  this baseline.

## Defaults
- MUST parameterize all external values; avoid string-concatenated SQL.
- SHOULD keep queries explicit and readable; avoid hidden implicit behavior.
- SHOULD select only needed columns; avoid `SELECT *` in production paths.
- SHOULD use clear aliasing and deterministic ordering when order matters.
- SHOULD keep transaction scope minimal and explicit.

## Data Modeling and Schema Evolution
- SHOULD use explicit primary keys and foreign key constraints unless there is a documented reason not to.
- SHOULD keep migrations forward-only and idempotent where feasible.
- SHOULD prefer additive schema changes for compatibility.
- SHOULD backfill large data in batches to avoid long locks.

## Query Performance Rules
- SHOULD design indexes for real access patterns, not assumptions.
- SHOULD validate query plans for hot-path queries.
- SHOULD avoid N+1 query patterns; batch or join intentionally.
- SHOULD use pagination for large result sets.
- SHOULD be explicit with join cardinality and filtering predicates.

## Transaction and Consistency Rules
- SHOULD keep transactions short; avoid user/network waits inside transactions.
- SHOULD pick isolation levels intentionally based on correctness needs.
- SHOULD handle deadlocks and transient failures with bounded retries.
- SHOULD keep write ordering deterministic when consistency depends on it.

## Security Rules
- MUST NOT interpolate untrusted input into SQL strings.
- MUST minimize granted DB privileges by role.
- SHOULD avoid returning sensitive columns unless required.
- MUST treat migration scripts as security-sensitive artifacts.

## Override Notes
- ORM/framework docs MAY adjust implementation style but MUST preserve
  parameterization, transaction safety, and query-plan awareness defined here.
