---
applies_to:
  load: "conditional"
  when: "package.json is present"
  languages: ["javascript"]
  globs: ["**/*.js", "**/*.jsx", "**/*.mjs"]
  annex: "JAVASCRIPT.ANNEX.md"
  purpose: "a complete JavaScript baseline for runtime-safe, maintainable code"
  inherits: ["SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# JAVASCRIPT

Guidance for AI agents implementing and reviewing JavaScript code.

## Defaults
- SHOULD prefer ESM modules (`import`/`export`) over CommonJS for new code unless the
  runtime/toolchain explicitly requires CommonJS.
- SHOULD keep modules focused; avoid files that mix unrelated responsibilities.
- SHOULD use `const` by default, `let` only when reassignment is required, avoid `var`.
- SHOULD prefer explicit `===`/`!==` over loose equality.
- SHOULD prefer nullish and optional operators (`??`, `?.`) over deep guard pyramids.
- SHOULD prefer pure functions and explicit inputs/outputs for business logic.

## Runtime Boundaries and Validation
- SHOULD treat all external data as untrusted: HTTP payloads, message queues, environment variables, filesystem input.
- SHOULD validate boundary data explicitly before domain use.
- SHOULD normalize data once at boundary adapters; keep core logic on normalized shapes.
- MUST NOT assume dynamic payload shape from naming conventions or comments.

## Async and Concurrency Rules
- MUST handle promise rejections.
- MUST NOT fire-and-forget async work unless intentional and observably tracked.
- SHOULD use `Promise.all` only when all tasks MAY fail-fast together.
- SHOULD use `Promise.allSettled` when partial success is acceptable.
- SHOULD set explicit timeouts/cancellation where IO can hang.
- SHOULD keep async flow linear and readable; avoid nested `.then` chains in new code.

## Error Handling
- SHOULD throw `Error` (or subclasses), not raw strings/objects.
- SHOULD add contextual metadata when rethrowing (`cause`, operation identifiers).
- SHOULD distinguish expected domain outcomes from exceptional failures.
- MUST NOT swallow errors silently; map, log, or rethrow intentionally.

## State and Mutation
- SHOULD avoid shared mutable state across modules.
- SHOULD prefer immutable updates (`{ ...obj }`, `map`, `filter`) for predictable flow.
- SHOULD clone cautiously at boundaries; avoid unnecessary deep cloning in hot paths.
- SHOULD keep side effects at edges (IO adapters, framework handlers), not in pure domain helpers.

## Control Flow and Readability
- SHOULD prefer guard clauses and early returns to reduce nesting.
- SHOULD keep functions focused on one responsibility.
- SHOULD avoid cascading ternary expressions.
- SHOULD keep boolean conditions explicit; extract named predicates when complex.

## Performance Baseline
- MUST NOT optimize blindly; measure first.
- SHOULD avoid repeated expensive work inside loops when values can be precomputed.
- SHOULD avoid accidental quadratic behavior in list operations on large data.
- SHOULD be careful with synchronous CPU-heavy work on event-loop-critical paths.

## Security Baseline
- MUST NOT build code paths that evaluate untrusted strings (`eval`, dynamic
  function constructors) unless there is no alternative and controls are strict.
- SHOULD avoid unsafe shell command construction from untrusted input.
- MUST sanitize/encode output for the target context (HTML, URL, shell).
- For SQL, MUST use parameterized queries/prepared statements rather than string escaping.
