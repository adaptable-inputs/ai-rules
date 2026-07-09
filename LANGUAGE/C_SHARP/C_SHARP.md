---
applies_to:
  load: "conditional"
  when: "a .csproj or .sln is present"
  languages: ["csharp"]
  globs: ["**/*.cs"]
  annex: "C_SHARP.ANNEX.md"
---
# C_SHARP

Guidance for AI agents implementing and reviewing C#/.NET code.

## Scope
- Define baseline C#/.NET rules for correctness, maintainability, and runtime
  safety.
- Apply this file for C#/.NET code generation and review tasks.

## Semantic Dependencies
- Inherit cross-cutting constraints from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `CORE/LOGGING.md`.
- Inherit shared language constraints from `LANGUAGE/CONVENTIONS.md` and
  `LANGUAGE/READABILITY.md`.
- Framework/library-specific C#/.NET docs MAY specialize API usage but MUST NOT
  weaken this baseline.

## Defaults
- SHOULD enable and respect nullable reference type warnings.
- SHOULD prefer explicit dependency injection over static/global dependencies.
- SHOULD keep async flows truly asynchronous end-to-end for IO paths.
- SHOULD keep exceptions specific, contextual, and centrally mapped at boundaries.
- SHOULD keep domain logic separated from transport/persistence concerns.

## Nullability and API Contracts
- SHOULD treat nullable annotations as part of API contract.
- SHOULD avoid returning null where an explicit optional/result model is clearer.
- SHOULD validate external inputs at boundaries and fail fast with clear errors.
- SHOULD keep DTO/domain model nullability intent explicit and consistent.

## Async, Concurrency, and Cancellation
- SHOULD use `async`/`await` for IO-bound work; avoid sync-over-async patterns.
- SHOULD propagate `CancellationToken` for request-scoped operations.
- SHOULD avoid blocking calls (`.Result`, `.Wait()`) in async paths.
- SHOULD keep shared mutable state synchronized and minimized.

## Exception and Resource Handling
- SHOULD throw and map specific exception types with actionable context.
- MUST NOT swallow exceptions silently.
- SHOULD use `using`/`await using` for deterministic disposal.
- SHOULD preserve inner exception/root cause when wrapping.

## Architectural Boundaries
- SHOULD keep dependency direction explicit and testable.
- SHOULD keep service classes cohesive with one primary responsibility.
- SHOULD avoid static utility sprawl for domain behavior.
- MUST keep configuration and secrets out of code.

## Override Notes
- Project-specific C#/.NET conventions MAY add stricter patterns, but nullable
  contract integrity, async/cancellation safety, explicit error handling, and
  boundary separation remain mandatory.
