---
applies_to:
  load: "conditional"
  when: "Package.swift or an Xcode project is present"
  languages: ["swift"]
  globs: ["**/*.swift"]
---
# SWIFT

Guidance for AI agents implementing and reviewing Swift code.

## Scope
- Define baseline Swift rules for correctness, maintainability, and runtime
  safety.
- Apply this file for Swift code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific Swift docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD prefer value semantics (`struct`, immutable state) when practical.
- SHOULD keep optional handling explicit and avoid force-unwrapping in runtime paths.
- SHOULD use Swift concurrency (`async`/`await`, actors) with explicit isolation.
- SHOULD keep API contracts and error paths explicit and testable.
- SHOULD keep domain logic separate from UI/framework lifecycle code.

## Optionals and Type Contracts
- SHOULD model absence with optionals intentionally.
- SHOULD avoid `!` unless a bounded invariant is proven and documented.
- SHOULD keep boundary parsing/validation explicit for external input.
- SHOULD use enums/value objects for constrained domain states where suitable.

## Concurrency and Isolation Rules
- SHOULD use structured concurrency for async workflows.
- SHOULD use actors or other safe synchronization for shared mutable state.
- SHOULD avoid blocking the main actor with long-running work.
- SHOULD keep cancellation and timeout behavior explicit for external IO.
- SHOULD keep task ownership/lifecycle clear to avoid orphaned async work.

## Error and Resource Handling
- SHOULD throw/map specific errors with actionable context.
- MUST NOT suppress errors silently.
- SHOULD use deterministic cleanup for files/network/resources.
- SHOULD preserve cause context when mapping low-level failures.

## API and Module Boundaries
- SHOULD keep module boundaries cohesive with explicit dependency direction.
- SHOULD keep protocol abstractions purposeful, not premature.
- SHOULD keep side effects isolated at service/adaptor boundaries.
- MUST keep configuration/secrets outside code.

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

## Override Notes
- Project-specific Swift conventions MAY add stricter patterns, but optional
  safety, structured concurrency/isolation, explicit error handling, and clear
  boundary separation remain mandatory.
