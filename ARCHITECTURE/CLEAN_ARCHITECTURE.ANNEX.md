---
applies_to:
  load: "annex"
  annex_of: "CLEAN_ARCHITECTURE.md"
  tasks: ["review", "test"]
---
# CLEAN_ARCHITECTURE - Annex

## High-Risk Pitfalls
1. Framework annotations leaking into domain models.
2. Use-case logic tightly coupled to ORM/HTTP types.
3. Anemic domain with all business rules pushed to controllers.
4. Shared "utils" bypassing boundaries and dependency direction.
5. Direct infrastructure calls from domain entities.
6. Over-abstraction without clear boundary value.

## Do / Don't Examples
### 1. Dependency Direction
```text
Don't: DomainService imports JdbcTemplate/ORM repository implementation.
Do:    DomainService depends on OrderRepository interface defined in core.
```

### 2. DTO Leakage
```text
Don't: Pass HTTP request objects into use-case methods.
Do:    Map request to explicit input DTO/value object first.
```

### 3. Composition Root
```text
Don't: new InfrastructureClient() inside use-case class.
Do:    inject interface implementation via outer-layer wiring.
```

## Code Review Checklist for Clean Architecture
- Are dependency directions inward and enforced?
- Are framework/infrastructure details isolated to outer layers?
- Are boundary contracts explicit and stable?
- Is business logic located in domain/use-case layers?
- Are mappers/adapters explicit and testable?
- Are transactions and side effects scoped to use-case boundaries?
- Are architecture constraints guarded by tests/static checks?

## Testing Guidance
- Add unit tests for domain invariants and use-case rules.
- Add integration tests for adapter/gateway behavior.
- Add architectural dependency tests (package/module boundary checks).
- Add regression tests when moving code across layers.
