---
applies_to:
  load: "conditional"
  when: "pom.xml or build.gradle is present"
  languages: ["java"]
  globs: ["**/*.java"]
---
# EFFECTIVE_JAVA

Guidance for AI agents applying Effective-Java-style decisions in modern Java
codebases.

## Scope
- Specialize `LANGUAGE/JAVA/JAVA.md` with higher-signal Java design heuristics.
- Use this file when selecting between multiple valid Java designs.

## Semantic Dependencies
- Inherit all rules from `LANGUAGE/JAVA/JAVA.md`.
- Inherit cross-cutting and testing rules from `SECURITY/SECURITY.md` and
  `TEST/TEST.md`.
- If this file conflicts with baseline Java guidance, baseline safety rules stay
  authoritative unless this file explicitly narrows behavior.

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
- Favor lists over arrays for API boundaries unless primitive array performance
  is required.
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

## High-Risk Pitfalls
1. Mutable value objects used as map/set keys.
2. Incorrect `equals`/`hashCode` causing container corruption.
3. Telescoping constructors with unclear argument ordering.
4. Raw types and unchecked casts leaking runtime failures.
5. Inheritance used for reuse instead of true subtype semantics.
6. Hidden shared mutable state in static utilities.
7. Java serialization used accidentally as persistence format.

## Do / Don't Examples
### 1. Static Factory vs Constructor Overload Noise
```java
// Don't: ambiguous overloaded constructors.
new User(true, false, "admin", 3600);

// Do: named static factories/builders for intent clarity.
User user = User.adminWithSessionTimeout(3600);
```

### 2. equals/hashCode Contract
```java
// Don't: override equals without hashCode.
@Override
public boolean equals(Object other) { ... }

// Do: keep both methods aligned.
@Override
public boolean equals(Object other) { ... }

@Override
public int hashCode() { ... }
```

### 3. Defensive Copy
```java
// Don't: expose internal mutable date.
public Date createdAt() {
  return createdAt;
}

// Do: return defensive copy.
public Date createdAt() {
  return new Date(createdAt.getTime());
}
```

## Code Review Checklist for Effective Java
- Is object construction API clear (`static factory`/`builder` when needed)?
- Are immutability and defensive copies applied at boundaries?
- Are equals/hashCode/toString semantics correct and safe?
- Are generics used correctly (no raw types/leaky casts)?
- Are resources closed safely via try-with-resources?
- Are concurrency/thread-safety guarantees explicit?
- Are inheritance decisions justified as true subtype modeling?
- Is serialization strategy explicit and compatibility-safe?

## Testing Guidance
- Add contract tests for equals/hashCode behavior.
- Test immutability/defensive-copy invariants.
- Test builder/factory invariants and invalid parameter handling.
- Test concurrent access behavior for shared components.
- Test serialization/deserialization compatibility where relevant.

## Override Notes
- This file narrows `LANGUAGE/JAVA/JAVA.md` with preference heuristics.
- When heuristics conflict with explicit project constraints (performance,
  interoperability), document the tradeoff and preserve baseline safety rules.
