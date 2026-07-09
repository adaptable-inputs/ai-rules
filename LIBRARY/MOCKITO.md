---
applies_to:
  load: "conditional"
  when: "mockito is a declared test dependency"
  libraries: ["mockito"]
---
# MOCKITO

Guidance for AI agents implementing and reviewing Mockito-based tests.

## Scope
- Define Mockito usage rules for behavior isolation without brittle tests.
- Apply this file to unit tests using mocks/spies/stubs.

## Semantic Dependencies
- Inherit baseline testing constraints from `TEST/TEST.md` and
  `LIBRARY/JUNIT.md`.
- Mockito guidance specializes mocking behavior only.

## Defaults
- SHOULD mock external collaborators, not value objects.
- SHOULD prefer constructor injection in production code to simplify mocking.
- SHOULD keep stubbing minimal and explicit.
- SHOULD verify behavior only where interaction contract matters.
- SHOULD prefer state/observable outcome assertions over interaction-heavy assertions.

## Stubbing Rules
- Stub only methods exercised by test scenario.
- SHOULD avoid broad deep-stub patterns unless no alternative.
- SHOULD keep `when`/`then` setup readable and scenario-focused.
- SHOULD use argument matchers consistently (avoid mixed raw + matcher misuse).

## Verification Rules
- SHOULD verify meaningful interactions, not every call by default.
- SHOULD use explicit/precise verification for critical side effects (for example once/never checks and argument
  constraints).
- SHOULD prefer strict stubbing to catch unused or mismatched stubs.
- SHOULD avoid over-verifying call counts in non-critical paths.
- SHOULD prefer `verifyNoMoreInteractions` sparingly and intentionally.

## Anti-Pattern Guardrails
- SHOULD avoid mocking the class under test.
- SHOULD avoid static/global mocking unless absolutely necessary.
- SHOULD avoid using spies to patch design smells; refactor boundaries instead.
- SHOULD avoid returning mutable shared objects from stubs unless intentional.

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

## Override Notes
- Framework-specific test utilities MAY supplement Mockito usage, but mocking
  boundary discipline and readability constraints here remain mandatory.
