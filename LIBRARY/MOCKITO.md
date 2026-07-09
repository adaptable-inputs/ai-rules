---
applies_to:
  load: "conditional"
  when: "mockito is a declared test dependency"
  libraries: ["mockito"]
  annex: "MOCKITO.ANNEX.md"
  purpose: "Mockito usage rules for behavior isolation without brittle tests"
  inherits: ["TEST/TEST.md", "LIBRARY/JUNIT.md"]
---
# MOCKITO

Guidance for AI agents implementing and reviewing Mockito-based tests.

## Defaults
- SHOULD mock external collaborators, not value objects.
- SHOULD prefer constructor injection in production code to simplify mocking.
- SHOULD keep stubbing minimal and explicit.
- SHOULD verify behavior only where interaction contract matters.
- SHOULD prefer state/observable outcome assertions over interaction-heavy assertions.

## Stubbing Rules
- SHOULD stub only methods exercised by test scenario.
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
