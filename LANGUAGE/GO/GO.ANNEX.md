---
applies_to:
  load: "annex"
  annex_of: "GO.md"
  tasks: ["review", "test"]
---
# GO - Annex

## High-Risk Pitfalls
1. Ignoring errors and assuming happy-path behavior.
2. Package-level globals introducing hidden mutable state.
3. Goroutine leaks due to missing cancellation/closure conditions.
4. Blocking operations with no context timeout.
5. Premature interface abstraction that reduces readability.
6. Panic-driven control flow in normal runtime paths.
7. Resource leaks due to missing close/defer handling.

## Do / Don't Examples
### 1. Error Handling
```text
Don't: discard returned error values.
Do:    handle or propagate errors with context.
```

### 2. Context Discipline
```text
Don't: perform network/database calls without timeout or cancellation context.
Do:    pass context and enforce deadlines at external boundaries.
```

### 3. Concurrency Safety
```text
Don't: spawn goroutines with no lifecycle control.
Do:    define clear cancellation and completion paths.
```

## Code Review Checklist for Go
- Are package boundaries clear and cohesive?
- Are errors handled explicitly with useful context?
- Are contexts/timeouts/cancellation used correctly for IO paths?
- Is concurrency free from obvious races/leaks/deadlocks?
- Are globals and shared mutable state minimized?
- Are dependencies justified and minimal?

## Testing Guidance
- Test error-path behavior and wrapped error context.
- Test context cancellation/timeout behavior for IO-bound operations.
- Test concurrency-sensitive code for races and goroutine leaks.
- Test package boundary contracts with integration-level coverage where needed.
- Add regression tests for previous bug classes.
