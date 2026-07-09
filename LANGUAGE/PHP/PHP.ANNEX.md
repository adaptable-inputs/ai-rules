---
applies_to:
  load: "annex"
  annex_of: "PHP.md"
  tasks: ["review", "test"]
---
# PHP - Annex

## High-Risk Pitfalls
1. Running with loose typing and implicit coercion in domain logic.
2. Mixed-array contracts with unclear schema/ownership.
3. Silent error suppression and missing boundary mappings.
4. Hidden globals/static state creating non-deterministic behavior.
5. Framework-coupled business logic reducing testability.
6. Unvalidated external input reaching domain/database layers.
7. Dependency growth without maintenance/compliance review.

## Do / Don't Examples
### 1. Type Safety
```text
Don't: rely on implicit type coercion in core business paths.
Do:    use strict types and explicit type contracts.
```

### 2. Error Handling
```text
Don't: suppress exceptions and continue with undefined state.
Do:    map exceptions explicitly at API/service boundaries.
```

### 3. Input Validation
```text
Don't: pass raw request payloads directly into domain logic.
Do:    validate and normalize boundary input first.
```

## Code Review Checklist for PHP
- Is strict typing enabled and used consistently?
- Are API contracts typed and explicit?
- Are exceptions mapped specifically and non-silently?
- Are side effects/global state minimized and clear?
- Are boundaries between framework and domain logic well defined?
- Are dependencies justified, maintained, and compliant?

## Testing Guidance
- Test boundary validation and normalization behavior.
- Test exception mapping and error-path outputs.
- Test type-contract-sensitive paths for coercion regressions.
- Test side-effect boundaries with focused integration tests.
- Add regression tests for previously observed bug classes.
