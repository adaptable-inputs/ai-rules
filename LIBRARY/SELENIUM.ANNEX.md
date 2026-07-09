---
applies_to:
  load: "annex"
  annex_of: "SELENIUM.md"
  tasks: ["review", "test"]
---
# SELENIUM - Annex

## High-Risk Pitfalls
1. Sleep-based waits leading to flaky/slow tests.
2. Fragile selectors coupled to layout changes.
3. Shared test data causing order dependence.
4. Massive E2E suites duplicating lower-level coverage.
5. Missing failure artifacts slowing triage.
6. Environment drift between local and CI browsers/drivers.

## Do / Don't Examples
### 1. Wait Strategy
```text
Don't: Thread.sleep(5000)
Do:    WebDriverWait until expected condition
```

### 2. Locator Stability
```text
Don't: xpath with deeply nested positional selectors.
Do:    stable id/test-id/role-driven selectors.
```

### 3. Isolation
```text
Don't: reuse mutable account state across many tests.
Do:    seed/reset state per test scenario.
```

## Code Review Checklist for Selenium
- Are tests focused on high-value user journeys?
- Are locators stable and maintainable?
- Are waits explicit and condition-driven?
- Is test state isolated and parallel-safe?
- Are browser/grid configurations deterministic?
- Are debug artifacts captured on failure?

## Testing Guidance
- Run Selenium suite in CI against target browser matrix.
- Track flaky tests and root causes.
- Keep runtime budget visible; prune low-value tests.
- Validate driver/browser version compatibility regularly.
