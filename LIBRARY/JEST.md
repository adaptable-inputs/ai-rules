---
applies_to:
  load: "conditional"
  when: "jest is a declared dev dependency"
  libraries: ["jest"]
  annex: "JEST.ANNEX.md"
  purpose: "Jest-specific rules for deterministic, maintainable tests"
  inherits: ["TEST/TEST.md", "LANGUAGE/**"]
---
# JEST

Guidance for AI agents implementing and reviewing Jest tests.

## Defaults
- SHOULD keep tests deterministic and isolated.
- SHOULD use descriptive `describe`/`it` names reflecting behavior.
- SHOULD reset shared state between tests.
- SHOULD prefer explicit assertions over brittle snapshots when scope is small.
- SHOULD keep async tests explicit (`await`, `resolves`, `rejects`).

## Mocking and Module Isolation
- SHOULD mock boundaries (network, filesystem, external services), not core logic.
- SHOULD keep mock setup local to scenario where possible.
- SHOULD reset/restore mocks between tests.
- SHOULD avoid deep global mocks that hide behavior changes.

## Async and Timer Rules
- MUST await async operations.
- SHOULD avoid dangling promises and unhandled rejections.
- SHOULD use fake timers only when needed and restore real timers after test.
- SHOULD keep timer-based tests explicit about scheduled operations.

## Snapshot Discipline
- SHOULD use snapshots for large stable outputs where explicit assertions are noisy.
- SHOULD keep snapshots focused and reviewed like code.
- SHOULD avoid broad snapshot capture that hides meaningful regression signals.

## Flakiness Controls
- SHOULD avoid real network/time randomness in unit tests.
- SHOULD control random inputs with deterministic seeds.
- SHOULD keep test order independence.
- MUST quarantine/remediate flaky tests quickly.
