---
applies_to:
  load: "conditional"
  when: "javax.money is a declared dependency"
  libraries: ["javamoney"]
  annex: "JAVA_MONEY.ANNEX.md"
---
# JAVA_MONEY

Guidance for AI agents implementing and reviewing JavaMoney usage for monetary
values in Java.

## Scope
- Define mandatory modeling and arithmetic rules for monetary values.
- Apply this file whenever Java code stores, computes, compares, or transfers
  money.
- Treat this file as the default monetary approach for Java codebases.

## Semantic Dependencies
- Inherit Java baseline from `LANGUAGE/JAVA/JAVA.md`.
- Inherit design heuristics from `LANGUAGE/JAVA/EFFECTIVE_JAVA.md`.
- Inherit SQL/persistence constraints from `LANGUAGE/SQL/SQL.md`,
  `ARCHITECTURE/N_PLUS_1.md`, and framework docs when persistence is involved.
- Cross-cutting baselines are inherited transitively via the parents above.

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
- This file narrows Java baseline monetary modeling by making JavaMoney the
  default approach.
- If a boundary cannot use JavaMoney, keep conversion localized at that
  boundary and return to JavaMoney types immediately in core logic.
