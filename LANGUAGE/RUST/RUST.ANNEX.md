---
applies_to:
  load: "annex"
  annex_of: "RUST.md"
  tasks: ["review", "test"]
---
# RUST - Annex

## High-Risk Pitfalls
1. Excess cloning to bypass ownership design issues.
2. Panic-based control flow in recoverable runtime paths.
3. Async code using blocking operations on executor threads.
4. Hidden invariants in `unsafe` code with no safety docs/tests.
5. Overcomplicated trait abstractions reducing readability.
6. Error types that lose root-cause context.
7. Unbounded concurrency without backpressure/timeouts.

## Do / Don't Examples
### 1. Error Handling
```text
Don't: use `unwrap()` in normal service runtime paths.
Do:    propagate recoverable failures using contextual `Result` errors.
```

### 2. Unsafe Isolation
```text
Don't: scatter unsafe blocks across business logic.
Do:    isolate unsafe code behind small reviewed safe abstractions.
```

### 3. Async Safety
```text
Don't: run blocking IO directly inside async tasks.
Do:    use async-compatible clients or isolate blocking work explicitly.
```

## Code Review Checklist for Rust
- Are ownership/lifetime contracts explicit and readable?
- Are error paths contextual and panic usage bounded?
- Are async and blocking behaviors correctly separated?
- Is unsafe/FFI code minimal, documented, and tested?
- Are module/trait boundaries cohesive and maintainable?
- Are concurrency limits/backpressure/cancellation explicit?

## Testing Guidance
- Test error-path behavior with contextual mapping.
- Test async timeout/cancellation and backpressure behavior.
- Test unsafe/FFI boundary invariants and failure modes.
- Test concurrency-sensitive code for race/deadlock/starvation risks.
- Add regression tests for previously observed bug classes.
