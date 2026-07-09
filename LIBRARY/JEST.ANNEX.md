---
applies_to:
  load: "annex"
  annex_of: "JEST.md"
  tasks: ["review", "test"]
---
# JEST - Annex

## High-Risk Pitfalls
1. Snapshot overuse masking semantic regressions.
2. Shared global mocks leaking between tests.
3. Fake timers not restored, impacting later tests.
4. Async tests passing falsely due to missing await/return.
5. Over-mocking implementation details.
6. Real IO in unit tests causing instability.

## Do / Don't Examples
### 1. Async Await
```ts
// Don't
test("saves user", () => {
  saveUser(input);
  expect(repo.save).toHaveBeenCalled();
});

// Do
test("saves user", async () => {
  await saveUser(input);
  expect(repo.save).toHaveBeenCalled();
});
```

### 2. Snapshot Scope
```text
Don't: snapshot entire huge page object for tiny behavior change.
Do:    assert explicit critical fields or focused snapshot fragment.
```

### 3. Timer Cleanup
```text
Don't: jest.useFakeTimers() without restoring.
Do:    use fake timers in test scope and restore afterwards.
```

## Code Review Checklist for Jest
- Are tests deterministic and isolated?
- Are async paths awaited and assertion-complete?
- Are mocks boundary-focused and reset between tests?
- Are snapshots focused and intentionally reviewed?
- Are fake timers and globals cleaned up safely?
- Are edge/error cases represented?

## Testing Guidance
- Run tests with parallel and serial modes for flaky detection where needed.
- Track flaky tests and stabilize quickly.
- Add regression tests for bug-fix scenarios.
- Keep CI reporting for failed test diagnostics and timing.
