---
applies_to:
  load: "conditional"
  when: "pom.xml or build.gradle is present"
  languages: ["java"]
  globs: ["**/*.java"]
---
# JAVA

Guidance for AI agents implementing and reviewing Java code.

## Scope
- Define the baseline Java ruleset for correctness, maintainability, and
  interoperability.
- Apply this file for all Java code generation and code review tasks.
- Use Java specialization layers as additions, not substitutes for this
  baseline.

## Semantic Dependencies
- Inherit cross-cutting constraints from:
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.
- Inherit shared language constraints from:
  `LANGUAGE/CONVENTIONS.md`, `LANGUAGE/READABILITY.md`.
- Java specialization docs MAY narrow and enrich this baseline.
- Framework/library docs (for example Spring, JPA) MAY specialize API usage
  but MUST NOT weaken Java safety constraints.

## Defaults
- SHOULD prefer immutability for value types and DTOs.
- SHOULD prefer constructor injection and explicit dependencies.
- SHOULD keep methods/classes focused and cohesive.
- SHOULD prefer interfaces for contracts and dependency boundaries.
- SHOULD prefer explicit domain-specific types over primitive obsession.
- SHOULD prefer checked validation and fail-fast preconditions at boundaries.

## Exact Numeric Domains (Money, Rates, Quantities)
- MUST NOT use `float`/`double` when values MUST stay exact (for example money).
- SHOULD prefer smallest-unit integers (for example cents in `long`) when unit and
  range are stable for the domain.
- MUST use JavaMoney (JSR 354, typically Moneta) for monetary values in Java.
- SHOULD restrict raw `BigDecimal` money handling to boundary conversions where JavaMoney types cannot be used directly.
- SHOULD avoid `new BigDecimal(double)`; if `BigDecimal` is unavoidable, construct
  from `String` for exact decimal values, or use `BigDecimal.valueOf(long)` for
  whole-number smallest-unit amounts, and centralize scale + rounding rules.
- SHOULD keep unit/currency attached to the amount type to prevent accidental mixing.

## Nullability and Optional
- SHOULD avoid returning `null` from public APIs where absence is expected;
  prefer `Optional<T>` for return values when semantically meaningful.
- MUST NOT use `Optional` for fields, method parameters, or serialization models
  unless there is a strong documented reason.
- SHOULD keep null-handling explicit at boundaries and legacy integration points.

## Collections and Mutability
- SHOULD return immutable or unmodifiable views where mutation is not intended.
- SHOULD make defensive copies for mutable inputs/outputs crossing boundaries.
- SHOULD prefer specific collection interfaces in signatures (`List`, `Map`, `Set`).
- SHOULD avoid exposing internal mutable collections directly.

## Exception Design
- SHOULD throw specific exception types with actionable context.
- MUST NOT swallow exceptions silently.
- SHOULD keep exception mapping consistent at API boundaries.
- SHOULD preserve root cause when wrapping exceptions.
- SHOULD use checked exceptions for genuinely recoverable scenarios; otherwise use runtime exceptions with clear domain
  meaning.

## API and Class Design
- SHOULD keep constructors light; avoid side effects and IO in constructors.
- SHOULD use builders for objects with many optional parameters.
- SHOULD keep equals/hashCode/toString aligned with type semantics.
- SHOULD avoid large utility classes with mixed responsibilities.
- SHOULD avoid boolean parameter combinations that hide intent; introduce
  explicit value objects or methods.

## Concurrency Baseline
- SHOULD avoid shared mutable state by default.
- SHOULD prefer immutable handoff between threads.
- When synchronization is required, SHOULD define and document invariants.
- SHOULD use high-level concurrency utilities over manual thread management.
- SHOULD keep blocking calls out of latency-critical paths where possible.

## Streams and Functional Style
- SHOULD use streams for readable transformations, not as a blanket replacement.
- SHOULD avoid side effects inside stream operations.
- SHOULD keep stream pipelines understandable; extract named methods when complex.
- SHOULD prefer loops when they are clearer than chained stream operations.

## String Construction and Formatting
- SHOULD prefer `String.format(...)` over `+` concatenation when constructing a
  string from a literal template and variables.
