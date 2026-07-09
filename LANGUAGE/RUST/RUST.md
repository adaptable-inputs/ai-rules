---
applies_to:
  load: "conditional"
  when: "Cargo.toml is present"
  languages: ["rust"]
  globs: ["**/*.rs"]
---
# RUST

Guidance for AI agents implementing and reviewing Rust code.

## Scope
- Define baseline Rust rules for correctness, maintainability, and runtime
  safety.
- Apply this file for Rust code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific Rust docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD prefer explicit ownership and lifetimes over workaround cloning.
- SHOULD keep type/state invariants encoded in types where practical.
- SHOULD use `Result`/`Option` explicitly and avoid panic-driven normal flow.
- SHOULD keep `unsafe` usage minimal, justified, and encapsulated.
- SHOULD keep public API surfaces small and stable.

## Ownership and API Design
- SHOULD design APIs that communicate ownership/borrowing intent clearly.
- SHOULD avoid unnecessary `clone()` in hot paths; address lifetime design first.
- SHOULD keep module boundaries cohesive and explicit.
- SHOULD keep trait abstractions purposeful, not premature.

## Error Handling and Panics
- SHOULD use domain-specific error enums/structs with contextual information.
- SHOULD propagate recoverable failures via `Result`.
- Reserve `panic!` for unrecoverable programmer invariants.
- SHOULD preserve source context when mapping lower-level errors.

## Async and Concurrency Rules
- SHOULD keep async boundaries explicit and runtime-aware.
- SHOULD avoid blocking operations on async executors.
- SHOULD keep shared mutable state synchronized and minimized.
- SHOULD use channels/message passing where it improves clarity and safety.
- SHOULD keep cancellation/timeout behavior explicit for external IO.

## Unsafe and FFI Boundaries
- SHOULD isolate `unsafe` blocks behind safe APIs and documented invariants.
- SHOULD keep FFI boundary contracts explicit about ownership/lifetime/thread safety.
- SHOULD add targeted tests around unsafe-critical behavior.
- SHOULD review unsafe code with extra scrutiny in PRs.

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

## Override Notes
- Project-specific Rust conventions MAY add stricter patterns, but explicit
  ownership contracts, safe error handling, bounded unsafe usage, and async
  runtime safety remain mandatory.
