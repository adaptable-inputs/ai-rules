---
applies_to:
  load: "conditional"
  when: "jooq is a declared dependency"
  libraries: ["jooq"]
---
# JOOQ

Guidance for AI agents implementing and reviewing jOOQ-based data access.

## Scope
- Define jOOQ usage rules for type-safe SQL and predictable query behavior.
- Apply this file to repository/query-layer implementation and review.

## Semantic Dependencies
- Inherit SQL baseline from `LANGUAGE/SQL/SQL.md`.
- Inherit Java baseline from `LANGUAGE/JAVA/JAVA.md`.
- Inherit N+1 constraints from `ARCHITECTURE/N_PLUS_1.md`.
- Inherit transaction/boundary constraints from
  `ARCHITECTURE/ARCHITECTURE.md` and `FRAMEWORK/SPRING_BOOT.md` where
  applicable.

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
- Parameterize all external values.
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

## High-Risk Pitfalls
1. Query builder chains too complex to review.
2. Schema drift between DB and generated classes.
3. Hidden N+1 query patterns around iterative jOOQ calls.
4. Broad `selectFrom` usage where narrow projection is sufficient.
5. Mixing jOOQ and ORM writes without transaction strategy.
6. Hand-written SQL fragments bypassing type safety unnecessarily.

## Do / Don't Examples
### 1. Projection
```text
Don't: select all columns when endpoint needs two fields.
Do:    select explicit fields required by use case.
```

### 2. Boundary Placement
```text
Don't: build jOOQ query directly in web controller.
Do:    encapsulate query in repository/adapter class.
```

### 3. Schema Sync
```text
Don't: use stale generated classes after migration.
Do:    regenerate jOOQ sources as part of migration/build workflow.
```

## Code Review Checklist for jOOQ
- Are queries explicit, readable, and boundary-contained?
- Are projections minimal and index-aware?
- Are generated types/codegen pipeline kept in sync with schema?
- Are transactions and locking semantics explicit?
- Are dynamic conditions parameterized and safe?
- Are query plans/performance considered for critical paths?

## Testing Guidance
- Add integration tests for non-trivial queries.
- Add migration + codegen synchronization checks in CI.
- Add query performance assertions for hot paths.
- Test transaction rollback/conflict behavior.

## Override Notes
- JPA MAY be used for simpler CRUD domains, but jOOQ usage SHOULD preserve SQL
  clarity, codegen alignment, and transaction safety constraints here.
