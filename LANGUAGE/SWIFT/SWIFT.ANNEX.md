---
applies_to:
  load: "annex"
  annex_of: "SWIFT.md"
  tasks: ["review", "test"]
---
# SWIFT - Annex

## High-Risk Pitfalls
1. Force-unwrapping optionals in normal runtime paths.
2. Unstructured tasks with unclear cancellation/lifecycle.
3. Data races from shared mutable state outside safe isolation.
4. Blocking main actor with network/disk-heavy operations.
5. Broad error handling that hides root causes.
6. Framework-coupled domain logic reducing testability.
7. Resource leaks from weak cleanup discipline.

## Do / Don't Examples
### 1. Optional Safety
```text
Don't: force-unwrap values from external input.
Do:    validate and handle optionals explicitly at boundaries.
```

### 2. Concurrency Isolation
```text
Don't: mutate shared state from multiple tasks without protection.
Do:    use actors or explicit synchronization boundaries.
```

### 3. UI/Main Thread Safety
```text
Don't: perform long IO work on the main actor.
Do:    move heavy work off main actor and update UI intentionally.
```

## Code Review Checklist for Swift
- Are optional/type contracts explicit and safe?
- Is async/task lifecycle structured with clear cancellation behavior?
- Is shared mutable state isolated safely (actors/synchronization)?
- Are error paths explicit and context-rich?
- Are domain and framework/UI boundaries cleanly separated?
- Are dependencies/configuration/secrets handled safely?

## Testing Guidance
- Test optional-handling and boundary validation behavior.
- Test async cancellation/timeout behavior under failure.
- Test actor/isolation-sensitive code for race/leak risks.
- Test error mapping and root-cause preservation.
- Add regression tests for previously observed bug classes.
