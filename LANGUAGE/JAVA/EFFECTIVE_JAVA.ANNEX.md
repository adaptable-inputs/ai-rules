---
applies_to:
  load: "annex"
  annex_of: "EFFECTIVE_JAVA.md"
  tasks: ["review", "test"]
---
# EFFECTIVE_JAVA - Annex

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
