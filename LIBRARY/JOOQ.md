---
applies_to:
  load: "conditional"
  when: "jooq is a declared dependency"
  libraries: ["jooq"]
  annex: "JOOQ.ANNEX.md"
  purpose: "jOOQ usage rules for type-safe SQL and predictable query behavior"
  inherits: ["LANGUAGE/SQL/SQL.md", "LANGUAGE/JAVA/JAVA.md", "ARCHITECTURE/N_PLUS_1.md", "ARCHITECTURE/ARCHITECTURE.md", "FRAMEWORK/SPRING_BOOT.md"]
---
# JOOQ

Guidance for AI agents implementing and reviewing jOOQ-based data access.

## Defaults
- SHOULD prefer generated jOOQ types for compile-time safety.
- SHOULD keep SQL logic in data-access boundaries, not service/controller layers.
- SHOULD keep query composition readable and explicit.
- SHOULD prefer explicit projections over broad row mapping where possible.
- SHOULD keep transaction boundaries aligned with use-case orchestration.

## Query Composition Rules
- SHOULD extract reusable query fragments only when readability improves.
- SHOULD avoid giant chained query builders with hidden conditions.
- SHOULD keep joins/conditions explicit and index-aware.
- MUST parameterize all external values.
- SHOULD validate generated SQL and query plans for hot paths.

## Code Generation and Schema Alignment
- SHOULD keep jOOQ codegen in sync with schema migrations.
- SHOULD treat generated source as build artifact (do not hand-edit).
- MUST pin generator/runtime versions consistently.
- SHOULD validate diff impact when schema changes.

## Transaction and Consistency
- SHOULD use transactional context explicitly for write workflows.
- SHOULD avoid mixing conflicting ORM contexts in same transaction without clear
  strategy.
- SHOULD keep retries/locking behavior intentional for conflict-prone operations.

## Override Notes
- JPA MAY be used for simpler CRUD domains, but jOOQ usage SHOULD preserve SQL
  clarity, codegen alignment, and transaction safety constraints here.
