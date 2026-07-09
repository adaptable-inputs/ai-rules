---
applies_to:
  load: "annex"
  annex_of: "JUNIT.md"
  tasks: ["review", "test"]
---
# JUNIT - Annex

## High-Risk Pitfalls
1. Shared mutable fixture state causing test order dependence.
2. Overly broad tests with unclear failure intent.
3. Assertions tied to private implementation details.
4. Missing edge-case coverage for boundary conditions.
5. Time/network-based flakiness in unit tests.
6. Test names that do not describe behavior.

## Do / Don't Examples
### 1. Test Naming
```text
Don't: test1(), shouldWork()
Do:    returnsValidationErrorWhenEmailIsInvalid()
```

### 2. Isolation
```text
Don't: static mutable list reused across tests.
Do:    fresh fixture setup in @BeforeEach.
```

### 3. Edge Coverage
```text
Don't: only happy-path assertions.
Do:    include invalid input and boundary cases.
```

## Code Review Checklist for JUnit
- Are tests deterministic and isolated?
- Do test names communicate behavior and condition?
- Is test scope focused with clear assertion intent?
- Are boundary/error paths covered?
- Are fixtures/setup explicit and maintainable?
- Are flakiness risks (time/network/order) addressed?

## Testing Guidance
- Run full test suite with consistent environment settings.
- Track flaky tests and quarantine/remediate quickly.
- Add coverage for bug-fix regressions.
- Keep CI reports readable with failing-test diagnostics.
