---
applies_to:
  load: "conditional"
  when: "go.mod is present"
  languages: ["go"]
  globs: ["**/*.go"]
  annex: "GO.ANNEX.md"
  purpose: "baseline Go rules for correctness, maintainability, and production safety"
  inherits: ["SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# GO

Guidance for AI agents implementing and reviewing Go code.

## Defaults
- SHOULD prefer simple, explicit code over abstraction-heavy indirection.
- SHOULD keep package boundaries cohesive with clear ownership.
- SHOULD return errors explicitly and handle them near boundaries.
- SHOULD use `context.Context` consistently for request-scoped cancellation/timeouts.
- SHOULD keep dependencies minimal and maintainable.

## API and Package Design
- SHOULD keep exported APIs small and stable.
- SHOULD use interfaces at boundaries where polymorphism is required, not everywhere.
- SHOULD keep package init logic minimal and side-effect free.
- SHOULD avoid cyclic package dependencies and hidden global coupling.

## Error Handling and Resource Safety
- SHOULD return rich, contextual errors and preserve root cause context.
- MUST NOT ignore returned errors.
- SHOULD keep panic usage exceptional (programmer errors/unrecoverable states).
- MUST close resources deterministically (`defer` with explicit error handling where needed).

## Concurrency and Context Rules
- SHOULD prefer message passing/channel patterns over shared mutable state when practical.
- SHOULD guard shared state explicitly when unavoidable.
- SHOULD avoid goroutine leaks; ensure cancellation and completion paths exist.
- SHOULD pass `context.Context` as first parameter for request-scoped operations.
- SHOULD keep timeouts/deadlines explicit for external IO.
