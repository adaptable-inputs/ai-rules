---
applies_to:
  load: "conditional"
  when: "a JPA provider is a declared dependency"
  libraries: ["jpa"]
---
# JPA

Guidance for AI agents implementing and reviewing JPA-based persistence.

## Scope
- Define JPA mapping and query usage rules for correctness and performance.
- Apply this file to entity modeling, repository logic, and transaction design.

## Semantic Dependencies
- Inherit Java baseline from `LANGUAGE/JAVA/JAVA.md`.
- Inherit SQL and N+1 constraints from
  `LANGUAGE/SQL/SQL.md` and `ARCHITECTURE/N_PLUS_1.md`.
- Inherit framework boundary constraints from `FRAMEWORK/SPRING_BOOT.md`.
- Cross-cutting baselines are inherited transitively via the language/framework
  parents above.

## Defaults
- SHOULD keep entities persistence-focused; keep business workflows in services.
- SHOULD prefer explicit mappings for non-trivial columns/relations.
- SHOULD use `@Enumerated(EnumType.STRING)` for enums.
- SHOULD prefer LAZY associations by default; fetch explicitly per use case.
- SHOULD keep transaction boundaries explicit and use-case aligned.

## Mapping and Entity Design
- SHOULD keep equals/hashCode on entities identity-safe.
- SHOULD avoid exposing mutable collections directly.
- SHOULD keep cascade rules minimal and intentional.
- SHOULD avoid bidirectional relationships unless they add real query/navigation value.
- SHOULD keep embeddables/value objects for cohesive grouped fields.

## Query and Fetch Strategy
- SHOULD avoid N+1 via fetch joins/entity graphs/DTO projections.
- SHOULD prefer explicit queries for non-trivial reads.
- SHOULD avoid large object graph loading when only subset fields are needed.
- SHOULD validate generated SQL for critical queries.

## Transaction and Consistency
- SHOULD keep transactions short; avoid remote IO inside transaction scope.
- MUST be explicit about locking strategy for concurrency-sensitive writes.
- SHOULD handle optimistic lock exceptions intentionally.
- SHOULD avoid Open Session in View dependence for core business behavior.

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

## Override Notes
- jOOQ or custom SQL MAY be preferred for complex query/reporting scenarios.
- JPA-specific convenience SHOULD NOT override query predictability and
  transaction safety constraints.
