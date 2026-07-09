---
applies_to:
  load: "annex"
  annex_of: "TEST.md"
  tasks: ["review", "test"]
---
# TEST - Annex

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
