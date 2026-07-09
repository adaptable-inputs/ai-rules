---
applies_to:
  load: "conditional"
  when: "javax.money is a declared dependency"
  libraries: ["javamoney"]
  annex: "JAVA_MONEY.ANNEX.md"
  purpose: "mandatory modeling and arithmetic rules for monetary values"
  inherits: ["LANGUAGE/JAVA/JAVA.md", "LANGUAGE/JAVA/EFFECTIVE_JAVA.md", "LANGUAGE/SQL/SQL.md", "ARCHITECTURE/N_PLUS_1.md"]
---
# JAVA_MONEY

Guidance for AI agents implementing and reviewing JavaMoney usage for monetary
values in Java.

## Defaults
- MUST use JavaMoney (`javax.money`, typically implemented with Moneta) for
  monetary values in Java.
- SHOULD model business monetary amounts as `MonetaryAmount` (or domain wrappers around it), not `BigDecimal` alone.
- SHOULD keep currency explicit for every monetary value.
- SHOULD centralize rounding rules with JavaMoney rounding operators.
- SHOULD restrict `BigDecimal` usage to integration boundaries where JavaMoney cannot be used directly.

## Modeling and API Design
- SHOULD use `MonetaryAmount` in domain/service method parameters and return types.
- MUST NOT pass `(BigDecimal amount, String currency)` pairs through internal
  APIs.
- SHOULD keep conversion to/from persistence and transport models in boundary adapters.
- SHOULD use dedicated domain value objects when additional invariants are required (for example non-negative totals).

## Arithmetic, Rounding, and Currency Conversion
- SHOULD perform business arithmetic via `MonetaryAmount` operations.
- SHOULD define legal rounding behavior once per use case (for example tax, invoice total, payout) and reuse it.
- SHOULD validate currency compatibility before arithmetic and comparison.
- SHOULD use JavaMoney conversion providers for FX conversion; do not hand-roll exchange-rate math in core business
  code.

## Override Notes
- If a boundary cannot use JavaMoney, keep conversion localized at that
  boundary and return to JavaMoney types immediately in core logic.
