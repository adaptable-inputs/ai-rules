---
applies_to:
  load: "conditional"
  when: "junit is a declared test dependency"
  libraries: ["junit"]
  annex: "JUNIT.ANNEX.md"
---
# JUNIT

Guidance for AI agents implementing and reviewing JUnit tests.

## Scope
- Define JUnit-specific testing patterns for reliable, readable tests.
- Apply this file to unit/integration tests using JUnit 5.

## Semantic Dependencies
- Inherit global testing baseline from `TEST/TEST.md`.
- Inherit language/readability baselines from
  `LANGUAGE/JAVA/JAVA.md`, `LANGUAGE/CONVENTIONS.md`, and
  `LANGUAGE/READABILITY.md`.
- Companion test-library docs MAY specialize mocking/integration behavior.

## Defaults
- SHOULD use JUnit 5.
- SHOULD keep tests deterministic and isolated.
- SHOULD use descriptive test names based on behavior and expectation.
- SHOULD keep one primary assertion intent per test.
- SHOULD prefer Arrange-Act-Assert structure.

## Test Design Rules
- SHOULD test observable behavior, not implementation details.
- SHOULD prefer small focused tests over large scenario monoliths.
- SHOULD keep setup explicit and local; avoid hidden magic fixtures.
- SHOULD avoid shared mutable state across tests.
- SHOULD use nested tests only when they improve readability and context.

## Lifecycle and Fixtures
- Default to per-test instance lifecycle unless a clear optimization need exists.
- SHOULD use `@BeforeEach`/`@AfterEach` for isolation-safe setup/cleanup.
- SHOULD keep expensive shared fixtures explicit and immutable when possible.

## Parameterized and Edge Testing
- SHOULD use parameterized tests for input matrix coverage.
- SHOULD include boundary, invalid, and edge-case scenarios.
- SHOULD keep parameter sources readable and domain-relevant.

## Flakiness Controls
- SHOULD avoid real network/time randomness in unit tests.
- SHOULD use fake clocks and controlled randomness where needed.
- SHOULD avoid order-dependent tests.
- SHOULD keep concurrency tests deterministic and bounded.

## Override Notes
- Library/framework test docs (for example Mockito and Spring test slices) MAY
  add specialization, but JUnit determinism and clarity constraints remain
  mandatory.
