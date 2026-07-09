---
applies_to:
  load: "conditional"
  when: "selenium is a declared test dependency"
  libraries: ["selenium"]
---
# SELENIUM

Guidance for AI agents implementing and reviewing Selenium-based tests.

## Scope
- Define Selenium E2E automation patterns for stable browser testing.
- Apply this file to Selenium/WebDriver tests and grid execution strategy.

## Semantic Dependencies
- Inherit baseline testing constraints from `TEST/TEST.md`.
- Inherit UI accessibility semantics from `LANGUAGE/HTML/HTML.md`.
- Use with complementary unit/component tests; avoid over-reliance on E2E.

## Defaults
- SHOULD keep Selenium suite focused on critical cross-browser flows.
- SHOULD use explicit waits and resilient locators.
- SHOULD keep tests isolated from each other.
- SHOULD keep browser/environment setup reproducible.

## Locator and Wait Rules
- SHOULD prefer stable locators (IDs/data-test attributes/accessible labels).
- SHOULD avoid brittle xpath/CSS selectors tied to transient layout.
- SHOULD use explicit waits with clear conditions.
- SHOULD avoid sleep-based synchronization.

## Test Architecture
- SHOULD use page objects or equivalent abstraction for repeated interactions.
- SHOULD keep assertions close to user-observable behavior.
- SHOULD keep test setup/teardown explicit and reusable.
- SHOULD keep parallel execution safe regarding shared data/state.

## Grid and Runtime Management
- SHOULD keep browser/version matrix intentional and documented.
- SHOULD keep Selenium Grid resources sized for workload.
- SHOULD isolate flaky environment issues from test logic defects.
- SHOULD capture logs/screenshots on failure.

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

## Override Notes
- Project-specific UI automation standards MAY add stricter page-object or
  locator conventions, but deterministic wait/locator/isolation rules remain
  mandatory.
