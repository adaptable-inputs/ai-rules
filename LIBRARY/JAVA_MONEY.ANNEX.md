---
applies_to:
  load: "annex"
  annex_of: "JAVA_MONEY.md"
  tasks: ["review", "test"]
---
# JAVA_MONEY - Annex

## High-Risk Pitfalls
1. Representing money as bare `BigDecimal` without currency.
2. Using `double`/`float` for monetary calculations.
3. Applying inconsistent rounding rules across code paths.
4. Mixing currencies in arithmetic without explicit conversion.
5. Spreading persistence/JSON conversion logic through domain services.
6. Using `FastMoney` without explicit precision-tradeoff analysis.

## Do / Don't Examples
### 1. API Modeling
```java
// Don't
public BigDecimal calculateTotal(Order order) { ... }

// Do
public MonetaryAmount calculateTotal(Order order) { ... }
```

### 2. Monetary Value Construction
```java
// Don't
BigDecimal price = new BigDecimal("19.99");
String currency = "USD";

// Do
MonetaryAmount price = Money.of(new BigDecimal("19.99"), "USD");
```

### 3. Rounding Strategy
```text
Don't: call setScale(...) ad-hoc in multiple services.
Do:    centralize and reuse JavaMoney rounding operators per business rule.
```

## Code Review Checklist for JavaMoney
- Are monetary values represented with `MonetaryAmount` (or wrappers)
  end-to-end?
- Is currency always explicit and validated before arithmetic/comparison?
- Are rounding rules centralized and domain-correct?
- Are FX conversions using JavaMoney services instead of manual math?
- Are persistence/transport conversions isolated to boundary layers?
- Are primitive and `BigDecimal` money values confined to explicit interop
  points?

## Testing Guidance
- Test arithmetic and aggregation with same- and mixed-currency scenarios.
- Test rounding rules for edge values (tax, discount, fractional-cent cases).
- Test currency-conversion behavior including missing-rate/error handling.
- Test boundary mapping between `MonetaryAmount` and persistence/transport
  schemas.
- Add regression tests for known monetary defect classes (rounding drift,
  currency mix-ups).
