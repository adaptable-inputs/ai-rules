---
applies_to:
  load: "annex"
  annex_of: "JPA.md"
  tasks: ["review", "test"]
---
# JPA - Annex

## High-Risk Pitfalls
1. N+1 queries from lazy relations in loops/serialization.
2. Over-cascading relations causing accidental writes/deletes.
3. Entity leakage into API boundaries.
4. Long transactions with remote calls.
5. Improper equals/hashCode breaking persistence behavior.
6. Blind eager fetching causing memory/perf spikes.

## Do / Don't Examples
### 1. Enum Mapping
```java
// Don't
@Enumerated(EnumType.ORDINAL)
private Status status;

// Do
@Enumerated(EnumType.STRING)
private Status status;
```

### 2. Query Strategy
```text
Don't: iterate orders and lazily load items per row.
Do:    fetch required relations/projection explicitly for endpoint use case.
```

### 3. Transaction Scope
```text
Don't: call external payment API inside DB transaction.
Do:    isolate external call from persistence transaction boundary.
```

## Code Review Checklist for JPA
- Are entity mappings explicit and identity-safe?
- Is fetch strategy intentional and N+1-safe?
- Are transaction boundaries short and explicit?
- Are cascade/orphan rules minimal and justified?
- Are entities kept out of external API contracts?
- Are locking/concurrency behaviors handled intentionally?

## Testing Guidance
- Add integration tests for mappings and custom queries.
- Add query-count/performance checks on hot paths.
- Test optimistic locking/conflict scenarios.
- Test transaction rollback behavior on failures.
- Test serialization boundaries to avoid lazy-loading surprises.
