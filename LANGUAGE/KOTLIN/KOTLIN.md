---
applies_to:
  load: "conditional"
  when: "Kotlin sources are present"
  languages: ["kotlin"]
  globs: ["**/*.kt", "**/*.kts"]
---
# KOTLIN

Guidance for AI agents implementing and reviewing Kotlin code.

## Scope
- Define baseline Kotlin rules for correctness, maintainability, and runtime
  safety.
- Apply this file for Kotlin code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific Kotlin docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD keep null-safety explicit and avoid defeating type guarantees.
- SHOULD prefer immutable data and explicit state transitions.
- SHOULD use coroutines for structured async/concurrent workflows.
- SHOULD keep exceptions specific and boundary mapping explicit.
- SHOULD keep domain logic separated from framework/runtime plumbing.

## Null-Safety and Type Contracts
- SHOULD model optionality with nullable types intentionally.
- SHOULD avoid `!!` unless a bounded invariant is proven and documented.
- SHOULD keep DTO/domain nullability contracts explicit and consistent.
- SHOULD prefer sealed/value types for constrained domain state where suitable.

## Coroutines and Concurrency Rules
- SHOULD use structured concurrency with explicit parent scope ownership.
- SHOULD avoid `GlobalScope` for application business workflows.
- SHOULD keep dispatcher selection explicit for IO/CPU-sensitive paths.
- SHOULD propagate cancellation signals and timeouts for external calls.
- MUST prevent shared mutable-state races with explicit synchronization.

## Exception and Resource Handling
- SHOULD throw/map specific exceptions with actionable context.
- MUST NOT swallow exceptions silently.
- SHOULD use `use {}` and lifecycle-aware resource management for deterministic cleanup.
- SHOULD preserve cause chains when wrapping exceptions at boundaries.

## API and Module Design
- SHOULD keep module/package boundaries cohesive and dependency direction explicit.
- SHOULD keep extension functions focused and avoid hidden side effects.
- SHOULD keep companion objects/static-like usage minimal and intentional.
- MUST keep configuration and secrets outside code.

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

## Override Notes
- Project-specific Kotlin conventions MAY add stricter patterns, but null-safety
  integrity, structured concurrency, explicit error handling, and boundary
  cohesion remain mandatory.