- SHOULD use clear, stable format templates for user-facing or logged text.
- In tight loops or append-heavy code paths, SHOULD prefer `StringBuilder`.

## Persistence/Serialization Boundaries
- SHOULD keep domain models independent from persistence/transport annotations when practical.
- SHOULD use dedicated DTOs for external boundaries.
- SHOULD avoid leaking persistence entities across API boundaries by default.

## High-Risk Pitfalls
1. Returning internal mutable state directly.
2. Overusing `Optional` in fields/parameters.
3. Catching broad exceptions and hiding root causes.
4. Mixing domain and infrastructure concerns in one class.
5. Blocking operations in shared thread pools without capacity planning.
6. Overly clever stream chains harming readability.
7. Implicit null contracts with no annotations/documentation.
8. Using floating-point types for exact monetary or quantity values.
9. Building literal-template strings with `+` instead of `String.format(...)`.

## Do / Don't Examples
### 1. Defensive Copying
```java
// Don't
public List<Item> getItemsUnsafe() {
  return items;
}
```

```java
// Do
public List<Item> getItemsSafe() {
  return List.copyOf(items);
}
```

### 2. Exception Mapping
```java
// Don't: swallow and continue silently.
try {
  repository.save(order);
} catch (Exception ignored) {
}

// Do: keep context and propagate meaningfully.
try {
  repository.save(order);
} catch (DataAccessException ex) {
  throw new OrderPersistenceException(order.id(), ex);
}
```

### 3. Optional Usage
```java
// Don't
private Optional<String> optionalMiddleName;
```

```java
// Do
private String middleName;

public Optional<String> middleName() {
  return Optional.ofNullable(middleName);
}
```

### 4. Exact Monetary Values
```java
// Don't: binary floating point or bare BigDecimal model for money.
double amount = 10.10;
BigDecimal unsafe = new BigDecimal(amount);

// Do: JavaMoney amount with explicit currency.
MonetaryAmount safe = Money.of(new BigDecimal("10.10"), "USD");
```

### 5. String Construction
```java
// Don't: concatenate literal template and variables.
String message = "User " + username + " has " + count + " pending tasks.";
```

```java
// Do: use a format template.
String message = String.format(
    "User %s has %d pending tasks.",
    username,
    count
);
```

## Code Review Checklist for Java
- Are mutability boundaries explicit and safe?
- Are nullability contracts explicit and consistent?
- Are exceptions specific, contextual, and non-silent?
- Is class/method responsibility cohesive?
- Are public APIs stable and domain-oriented?
- Are concurrency assumptions documented and safe?
- Are stream usages readable and side-effect free?
- Are literal-template strings with variables using `String.format(...)`
  instead of `+` concatenation?
- Are persistence and transport concerns separated from domain types?
- Are monetary values modeled with JavaMoney and explicit currency instead of
  `float`/`double` or bare `BigDecimal`?

## Testing Guidance for Java
- Test null/absence behavior for public APIs.
- Test exception mapping and preserved causes.
- Test mutability boundaries (defensive copy and immutability expectations).
- Test concurrency-sensitive code for race and visibility risks.
- Add regression tests for previous bug classes (state leaks, conversion errors,
  mapper issues).
- Test rounding, scaling, and currency/unit conversion behavior for exact-value
  domains.

## VCS Ignore Additions
Add these when using Java build tools (if not already covered by baseline
ignore rules):
- `target/`, `build/`
- `*.class`, `*.war`, `*.ear`
- `pom.xml.tag`, `pom.xml.releaseBackup`, `pom.xml.versionsBackup`,
  `pom.xml.next`
- `release.properties`, `dependency-reduced-pom.xml`,
  `buildNumber.properties`
- `.gradle/`

Do not ignore wrapper scripts or wrapper JARs required to build projects
(for example `gradle/wrapper/gradle-wrapper.jar`,
`.mvn/wrapper/maven-wrapper.jar`).

## Override Notes
- This file is the Java baseline.
- Java specialization docs and Java framework/library docs MAY narrow patterns
  for specific contexts, but MUST keep this file's safety and clarity defaults.
