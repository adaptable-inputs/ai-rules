---
applies_to:
  load: "conditional"
  when: "Kotlin sources are present"
  languages: ["kotlin"]
  globs: ["**/*.kt", "**/*.kts"]
  annex: "KOTLIN.ANNEX.md"
  purpose: "baseline Kotlin rules for correctness, maintainability, and runtime safety"
  inherits: ["SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# KOTLIN

Guidance for AI agents implementing and reviewing Kotlin code.

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
