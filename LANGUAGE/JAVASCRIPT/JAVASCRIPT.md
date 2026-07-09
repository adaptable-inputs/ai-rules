---
applies_to:
  load: "conditional"
  when: "package.json is present"
  languages: ["javascript"]
  globs: ["**/*.js", "**/*.jsx", "**/*.mjs"]
---
# JAVASCRIPT

Guidance for AI agents implementing and reviewing JavaScript code.

## Scope
- Define a complete JavaScript baseline for runtime-safe, maintainable code.
- Apply this file for plain JavaScript projects and as parent guidance for
  TypeScript and JavaScript-based framework docs.

## Semantic Dependencies
- Inherit cross-cutting constraints from:
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.
- Inherit shared language constraints from:
  `LANGUAGE/CONVENTIONS.md`, `LANGUAGE/READABILITY.md`.
- Specialized docs (for example TypeScript and framework-specific docs) MAY
  narrow this guidance but MUST NOT silently weaken it.

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

## High-Risk Pitfalls
1. Unhandled promise rejections causing hidden failures.
2. Trusting external payload shape without validation.
3. Mutating shared objects across module boundaries.
4. Using `==`/`!=` and relying on coercion side effects.
5. Silent catch blocks that drop operational failures.
6. Fire-and-forget async tasks without cancellation/logging.
7. Mixing CommonJS and ESM inconsistently in one package.

## Do / Don't Examples
### 1. Promise Rejection Handling
```js
// Don't: unhandled rejection.
function saveUserBad(user) {
  db.write(user);
}

// Do: await and handle failure with context.
async function saveUserGood(user) {
  try {
    await db.write(user);
  } catch (error) {
    logger.error("user.save.failed", { userId: user.id, error });
    const wrappedError = new Error(`Failed to save user ${user.id}`, {
      cause: error,
    });
    if (wrappedError.cause === undefined) {
      wrappedError.cause = error;
    }
    throw wrappedError;
  }
}
```

### 2. Boundary Validation
```js
// Don't: trust request body shape.
function createInvoiceBad(req) {
  return invoiceService.create(req.body.amount, req.body.currency);
}

// Do: validate and normalize at boundary.
function createInvoiceGood(req) {
  const payload = validateInvoiceRequest(req.body);
  return invoiceService.create(payload.amount, payload.currency);
}
```

### 3. Shared Mutation
```js
// Don't: mutate imported/shared state.
settings.timeoutMs = 5000;

// Do: create explicit derived config.
const runtimeSettings = { ...settings, timeoutMs: 5000 };
```

## Code Review Checklist for JavaScript
- Are all external inputs validated at boundaries?
- Are promise rejections handled for all async operations?
- Is error handling explicit, contextual, and non-silent?
- Is module state mutation controlled and intentional?
- Are `===`/`!==` used consistently?
- Are side effects isolated from pure domain logic?
- Are there event-loop blocking operations on hot paths?
- Are security-sensitive APIs (`eval`, shell exec, dynamic code paths) avoided
  or tightly controlled?

## Testing Guidance for JavaScript
- Test boundary validators with valid, invalid, and malicious payloads.
- Test async failure paths, including timeout/cancellation behavior.
- Test concurrency behavior for multi-promise flows.
- Test mutation-sensitive logic for unintended shared-state side effects.
- Add regression tests for previously observed runtime edge cases.

## Override Notes
- Type-specialized JavaScript docs MAY narrow typing discipline and
  compile-time safety rules for TypeScript codebases and other typed JavaScript
  projects.
- Framework docs MAY further specialize state/lifecycle/rendering behavior but
  MUST keep this file's runtime safety baseline.
