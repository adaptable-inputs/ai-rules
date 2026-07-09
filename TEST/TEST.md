---
applies_to:
  load: "always"
---
# TEST

Guidance for AI agents implementing, updating, and reviewing tests.

## Scope
Defines baseline testing expectations for all stacks and domains.

## Semantic Dependencies (Upstream Rules)
- Inherits `CORE/CORE.md` and `CORE/RULE_DEPENDENCY_TREE.md` precedence.
- Security-sensitive scenarios MUST also satisfy `SECURITY/SECURITY.md`.
- Language/framework/library-specific test techniques MAY specialize this
  baseline but MUST NOT weaken it without explicit rationale.

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
- SHOULD avoid reliance on wall-clock time, random seeds, network timing, and shared
  mutable state without explicit control.
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
- High line coverage alone is insufficient; MUST prioritize meaningful assertions and
  branch/error-path validation.
- MUST cover happy paths, edge cases, failure modes, and regression paths.
- If coverage targets are not met, MUST document exact gaps and risk rationale.

## CI and Reporting Expectations
- MUST run relevant tests before opening a PR.
- MUST report what was executed and what was not.
- In CI, MUST fail builds on test failures.
- SHOULD publish actionable reports/artifacts for failed runs when available.

## High-Risk Pitfalls
1. Changing behavior without adding/updating tests.
2. Treating snapshot-only assertions as sufficient behavior verification.
3. Accepting flaky tests to keep pipelines green.
4. Mocking internals so heavily that integration defects are hidden.
5. Using shared mutable fixtures that create order-dependent failures.
6. Ignoring error-path and boundary-condition testing.
7. Claiming confidence from coverage metrics without assertion quality.

## Do / Don't Examples
### 1. Behavior Change Coverage
```text
Don't: merge a behavior change without updating tests.
Do:    add/adjust tests for happy path, edge cases, and failure paths.
```

### 2. Flakiness Control
```text
Don't: rerun flaky tests until green and call it stable.
Do:    quarantine/fix flaky tests and remove nondeterministic dependencies.
```

### 3. Assertion Quality
```text
Don't: rely only on snapshots for critical behavior.
Do:    use explicit assertions tied to business-relevant outcomes.
```

## Code Review Checklist for Testing
- Do behavior changes include corresponding tests?
- Are tests deterministic and independent of execution order?
- Are boundary integrations covered where risk demands it?
- Are failure paths and edge cases explicitly validated?
- Are assertions behavior-focused (not only implementation details)?
- Are mocks/stubs used at the right boundary level?
- Are fixture/test assets correctly isolated from production packaging?
- Is test execution scope and result reporting clear in PR notes?

## Validation Notes for Delivery
When delivering a change, include:
- Tests executed (unit/integration/e2e).
- Key manual checks (if applicable).
- Known test gaps and risk justification.
- Follow-up issue references for deferred test debt.

## Override Notes
- Downstream docs MAY specialize this baseline (for example framework-specific
  testing patterns), but MUST NOT reduce determinism, coverage of critical
  paths, or reporting clarity without explicit justification.
