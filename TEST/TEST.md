---
applies_to:
  load: "always"
  annex: "TEST.ANNEX.md"
  inherits: ["CORE/CORE.md", "CORE/RULE_DEPENDENCY_TREE.md"]
---
# TEST

Guidance for AI agents implementing, updating, and reviewing tests.

## Testing Defaults
- MUST add or update tests for every behavior change.
- SHOULD prefer deterministic and isolated tests.
- SHOULD keep test suites fast enough for frequent CI execution.
- MUST use risk-based depth: higher business/security impact requires stronger test coverage across layers.

## Test Strategy by Layer
- Unit tests:
  - SHOULD be the default first choice for business logic.
  - MUST be fast, isolated, and behavior-focused.
- Integration tests:
  - MUST be used for boundaries (DB, queues, file systems, external services).
  - MUST validate wiring, contracts, and transactional behavior.
- End-to-end tests:
  - MUST cover critical user/value flows only.
  - MUST keep suite small, stable, and non-flaky.

## Determinism and Flakiness Control
- SHOULD avoid reliance on wall-clock time, random seeds, network timing, and shared mutable state without explicit
  control.
- MUST use stable fixtures and explicit setup/teardown.
- SHOULD control time/randomness with test doubles where feasible.
- MUST quarantine and fix flaky tests; do not normalize flaky behavior as acceptable.

## Mocks, Stubs, and Fakes
- MUST mock boundaries, not core behavior under test.
- SHOULD avoid over-mocking that hides integration risks.
- SHOULD use fakes/stubs for dependencies that are slow, non-deterministic, or unavailable in the test environment.
- MUST reset shared test doubles between tests to avoid cross-test coupling.

## Data and Fixtures
- MUST keep fixtures in test-only paths.
- MUST NOT ship test fixtures in production artifacts.
- SHOULD prefer minimal fixture data that expresses intent clearly.
- SHOULD use scenario-based datasets for edge and failure-path coverage.

## Coverage and Confidence
- High line coverage alone is insufficient; MUST prioritize meaningful assertions and branch/error-path validation.
- MUST cover happy paths, edge cases, failure modes, and regression paths.
- If coverage targets are not met, MUST document exact gaps and risk rationale.

## CI and Reporting Expectations
- MUST run relevant tests before opening a PR.
- MUST report what was executed and what was not.
- In CI, MUST fail builds on test failures.
- SHOULD publish actionable reports/artifacts for failed runs when available.

## Validation Notes for Delivery
When delivering a change, include:
- Tests executed (unit/integration/e2e).
- Key manual checks (if applicable).
- Known test gaps and risk justification.
- Follow-up issue references for deferred test debt.

## Override Notes
- Security-sensitive scenarios MUST also satisfy `SECURITY/SECURITY.md`.
