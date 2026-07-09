---
applies_to:
  load: "annex"
  annex_of: "JAVA.md"
  tasks: ["review", "test"]
---
# JAVA - Annex

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
- Are literal-template strings with variables using `String.format(...)` instead of `+` concatenation?
- Are persistence and transport concerns separated from domain types?
- Are monetary values modeled with JavaMoney and explicit currency instead of `float`/`double` or bare `BigDecimal`?

## Testing Guidance for Java
- Test null/absence behavior for public APIs.
- Test exception mapping and preserved causes.
- Test mutability boundaries (defensive copy and immutability expectations).
- Test concurrency-sensitive code for race and visibility risks.
- Add regression tests for previous bug classes (state leaks, conversion errors, mapper issues).
- Test rounding, scaling, and currency/unit conversion behavior for exact-value domains.
