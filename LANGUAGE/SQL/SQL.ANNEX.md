---
applies_to:
  load: "annex"
  annex_of: "SQL.md"
  tasks: ["review", "test"]
---
# SQL - Annex

## High-Risk Pitfalls
1. SQL injection from dynamic string concatenation.
2. Unbounded queries and full scans on large tables.
3. Missing indexes for frequent filter/join predicates.
4. N+1 query patterns hidden behind ORM abstractions.
5. Long-running transactions causing lock contention.
6. Breaking schema changes without compatibility window.
7. Non-deterministic ordering in pagination queries.

## Do / Don't Examples
### 1. Parameterization
```text
Don't: build SQL in application code using string interpolation/concatenation.
Example: `"... WHERE email = '" + input + "'"`.
```

```sql
-- Do: parameterized query with explicit column list
SELECT id, email FROM users WHERE email = :email;
```

### 2. Deterministic Pagination
```sql
-- Don't: no stable ordering
SELECT id, name FROM orders LIMIT 50 OFFSET 100;

-- Do: stable ordering key
SELECT id, name
FROM orders
ORDER BY created_at DESC, id DESC
LIMIT :limit OFFSET :offset;
```

### 3. N+1 Avoidance
```sql
-- Don't: one query per parent row in application loop

-- Do: batch children by parent ids with query-builder-expanded placeholders
SELECT order_id, sku, quantity
FROM order_items
WHERE order_id IN (
  -- expanded by query builder from a collection bind like :orderIds
  :orderId1, :orderId2, :orderId3
);
```

Note: the expanded placeholders above are illustrative. Generate collection bindings/placeholders through the DB
driver/query builder; never string-interpolate `IN (...)` values.

## Code Review Checklist for SQL
- Are all dynamic values parameterized?
- Are selected columns minimal and intentional?
- Is ordering explicit where result order matters?
- Does every query with unbounded result size paginate, and does each filter and sort column have a supporting index?
- Are transaction boundaries and isolation choices explicit?
- Are migration scripts backward-compatible and operationally safe?
- Are query plans acceptable for hot paths?

## Testing Guidance for SQL
- Add integration tests for non-trivial queries and edge-case filters.
- Test migration upgrade paths on realistic dataset sizes.
- Test transaction rollback/consistency behavior under failure.
- Add performance regression checks for critical queries.
- Test authorization/role constraints for sensitive operations.
