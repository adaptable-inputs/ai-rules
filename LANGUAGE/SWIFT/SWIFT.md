---
applies_to:
  load: "conditional"
  when: "Package.swift or an Xcode project is present"
  languages: ["swift"]
  globs: ["**/*.swift"]
  annex: "SWIFT.ANNEX.md"
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

## Override Notes
- Project-specific Swift conventions MAY add stricter patterns, but optional
  safety, structured concurrency/isolation, explicit error handling, and clear
  boundary separation remain mandatory.
