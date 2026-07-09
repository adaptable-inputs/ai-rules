---
applies_to:
  load: "conditional"
  when: "pom.xml or build.gradle is present"
  languages: ["java"]
  globs: ["**/*.java"]
  annex: "EFFECTIVE_JAVA.ANNEX.md"
  inherits: ["LANGUAGE/JAVA/JAVA.md", "SECURITY/SECURITY.md", "TEST/TEST.md"]
---
# EFFECTIVE_JAVA

Guidance for AI agents applying Effective-Java-style decisions in modern Java
codebases.

## Core Design Preferences
- SHOULD prefer static factories over constructors when they improve readability,
  caching, or subtype flexibility.
- SHOULD use builders for objects with many optional parameters or invariants.
- SHOULD prefer immutable value types and make defensive copies of mutable state.
- SHOULD prefer composition over inheritance unless subtype truly models an `is-a`
  relationship.
- SHOULD minimize visibility of classes/members; keep APIs as small as possible.

## Equality and Identity
- Override `equals` and `hashCode` together when value semantics apply.
- SHOULD keep equality consistent with domain meaning; avoid including volatile or derived fields unintentionally.
- MUST keep `toString` useful for diagnostics but free of secrets.

## Generics and Collections
- SHOULD prefer generic types over raw types.
- SHOULD favor lists over arrays for API boundaries unless primitive array performance is required.
- SHOULD use bounded wildcards intentionally (`? extends`, `? super`) to improve API flexibility.
- SHOULD prefer empty collections over `null` returns.

## Optional and Nullability
- SHOULD return `Optional<T>` when absence is part of API semantics.
- SHOULD avoid `Optional` in fields/parameters unless there is a strong documented
  reason.
- MUST NOT use `Optional.get()` without presence checks.

## Exceptions and Resource Management
- SHOULD throw domain-relevant exception types with actionable context.
- SHOULD use checked exceptions only for recoverable conditions.
- SHOULD use try-with-resources for closeable resources.
- MUST NOT ignore exceptions; if suppressed intentionally, document rationale.

## Concurrency Guidance
- SHOULD prefer immutable/shared-nothing designs over synchronization.
- SHOULD use high-level concurrency abstractions (`ExecutorService`, `CompletableFuture`, Structured
  Concurrency/virtual-thread APIs where available) over ad-hoc thread creation.
- SHOULD document thread-safety guarantees for shared components.
- SHOULD avoid exposing mutable static state.

## Serialization and Compatibility
- SHOULD prefer explicit DTO/schema mappers over default Java serialization.
- If Java serialization is unavoidable, SHOULD declare `serialVersionUID` and treat serialized forms as compatibility
  contracts.
- SHOULD validate invariants after deserialization.

## Override Notes
- This file narrows `LANGUAGE/JAVA/JAVA.md` with preference heuristics.
- When heuristics conflict with explicit project constraints (performance,
  interoperability), document the tradeoff and preserve baseline safety rules.
