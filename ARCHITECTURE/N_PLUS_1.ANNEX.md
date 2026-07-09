---
applies_to:
  load: "annex"
  annex_of: "N_PLUS_1.md"
  tasks: ["review", "test"]
---
# N_PLUS_1 - Annex

## High-Risk Pitfalls
1. Query in loop over parent records.
2. Lazy relation access during JSON serialization.
3. Missing DataLoader in GraphQL nested fields.
4. Over-eager joins creating huge Cartesian-like payloads.
5. Query-count regressions not covered by tests.
6. Repository abstractions hiding repeated DB calls.

## Do / Don't Examples
### 1. Application Loop Query
```text
Don't:
for each order -> query order_items by order_id

Do:
query orders
collect ids
query order_items where order_id in (:ids)
map in memory
```

### 2. GraphQL Resolver
```text
Don't: resolver loads user profile with DB call per row.
Do:    resolver uses request-scoped DataLoader keyed by userId.
```

### 3. ORM Serialization
```text
Don't: return entities with lazy relations and let serializer trigger queries.
Do:    project explicitly to DTO with preloaded required fields.
```

## Code Review Checklist for N+1 Risk
- Are there queries inside loops over records/resolvers?
- Are ORM fetch plans explicit for endpoint/query use case?
- Are GraphQL loaders present and request-scoped where needed?
- Is query count predictable and bounded under pagination?
- Are joins/batches chosen to avoid both N+1 and row explosion?
- Are query-count regressions covered in tests?

## Testing Guidance
- Add query-count assertions for critical endpoints/resolvers.
- Add integration tests for large parent sets and pagination behavior.
- Test GraphQL nested query performance characteristics.
- Track and alert on unexpected query count growth in performance tests.
