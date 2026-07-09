---
applies_to:
  load: "conditional"
  when: "playwright is a declared dev dependency"
  libraries: ["playwright"]
  annex: "PLAYWRIGHT.ANNEX.md"
---
# PLAYWRIGHT

Guidance for AI agents implementing and reviewing Playwright tests.

## Scope
- Define Playwright E2E/integration testing rules for reliability and
  maintainability.
- Apply this file to browser automation tests and test infrastructure.

## Semantic Dependencies
- Inherit testing baseline from `TEST/TEST.md`.
- Inherit UI accessibility semantics from `LANGUAGE/HTML/HTML.md`.
- Complements unit/component testing docs (Jest/JUnit etc.).

## Defaults
- SHOULD focus E2E tests on critical user journeys.
- SHOULD keep tests deterministic with isolated test data/state.
- SHOULD use robust locators (`getByRole`, test IDs via `data-testid` + `getByTestId`) over brittle CSS/XPath chains.
- SHOULD use Playwright auto-waiting and explicit assertions.
- SHOULD keep setup/teardown reusable through fixtures.

## Locator and Interaction Rules
- SHOULD prefer accessible-role/text/test-id locators.
- SHOULD avoid selectors tied to fragile DOM structure.
- SHOULD keep waits condition-based, not sleep-based.
- SHOULD keep user actions explicit and semantically aligned.

## Flakiness Controls
- SHOULD avoid real third-party dependencies when stubbing is possible.
- SHOULD isolate each test scenario state.
- SHOULD use retries sparingly; fix root cause first.
- SHOULD keep parallelization aware of shared-resource contention.

## Debuggability and Artifacts
- SHOULD capture traces/screenshots/videos on failure according to policy.
- SHOULD keep logs/artifacts easy to correlate with failed scenario.
- SHOULD use step-level diagnostics for complex flows.

## Override Notes
- Project-specific E2E policy MAY define stricter locator/test-ID conventions,
  but determinism and stable-locator constraints here remain mandatory.
