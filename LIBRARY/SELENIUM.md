---
applies_to:
  load: "conditional"
  when: "selenium is a declared test dependency"
  libraries: ["selenium"]
  annex: "SELENIUM.ANNEX.md"
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

## Override Notes
- Project-specific UI automation standards MAY add stricter page-object or
  locator conventions, but deterministic wait/locator/isolation rules remain
  mandatory.
