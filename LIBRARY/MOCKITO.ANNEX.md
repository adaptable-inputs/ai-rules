---
applies_to:
  load: "annex"
  annex_of: "MOCKITO.md"
  tasks: ["review", "test"]
---
# MOCKITO - Annex

## High-Risk Pitfalls
1. Over-mocked tests coupled to implementation details.
2. Lenient stubs hiding dead code/path drift.
3. Mixing matchers incorrectly leading to false positives.
4. Brittle call-order assertions with low business value.
5. Static mocking as default instead of design improvement.

## Do / Don't Examples
### 1. Mock Boundary
```text
Don't: mock simple DTO/value classes.
Do:    mock external gateway/repository collaborators.
```

### 2. Verification Discipline
```text
Don't: verify every internal helper call.
Do:    verify externally observable side-effect interactions.
```

### 3. Stubbing Scope
```text
Don't: giant shared test setup with many unused stubs.
Do:    scenario-local stubs used by current test only.
```

## Code Review Checklist for Mockito
- Are only meaningful collaborator boundaries mocked?
- Is stubbing minimal, explicit, and scenario-focused?
- Is verification tied to behavior contracts, not implementation trivia?
- Are matchers used correctly and consistently?
- Are static/spying patterns justified and bounded?
- Do tests remain readable and maintainable?

## Testing Guidance
- Enable strict stubbing mode where feasible.
- Refactor tests to remove unused stubs/verifications.
- Combine Mockito tests with integration tests for mocked boundaries.
- Add regression tests for previously flaky mock interactions.
