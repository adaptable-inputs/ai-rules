---
applies_to:
  load: "annex"
  annex_of: "KOTLIN.md"
  tasks: ["review", "test"]
---
# KOTLIN - Annex

## High-Risk Pitfalls
1. Frequent `!!` usage that bypasses null-safety contracts.
2. Unstructured coroutine launching with lifecycle leaks.
3. Blocking calls inside coroutine contexts without dispatcher isolation.
4. Catch-all exceptions that hide root causes.
5. Mutable shared state with no concurrency strategy.
6. Framework-coupled domain logic reducing testability.
7. Resource leaks due to missing scoped cleanup.

## Do / Don't Examples
### 1. Null Safety
```text
Don't: rely on `!!` in routine business logic.
Do:    model nullable intent explicitly and validate boundaries.
```

### 2. Coroutine Scope
```text
Don't: launch business-critical coroutines in `GlobalScope`.
Do:    use structured scopes with explicit lifecycle ownership.
```

### 3. Cancellation
```text
Don't: ignore cancellation and timeout behavior for external calls.
Do:    propagate cancellation and set explicit timeout boundaries.
```

## Code Review Checklist for Kotlin
- Are nullability contracts explicit and consistently enforced?
- Are coroutine scopes structured with clear lifecycle ownership?
- Are dispatcher usage and blocking behavior safe?
- Are exception mappings specific and non-silent?
- Are module boundaries cohesive and maintainable?
- Are dependencies/configuration/secrets handled safely?

## Testing Guidance
- Test nullability and boundary validation behavior.
- Test coroutine cancellation/timeout behavior under failure.
- Test concurrency-sensitive code for race/leak risks.
- Test exception mapping and root-cause preservation.
- Add regression tests for previously observed bug classes.
