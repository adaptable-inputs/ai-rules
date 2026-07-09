---
applies_to:
  load: "annex"
  annex_of: "JOOQ.md"
  tasks: ["review", "test"]
---
# JOOQ - Annex

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
